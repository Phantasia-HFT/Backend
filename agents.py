from typing import Annotated
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_groq import ChatGroq
import os

load_dotenv()

groq_api = os.getenv("GROQ_API_KEY")
tavily_api = os.getenv("TAVILY_API_KEY")

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    messages: Annotated[list, add_messages]

llm = ChatGroq(
    model="llama-3.2-3b-preview",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=groq_api
)

# Script generation function
def script_generator(state):
    system_prompt = (
        "You are a script writer, you have to think of extremely good scenarios and write scripts of two people interacting with each other"
        "This script will be used by a voice model to generate audio. Generate accordingly."
        "search the web using the tool for getting context for the scenes to be generated"
        "use tools to search about the characters and study them. Generate dialogues accordingly"
        "Create a scenario first"
        "Create dialogues after evaluating the scenario you just created."
        "The script must be at least 500 words long!!!!!!"
        "Only dialogues have to be included"
        "The script should follow the format <name_of_character>: <text> "
        "Keep sentences concise and straightforward. Avoid long or overly complex sentences."
        "..."
    )

    state["messages"].append({"role": "system", "content": system_prompt})

    # Invoke the model
    ai_message = llm.invoke(state["messages"])

    # Append the AI's response to the messages
    state["messages"].append({"role": "assistant", "content": ai_message.content})

    # Return the updated state
    return state

# Function for self-critiquing the script
def critique_script(state: State) -> State:
    critique_prompt = (
        "Evaluate the following script based on emotional depth, natural dialogue, pacing, and clarity. "
        "Provide a score from 1 to 10 for each of these criteria, and suggest improvements for each aspect. "
        "Return the critique in the following format:\n"
        "Emotional Depth: <score> (<suggested improvement>)\n"
        "Natural Dialogue: <score> (<suggested improvement>)\n"
        "Pacing: <score> (<suggested improvement>)\n"
        "Clarity: <score> (<suggested improvement>)"
    )
    
    script = state["messages"][-1]["content"]  # Get the latest generated script
    
    # Ask the LLM to critique the script
    critique_input = critique_prompt + "\n\n" + script
    state["messages"].append({"role": "user", "content": critique_input})
    
    # Get critique from LLM
    critique_message = llm.invoke(state["messages"])
    
    # Append critique to the state
    state["messages"].append({"role": "assistant", "content": critique_message.content})
    
    return state

# Function for revising the script based on the critique
def revise_script(state: State) -> State:
    critique = state["messages"][-1]["content"]
    revision_prompt = (
        "Using the critique below, revise the original script to improve it. Focus on the areas where the critique suggests improvements."
        "Provide the revised version of the script, incorporating the suggested changes."
        "\n\nCritique:\n" + critique
    )
    
    # Invoke LLM to revise the script based on the critique
    state["messages"].append({"role": "user", "content": revision_prompt})
    revised_message = llm.invoke(state["messages"])

    # Append the revised script to the state
    state["messages"].append({"role": "assistant", "content": revised_message.content})

    return state

# Self-Critiquing and Revision Loop
def self_critique_and_revise(state: State) -> State:
    # Generate the initial script
    state = script_generator(state)
    
    # Critique the generated script
    state = critique_script(state)
    
    # Revise the script based on critique
    state = revise_script(state)
    
    # Critique the revised script again
    state = critique_script(state)
    
    # If the critique is not ideal (or we need more revisions), keep revising
    # You can implement a loop or condition to continue refining until a certain score threshold is met
    return state

# Graph Builder
graph_builder = StateGraph(State)
tool = TavilySearchResults(max_results=2)
tools = [tool]
llm_with_tools = llm.bind_tools(tools)

# Add nodes to the graph
graph_builder.add_node("script", script_generator)
tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

# Conditional edge for calling tools
graph_builder.add_conditional_edges("script", tools_condition)
graph_builder.add_edge("tools", "script")
graph_builder.add_edge(START, "script")
graph = graph_builder.compile()

# User input
user_input = "Conversation between Barney from How i met your mother and Walter from Breaking Bad."

# Configuration
def get_content(user_input):
    config = {"configurable": {"thread_id": "1"}}
    full_content = ""

    # Stream the graph with the user input
    events = graph.stream({"messages": [("user", user_input)]}, config, stream_mode="values")
    
    for event in events:
        # Assuming event["messages"][-1] is an instance of HumanMessage
        last_message = event["messages"][-1]
        
        # Access the content of the last message properly (adjust this based on actual object structure)
        content = last_message.content  # Assuming 'content' is an attribute, not a dictionary
        
        # Append the content to full_content
        full_content += content + "\n"
    
    return full_content

# Call the function with user_input
user_input = "Conversation between Barney from How I Met Your Mother and Walter from Breaking Bad."
result = get_content(user_input)
print(result)


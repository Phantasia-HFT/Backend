def parser(content):
    script_lines = content.splitlines()
    formatted_script = []

    for line in script_lines:
        # Split the line into name and content at the first colon
        if ':' in line:
            name, content = line.split(":", 1)  # Split only at the first colon
            formatted_script.append([name.strip(), content.strip()])  #
    print(formatted_script)
    return formatted_script

#this was for testing

'''script= """Barney: Hey, Walter, you know, I have to admit, I never thought we'd be having this conversation.
Walter: Yeah, well, life has a funny way of throwing curveballs, doesn't it?
Barney: You can say that again. So, tell me, what's the plan here? How do we make this work?
Walter: [pauses] First, you need to understand the risks involved, Barney."""

parser(script)'''
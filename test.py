import requests
from helper import parser
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
groq_api=os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api)
filename = os.path.dirname(__file__) + "/audio/audio1.mp3"

with open(filename, "rb") as file:
    transcription = client.audio.transcriptions.create(
      file=(filename, file.read()),
      model="whisper-large-v3",
      response_format="verbose_json",
    )
    print(transcription.text)
      
# Data you want to send as JSON in the body
data = {'user_input': 'phil from modern family and chandler arguing'}

# Sending the POST request with JSON body
response = requests.post("http://127.0.0.1:5000/getscript", json=data)

# Check the response status and content
print(response.status_code)
print(response.json())  # If the response is JSON, this will parse and print it
parser(response.json()['script'])
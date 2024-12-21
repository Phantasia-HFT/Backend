from flask import Flask, render_template, request, jsonify
from agents import get_content
import os
from groq import Groq


app = Flask(__name__)
client=Groq()
@app.route('/getscript', methods=['POST'])
def get_script():
    if request.method == 'POST':
        # Assuming the incoming data is JSON
        data = request.get_json()  # This will parse the JSON body
        
        # Example of extracting user input (make sure it's passed as a key in the JSON body)
        user_input = data.get('user_input')
        
        if user_input:
            script = get_content(user_input)  # Assuming your get_content function handles the input
            return jsonify({"script": script}), 200  # Return the generated script as a JSON response
        else:
            return jsonify({"error": "No user_input provided"}), 400

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save the uploaded file temporarily
    temp_path = f"./{file.filename}"
    file.save(temp_path)
    
    try:
        # Transcribe the audio
        with open(temp_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(temp_path, file.read()),
                model="whisper-large-v3",
                response_format="verbose_json",
                )
        print(transcription.text)
    finally:
        # Clean up the temporary file
        os.remove(temp_path)

if __name__ == '__main__':
    app.run()
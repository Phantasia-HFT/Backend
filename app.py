from flask import Flask, render_template, request, jsonify , send_file
from agents import get_content
import os
from groq import Groq
from helper import parser
import time
from elevenlabs import ElevenLabs
from request import convert_text_to_speech
from  dotenv import load_dotenv
from mergefiles import merge_audio_files

load_dotenv()
voice_id1=os.getenv("voicemodel_id_phil")
voice_id2=os.getenv("voicemodel_id_walter")


app = Flask(__name__)
client=Groq()
@app.route('/getscript', methods=['POST'])
def get_script():
    if request.method == 'POST':
        data = request.get_json()  # Parse JSON input
        
        user_input = data.get('user_input')
        if not user_input:
            return jsonify({"error": "No user_input provided"}), 400
        
        script = get_content(user_input)  # Fetch script content
        formatted_script = parser(script)  # Parse the script
        print("Formatted Script:", formatted_script)
        
        count = 0  # Initialize count for unique filenames
        for element in formatted_script:
            speaker, dialogue = element[0], element[1]
            
            if speaker and dialogue:
                print(f"Processing: {speaker}: {dialogue}")
                
                # Determine the voice ID based on the speaker
                voice_id = voice_id1 if speaker == "Phil Dunphy" else voice_id2 if speaker == "Walter White" else None
                
                if voice_id:
                    convert_text_to_speech(dialogue, voice_id, count)
                    count += 1  # Increment count for unique filenames
            else:
                print(f"Skipped invalid element: {element}")
        merge_audio_files("./audio","./finalaudio.mp3")

        output_file = "./finalaudio.mp3"
        if os.path.exists(output_file):
            return send_file(output_file, as_attachment=True, download_name="finalaudio.mp3", mimetype="audio/mpeg")
        else:
            return jsonify({"error": "Failed to generate audio file"}), 500

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

##Post request to get the audio from 11labs

@app.route("/getaudio", methods=["POST"])
def get_audio():
    if request.method == 'POST':
        pass


if __name__ == '__main__':
    app.run()
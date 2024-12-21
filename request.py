import time
from elevenlabs import ElevenLabs
from  dotenv import load_dotenv
import os


load_dotenv()
elevenlabs_api =  os.getenv("elevenlabs_id")

client = ElevenLabs(api_key=elevenlabs_api)
output_format = "mp3_44100_128"
voice_settings = {
    "stability": 0.3,
    "similarity_boost": 0.9,
    "style": 0.6
}

def convert_text_to_speech(text, voice_id, count):
    try:
        # Ensure the output directory exists
        output_dir = "./audio"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate audio
        audio_generator = client.text_to_speech.convert(
            voice_id=voice_id,
            output_format=output_format,
            text=text,
            model_id="eleven_multilingual_v2",
            voice_settings=voice_settings
        )
        
        # Save the audio file with a unique name
        filename = f"{output_dir}/output{count}.mp3"
        with open(filename, "wb") as audio_file:
            for chunk in audio_generator:
                audio_file.write(chunk)
        print(f"Audio saved as {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    return True


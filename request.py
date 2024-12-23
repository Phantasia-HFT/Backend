import time
from elevenlabs import ElevenLabs
from  dotenv import load_dotenv
import os
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

load_dotenv()
elevenlabs_api =  os.getenv("elevenlabs_id")

client = ElevenLabs(api_key=elevenlabs_api)
output_format = "mp3_44100_128"
voice_settings = {
    "stability": 0.3,
    "similarity_boost": 0.9,
    "style": 0.6
}

# Cloudinary Configuration          
cloudinary.config( 
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"), 
    api_key = os.getenv("CLOUDINARY_API_KEY"), 
    api_secret =os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

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

def upload_to_cloudinary(file_path):
    try:
        response = cloudinary.uploader.upload(
            file_path,
            resource_type="video",  # Use "video" for audio files
            folder = "audio_files",
            use_filename=True,
            unique_filename=True
        )
        print(f"File uploaded successfully. URL: {response['secure_url']}")
        return response['secure_url']
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None


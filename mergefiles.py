import os
from pydub import AudioSegment

def merge_audio_files(input_folder, output_file):
    try:
        audio_files = sorted(
            [f for f in os.listdir(input_folder) if f.endswith('.mp3') and os.path.isfile(os.path.join(input_folder, f))],
            key=lambda x: int(x.split('output')[-1].split('.mp3')[0])
        )

        combined = AudioSegment.empty()
        for audio_file in audio_files:
            file_path = os.path.join(input_folder, audio_file)
            try:
                print(f"Adding {file_path} to the final output...")
                audio_segment = AudioSegment.from_file(file_path)
                combined += audio_segment
            except Exception as e:
                print(f"Skipping {file_path} due to an error: {e}")

        combined.export(output_file, format="mp3")
        print(f"All files merged successfully into {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            for file_name in os.listdir(input_folder):
                file_path = os.path.join(input_folder, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Removed {file_path}")
        except Exception as e:
            print(f"Error while cleaning up the folder: {e}")


if __name__ == "__main__":
    input_folder = "./audio"
    output_file = "./merged_output.mp3"
    merge_audio_files(input_folder, output_file)

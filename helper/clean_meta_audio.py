import os
import wave

def remove_metadata(input_file, output_file):
    try:
        # Open the input WAV file
        with wave.open(input_file, 'rb') as wav_in:
            # Get parameters from the input WAV file
            params = wav_in.getparams()
            n_frames = wav_in.getnframes()
            
            # Read raw audio data
            audio_data = wav_in.readframes(n_frames)

            # Write raw audio data to the output WAV file
            with wave.open(output_file, 'wb') as wav_out:
                wav_out.setparams(params)
                wav_out.writeframes(audio_data)
        
        print(f"Metadata removed from: {input_file} -> {output_file}")
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

def process_folder(input_folder, output_folder):
    try:
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        
        # Loop through all files in the input folder
        for file_name in os.listdir(input_folder):
            # Full path to the input file
            input_path = os.path.join(input_folder, file_name)
            
            # Check if it's a WAV file
            if os.path.isfile(input_path) and file_name.lower().endswith('.wav'):
                # Full path to the output file
                output_path = os.path.join(output_folder, file_name)
                remove_metadata(input_path, output_path)
    except Exception as e:
        print(f"Error processing folder: {e}")

# Example usage
input_folder = '/Users/PhanithLIM/Downloads/vannda copy'  # Replace with your input folder path
output_folder = 'output'
process_folder(input_folder, output_folder)

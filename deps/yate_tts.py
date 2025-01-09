#!/usr/bin/env python3
import subprocess
import os

def generate_raw_audio(piper_path, model_path, text, output_file):
    """
    Generate raw audio files with Piper TTS.

    Parameters:
        piper_path (str): The path to the Piper executable.
        model_path (str): The path to the Piper model file.
        text (str): The text to synthesize.
        output_file (str): The path to save the raw audio file.

    Returns:
        bool: True if the process succeeded, False otherwise.
    """
    try:
        # Generate a temporary WAV file
        temp_wav_file = "temp_output.wav"

        # Construct Piper command
        command = [
            piper_path,
            "--model", model_path,
            "--output_file", temp_wav_file
        ]

        # Run Piper
        subprocess.run(command, input=text, text=True, check=True)

        # Convert WAV to RAW with specific format (8000 Hz, Mono)
        command_raw = [
            "ffmpeg",
            "-y",  # Overwrite output file if it exists
            "-i", temp_wav_file,
            "-ar", "8000",  # Set sample rate to 8000 Hz
            "-ac", "1",  # Set channels to Mono
            "-f", "s16le",  # Set RAW format
            output_file
        ]

        subprocess.run(command_raw, check=True)

        # Cleanup temporary WAV file
        if os.path.exists(temp_wav_file):
            os.remove(temp_wav_file)

        print(f"Audio saved to {output_file}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error during audio generation: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    # Example usage
    piper_executable = "/home/c3telegaming/c3telegaming/deps/venv/bin/piper"
    model_file = "/home/c3telegaming/c3telegaming/deps/de_DE-eva_k-x_low.onnx"
    text_to_speak = "ahoy, hier ist C3 Telegaming."
    output_raw_file = "/home/c3telegaming/c3telegaming/sounds/telegaming/intro.slin"

    success = generate_raw_audio(piper_executable, model_file, text_to_speak, output_raw_file)
    if success:
        print("Raw audio file generated successfully.")
    else:
        print("Failed to generate raw audio file.")

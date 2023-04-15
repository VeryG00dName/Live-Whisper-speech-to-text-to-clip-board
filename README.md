# Whisper Transcriber
This is a Python script that uses [Whisper](https://github.com/openai/whisper) to transcribe speech from the device microphone in real-time, translate it to English and copy it to the clipboard.

## Requirements
Python 3.6 or higher
* whisper
* os
* numpy
* sounddevice
* scipy
* keyboard
* pyperclip

## Usage
1. Clone or download this repository
2. Install the required modules using pip install -r requirements.txt
3. Run the script using python whisper_transcriber.py
4. Wait for it to load
5. Press f12 and speak into the microphone and wait for the transcription to appear in the console and clipboard
6. Press Ctrl+C to stop the script

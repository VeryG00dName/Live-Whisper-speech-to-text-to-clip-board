import whisper
import os
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import keyboard
import pyperclip

# This is my attempt to make psuedo-live transcription of speech using Whisper.
# Since my system can't use pyaudio, I'm using sounddevice instead.

Model = 'small'  # Whisper model size (tiny, base, small, medium, large)
English = True  # Use English-only model?
Translate = False  # Translate non-English to English?

SampleRate = 44100  # Stream device recording frequency

BlockSize = 30  # Block size in milliseconds
Threshold = 0.1  # Minimum volume threshold to activate listening
Vocals = [50, 1000]  # Frequency range to detect sounds that could be speech
EndBlocks = 40  # Number of blocks to wait before sending to Whisper


class StreamHandler:
    def __init__(self):
        self.running = True
        self.padding = 0
        self.prevblock = self.buffer = np.zeros((0,))
        self.fileready = False
        print("\033[96mLoading Whisper Model..\033[0m", end='', flush=True)
        self.model = whisper.load_model(f'{Model}{".en" if English else ""}')
        print("\033[90m Done.\033[0m")

    def callback(self, indata, frames, time, status):
        if not np.any(indata):
            return

        freq = np.argmax(np.abs(np.fft.rfft(indata[:, 0]))) * SampleRate / frames
        if np.sqrt(np.mean(indata**2)) > Threshold and Vocals[0] <= freq <= Vocals[1]:
            if self.padding < 1:
                self.buffer = self.prevblock.copy()
            self.buffer = np.concatenate((self.buffer, indata[:, 0]))
            self.padding = EndBlocks
        else:
            self.padding -= 1
            if self.padding > 1:
                self.buffer = np.concatenate((self.buffer, indata[:, 0]))
            elif self.padding < 1 < self.buffer.shape[0] > SampleRate:
                # if enough silence has passed, write to file.
                self.fileready = True
                write('dictate.wav', SampleRate, self.buffer)
                self.buffer = np.zeros((0,))

    def transcribe(self):
        transcript = whisper.transcribe(audio='dictate.wav', model=self.model, task='transcribe')
        print(transcript['text'])
        pyperclip.copy(transcript['text'])


streamer = StreamHandler()

def on_press(event):
    if event.name == 'f12':
        print('F12 key pressed. Recording audio...')
        with sd.InputStream(callback=streamer.callback):
            while not streamer.fileready:
                sd.sleep(BlockSize)
            streamer.transcribe()
            streamer.fileready = False


print('Program ready. Press F12 to record audio.')
# Listen for key press
keyboard.on_press(on_press)
keyboard.wait()
# # For testing purposes, so I can get access to speech_recog testing file
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import os
# Get the directory where the current script is located
current_dir = os.path.abspath(os.path.dirname(__file__))
# Construct the full path to the audio file
audio_file_path = os.path.join(current_dir, "normalAudio.wav")

import pytest
from speech_recog import transcription

def test_transcribe_normal_hello():
    text = transcription(audio_file_path)
    print(text);
    assert text == "hello my name is william"
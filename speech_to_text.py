import time
from models_loader import stt_model

WAKE_WORD = "hey"

def transcribe(wav_path):
    start_time = time.time()
    text = ""
    segments = stt_model.transcribe(wav_path)
    for segment in segments:
        text += segment.text
    print(f"Transcription completed in {(time.time() - start_time) * 1000:.2f}ms. Text is: '{text}'")
    return text

def detect_wake_word(audio_file):
    result = stt_model.transcribe(audio_file)
    text = " ".join([seg.text.lower() for seg in result])
    return WAKE_WORD in text
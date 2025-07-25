from pywhispercpp.model import Model

WAKE_WORD = "computer"
whisper = Model("whisper_models/ggml-tiny.en.bin")

def transcribe(wav_path):
    text = ""
    segments = whisper.transcribe(wav_path)
    for segment in segments:
        text += segment.text
    print(f"Transcribed text is: '{text}'")
    return text

def detect_wake_word(audio_file):
    result = whisper.transcribe(audio_file)
    text = " ".join([seg.text.lower() for seg in result])
    print(f"Transcript: {text}")
    return WAKE_WORD in text
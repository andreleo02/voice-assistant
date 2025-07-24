from pywhispercpp.model import Model

whisper = Model("whisper_models/ggml-tiny.en.bin")

def transcribe(wav_path):
    text = ""
    segments = whisper.transcribe(wav_path)
    for segment in segments:
        text += segment.text
    print(f"Transcribed text is: '{text}'")
    return text
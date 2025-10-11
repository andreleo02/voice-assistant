import time
from resource_watcher import monitor_resources
from mqtt_bridge import publish

WAKE_WORD = "assistant"

@monitor_resources("STT", interval=0.5)
def transcribe(stt_model, wav_path):
    """
    Transcription of the audio file in text
    using speech-to-text model (Whisper Tiny)
    """
    start_time = time.time()
    text = ""
    segments = stt_model.transcribe(wav_path)
    for segment in segments:
        text += segment.text
    print(f"[STT] Transcription completed in {(time.time() - start_time) * 1000:.2f}ms. Text is: '{text}'")
    publish("assistant/stt", text)
    return text

def detect_wake_word(stt_model, audio_file):
    """
    Transcription of the audio file in text
    using speech-to-text model (Whisper Tiny) and wake-word detection
    """
    result = stt_model.transcribe(audio_file)
    text = " ".join([seg.text.lower() for seg in result])
    print(f"[STT] Wake-word detection text is '{text}'")
    return WAKE_WORD in text
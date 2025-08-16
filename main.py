import os
from pathlib import Path
os.environ["TTS_HOME"] = str((Path.cwd() / "tts_models").resolve())
import time
import threading
from text_to_speech import audio_player
from llm_engine import stream_and_speak
from microphone_listener import record_audio
from audio_file_queue import audio_done_event
from speech_to_text import transcribe, detect_wake_word

def run_conversation():
    print("LISTENING ...")

    # setup a microphone input to listen for user queries
    audio_file = record_audio(duration=5)

    print("THINKING ...")

    # convert the audio to a prompt (STT using Whisper)
    transcription = transcribe(wav_path=audio_file)

    # run a small LLM locally to generate a text response based on the input
    stream_and_speak(prompt=transcription)

# coordinate the entire process through a controller script
if __name__ == "__main__":
    threading.Thread(target=audio_player, daemon=True).start()
    print("ASSISTANT READY. WAITING FOR TRIGGER WORD ...")
    while True:
        audio_done_event.wait()
        file = record_audio(duration=2)
        if detect_wake_word(file):
            run_conversation()
            print("WAITING FOR TRIGGER WORD ...")
        time.sleep(0.2)
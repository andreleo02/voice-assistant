import os
import threading
from pathlib import Path
from text_to_speech import audio_player
from llm_engine import stream_and_speak
from microphone_listener import record_audio
from audio_file_queue import audio_done_event
from speech_to_text import transcribe, detect_wake_word

os.environ["TTS_HOME"] = str((Path.cwd() / "tts_models").resolve())

def run_conversation():
    """
    Executes the conversation flow. (1) Audio prompt recording,
    (2) speech-to-text conversion, (3) LLM prompt submission and response streaming,
    (4) text-to-speech response conversion.
    """
    print("[MAIN] LISTENING ...")

    # setup a microphone input to listen for user queries
    audio_file = record_audio()

    print("[MAIN] THINKING ...")

    # convert the audio to a prompt (STT using Whisper)
    transcription = transcribe(wav_path=audio_file)

    # run a small LLM locally to generate a text response based on the input
    stream_and_speak(prompt=transcription)

# coordinate the entire process through a controller script
if __name__ == "__main__":
    threading.Thread(target=audio_player, daemon=True).start()
    print("[MAIN] ASSISTANT SETUP COMPLETED.")
    while True:
        audio_done_event.wait()
        print("[MAIN] WAITING FOR TRIGGER WORD ...")
        file = record_audio()
        if detect_wake_word(file):
            run_conversation()
import time
import threading
from microphone_listener import record_audio
from speech_to_text import transcribe, detect_wake_word
from llm_engine import stream_and_speak
from text_to_speech import audio_player
from audio_file_queue import audio_done_event

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
    while True:
        audio_done_event.wait()
        print("WAITING FOR TRIGGER WORD ...")
        file = record_audio(duration=3)
        if detect_wake_word(file):
            print("Wake word detected! Start conversation ...")
            run_conversation()
        time.sleep(0.5)
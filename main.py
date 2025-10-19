import os
import sys
import threading
from pathlib import Path
from text_to_speech import audio_player
from llm_engine import stream_and_speak
from init_assistant import init_components
from microphone_listener import record_audio
from audio_file_queue import audio_done_event
from speech_to_text import transcribe, detect_wake_word
from mqtt_bridge import mqtt_client, publish, stop_mqtt, shutdown_event

os.environ["TTS_HOME"] = str((Path.cwd() / "tts_models").resolve())

def run_conversation(recognizer, stt_model, llm_model, tts_model):
    """
    Executes the conversation flow. (1) Audio prompt recording,
    (2) speech-to-text conversion, (3) LLM prompt submission and response streaming,
    (4) text-to-speech response conversion.
    """
    print("[MAIN] LISTENING ...")

    # setup a microphone input to listen for user queries
    audio_file = record_audio(r=recognizer)

    print("[MAIN] THINKING ...")
    publish("assistant/state", "thinking")

    # convert the audio to a prompt (STT using Whisper)
    transcription = transcribe(stt_model=stt_model, wav_path=audio_file)

    # run a small LLM locally to generate a text response based on the input
    stream_and_speak(llm_model=llm_model, prompt=transcription, tts_model=tts_model)

# coordinate the entire process through a controller script
if __name__ == "__main__":
    mqtt_client()
    try:
        recognizer, stt_model, llm_model, tts_model = init_components()
        threading.Thread(target=audio_player, daemon=True).start()
        print("[MAIN] ASSISTANT SETUP COMPLETED")
        while not shutdown_event.is_set():
            audio_done_event.wait()
            print("[MAIN] WAITING FOR TRIGGER WORD ...")
            publish("assistant/state", "ready")
            while not audio_done_event.wait(timeout=0.5):
                if shutdown_event.is_set():
                    break
            if shutdown_event.is_set():
                break
            file = record_audio(r=recognizer)
            if detect_wake_word(stt_model=stt_model, audio_file=file):
                publish("assistant/state", "listening")
                run_conversation(recognizer=recognizer,
                                stt_model=stt_model,
                                llm_model=llm_model,
                                tts_model=tts_model)
    finally:
        stop_mqtt()
        sys.exit(0)
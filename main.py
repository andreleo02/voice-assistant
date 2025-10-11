import os
import threading
from pathlib import Path
from text_to_speech import audio_player
from llm_engine import stream_and_speak
from init_assistant import init_components
from microphone_listener import record_audio
from audio_file_queue import audio_done_event
from speech_to_text import transcribe, detect_wake_word
from mqtt_bridge import mqtt_client, publish, paused_event, cmd_queue

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

    # convert the audio to a prompt (STT using Whisper)
    transcription = transcribe(stt_model=stt_model, wav_path=audio_file)

    # run a small LLM locally to generate a text response based on the input
    stream_and_speak(llm_model=llm_model, prompt=transcription, tts_model=tts_model)

# coordinate the entire process through a controller script
if __name__ == "__main__":
    mqtt_client()
    recognizer, stt_model, llm_model, tts_model = init_components()
    threading.Thread(target=audio_player, daemon=True).start()
    print("[MAIN] ASSISTANT SETUP COMPLETED"); publish("assistant/state", "ready")
    while True:
        publish("assistant/state", "idle")
        audio_done_event.wait()
        print("[MAIN] WAITING FOR TRIGGER WORD ...")
        while paused_event.is_set():
            publish("assistant/state", "paused")
            try:
                cmd, text = cmd_queue.get(timeout=0.5)
                if cmd == "say":
                    stream_and_speak(llm_model=llm_model, prompt=text, tts_model=tts_model)
            except Exception:
                pass
        file = record_audio(r=recognizer)
        if detect_wake_word(stt_model=stt_model, audio_file=file):
            run_conversation(recognizer=recognizer,
                             stt_model=stt_model,
                             llm_model=llm_model,
                             tts_model=tts_model)
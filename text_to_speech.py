import os
import time
from playsound3 import playsound
from audio_file_queue import audio_queue, audio_done_event

def synthesize_text(tts_model, text, folder="outputs", prefix="chunk"):
    """
    Receives text and synthesizes it in a wav file using text-to-speech model
    """
    start_time = time.time()
    os.makedirs(folder, exist_ok=True)
    timestamp = int(start_time * 1000)
    output_path = os.path.join(folder, f"{prefix}_{timestamp}.wav")
    tts_model.tts_to_file(text=text, file_path=output_path)
    print(f"[TTS] Audio synthesized in {(time.time() - start_time) * 1000:.2f}ms")
    return output_path

def audio_player():
    """
    Reads continuously from the audio queue synthesized speechs,
    reproduces them and deletes from the system
    """
    while True:
        try:
            file = audio_queue.get()
            if file is None:
                time.sleep(0.5)
                continue
            audio_done_event.clear()
            try:
                print("[MAIN] SPEAKING ...")
                playsound(file)
            except Exception as e:
                print(f"[AUDIO PLAYER] Playback error: {e}")
            try:
                os.remove(file)
            except Exception as e:
                print(f"[AUDIO PLAYER] Failed to delete {file}: {e}")
            if audio_queue.empty():
                audio_done_event.set()
        except Exception as e:
            print(f"[AUDIO PLAYER] Top-level exception: {e}")
            audio_done_event.set()
        time.sleep(0.3)

import os
import time
from TTS.api import TTS
from playsound3 import playsound
from audio_file_queue import audio_queue, audio_done_event

model_dir = "tts_models"
model_path = os.path.join(model_dir, "tts", "tts_models--en--ljspeech--tacotron2-DDC", "model.pth")
config_path = os.path.join(model_dir, "tts", "tts_models--en--ljspeech--tacotron2-DDC", "config.json")
vocoder_path = os.path.join(model_dir, "tts", "vocoder_models--en--ljspeech--hifigan_v2", "model.pth")
vocoder_config_path = os.path.join(model_dir, "tts", "vocoder_models--en--ljspeech--hifigan_v2", "config.json")

tts = TTS(
    model_path=model_path,
    config_path=config_path,
    vocoder_path=vocoder_path,
    vocoder_config_path=vocoder_config_path,
    progress_bar=False,
    gpu=False,
)

def synthesize_text(text, folder="outputs", prefix="chunk"):
    os.makedirs(folder, exist_ok=True)
    timestamp = int(time.time() * 1000)
    output_path = os.path.join(folder, f"{prefix}_{timestamp}.wav")
    tts.tts_to_file(text=text, file_path=output_path)
    return output_path

def audio_player():
    while True:
        try:
            file = audio_queue.get()

            if file is None:
                time.sleep(0.1)
                continue

            audio_done_event.clear()

            try:
                print("SPEAKING ...")
                playsound(file)
            except Exception as e:
                print(f"[AudioPlayer] Playback error: {e}")

            try:
                os.remove(file)
            except Exception as e:
                print(f"[AudioPlayer] Failed to delete {file}: {e}")

            if audio_queue.empty():
                print("[AudioPlayer] Queue empty, setting event.")
                audio_done_event.set()

        except Exception as e:
            print(f"[AudioPlayer] Top-level exception: {e}")
            audio_done_event.set()
        time.sleep(0.5)

import os
import time
import platform
from TTS.api import TTS
from audio_file_queue import audio_queue, audio_done_event

model_dir = "tts_models"
model_path = os.path.join(model_dir, "tts_models--en--ljspeech--tacotron2-DDC", "model.pth")
config_path = os.path.join(model_dir, "tts_models--en--ljspeech--tacotron2-DDC", "config.json")
vocoder_path = os.path.join(model_dir, "vocoder_models--en--ljspeech--hifigan_v2", "model.pth")
vocoder_config_path = os.path.join(model_dir, "vocoder_models--en--ljspeech--hifigan_v2", "config.json")

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

def play_wav_blocking(path):
    if platform.system() == "Darwin":
        return os.system(f"afplay '{path}'")
    elif platform.system() == "Linux":
        return os.system(f"aplay '{path}'")
    elif platform.system() == "Windows":
        return os.system(f'start /wait wmplayer "{path}"')
    else:
        raise RuntimeError("Unsupported platform for audio playback")

def audio_player():
    while True:
        file = audio_queue.get()
        if file is None:
            time.sleep(0.3)
            continue
        try:
            print("SPEAKING ...")
            audio_done_event.clear()
            play_wav_blocking(file)
        finally:
            try:
                os.remove(file)
            except Exception as e:
                print(f"Failed to delete audio file {file}: {e}")
            if audio_queue.empty():
                audio_done_event.set()

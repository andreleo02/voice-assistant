import os
from TTS.utils.manage import ModelManager

def download_model(save_dir="tts_models"):
    os.makedirs(save_dir, exist_ok=True)
    manager = ModelManager()

    model_name = "tts_models/en/ljspeech/tacotron2-DDC"
    model_path = manager.download_model(model_name)

    print("Coqui TTS model and vocoder downloaded.")
    print("Model Path:", model_path)

if __name__ == "__main__":
    download_model()

import os
from TTS.utils.manage import ModelManager

def download_models(save_dir="tts_models"):
    os.makedirs(save_dir, exist_ok=True)
    manager = ModelManager()

    model_name = "tts_models/en/ljspeech/tacotron2-DDC"
    manager.download_model(model_name)

    model_name = "vocoder_models/en/ljspeech/hifigan_v2"
    manager.download_model(model_name)

    print("Coqui TTS model and vocoder downloaded.")

if __name__ == "__main__":
    download_models()

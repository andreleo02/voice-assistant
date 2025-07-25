from TTS.api import TTS
import os
import platform

def speak(text, output_path="response.wav"):
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
    if os.path.exists(output_path):
        os.remove(output_path)
    tts.tts_to_file(text=text, file_path=output_path)

    print("SPEAKING ...")
    if platform.system() == "Darwin":
        os.system(f"afplay {output_path}")
    elif platform.system() == "Linux":
        os.system(f"aplay {output_path}")
    elif platform.system() == "Windows":
        os.system(f'start /min wmplayer "{output_path}"')

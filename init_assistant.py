import os
import time
from TTS.api import TTS
from llama_cpp import Llama
import speech_recognition as sr
from pywhispercpp.model import Model
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

WHISPER_PATH = PROJECT_ROOT / "whisper_models" / "ggml-tiny.en.bin"
LLM_PATH = PROJECT_ROOT / "llm_models" / "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
TTS_DIR = PROJECT_ROOT / "tts_models"

def init_speech_recognition():
    """
    Initialize speech recognition component
    """
    start_time = time.time()
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=16_000) as source:
        r.adjust_for_ambient_noise(source, duration=1.0)
        r.pause_threshold = 0.8
    print(F"[INIT] Speech recognizer loaded in {(time.time() - start_time) * 1000:.2f}ms")
    return r

def load_stt():
    """
    Loads speech-to-text model
    """
    start_time = time.time()
    stt = Model(WHISPER_PATH.absolute().as_posix())
    print(f"[INIT] STT model loaded in {(time.time() - start_time) * 1000:.2f}ms")
    return stt

def load_llm():
    """
    Loads LLM model
    """
    start_time = time.time()
    llm = Llama(
        model_path=LLM_PATH.absolute().as_posix(),
        n_ctx=2048,
        n_threads=8,
        n_gpu_layers=0
    )
    print(f"[INIT] LLM model loaded in {(time.time() - start_time) * 1000:.2f}ms")
    return llm

def load_tts():
    """
    Loads text-to-speech model
    """
    start_time = time.time()
    model_dir = TTS_DIR
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
    print(f"[INIT] TTS model loaded in {(time.time() - start_time) * 1000:.2f}ms")
    return tts

def init_components():
    return init_speech_recognition(), load_stt(), load_llm(), load_tts()
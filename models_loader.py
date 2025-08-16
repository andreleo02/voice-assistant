import os
import time
from TTS.api import TTS
from llama_cpp import Llama
from pywhispercpp.model import Model

def load_stt():
    start_time = time.time()
    stt = Model("whisper_models/ggml-tiny.en.bin")
    print(f"STT model loaded in {(time.time() - start_time) * 1000:.2f}ms")
    return stt

def load_llm():
    start_time = time.time()
    llm = Llama(
        model_path="./llm_models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        n_ctx=2048,
        n_threads=8,
        n_gpu_layers=0
    )
    print(f"LLM model loaded in {(time.time() - start_time) * 1000:.2f}ms")
    return llm

def load_tts():
    start_time = time.time()
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
    print(f"TTS model loaded in {(time.time() - start_time) * 1000:.2f}ms")
    return tts

stt_model = load_stt()
llm_model = load_llm()
tts_model = load_tts()
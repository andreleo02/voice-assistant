import os
import time
import subprocess
from pathlib import Path

start_time = time.time()

os.environ["CMAKE_GENERATOR"] = "NMake Makefiles"
os.environ["DISTUTILS_USE_SDK"] = "1"
os.environ["USE_VS2022"] = "1"
os.environ["TTS_HOME"] = str((Path.cwd() / "tts_models").resolve())

def run(command, check=False):
    print(f"Running: {command}")
    subprocess.run(command, shell=True, check=check)

def download_file(url, dest_path):
    if not dest_path.exists():
        print(f"Downloading {dest_path.name}...")
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        run(f"curl -L -o {dest_path} {url}")

print("Setting up offline voice assistant environment...")

# --- Create virtual environment ---
venv_path = Path("venv")
if not venv_path.exists():
    print("Creating virtual environment 'venv'...")
    run("python3 -m venv venv")

venv_python = venv_path / "Scripts" / "python.exe"
activate_script = venv_path / "Scripts" / "activate.bat"
run(f"{activate_script} && {venv_python} -m pip install --upgrade pip")

# --- Install only torch (without GPU) ---
run(f"{activate_script} && {venv_python} -m pip install torch --index-url https://download.pytorch.org/whl/cpu")

# --- Install required packages ---
packages = [
    "llama-cpp-python", "coqui-tts", "pywhispercpp", "sounddevice",
    "scipy", "numpy", "huggingface_hub", "playsound3"
]
print("Installing Python dependencies...")
run(f"{activate_script} && {venv_python} -m pip install " + " ".join(packages))

# --- Whisper Tiny Model ---
whisper_model = Path("whisper_models/ggml-tiny.en.bin")
download_file(
    "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin",
    whisper_model
)

# --- LLaMA Model ---
llama_model = Path("llm_models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")
if not llama_model.exists():
    print("Downloading Tiny LLaMA model via Python...")
    run(f"{venv_python} llm_model_downloader.py")

# --- TTS Models ---
tts_model_dir = Path("tts_models")
tts_model = tts_model_dir / "tts_models--en--ljspeech--tacotron2-DDC"
vocoder_model = tts_model_dir / "vocoder_models--en--ljspeech--hifigan_v2"
if not tts_model.exists():
    print("Downloading TTS models via Python...")
    run(f"{venv_python} tts_model_downloader.py")

print(rf"Setup complete in {(time.time() - start_time) * 1000:.2f}ms.")
print(r"To launch the application, activate the environment with venv\Scripts\activate and run: python main.py")

import os
import subprocess
from pathlib import Path

os.environ["CMAKE_GENERATOR"] = "NMake Makefiles"
os.environ["DISTUTILS_USE_SDK"] = "1"
os.environ["USE_VS2022"] = "1"

def run(command, check=True):
    print(f"Running: {command}")
    subprocess.run(command, shell=True, check=check)

def download_file(url, dest_path):
    if not dest_path.exists():
        print(f"Downloading {dest_path.name}...")
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        run(f"curl -L -o {dest_path} {url}")
    else:
        print(f"File already exists: {dest_path}")

def create_symlink(source, target):
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        print(f"Creating symlink from {source} to {target}")
        target.symlink_to(source)
    else:
        print(f"Symlink already exists: {target}")

print("Setting up offline voice assistant environment...")

# --- Create virtual environment ---
venv_path = Path("venv")
if not venv_path.exists():
    print("Creating virtual environment 'venv'...")
    run("python3 -m venv venv")

activate_script = venv_path / "Scripts" / "activate.bat"
pip_script = venv_path / "Scripts" / "python.exe"
run(f"{activate_script} && {pip_script} -m pip install --upgrade pip", check=False)

# --- Install required packages ---
packages = [
    "llama-cpp-python", "coqui-tts", "pywhispercpp", "sounddevice",
    "scipy", "numpy", "huggingface_hub", "playsound3"
]
print("Installing Python dependencies...")
run(f"{activate_script} && {pip_script} -m pip install " + " ".join(packages), check=False)

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
    run("python3 llm_model_downloader.py")

# --- TTS Models ---
tts_model_dir = Path("tts_models")
tts_model = tts_model_dir / "tts_models--en--ljspeech--tacotron2-DDC"
vocoder_model = tts_model_dir / "vocoder_models--en--ljspeech--hifigan_v2"
if not tts_model.exists():
    print("Downloading TTS models via Python...")
    run("python3 tts_model_downloader.py")

    local_tts_base = Path.home() / ".local/share/tts"
    create_symlink(local_tts_base / tts_model.name, tts_model)
    create_symlink(local_tts_base / vocoder_model.name, vocoder_model)

print("Setup complete. To activate the environment, run: source venv/bin/activate")
print("To launch the application, run: python3 main.py")

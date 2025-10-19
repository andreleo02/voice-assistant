import os
import sys
import time
import platform
import subprocess
from pathlib import Path
from urllib.request import urlretrieve

start_time = time.time()

# --- lock working dir to the project root ---
PROJECT_ROOT = Path(__file__).resolve().parent
os.chdir(PROJECT_ROOT)

# env for Coqui TTS build cache and Windows toolchain
os.environ["CMAKE_GENERATOR"] = "NMake Makefiles"
os.environ["DISTUTILS_USE_SDK"] = "1"
os.environ["USE_VS2022"] = "1"
os.environ["TTS_HOME"] = str((PROJECT_ROOT / "tts_models").resolve())

def runp(args, **kw):
    print("Running:", " ".join(map(str, args)))
    subprocess.run(args, check=True, **kw)

def download(url: str, dest: Path):
    if dest.exists():
        return
    print(f"Downloading {dest.name} …")
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(["curl", "-L", "-o", str(dest), url], check=True)
    except Exception:
        urlretrieve(url, dest)

print("Setting up offline voice assistant environment…")
print("Project root:", PROJECT_ROOT)

# --- Create virtual environment with the Python running this script ---
venv_path = PROJECT_ROOT / "venv"
if not venv_path.exists():
    print("Creating virtual environment 'venv' …")
    runp([sys.executable, "-m", "venv", str(venv_path)])

if platform.system().lower().startswith("win"):
    venv_python = venv_path / "Scripts" / "python.exe"
else:
    venv_python = venv_path / "bin" / "python"

# --- Upgrade pip ---
runp([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"])

# --- Torch CPU only (works offline) ---
runp([str(venv_python), "-m", "pip", "install", "torch",
      "--index-url", "https://download.pytorch.org/whl/cpu"])

# --- Install required packages ---
packages = [
    "llama-cpp-python", "coqui-tts", "pywhispercpp", "paho-mqtt",
    "playsound3", "huggingface_hub", "SpeechRecognition[audio]"
]
print("Installing Python dependencies …")
runp([str(venv_python), "-m", "pip", "install", *packages])

# --- Whisper Tiny model (path used by init_assistant.load_stt) ---
whisper_model = PROJECT_ROOT / "whisper_models" / "ggml-tiny.en.bin"
download("https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin",
         whisper_model)

# --- TinyLlama model (path used by init_assistant.load_llm) ---
llama_model = PROJECT_ROOT / "llm_models" / "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
if not llama_model.exists():
    print("Downloading TinyLLaMA via Python helper …")
    runp([str(venv_python), str(PROJECT_ROOT / "llm_model_downloader.py")])

# --- TTS models (paths used by init_assistant.load_tts) ---
tts_model_dir = PROJECT_ROOT / "tts_models"
tts_tacotron = tts_model_dir / "tts" / "tts_models--en--ljspeech--tacotron2-DDC"
vocoder = tts_model_dir / "tts" / "vocoder_models--en--ljspeech--hifigan_v2"
if not tts_tacotron.exists():
    print("Downloading TTS models via Python helper …")
    runp([str(venv_python), str(PROJECT_ROOT / "tts_model_downloader.py")])

# --- Create SQLite db folder and file ---
data_dir = PROJECT_ROOT / "data"
sqlite_db = data_dir / "assistant.db"
if not sqlite_db.exists():
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    open(sqlite_db, mode="x")


elapsed = (time.time() - start_time) / 60
print(f"Setup complete in {elapsed:.1f} min.")
print(r"To launch: venv\Scripts\python.exe main.py  (or use the Node-RED Exec node)")

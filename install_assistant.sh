#!/bin/bash

echo "Setting up offline voice assistant environment..."

# --- Create virtual environment ---
echo "Creating virtual environment 'venv'..."
python3 -m venv venv
source venv/bin/activate

# --- Upgrade pip ---
pip install --upgrade pip

# --- Install required Python packages ---
echo "Installing Python dependencies..."
pip install pyttsx3 llama-cpp-python coqui-tts git+https://github.com/absadiki/pywhispercpp sounddevice scipy numpy

# --- Installing system libraries ---
echo "Installing system libraries..."
sudo apt-get update && sudo apt-get install -y cmake libportaudio2

# --- Download Whisper Tiny English model ---
WHISPER_MODEL="whisper_models/ggml-tiny.en.bin"
if [ -f "$WHISPER_MODEL" ]; then
    echo "Whisper model already exists: $WHISPER_MODEL"
else
    echo "Downloading Whisper Tiny model..."
    mkdir -p whisper_models
    curl -L -o "$WHISPER_MODEL" https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin
fi

# --- Download Tiny Llama model ---
MODEL_DIR="llm_models"
MODEL_NAME="TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"
MODEL_FILE="tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
LLAMA_MODEL="$MODEL_DIR/$MODEL_FILE"
if [ -f "$LLAMA_MODEL" ]; then
    echo "Tiny Llama model already exists $LLAMA_MODEL"
else 
    pip install huggingface-hub

    mkdir -p $MODEL_DIR

    python3 - <<EOF
from huggingface_hub import hf_hub_download
print("Downloading TinyLlama-Chat model…")
hf_hub_download(
    repo_id="$MODEL_NAME",
    filename="$MODEL_FILE",
    local_dir="$MODEL_DIR",
    local_dir_use_symlinks=False
)
EOF

    echo "Model saved to $LLAMA_MODEL"
fi

TTS_MODELS_DIR="tts_models"
if [ -f "$TTS_MODELS_DIR" ]; then
    echo "TTS model already exists $TTS_MODELS_DIR"
else
    mkdir "$TTS_MODELS_DIR"
    python3 tts_model_downloader.py
    ln -s ~/.local/share/tts/tts_models--en--ljspeech--tacotron2-DDC $TTS_MODELS_DIR
    ln -s ~/.local/share/tts/vocoder_models--en--ljspeech--hifigan_v2 $TTS_MODELS_DIR
fi

echo "Setup complete. To activate the environment, run: source venv/bin/activate"
echo "To launch the application, run: python3 main.py"
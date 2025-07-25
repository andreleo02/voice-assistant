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
pip install llama-cpp-python coqui-tts pywhispercpp sounddevice scipy numpy huggingface-hub

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
MODEL_FILE="tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
LLAMA_MODEL="$MODEL_DIR/$MODEL_FILE"
if [ -f "$LLAMA_MODEL" ]; then
    echo "Tiny Llama model already exists $LLAMA_MODEL"
else
    python3 llm_model_downloader.py
fi

TTS_MODELS_DIR="tts_models"
TTS_MODEL="tts_models--en--ljspeech--tacotron2-DDC"
VOCODER_MODEL="vocoder_models--en--ljspeech--hifigan_v2"
if [ -d "$TTS_MODELS_DIR/$TTS_MODEL" ]; then
    echo "TTS model already exists $TTS_MODELS_DIR/$TTS_MODEL"
else
    python3 tts_model_downloader.py
    ln -s ~/.local/share/tts/$TTS_MODEL $TTS_MODELS_DIR/$TTS_MODEL
    ln -s ~/.local/share/tts/$VOCODER_MODEL $TTS_MODELS_DIR/$VOCODER_MODEL
fi

echo "Setup complete. To activate the environment, run: source venv/bin/activate"
echo "To launch the application, run: python3 main.py"
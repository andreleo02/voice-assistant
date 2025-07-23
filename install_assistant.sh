#!/bin/bash

# Setup script for Offline Voice Assistant

echo "Setting up offline voice assistant environment..."

# --- Create virtual environment ---
echo "Creating virtual environment 'venv'..."
python3 -m venv venv
source venv/bin/activate

# --- Upgrade pip ---
pip install --upgrade pip

# --- Install required Python packages ---
echo "Installing Python dependencies..."
pip install sounddevice scipy pyttsx3

# --- Ensure cmake is installed ---
if ! command -v cmake &> /dev/null; then
    echo "Installing cmake..."
    sudo apt-get update && sudo apt-get install -y cmake
fi

# --- Clone and build whisper.cpp ---
if [ -d "whisper.cpp" ]; then
    echo "whisper.cpp already exists, skipping clone."
else
    echo "Cloning whisper.cpp..."
    git clone https://github.com/ggerganov/whisper.cpp.git
fi
cd whisper.cpp
echo "Building whisper.cpp..."
make
cd ..

# --- Download Whisper Tiny English model ---
WHISPER_MODEL="whisper_models/ggml-tiny.en.bin"
if [ -f "$WHISPER_MODEL" ]; then
    echo "Whisper model already exists: $WHISPER_MODEL"
else
    echo "Downloading Whisper Tiny model..."
    mkdir -p whisper_models
    curl -L -o "$WHISPER_MODEL" https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin
fi

# --- Download GPT4All model (Groovy) ---
# echo "Downloading GPT4All Groovy model..."
# mkdir -p llm_models
# curl -L -o llm_models/ggml-gpt4all-j-v1.3-groovy.bin https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin

echo "Setup complete. To activate the environment, run: source venv/bin/activate"

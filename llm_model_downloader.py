import os
from huggingface_hub import hf_hub_download

def download_model(save_dir="llm_models"):
    os.makedirs(save_dir, exist_ok=True)
    print("Downloading TinyLlama-Chat model…")
    hf_hub_download(
        repo_id="TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
        filename="tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        local_dir=save_dir
    )

if __name__ == "__main__":
    download_model()
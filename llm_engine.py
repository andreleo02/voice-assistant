from llama_cpp import Llama
from text_to_speech import synthesize_text
from audio_file_queue import audio_queue

llm = Llama(
    model_path="./llm_models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=8,
    n_gpu_layers=0
)

def generate_response(prompt: str, system_message: str = "You are a helpful assistant."):
    full_prompt = f"<|system|>\n{system_message}</s>\n<|user|>\n{prompt}</s>\n<|assistant|>"
    stream = llm(
        full_prompt,
        max_tokens=256,
        stop=["</s>", "<|user|>"],
        echo=False,
        stream=True
    )

    buffer = ""
    for chunk in stream:
        token = chunk["choices"][0]["text"]
        buffer += token
        if token in [".", "!", "?", "\n"]:
            yield buffer.strip()
            buffer = ""
    if buffer.strip():
        yield buffer.strip()

def stream_and_speak(prompt: str):
    for phrase in generate_response(prompt):
        if not phrase:
            continue
        audio_path = synthesize_text(phrase)
        audio_queue.put(audio_path)
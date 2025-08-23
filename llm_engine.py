import time
from text_to_speech import synthesize_text
from audio_file_queue import audio_queue
from models_loader import llm_model

MAX_TOKENS = 256
MIN_BUFFER_LENGHT = 20

def generate_response(prompt: str, system_message: str = "You are a helpful assistant."):
    """
    Prompt submission to LLM model (TinyLlama) and
    stream response in chunks
    """
    start_time = time.time()
    full_prompt = f"<|system|>\n{system_message}</s>\n<|user|>\n{prompt}</s>\n<|assistant|>"
    stream = llm_model(
        full_prompt,
        max_tokens=MAX_TOKENS,
        stop=["</s>", "<|user|>"],
        echo=False,
        stream=True
    )
    print(f"[LLM] LLM responded in {(time.time() - start_time) * 1000:.2f}ms")

    buffer = ""
    for chunk in stream:
        token = chunk["choices"][0]["text"]
        buffer += token
        if token in [".", "!", "?", "\n"] and len(buffer) > MIN_BUFFER_LENGHT:
            yield buffer.strip()
            buffer = ""
    if buffer.strip():
        yield buffer.strip()

def stream_and_speak(prompt: str):
    """
    Calls the generate_response(...) method and receives the
    response in chunks, that are synthesized and added to the
    audio queue
    """
    for phrase in generate_response(prompt):
        if not phrase:
            continue
        audio_path = synthesize_text(phrase)
        audio_queue.put(audio_path)
import time
from resource_watcher import monitor_resources
from text_to_speech import synthesize_text
from audio_file_queue import audio_queue
from mqtt_bridge import publish

MAX_TOKENS = 256
MIN_BUFFER_LENGHT = 20

@monitor_resources("LLM", interval=0.5)
def generate_response(llm_model, prompt: str, system_message: str = "You are an assistant which answers in a precise but concise way."):
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
            phrase = buffer.strip()
            publish("assistant/llm_chunk", phrase)
            yield phrase
            buffer = ""
    if buffer.strip():
        publish("assistant/llm_chunk", buffer.strip())
        yield buffer.strip()

def stream_and_speak(llm_model, prompt: str, tts_model):
    """
    Calls the generate_response(...) method and receives the
    response in chunks, that are synthesized and added to the
    audio queue
    """
    for phrase in generate_response(llm_model=llm_model, prompt=prompt):
        if not phrase:
            continue
        print(f"[LLM] LLM response is '{phrase}'")
        audio_path = synthesize_text(tts_model=tts_model, text=phrase)
        audio_queue.put(audio_path)
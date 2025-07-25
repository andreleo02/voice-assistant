from llama_cpp import Llama

llm = Llama(
    model_path="./llm_models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=8,
    n_gpu_layers=0
)

def generate_response(prompt: str, system_message: str = "You are a helpful assistant.") -> str:
    full_prompt = f"<|system|>\n{system_message}</s>\n<|user|>\n{prompt}</s>\n<|assistant|>"
    output = llm(
        full_prompt,
        max_tokens=256,
        stop=["</s>", "<|user|>"],
        echo=False
    )
    
    response = output["choices"][0]["text"].strip()
    print(f"LLM response is: '{response}'")
    return response

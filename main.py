from microphone_listener import record_audio

def run_conversation():
    # setup a microphone input to listen for user queries
    audio_file = record_audio()

    # implement STT pipeline using a lightweight local model (WhisperTiny)

    # run a small LLM locally to generate a text response based on the input

    # convert the text response into audio using TTS engine (VITS or Coqui TTS)

# coordinate the entire process through a controller script
if __name__ == "__main__":
    run_conversation()

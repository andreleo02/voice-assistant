from microphone_listener import record_audio
from speech_to_text import transcribe
from llm_engine import generate_response
from text_to_speech import speak

def run_conversation():
    # setup a microphone input to listen for user queries
    audio_file = record_audio()

    # convert the audio to a prompt (STT using Whisper)
    transciption = transcribe(wav_path=audio_file)

    # run a small LLM locally to generate a text response based on the input
    response = generate_response(transciption)

    # convert the text response into audio using Coqui TTS
    speak(response)

# coordinate the entire process through a controller script
if __name__ == "__main__":
    run_conversation()

import time
from microphone_listener import record_audio
from speech_to_text import transcribe, detect_wake_word
from llm_engine import generate_response
from text_to_speech import speak

def run_conversation():
    print("LISTENING ...")

    # setup a microphone input to listen for user queries
    audio_file = record_audio(duration=5)

    # convert the audio to a prompt (STT using Whisper)
    print("THINKING ...")
    transciption = transcribe(wav_path=audio_file)

    # run a small LLM locally to generate a text response based on the input
    response = generate_response(transciption)

    # convert the text response into audio using Coqui TTS
    speak(response)

# coordinate the entire process through a controller script
if __name__ == "__main__":
    print("WAITING FOR TRIGGER WORD ...")
    while True:
        file = record_audio(duration=3)
        if detect_wake_word(file):
            print("Wake word detected! Start conversation...")
            run_conversation()
        time.sleep(0.2)
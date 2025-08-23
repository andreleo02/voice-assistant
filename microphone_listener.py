import tempfile
import speech_recognition as sr

def record_audio(samplerate=16000):
    """
    Records from mic until the user stops talking (silence detected),
    then returns the path to a temporary WAV file.
    """
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=samplerate) as source:
        r.adjust_for_ambient_noise(source, duration=0.8)
        r.pause_threshold = 0.8
        r.energy_threshold = r.energy_threshold

        print("[LISTENER] Listening... stop speaking to end")
        audio = r.listen(source)

    wav_bytes = audio.get_wav_data(convert_rate=samplerate, convert_width=2)
    return save_temp_wav(wav_bytes)

def save_temp_wav(wav_bytes):
    """
    Receives the wav bytes and saves them in a temporary file
    """
    tmpfile = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    with open(tmpfile.name, "wb") as f:
        f.write(wav_bytes)
    return tmpfile.name
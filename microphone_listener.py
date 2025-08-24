import tempfile
import speech_recognition as sr

def record_audio(r):
    """
    Records from mic until the user stops talking (silence detected),
    then returns the path to a temporary WAV file.
    """
    with sr.Microphone(sample_rate=16_000) as source:
        print("[LISTENER] Listening... stop speaking to end")
        audio = r.listen(source)

    wav_bytes = audio.get_wav_data(convert_rate=16_000, convert_width=2)
    return save_temp_wav(wav_bytes)

def save_temp_wav(wav_bytes):
    """
    Receives the wav bytes and saves them in a temporary file
    """
    tmpfile = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    with open(tmpfile.name, "wb") as f:
        f.write(wav_bytes)
    return tmpfile.name
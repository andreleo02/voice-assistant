import tempfile
import speech_recognition as sr

def record_audio(samplerate=16000):
    """
    Records from mic until the user stops talking (silence detected),
    then returns the path to a temporary WAV file.
    """
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=samplerate) as source:
        # Optional: auto-calibrate mic noise floor
        r.adjust_for_ambient_noise(source, duration=0.8)
        # Tune silence detection if needed
        r.pause_threshold = 0.8       # seconds of silence to stop
        r.energy_threshold = r.energy_threshold  # keep what was learned

        print("Listening... stop speaking to end")
        audio = r.listen(source)  # blocks until silence

    # Save as 16-bit PCM WAV at desired samplerate
    wav_bytes = audio.get_wav_data(convert_rate=samplerate, convert_width=2)
    return _save_temp_wav_bytes(wav_bytes)

def _save_temp_wav_bytes(wav_bytes):
    tmpfile = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    with open(tmpfile.name, "wb") as f:
        f.write(wav_bytes)
    return tmpfile.name
import tempfile
import scipy.io.wavfile
import sounddevice as sd

def record_audio(duration=10, samplerate=16000):
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    return save_temp_wav(audio.flatten(), samplerate)

def save_temp_wav(data, samplerate):
    tmpfile = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    scipy.io.wavfile.write(tmpfile.name, samplerate, data)
    print(tmpfile.name)
    return tmpfile.name
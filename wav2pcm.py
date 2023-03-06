import numpy as np
def wav2pcm(wavfile, pcmfile, data_type=np.int16):
    f = open(wavfile, "rb")
    f.seek(0)
    f.read(44)
    data = np.fromfile(f, dtype= data_type)
    data.tofile(pcmfile)

def pcm2wav(pcmfile, wavfile, data_type=np.int16):
    f = open(pcmfile, "rb")
    data = np.fromfile(f, dtype= data_type)
    data = data * 1.0 / (max(abs(data)))
    data = data * 32767.0
    data = data.astype(np.int16)
    data.tofile(wavfile)
    
if __name__ == "__main__":
    wav2pcm("lu.wav", "lu1.pcm")
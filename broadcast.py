from audio_spectrum import AudioSpectrum
import utility
from udp import *
import time

udp = UdpClient(port=5555)
audio = AudioSpectrum("chirp.wav", 1024)

while True:
    udp.send(audio.next().tobytes())
    time.sleep(0.016)
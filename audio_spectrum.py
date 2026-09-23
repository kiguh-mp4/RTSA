import sys
import numpy as np
from scipy.io import wavfile

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore


class AudioSpectrum:
    def __init__(self, filename, fft_size=1024):        
        self.sample_rate, audio = wavfile.read(filename)

        if audio.ndim == 2:
            audio = audio.mean(axis=1)

        audio = audio.astype(np.float32)

        max_value = np.max(np.abs(audio))

        if max_value > 0:
            audio /= max_value

        self.audio = audio

        self.fft_size = fft_size
        self.position = 0

        self.frequency = np.fft.rfftfreq(self.fft_size, 1.0 / self.sample_rate)

    def next(self):
        if (self.position + self.fft_size > len(self.audio)):
            self.position = 0

        samples = self.audio[self.position:(self.position + self.fft_size)]
        self.position += self.fft_size // 4

        window = np.hanning(self.fft_size)

        samples = samples * window

        spectrum = np.fft.rfft(samples)

        magnitude = np.abs(spectrum)

        db = 20 * np.log10(magnitude + 1e-12)

        db -= np.max(db)

        return db

if __name__ == "__main__":

    filename = "generic.wav"

    analyzer = AudioSpectrum(filename)

    app = QtWidgets.QApplication(sys.argv)
    win = pg.GraphicsLayoutWidget()
    win.setWindowTitle("Audio Spectrum Analyzer")
    win.resize(1200, 600)

    plot = win.addPlot(title="Spectrum")
    plot.setLabel("bottom","Frequency",units="Hz")
    plot.setLabel("left","Level",units="dB")
    plot.setXRange(0,analyzer.sample_rate / 2)
    plot.setYRange(-100,0)
    plot.showGrid(x=True,y=True,alpha=0.3)

    curve = plot.plot(
        pen=pg.mkPen(
            color=(0, 255, 0),
            width=1
        )
    )
        
    win.show()

    def update():
        curve.setData(analyzer.frequency, analyzer.next())

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(16)

    sys.exit(app.exec())
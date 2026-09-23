import sys
from pyqtgraph.Qt import QtWidgets, QtCore
from audio_spectrum import AudioSpectrum
from data_manager import DataManager
import painters as pt
import numpy as np
from udp import *


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    window.setWindowTitle("RTSA")
    window.resize(800, 600)
    window.show()
    layout = QtWidgets.QVBoxLayout(window)

    manager = DataManager(fft_size=513, history=50, db_min=-100)
    painters: list[pt.IWidgetPainter] = [
        pt.Spectrum(manager),
        pt.Spectrogram(manager, gamma=0.6),
        pt.DpxSpectrum(manager, gamma=5),
    ]

    for painter in painters:
        layout.addWidget(painter.plot)

    def update_fft(data):
        manager.append(np.asarray(np.frombuffer(data), dtype=np.float32))
        update_widgets()

    def update_widgets():
        for painter in painters:
            painter.refresh()

    udp = UdpClient(port=22222)
    udp.start(update_fft)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
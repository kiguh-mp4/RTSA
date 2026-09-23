import sys
from pyqtgraph.Qt import QtWidgets, QtCore
from audio_spectrum import AudioSpectrum
from data_manager import DataManager
import painters as pt
import utility


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

    audio = AudioSpectrum("chirp.wav", 1024)

    def update_fft():
        manager.append(audio.next())
        update_widgets()

    def update_widgets():
        for painter in painters:
            painter.refresh()



    timer = utility.timer(update_fft, 16)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
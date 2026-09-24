from pyqtgraph.Qt import QtCore

def timer(callback, ms:int) -> QtCore.QTimer:
    timer = QtCore.QTimer()
    timer.timeout.connect(callback)
    timer.start(ms)
    return timer
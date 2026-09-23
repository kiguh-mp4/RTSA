import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from data_manager import DataManager

class IWidgetPainter:
    def __init__(
            self,
            plot: pg.PlotWidget,
            manager: DataManager
            ):
        
        if plot is None:
            self.plot = pg.PlotWidget()
        else:
            self.plot = plot
        self.manager = manager
    
    def refresh():
        pass

class ColorMapBase(IWidgetPainter):
    def __init__(
            self,
            plot: pg.PlotWidget,
            manager: DataManager,
            gamma: float
            ):
        super().__init__(plot, manager)

        colors = np.array([
            [0, 0, 0],        # 黒
            [0, 0, 128],      # 紺
            [0, 0, 255],      # 青
            [0, 255, 255],    # シアン
            [0, 255, 0],      # 緑
            [255, 255, 0],    # 黄
            [255, 0, 0],      # 赤
            [255, 255, 255],  # 白
        ], dtype=np.ubyte)
        positions = np.linspace(0, 1, len(colors)) ** gamma
        cmap = pg.ColorMap(positions, colors)


        self.image = pg.ImageItem()
        self.image.setColorMap(cmap)

        self.plot.addItem(self.image)
        self.plot.showGrid(x=True, y=True, alpha=0.2)


class Spectrum(IWidgetPainter):
    def __init__(
            self,
            manager: DataManager,
            plot: pg.PlotWidget = None,
        ):
        super().__init__(plot, manager)

        self.plot.setWindowTitle("Spectrum")
        self.plot.setLabel("bottom", "Frequency", units="Hz")
        self.plot.setLabel("left", "Power", units="dB")
        self.plot.setXRange(manager.start, manager.end)
        self.plot.setYRange(manager.db_min, manager.db_max)
        self.plot.showGrid(x=True, y=True, alpha=0.2)

        self.curve = self.plot.plot(
            pen=pg.mkPen(
                color=(0, 255, 0),
                width=1
            )
        )

    def refresh(self):
        self.curve.setData(self.manager.frequency, self.manager.get(0))
        
class Spectrogram(ColorMapBase):
    def __init__(
            self,
            manager: DataManager,
            plot: pg.PlotWidget = None,
            gamma: float = 1.0
        ):
        super().__init__(plot, manager, gamma)

        self.plot.setWindowTitle("Spectrogram")
        self.plot.setLabel("bottom", "Frequency", units="Hz")
        self.plot.setLabel("left", "Time", units="Histories")
        self.plot.setXRange(manager.start, manager.end)
        self.plot.setYRange(0, self.manager.history)
        

        # WidthとHeightは1を基準とする倍率。500要素のとき1.5と設定すれば、0から750の範囲に描画される。
        self.image.setRect(
            QtCore.QRectF(
                manager.cf - manager.span / 2,
                0,
                manager.span / manager.fft_size,
                1
            )
        )
        self.image.setLevels([manager.db_min, manager.db_max])

    def refresh(self):
        self.image.setImage(np.transpose(self.manager.data), autoLevels=False)

class DpxSpectrum(ColorMapBase):
    def __init__(
            self,
            manager: DataManager,
            height: int = 600,
            plot: pg.PlotWidget = None,
            gamma: float = 1.0
        ):
        super().__init__(plot, manager, gamma)

        self.height = height

        self.plot.setWindowTitle("DPX Spectrum")
        self.plot.setLabel("bottom", "Frequency", units="Hz")
        self.plot.setLabel("left", "Power", units="dB")
        self.plot.setXRange(manager.start, manager.end)
        self.plot.setYRange(manager.db_min, manager.db_max)
        

        # WidthとHeightは1を基準とする倍率。500要素のとき1.5と設定すれば、0から750の範囲に描画される。
        self.image.setRect(
            QtCore.QRectF(
                manager.cf - manager.span / 2,
                manager.db_min,
                manager.span / manager.fft_size,
                (self.manager.db_max - self.manager.db_min) / self.height
            )
        )
        self.image.setLevels([manager.db_min, manager.db_max])

    def refresh(self):        
        mapped = np.interp(
            self.manager.data,
            (self.manager.db_min, self.manager.db_max),
            (0, self.height - 1)
        )
        mapped = mapped.astype(np.int32)
        mapped = mapped.clip(0, self.height - 1)

        data = np.full((self.height, self.manager.fft_size), 0, dtype=np.uint16)

        np.add.at(data, (mapped, np.arange(self.manager.fft_size)), 1)

        self.image.setImage(np.transpose(data), autoLevels=False)
        self.image.setLevels([0, np.max(data)])
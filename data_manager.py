import numpy as np

class DataManager:
    def __init__(
        self,
        fft_size=1024,
        history=500,
        db_min=-100,
        db_max=0,
        center_frequency=50e6,
        span=100e6,
    ):
        self.fft_size = fft_size
        self.history = history
        self.data = np.full((history, fft_size), db_min, dtype=np.float32)
        self.db_min = db_min
        self.db_max = db_max
        self.cf = center_frequency
        self.span = span

        self.start = self.cf - self.span / 2
        self.end = self.cf + self.span / 2
        self.frequency = np.linspace(self.start, self.end, fft_size)

    def append(self, fft_db):
        size = int(fft_db.shape[0] / self.fft_size)
        self.data[size:] = self.data[:-size]
        self.data[0:size, :] = fft_db.reshape(size, self.fft_size)[::-1]

    def get(self, index):
        return self.data[index]
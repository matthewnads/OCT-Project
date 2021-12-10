from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QComboBox,
    QMainWindow,
    QAction,
    QWidget,
    qApp,
    QApplication,
    QPushButton,
    QLabel,
    QVBoxLayout,
)
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import matlab.engine
import numpy as np
import scipy.io.wavfile as wav
import sys
import random
import colorsys

eng1 = matlab.engine.start_matlab()


class WaveformWindow(QWidget):
    _inputDevs = None
    _outputDevs = None
    _filepath = None
    _y = None
    _Fs = None
    _output = None
    # _names, _dq, _channels = eng1.initOutput(nargout=3)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Waveform Creator")
        # layout.addWidget(self.label)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.waveform = QComboBox()
        self.waveform.addItems(["Sine", "Chirp", "Sound File"])
        layout.addWidget(self.waveform)
        self.waveform.activated.connect(self.waveSelect)

    def waveSelect(self, idx):
        global _output
        _output = eng1.createOutput(idx)

    # def dynamicMenu(self):


class MainWindow(QtWidgets.QMainWindow):
    _filepath = None
    _y = None
    _Fs = None

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.playW = None
        self.setWindowTitle("Generator and Editor")

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground("w")

        self.setCentralWidget(self.graphWidget)

        self.defineToolbar()

    def plottingFig(self, y, Fs, tt, graphWidget):
        h, s, l = (
            random.random(),
            0.5 + random.random() / 2.0,
            0.4 + random.random() / 5.0,
        )
        r, g, b = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]
        y = np.asarray(y, dtype=np.float32)
        y = y.reshape(
            len(y),
        )
        t = np.arange(0, tt, 1 / Fs)
        self.graphWidget.setLabel(
            "left", '<span style="color:black;font-size:20px">Amplitude</span>'
        )
        self.graphWidget.setLabel(
            "bottom", '<span style="color:black;font-size:20px">Time (Seconds)</span>'
        )
        graphWidget.plot(t, y, pen=pg.mkPen(color=(r, g, b)))

    def defineToolbar(self):
        self.toolbar = QtWidgets.QToolBar()
        self.addToolBar(self.toolbar)

        fileButton = QAction("File", self)
        fileButton.setShortcut("Ctrl+O")
        fileButton.triggered.connect(self.getFiles)
        self.toolbar.addAction(fileButton)
        waveformButton = QAction("Create Waveform", self)
        waveformButton.triggered.connect(self.waveform)
        self.toolbar.addAction(waveformButton)
        playButton = QAction("Play", self)
        playButton.triggered.connect(self.play)
        self.toolbar.addAction(playButton)
        # graphButton = QAction("Graph", self)
        # graphButton.setShortcut('Ctrl+O')
        # graphButton.triggered.connect(self.plottingFig(self.graphWidget))
        # self.toolbar.addAction(graphButton)

        # print("filepath:", self.filepath)

    def getFiles(self):
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Single File", QtCore.QDir.rootPath(), "*.wav"
        )
        self.readFile(filepath)

    def readFile(self, filepath):
        # Fs, y = wav.read(filepath)
        # y = y / 32768.0
        # tt = len(y)/float(Fs)
        y, Fs, tt = eng1.tGraph(filepath, nargout=3)

        self.plottingFig(y, Fs, tt, self.graphWidget)
        global _filepath, _y, _Fs
        _filepath = filepath
        _y, _Fs = y, Fs

    def waveform(self):
        if self.playW is None:
            self.playW = WaveformWindow()
        self.playW.show()

    def play(self):  # build out to support waveform.
        print("Play something")

        # samplerate = sd.query_devices(args.device, 'output')['default_samplerate']
        # sd.play(_y, _Fs)
        # with sd.OutputStream(device=args.device)
        # pgame.mixer.init(frequency=_Fs, size=-16, channels=2, buffer=4096)
        # sound0 = pgame.mixer.Sound(_filepath)
        # channel0 = pgame.mixer.Channel(0)
        # channel0.play(sound0)
        # channel0.set_volume(1.0, 0.0)


def main():

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    # print(sd.query_devices())  # fix
    sys.exit(app.exec_())


#     commented  the below out because of conflict to from qt to main
#     filepath = askopenfilename()
#     print(filepath)

#     # playSound()

#     y, Fs, tt = readFile(filepath)

#     y,Fs,tt = eng1.tGraph(filepath,nargout=3)


if __name__ == "__main__":
    main()

eng1.quit()

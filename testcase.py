from PyQt5 import QtWidgets, QtCore, QtGui
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
generateWindow = None


class MainWindow(QtWidgets.QMainWindow):
    _inputDevs = None
    _outputDevs = None
    _filepath = None
    _y = None
    _Fs = None
    _output = None
    # _names, _dq, _channels = eng1.initOutput(nargout=3)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Generator and Editor")

        self.mainLayout = QtWidgets.QVBoxLayout()

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground("w")

        self.central = QtWidgets.QWidget(self)
        self.central.setFocus()

        self.mainLayout.addWidget(self.graphWidget)

        self.setCentralWidget(self.central)
        self.central.setLayout(self.mainLayout)
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

        generateButton = QAction("Generate", self)
        generateButton.triggered.connect(self.generate)
        self.toolbar.addAction(generateButton)

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

    def generate(self):
        global generateWindow
        generateWindow.show()

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


class GenerateWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(GenerateWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Waveform Creator")

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.top_inputs = QtWidgets.QGridLayout()

        self.signals_label = QtWidgets.QLabel("Signal Type:")
        self.signals = QtWidgets.QComboBox()
        self.signals.insertItem(0, "Periodic")
        self.signals.insertItem(0, "Sine")
        self.signals.insertItem(0, "Chirp")
        self.signals.insertItem(0, "Noise")
        self.signals.insertItem(0, "Pulse")
        self.top_inputs.addWidget(self.signals_label, 0, 0)
        self.top_inputs.addWidget(self.signals, 0, 1)
        self.signals.currentIndexChanged.connect(
            lambda: change(
                str(self.signals.currentText()), self.pulse_box, self.sin_box
            )
        )  # USE THIS TO PASS THE COMBOBOX INTO THE FUNCTION ARGUMENT - USE THAT FOR DYNAMIC MENU CHANGES ON CHANGE
        self.signals.activated.connect(self.waveSelect)

        self.signals_label = QtWidgets.QLabel("Sampling Frequency:")
        self.signal_freq = QtWidgets.QLineEdit()
        int_validator = QtGui.QIntValidator(0, 10000)
        self.signal_freq.setValidator(int_validator)
        self.top_inputs.addWidget(self.signals_label, 1, 0)
        self.top_inputs.addWidget(self.signal_freq, 1, 1)

        self.signals_label = QtWidgets.QLabel("Signal Amplitude:")
        self.signal_amp = QtWidgets.QLineEdit()
        self.signal_amp.setValidator(int_validator)
        self.top_inputs.addWidget(self.signals_label, 2, 0)
        self.top_inputs.addWidget(self.signal_amp, 2, 1)

        self.signals_label = QtWidgets.QLabel("T-silence:")
        self.signal_silence = QtWidgets.QLineEdit()
        self.signal_silence.setValidator(int_validator)
        self.top_inputs.addWidget(self.signals_label, 3, 0)
        self.top_inputs.addWidget(self.signal_silence, 3, 1)

        self.signals_label = QtWidgets.QLabel("T-ramp:")
        self.signal_tramp = QtWidgets.QLineEdit()
        self.signal_tramp.setValidator(int_validator)
        self.top_inputs.addWidget(self.signals_label, 4, 0)
        self.top_inputs.addWidget(self.signal_tramp, 4, 1)

        self.signals_label = QtWidgets.QLabel("Offset:")
        self.signal_offset = QtWidgets.QLineEdit()
        self.signal_offset.setValidator(int_validator)
        self.top_inputs.addWidget(self.signals_label, 5, 0)
        self.top_inputs.addWidget(self.signal_offset, 5, 1)

        # pulse dynamic menu
        self.pulse_box = QtWidgets.QGroupBox()
        self.pulse_layout = QtWidgets.QGridLayout()
        label = QtWidgets.QLabel("Duty Cycle:")
        duty_cycle = QtWidgets.QLineEdit()
        int_validator = QtGui.QIntValidator(0, 10000)
        duty_cycle.setValidator(int_validator)
        self.pulse_layout.addWidget(label, 6, 0)
        self.pulse_layout.addWidget(duty_cycle, 6, 1)
        self.pulse_box.setLayout(self.pulse_layout)

        # sin dynamic menu
        self.sin_box = QtWidgets.QGroupBox()
        self.sin_layout = QtWidgets.QGridLayout()
        label = QtWidgets.QLabel("Waveform Frequency:")
        frequency = QtWidgets.QLineEdit()
        int_validator = QtGui.QIntValidator(0, 10000)
        frequency.setValidator(int_validator)
        self.sin_layout.addWidget(label, 6, 0)
        self.sin_layout.addWidget(frequency, 6, 1)
        self.sin_box.setLayout(self.sin_layout)

        self.top_inputs_box = QtWidgets.QGroupBox()
        self.top_inputs_box.setLayout(self.top_inputs)
        self.mainLayout.addWidget(self.top_inputs_box)
        self.mainLayout.addWidget(self.pulse_box)
        self.mainLayout.addWidget(self.sin_box)
        self.sin_box.hide()
        self.pulse_box.hide()
        self.setLayout(self.mainLayout)

    def waveSelect(self, idx):
        print(idx)
        # global _output
        # _output = eng1.createOutput(idx)


def change(text, pulse, sin):

    if text == "Pulse":
        pulse.show()
        sin.hide()

    elif text == "Sine":
        pulse.hide()
        sin.show()
    else:
        pulse.hide()
        sin.hide()


def main():

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    global generateWindow
    generateWindow = GenerateWindow()
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

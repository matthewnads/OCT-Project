# NOTE: testGUI.py is the most complete form of the software.
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import matlab.engine
import numpy as np
import scipy.io.wavfile as wav
import sys
import random
import colorsys

np.set_printoptions(threshold=sys.maxsize)  # to prevent truncation

eng1 = matlab.engine.start_matlab()
generateWindow = None
# set up these global variables so that we can send them to the backend later on (never ended up getting to that point)
# the idea is that we use these variables to construct our wave patterns in matlab
signal_frequency = 0
signal_amplitude = 0
t_silence = 0
t_ramp = 0
offset = 0
sampling_frequency = 0
output = None
n = 0


class MainWindow(QtWidgets.QMainWindow):

    _filepath = None

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Generator and Editor")
        # The mainLayout is the layout of the our main window.
        self.mainLayout = QtWidgets.QVBoxLayout()

        # --------------------------------------------------------------------
        # Graph Widget
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground("w")

        # --------------------------------------------------------------------
        # this is our central widget. mainLayout will get added to the central widget which makes up our window
        self.central = QtWidgets.QWidget(self)
        self.central.setFocus()
        # ------------------------------------------------------------------------
        # add widgets to main layout

        self.mainLayout.addWidget(self.graphWidget)

        self.setCentralWidget(self.central)
        self.central.setLayout(self.mainLayout)
        self.defineToolbar()

    def plottingFig(self):
        h, s, l = (
            random.random(),
            0.5 + random.random() / 2.0,
            0.4 + random.random() / 5.0,
        )
        r, g, b = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]
        y = np.asarray(output, dtype=np.float32)
        y = output
        Fs = sampling_frequency

        t = np.arange(0, n, 1 / Fs)  # n is reps and is used as seconds.
        self.graphWidget.setLabel(
            "left", '<span style="color:black;font-size:20px">Amplitude (Volts)</span>'
        )
        self.graphWidget.setLabel(
            "bottom", '<span style="color:black;font-size:20px">Time (Seconds)</span>'
        )
        self.graphWidget.plot(t, y, pen=pg.mkPen(color=(r, g, b)))

    # ------------------------------------------------------------------------
    # function to define toolbar
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

    #   ------------------------------------------------------------------------
    # this was a function i used for testing buttons
    def button1(self):
        print("this is button one")

    #   ------------------------------------------------------------------------
    # used to get and read files from the "file" toolbar button
    def getFiles(self):
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Single File", QtCore.QDir.rootPath(), "*.wav"
        )
        self.readFile(filepath)

    def readFile(self, filepath):  # deprecated function

        y, Fs, tt = eng1.tGraph(filepath, nargout=3)
        self.plottingFig(y, Fs, tt, self.graphWidget)
        global _filepath
        _filepath = filepath

    ##   ------------------------------------------------------------------------
    # calls the matlab playsound function
    def play(self):
        data = matlab.double(output.tolist())  # convert output list to regular list
        eng1.playSound(sampling_frequency, data, nargout=0)

    #   ------------------------------------------------------------------------
    # this function opens up the generate window (defined below)
    def generate(self):
        self.generateWindow = GenerateWindow()
        self.generateWindow.closed.connect(self.plottingFig)
        self.generateWindow.show()


# This class is what makes up the Generate window (after clicking the generate button the in MainWindow)
class GenerateWindow(QtWidgets.QWidget):
    # You might notice that this is structured a little bit differently (the window is actually a widget that we add to)
    # Compared to MainWindow which is a window, that has a central widget that we add things to

    closed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(GenerateWindow, self).__init__(*args, **kwargs)
        # We are setting up 2 layoutsL: mainLayout and top_inputs
        # mainLayout is the main layout of the generate window. Everything gets added to this
        # top_inputs is the layout of the paramters that are not included in the dynamic menus (currently the extra sin/chirp/periodic params)
        # There are separate layouts and boxes like this (as you'll see below) so I could format and control them independently of each other
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.top_inputs = QtWidgets.QGridLayout()
        # This is the dropdown menu to select a signal type
        self.signals_label = QtWidgets.QLabel("Signal Type:")
        self.signals = QtWidgets.QComboBox()
        self.signals.insertItem(0, "Periodic")
        self.signals.insertItem(0, "Sin")
        self.signals.insertItem(0, "Chirp")
        self.signals.insertItem(0, "Noise")
        self.signals.insertItem(0, "Pulse")
        self.signals.setCurrentIndex(0)
        self.top_inputs.addWidget(self.signals_label, 0, 0)
        self.top_inputs.addWidget(self.signals, 0, 1)
        # This line connects the dropdown to a function that populates the dynamic menus. We pass in 3 arguments: the current text selected, and the two boxes for the dynamic menu
        self.signals.currentIndexChanged.connect(
            lambda: change(
                str(self.signals.currentText()), self.sin_box, self.chirp_box
            )
        )

        # ----------------------------------------------------------------------------------------------------------------------------------------------
        # The following section is setting up the different textboxes for the various paramters. They currently are not attached to any functions,
        # so when you want add them to the backend this needs to be added in so they're linked to the global variables above

        # first we create the different components (label, units, textbox and validator which limits the inputs (floats, int, etc))
        self.signals_label = QtWidgets.QLabel("Sampling Frequency:")
        self.signals_unit = QtWidgets.QLabel("kHz")
        self.signal_freq = QtWidgets.QLineEdit()
        int_validator = QtGui.QDoubleValidator(0, 10000, 4)
        self.signal_freq.setValidator(int_validator)
        # then these 3 lines add them into our layout. The numbers inidicate the location (treating the layout like a grid format)
        self.top_inputs.addWidget(self.signals_label, 1, 0)
        self.top_inputs.addWidget(self.signal_freq, 1, 1)
        self.top_inputs.addWidget(self.signals_unit, 1, 2)

        self.signals_label = QtWidgets.QLabel("Signal Amplitude:")
        self.signal_amp = QtWidgets.QLineEdit()
        self.signals_unit = QtWidgets.QLabel("V")
        self.signal_amp.setValidator(int_validator)
        self.top_inputs.addWidget(self.signals_label, 2, 0)
        self.top_inputs.addWidget(self.signal_amp, 2, 1)
        self.top_inputs.addWidget(self.signals_unit, 2, 2)

        self.signals_label = QtWidgets.QLabel("T-silence:")
        self.signal_silence = QtWidgets.QLineEdit()
        self.signals_unit = QtWidgets.QLabel("ms")
        self.signal_silence.setValidator(int_validator)
        self.top_inputs.addWidget(self.signals_label, 3, 0)
        self.top_inputs.addWidget(self.signal_silence, 3, 1)
        self.top_inputs.addWidget(self.signals_unit, 3, 2)

        self.signals_label = QtWidgets.QLabel("T-ramp:")
        self.signal_tramp = QtWidgets.QLineEdit()
        self.signals_unit = QtWidgets.QLabel("ms")
        self.signal_tramp.setValidator(int_validator)
        self.top_inputs.addWidget(self.signals_label, 4, 0)
        self.top_inputs.addWidget(self.signal_tramp, 4, 1)
        self.top_inputs.addWidget(self.signals_unit, 4, 2)

        self.signals_label = QtWidgets.QLabel("Offset:")
        self.signal_offset = QtWidgets.QLineEdit()
        self.signals_unit = QtWidgets.QLabel("V")
        self.signal_offset.setValidator(int_validator)
        self.top_inputs.addWidget(self.signals_label, 5, 0)
        self.top_inputs.addWidget(self.signal_offset, 5, 1)
        self.top_inputs.addWidget(self.signals_unit, 5, 2)

        self.signals_label = QtWidgets.QLabel("Number of Reps:")
        self.reps = QtWidgets.QLineEdit()
        rep_validator = QtGui.QIntValidator(1, 1000000)
        self.reps.setValidator(rep_validator)
        self.top_inputs.addWidget(self.signals_label, 6, 0)
        self.top_inputs.addWidget(self.reps, 6, 1)
        self.top_inputs.addWidget(self.signals_unit, 6, 2)

        # ----------------------------------------------------------------------------------------------------------------------------------------------
        # These are the dynamic menus that use separate layouts and boxes so we can control them independently
        # start f0 and end f2 dynamic menu
        self.chirp_box = QtWidgets.QGroupBox()
        self.chirp_layout = QtWidgets.QGridLayout()
        label = QtWidgets.QLabel("Start Frequency:")
        self.f0 = QtWidgets.QLineEdit()
        self.f0.setValidator(int_validator)
        f0units = QtWidgets.QLabel("kHz")
        labelf1 = QtWidgets.QLabel("End Frequency:")
        self.f1 = QtWidgets.QLineEdit()
        self.f1.setValidator(int_validator)
        f1units = QtWidgets.QLabel("kHz")
        self.chirp_layout.addWidget(label, 7, 0)
        self.chirp_layout.addWidget(self.f0, 7, 1)
        self.chirp_layout.addWidget(f0units, 7, 2)
        self.chirp_layout.addWidget(labelf1, 8, 0)
        self.chirp_layout.addWidget(self.f1, 8, 1)
        self.chirp_layout.addWidget(f1units, 8, 2)
        self.chirp_box.setLayout(self.chirp_layout)

        # sin dynamic menu
        self.sin_box = QtWidgets.QGroupBox()
        self.sin_layout = QtWidgets.QGridLayout()
        label = QtWidgets.QLabel("Signal Frequency:")
        self.frequency = QtWidgets.QLineEdit()
        self.signals_unit = QtWidgets.QLabel("kHz")
        self.frequency.setValidator(int_validator)
        self.sin_layout.addWidget(label, 6, 0)
        self.sin_layout.addWidget(self.frequency, 6, 1)
        self.sin_layout.addWidget(self.signals_unit, 6, 2)
        self.sin_box.setLayout(self.sin_layout)
        # ----------------------------------------------------------------------------------------------------------------------------------------------

        # This is the button that should be used to eventually add the paramters to the global variables.
        # Should make a function to do this that connects to this button (like we did with the drop down menu above)
        self.confirm = QtWidgets.QPushButton("Generate")
        self.confirm.clicked.connect(lambda: self.createWaveform())

        # here we add the layouts the the mainlayout
        self.top_inputs_box = QtWidgets.QGroupBox()
        self.top_inputs_box.setLayout(self.top_inputs)
        self.mainLayout.addWidget(self.top_inputs_box)
        self.mainLayout.addWidget(self.chirp_box)
        self.mainLayout.addWidget(self.sin_box)
        self.mainLayout.addWidget(self.confirm)
        self.sin_box.hide()
        self.chirp_box.hide()
        self.setLayout(self.mainLayout)

    def createWaveform(self):
        # main params: type, sampling frequency (khz), amp (v), tsilence (ms), t-ramp (ms), offset (0 default, in volts), stop time (s)
        # optional args: duty cycle, period, f0, f1 (chirp), sine
        global output, sampling_frequency, n

        sampling_frequency = float(self.signal_freq.text()) * 1000
        n = int(self.reps.text())

        if self.signals.currentIndex() == 3:  # sine function inputs
            output = eng1.createOutput(
                self.signals.currentIndex(),  # index to indicate what kind of function
                sampling_frequency,  # sampling frequency
                float(self.signal_amp.text()),  # signal amplitude
                float(self.signal_silence.text()),  # t silence
                float(self.signal_tramp.text()),  # t ramp
                float(self.signal_offset.text()),  # offset
                float(self.frequency.text()),  # sine frequency
            )
        elif self.signals.currentIndex() == 2 or self.signals.currentIndex() == 4:
            # chirp and whatever else function inputs
            output = eng1.createOutput(
                float(self.signals.currentIndex()),
                sampling_frequency,
                float(self.signal_amp.text()),
                float(self.signal_silence.text()),
                float(self.signal_tramp.text()),
                float(self.signal_offset.text()),
                float(self.f0.text()),
                float(self.f1.text()),
            )
        else:
            output = eng1.createOutput(  # all other functions i.e. noise function.
                self.signals.currentIndex(),
                sampling_frequency,
                float(self.signal_amp.text()),
                float(self.signal_silence.text()),
                float(self.signal_tramp.text()),
                float(self.signal_offset.text()),
            )
        output = np.asarray(output, dtype=np.float32)
        output = output.reshape(len(output))
        output = np.tile(output, n)
        # based one second time intervals for total signal size per wave
        self.close()

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()


# function to display the different dynamic menus
def change(text, sin, chirp):
    if text == "Sin":
        chirp.hide()
        sin.show()
    elif text == "Chirp":
        chirp.show()
        sin.hide()
    elif text == "Periodic":
        chirp.show()
        sin.hide()
    else:
        chirp.hide()
        sin.hide()


# main function that populates everything
def main():

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

eng1.quit()

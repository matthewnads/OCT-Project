from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication
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
signal_frequency = 0 
signal_amplitude = 0  
t_silence = 0 
t_ramp =0 
offset = 0
sampling_frequency = 0


#Dynamic Window Layouts


     
        # self.dynamic_menu = QtWidgets.QGridLayout()
        # self.dynamic_menu_box = QtWidgets.QGroupBox()
        # self.dynamic_menu_box.hide()
        # self.dynamic_menu_box.setLayout(self.dynamic_menu)
     
        # self.top_inputs_box = QtWidgets.QGroupBox() 
        # self.top_inputs_box.setLayout(self.top_inputs)
        # self.mainLayout.addWidget(self.top_inputs_box)
        # self.mainLayout.addWidget(self.dynamic_menu_box)
        # self.setLayout(self.mainLayout)


class MainWindow(QtWidgets.QMainWindow):

    _filepath = None

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Generator and Editor")
        #main layout (components get added to this)
        self.mainLayout = QtWidgets.QVBoxLayout()
        
       
        #--------------------------------------------------------------------
        #Graph Widget 
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('w')
        
        
        
        #--------------------------------------------------------------------
        #Paramter textboxes
        
        
        #NOTES NOV19
        # sampling rate, duration, amplitude  (voltage for DAQ), type of signal (periodic wave, sin, chirp, noise, white noise, pulse)
        # silent spaces before and after the sound, ramp up duration/ ramp down duration (number of seconds for each)
        #duration = seconds , then number of samples based off of sampling frequency and duration
        # think about averages ...
        #corrections/alterations to the waveform 
        #want it coming out of daq board 
        #number of reps (dont show all reps) 
        #multichannel 
        
        
        
        self.central = QtWidgets.QWidget(self)
        self.central.setFocus() 
        # ------------------------------------------------------------------------
        # add widgets to main layout 
 
        self.mainLayout.addWidget(self.graphWidget)

        self.setCentralWidget(self.central)
        self.central.setLayout(self.mainLayout)
        self.defineToolbar()

    def plottingFig(self, y, Fs, tt, graphWidget):
        h, s, l = random.random(), 0.5 + random.random()/2.0, 0.4 + random.random()/5.0
        r, g, b = [int(256*i) for i in colorsys.hls_to_rgb(h, l, s)]
        y = np.asarray(y, dtype=np.float32)
        y = y.reshape(len(y),)
        t = np.arange(0, tt, 1/Fs)
        self.graphWidget.setLabel('left', "<span style=\"color:black;font-size:20px\">Amplitude</span>")
        self.graphWidget.setLabel('bottom', "<span style=\"color:black;font-size:20px\">Time (Seconds)</span>")
        graphWidget.plot(t, y, pen=pg.mkPen(color=(r, g, b)))


    def defineToolbar(self):
        self.toolbar = QtWidgets.QToolBar()
        self.addToolBar(self.toolbar)

        fileButton = QAction("File", self)
        fileButton.setShortcut('Ctrl+O')
        fileButton.triggered.connect(self.getFiles)
        self.toolbar.addAction(fileButton)
        
        generateButton = QAction("Generate",self) 
        generateButton.triggered.connect(self.generate)
        self.toolbar.addAction(generateButton)
        
        playButton=QAction("Play",self)
        playButton.triggered.connect(self.play)
        self.toolbar.addAction(playButton)
        #graphButton = QAction("Graph", self)
        #graphButton.setShortcut('Ctrl+O')
        #graphButton.triggered.connect(self.plottingFig(self.graphWidget))
        #self.toolbar.addAction(graphButton)

        #print("filepath:", self.filepath)
        
    def button1(self): 
        print("this is button one")
    def getFiles(self):
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Single File', QtCore.QDir.rootPath(), '*.wav')
        self.readFile(filepath)

    def readFile(self, filepath):
        #Fs, y = wav.read(filepath)
        #y = y / 32768.0
        #tt = len(y)/float(Fs)
        y, Fs, tt = eng1.tGraph(filepath, nargout=3)
        self.plottingFig(y, Fs, tt, self.graphWidget)
        global _filepath
        _filepath = filepath 
        
        
    def play(self):
        eng1.playSound(_filepath,nargout=0)
        
    def generate(self):
        global generateWindow
        generateWindow.show()
        
 

class GenerateWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(GenerateWindow, self).__init__(*args, **kwargs)
    
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.top_inputs = QtWidgets.QGridLayout() 
        
        self.signals_label = QtWidgets.QLabel("Signal Type:")
        self.signals = QtWidgets.QComboBox()
        # self.signals.insertAtTop("Please select a signal")
        self.signals.insertItem(0,"Periodic")
        self.signals.insertItem(0,"Sin")
        self.signals.insertItem(0,"Chirp")
        self.signals.insertItem(0,"Noise")
        self.signals.insertItem(0,"Pulse")
        self.top_inputs.addWidget(self.signals_label,0,0)
        self.top_inputs.addWidget(self.signals,0,1)
        self.signals.currentIndexChanged.connect(lambda: change(str(self.signals.currentText()),self.sin_box,self.chirp_box)) # USE THIS TO PASS THE COMBOBOX INTO THE FUNCTION ARGUMENT - USE THAT FOR DYNAMIC MENU CHANGES ON CHANGE 
        
        
        
# NOTES – 
# Tsilence, tramp = ms
# Freq khz
# Amp volts 
# offset = 0 default, read only volts
# send generated waves to spescific channels in generate menu 
#number of repeeated sounds -> called number of averages 
#floats for all except number reps 
#multiple graphs - stack them 

        
        self.signals_label = QtWidgets.QLabel("Sampling Frequency:")
        self.signals_unit = QtWidgets.QLabel("kHz")
        self.signal_freq = QtWidgets.QLineEdit()
        int_validator= QtGui.QDoubleValidator(0,10000,4)
        self.signal_freq.setValidator(int_validator)
        self.top_inputs.addWidget(self.signals_label,1,0)
        self.top_inputs.addWidget(self.signal_freq,1,1)
        self.top_inputs.addWidget(self.signals_unit,1,2)
        
        self.signals_label = QtWidgets.QLabel("Signal Amplitude:")
        self.signal_amp = QtWidgets.QLineEdit()
        self.signals_unit = QtWidgets.QLabel("V")
        self.signal_amp.setValidator(int_validator)
        self.top_inputs.addWidget(self.signals_label,2,0)
        self.top_inputs.addWidget(self.signal_amp,2,1)
        self.top_inputs.addWidget(self.signals_unit,2,2)
        
        self.signals_label = QtWidgets.QLabel("T-silence:")
        self.signal_silence = QtWidgets.QLineEdit()
        self.signals_unit = QtWidgets.QLabel("ms")
        self.signal_silence.setValidator(int_validator)
        self.top_inputs.addWidget(self.signals_label,3,0)
        self.top_inputs.addWidget(self.signal_silence,3,1)
        self.top_inputs.addWidget(self.signals_unit,3,2)
        
        self.signals_label = QtWidgets.QLabel("T-ramp:")
        self.signal_tramp = QtWidgets.QLineEdit()
        self.signals_unit = QtWidgets.QLabel("ms")
        self.signal_tramp.setValidator(int_validator)
        self.top_inputs.addWidget(self.signals_label,4,0)
        self.top_inputs.addWidget(self.signal_tramp,4,1)
        self.top_inputs.addWidget(self.signals_unit,4,2)
        
        self.signals_label = QtWidgets.QLabel("Offset:")
        self.signal_offset = QtWidgets.QLineEdit()
        self.signal_offset.setReadOnly(True)
        self.signals_unit = QtWidgets.QLabel("V") 
        self.signal_offset.setValidator(int_validator)
        self.top_inputs.addWidget(self.signals_label,5,0)
        self.top_inputs.addWidget(self.signal_offset,5,1)
        self.top_inputs.addWidget(self.signals_unit,5,2)
        
        self.signals_label = QtWidgets.QLabel("Number of Reps:")
        self.signal_freq = QtWidgets.QLineEdit()
        rep_validator= QtGui.QIntValidator(1,1000000)
        self.signal_freq.setValidator(rep_validator)
        self.top_inputs.addWidget(self.signals_label,6,0)
        self.top_inputs.addWidget(self.signal_freq,6,1)
        self.top_inputs.addWidget(self.signals_unit,6,2)
        
        #start f0 and end f2 dynamic menu
        self.chirp_box = QtWidgets.QGroupBox() 
        self.chirp_layout= QtWidgets.QGridLayout() 
        label = QtWidgets.QLabel("Start Frequency:")
        f0 = QtWidgets.QLineEdit()
        f0.setValidator(int_validator)
        f0units = QtWidgets.QLabel("kHz")
        labelf1 = QtWidgets.QLabel("End Frequency:")
        f1 =  QtWidgets.QLineEdit()
        f1.setValidator(int_validator)
        f1units = QtWidgets.QLabel("kHz")
        self.chirp_layout.addWidget(label,7,0)
        self.chirp_layout.addWidget(f0,7,1)
        self.chirp_layout.addWidget(f0units,7,2)
        self.chirp_layout.addWidget(labelf1,8,0)
        self.chirp_layout.addWidget(f1,8,1)
        self.chirp_layout.addWidget(f1units,8,2)
        self.chirp_box.setLayout(self.chirp_layout)
        
        
        #sin dynamic menu        
        self.sin_box = QtWidgets.QGroupBox() 
        self.sin_layout= QtWidgets.QGridLayout() 
        label = QtWidgets.QLabel("Signal Frequency:")
        frequency = QtWidgets.QLineEdit()
        self.signals_unit = QtWidgets.QLabel("kHz")
        frequency.setValidator(int_validator)
        self.sin_layout.addWidget(label,6,0)
        self.sin_layout.addWidget(frequency,6,1)
        self.sin_layout.addWidget(self.signals_unit,6,2)
        self.sin_box.setLayout(self.sin_layout)
        
        
        self.confirm = QtWidgets.QPushButton("Generate")
        
      
        
        self.top_inputs_box = QtWidgets.QGroupBox() 
        self.top_inputs_box.setLayout(self.top_inputs)
        self.mainLayout.addWidget(self.top_inputs_box)
        self.mainLayout.addWidget(self.chirp_box)
        self.mainLayout.addWidget(self.sin_box)
        self.mainLayout.addWidget(self.confirm)
        self.sin_box.hide() 
        self.chirp_box.hide()
        self.setLayout(self.mainLayout)
        

        
def change(text,sin,chirp): 
    if(text=="Sin"): 
        chirp.hide()
        sin.show()
    elif(text=="Chirp"):
        chirp.show()
        sin.hide()
    elif(text=="Periodic"):
        chirp.show()
        sin.hide()
    else: 
        chirp.hide()
        sin.hide()
        
def main():
    # playSound(filepath)

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    global generateWindow
    generateWindow = GenerateWindow()
    sys.exit(app.exec_())


def playSound(eng1):
    eng1.playSound(nargout=0)


if __name__ == '__main__':
    main()

eng1.quit()

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import matlab.engine
import numpy as np
import scipy.io.wavfile as wav
import sys

eng1 = matlab.engine.start_matlab()

class MainWindow(QtWidgets.QMainWindow):

    _filepath = None

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Generator and Editor")

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.defineToolbar()

        

        # plot data: x, y values
        #self.graphWidget.plot(hour, temperature)

    def plottingFig(self, y, Fs, tt, graphWidget):
        y = np.asarray(y, dtype=np.float32)
        y = y.reshape(len(y),)
        t = np.arange(0, tt, 1/Fs)
        graphWidget.plot(t, y)

    def defineToolbar(self):
        self.toolbar = QtWidgets.QToolBar()
        self.addToolBar(self.toolbar)

        fileButton = QAction("Browse", self)
        fileButton.setShortcut('Ctrl+O')
        fileButton.triggered.connect(self.getFiles)
        self.toolbar.addAction(fileButton)
        playButton=QAction("Play",self)
        playButton.triggered.connect(self.play)
        self.toolbar.addAction(playButton)
        #graphButton = QAction("Graph", self)
        #graphButton.setShortcut('Ctrl+O')
        #graphButton.triggered.connect(self.plottingFig(self.graphWidget))
        #self.toolbar.addAction(graphButton)

        #print("filepath:", self.filepath)

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
 


def main():
    # playSound(filepath)

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

def playSound(eng1):
    eng1.playSound(nargout=0)


if __name__ == '__main__':
    main()

eng1.quit()

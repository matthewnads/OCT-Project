from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys 



def window():
    app = QApplication(sys.argv)
    win= QMainWindow()
    xpos = 0
    ypos = 0
    width = 300
    height = 300
    win.setGeometry(xpos,ypos,width,height)
    win.setWindowTitle("OCT")
    
    win.show(); 
    sys.exit(app.exec_()) 



window() 
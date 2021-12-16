# OCT-Project
Main branch is production code. It is highly suggested any changes be committed to separate branches and rigourously tested to ensure that nothing breaks in production.

### testGUI.py 
This has the latest code for the GUI. The idea was that the backend will eventually connect here to get the global variables and use them in subsequent MATLAB functions. 

### Resources 
[Official Qt5 docs (PySide2)](https://doc.qt.io/qtforpython-5/)

Remember, we don't actually use PySide2 but [PyQt5](https://www.riverbankcomputing.com/software/pyqt/). Here are the [docs](riverbankcomputing.com/static/Docs/PyQt5/) which you may need if you run into any errors, but you should be fine with the PySide docs.

### initOutput.m

This function is ready to be used with Windows Directsound devices and NI DAQ devices. Currently it is set to initialize only NI DAQ devices. To switch to Directsound devices, ensure that all the output arguments are commented out appropriately, otherwise it will throw an error at you.

### playSound.m

This function is also ready to be used with Windows Directsound devices and NI DAQ devices. It is also capable of listening for trigger signals (from the appropriate inputs). Comment out the appropriate lines to enable the functionality you desire.

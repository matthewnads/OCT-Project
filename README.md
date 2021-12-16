# OCT-Project
Main branch is production code. It is highly suggested any changes be committed to separate branches and rigourously tested to ensure that nothing breaks in production.

## Resources 
[Official Qt5 docs (PySide2)](https://doc.qt.io/qtforpython-5/)

Remember, we don't actually use PySide2 but [PyQt5](https://www.riverbankcomputing.com/software/pyqt/). Here are the [docs](riverbankcomputing.com/static/Docs/PyQt5/) which you may need if you run into any errors, but you should be fine with the PySide docs.

## Code

The following are brief descriptions and quick tips for relevant Matlab functions and python files in this project.

### testGUI.py 
This has the latest code for the GUI. The idea was that the backend will eventually connect here to get the global variables and use them in subsequent MATLAB functions. 

A few troubleshooting tips:
* If you are returning more than one argument from a matlab engine function to python i.e. `var1, var2 = matlabengine.someFunc(nargout=2)`, it may be necessary to set nargout to the number of your output arguments. Typically, the function expects one return argument only.
* Passing an array from python to matlab may require you to cast it as a matlab type, i.e. 
```
import numpy as np

arr = np.random.rand(5)
matlabarr = matlab.double(arr.tolist())
matlabengine.someFunc(matlabarr)
```
As shown in the above example, if you are using a numpy array, it should be also casted as list too. Depending on whether you need static or instance variables depends on the situational needs. 
* If you want to share variables between classes, there's a couple of ways to do it.
    * Declaring variables outside the classes and calling `global` to mutate these variables within a local function is one way.
    * Another way is to declare an object of a class within another class (i.e. `obj = ClassB()`) and mutate and access the class variable you desire (i.e. `var1 = obj.classvar1`.

### initOutput.m

This function initializes a DAQ device to be used. It is ready to be used with Windows Directsound devices and NI DAQ devices. Currently it is set to initialize only NI DAQ devices. To switch to Directsound devices, ensure that all the output arguments are commented out appropriately, otherwise it will throw an error at you.

### playSound.m

This function can drive output or be made to get input from hardware. This function is also ready to be used with Windows Directsound devices and NI DAQ devices. It is also capable of listening for trigger signals (from the appropriate inputs). Comment out the appropriate lines to enable the functionality you desire.

### createOutput.m

This function creates the output array with specified evenlope of a signal. It uses switch case to create the necessary function and then applies the appropriate amplitude, offset, etc.

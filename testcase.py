import tkinter as tk
from tkinter.filedialog import askopenfilename
import matlab.engine
import numpy as np
import scipy.io.wavfile as wav
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

eng1 = matlab.engine.start_matlab()

root = tk.Tk()
root.wm_title("Sound Generator and Editor")

def playSound(eng1):
    eng1.playSound(nargout=0)

def plottingFig(y, Fs, tt):
    fig = Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, tt, 1/Fs)
    fig.add_subplot().plot(t, y)
    return fig

def disp_toolbar(canvas):
    toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
    toolbar.update()

    canvas.mpl_connect(
        "key_press_event", lambda event: print(f"you pressed {event.key}"))
    canvas.mpl_connect("key_press_event", key_press_handler)
    return toolbar

def readFile(filepath): #optional read using python
    Fs, y = wav.read(filepath)
    y = y / 32768.0
    tt = len(y)/float(Fs)
    return y, Fs, tt

def main():

    filepath = askopenfilename()
    print(filepath)

    # playSound()

    y, Fs, tt = readFile(filepath)

    y,Fs,tt = eng1.tGraph(filepath,nargout=3)

    fig = plottingFig(y,Fs,tt)

    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()

    toolbar = disp_toolbar(canvas)

    toolbar.pack(side=tk.TOP, fill=tk.X)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    root.mainloop()

if __name__ == "__main__":
    main()


eng1.quit()

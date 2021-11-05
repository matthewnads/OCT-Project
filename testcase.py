import tkinter as tk
import matlab.engine
import pandas as pd

def main ():
    eng1 = matlab.engine.start_matlab()

    root = tk.Tk()

    Fs = eng1.tGraph('handel.wav',nargout=0)
    print(type(Fs))

    root.mainloop()

    eng1.quit()

if __name__ == "__main__":
    main()


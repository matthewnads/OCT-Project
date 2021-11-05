import tkinter as tk
import matlab.engine
import pandas as pd

def main ():
    eng1 = matlab.engine.start_matlab()

    root = tk.Tk()

    y = matlab.double(eng1.tGraph('handel.wav',nargout=0))

    print(y)

    root.mainloop()

    eng1.quit()

if __name__ == "__main__":
    main()


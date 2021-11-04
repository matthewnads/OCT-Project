import tkinter as tk
import matlab.engine

eng1 = matlab.engine.start_matlab()

print(eng1)

eng1.quit()
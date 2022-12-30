from func import DefinitionScreen
from tkinter import Tk

gui = Tk()

gui.title("")

gui.iconbitmap("data/Blank.ico")

gui.resizable(False, False)

gui.geometry("400x600")

def_screen = DefinitionScreen(gui)

def_screen.grid()

gui.mainloop()

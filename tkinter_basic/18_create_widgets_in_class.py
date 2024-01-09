import tkinter as tk
from tkinter import ttk

def create_widget(parent, label_text, button_text):
    frame = ttk.Frame(parent)

    frame.rowconfigure(0, weight = 1)
    frame.columnconfigure((0,1,2), weight = 1, uniform='a')

    tk.Label(frame, text=label_text).grid(row=0, column=0)
    tk.Button(frame, text=button_text).grid(row=0, column=1)

    return frame

class Segment(ttk.Frame):
    def __init__(self, parent, label_text, button_text):
        super().__init__(parent)

        # grid layout
        self.rowconfigure(0, weight = 1)
        self.columnconfigure((0,1,2), weight = 1, uniform='a')

        tk.Label(self, text=label_text).grid(row=0, column=0, sticky='nsew')
        tk.Button(self, text=button_text).grid(row=0, column=1, sticky='nsew')
        self.create_ex('exercise').grid(row=0, column=2, sticky='nsew')

        self.pack(expand=True, fill='both')

    def create_ex(self, text):
        frame = ttk.Frame(self)
        ttk.Entry(frame).pack(expand=True, fill='both')
        tk.Button(frame, text=text).pack(expand=True, fill='both')

        return frame

root = tk.Tk()
root.title("Mium mium")
root.geometry("640x640+400+200")

Segment(root, 'label1', 'button1')
Segment(root, 'label2', 'button2')
Segment(root, 'label3', 'button3')
create_widget(root, 'label4', 'button4').pack(expand=True, fill='both')
create_widget(root, 'label5', 'button5').pack(expand=True, fill='both')

root.mainloop()
import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self, title, size):

        # Main Setup
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}+400+200")
        self.minsize(600, 600)

        # widgets
        self.menu = Menu(self)
        self.main = Main(self)

        # run
        self.mainloop()

class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, y=0, relwidth=0.3, relheight=1)

        self.create_widgets()

    def create_widgets(self):
        menu_btn1 = tk.Button(self, text='Button 1')
        menu_btn2 = tk.Button(self, text='Button 2')
        menu_btn3 = tk.Button(self, text='Button 3')

        menu_slider1 = ttk.Scale(self, orient='vertical')
        menu_slider2 = ttk.Scale(self, orient='vertical')

        toggle_frame = ttk.Frame(self)
        menu_toggle1 = ttk.Checkbutton(toggle_frame, text='Check 1')
        menu_toggle2 = ttk.Checkbutton(toggle_frame, text='Check 2')

        entry = ttk.Entry(self)

        # Create Grid
        self.columnconfigure((0,1,2), weight=1, uniform='a')
        self.rowconfigure((0,1,2,3,4), weight=1, uniform='a')

        # Place the widgets
        menu_btn1.grid(row=0, column=0, sticky='nswe', columnspan=2)
        menu_btn2.grid(row=0, column=2, sticky='nswe')
        menu_btn3.grid(row=1, column=0, sticky='nswe', columnspan=3)

        menu_slider1.grid(row=2, column=0, rowspan=2, sticky='nswe', pady=20, padx=20)
        menu_slider2.grid(row=2, column=2, rowspan=2, sticky='nswe', pady=20, padx=20)

        toggle_frame.grid(row=4, column=0, columnspan=3, sticky='nswe')
        menu_toggle1.pack(side='left', expand=True)
        menu_toggle2.pack(side='left', expand=True)

        entry.place(relx=0.5, rely=0.95, relwidth=0.9, anchor='center')

class Main(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx = 0.3, y = 0, relwidth = 0.7, relheight = 1)

        # Main Widgets
        entry_frame1 = ttk.Frame(self)
        main_label1 = tk.Label(entry_frame1, text="Label 1", bg='gold')
        main_button1 = tk.Button(entry_frame1, text="Button 1")

        entry_frame2 = ttk.Frame(self)
        main_label2 = tk.Label(entry_frame2, text="Label 2", bg='salmon')
        main_button2 = tk.Button(entry_frame2, text="Button 2")

        # Main Layout
        entry_frame1.pack(side='left', expand=True, fill='both', padx=10, pady=20)
        entry_frame2.pack(side='left', expand=True, fill='both', padx=10, pady=20)

        main_label1.pack(expand=True, fill='both')
        main_button1.pack(expand=True, fill='both')

        main_label2.pack(expand=True, fill='both')
        main_button2.pack(expand=True, fill='both')

App('Class based App', (640, 640))
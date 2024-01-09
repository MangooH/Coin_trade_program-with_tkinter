import tkinter as tk
from tkinter import ttk

# window
window = tk.Tk()
window.title("Layout intro") 
window.geometry("500x600")

# Top Frame
top_frame = ttk.Frame(window)
label1 = tk.Label(top_frame, text="label 1", bg='gold')
label2 = tk.Label(top_frame, text="label 2", bg='salmon')

# Middel Widget
label3 = tk.Label(window, text="label 3", bg='tomato')

# Bottom frame
bottom_frame = ttk.Frame(window)
label4 = tk.Label(bottom_frame, text="Last of the Label", background='azure')
btn1 = tk.Button(bottom_frame, text='A Button')
btn2 = tk.Button(bottom_frame, text='Another Button')
# Bottom right frame
ex_frame = ttk.Frame(bottom_frame)
btn3 = tk.Button(ex_frame, text='Button1')
btn4 = tk.Button(ex_frame, text='Button2')
btn5 = tk.Button(ex_frame, text='Button3')
# top layout
label1.pack(side='left', fill='both', expand=True)
label2.pack(side='left', fill='both', expand=True)
top_frame.pack(fill='both', expand=True)

# Middel Layout
label3.pack(expand=True)

# Bottm layout
btn1.pack(side='left', expand=True, fill='both')
label4.pack(side='left', expand=True, fill='both')
btn2.pack(side='left', expand=True, fill='both')

btn3.pack(expand=True, fill='both')
btn4.pack(expand=True, fill='both')
btn5.pack(expand=True, fill='both')
ex_frame.pack(side='left', fill='both', expand=True)

bottom_frame.pack(expand=True, fill='both', padx=20, pady=20)



# run
window.mainloop()

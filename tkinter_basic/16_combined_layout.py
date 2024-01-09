import tkinter as tk
from tkinter import ttk

root = tk.Tk()
# title 설정
root.title("Mium mium")
root.geometry("640x640+400+200")

# main layout widgets
menu_frame = ttk.Frame(root)
main_frame = ttk.Frame(root)

# main place layout
# place(x, y, w, h)
menu_frame.place(x=0, y=0, relwidth=0.3, relheight=1)
main_frame.place(relx = 0.3, y = 0, relwidth = 0.7, relheight = 1)

# Menu Widgets
menu_btn1 = tk.Button(menu_frame, text='Button 1')
menu_btn2 = tk.Button(menu_frame, text='Button 2')
menu_btn3 = tk.Button(menu_frame, text='Button 3')

menu_slider1 = ttk.Scale(menu_frame, orient='vertical')
menu_slider2 = ttk.Scale(menu_frame, orient='vertical')

toggle_frame = ttk.Frame(menu_frame)
menu_toggle1 = ttk.Checkbutton(toggle_frame, text='Check 1')
menu_toggle2 = ttk.Checkbutton(toggle_frame, text='Check 2')

entry = ttk.Entry(menu_frame)

# Menu Layout
'''
uniform = 'a' -> their sizes are always in strict proportion
'''
menu_frame.columnconfigure((0,1,2), weight=1, uniform='a')
menu_frame.rowconfigure((0,1,2,3,4), weight=1, uniform='a')

menu_btn1.grid(row=0, column=0, sticky='nswe', columnspan=2)
menu_btn2.grid(row=0, column=2, sticky='nswe')
menu_btn3.grid(row=1, column=0, sticky='nswe', columnspan=3)

menu_slider1.grid(row=2, column=0, rowspan=2, sticky='nswe', pady=20, padx=20)
menu_slider2.grid(row=2, column=2, rowspan=2, sticky='nswe', pady=20, padx=20)

toggle_frame.grid(row=4, column=0, columnspan=3, sticky='nswe')
menu_toggle1.pack(side='left', expand=True)
menu_toggle2.pack(side='left', expand=True)

entry.place(relx=0.5, rely=0.95, relwidth=0.9, anchor='center')

# Main Widgets
entry_frame1 = ttk.Frame(main_frame)
main_label1 = tk.Label(entry_frame1, text="Label 1", bg='gold')
main_button1 = tk.Button(entry_frame1, text="Button 1")

entry_frame2 = ttk.Frame(main_frame)
main_label2 = tk.Label(entry_frame2, text="Label 2", bg='salmon')
main_button2 = tk.Button(entry_frame2, text="Button 2")

# Main Layout
entry_frame1.pack(side='left', expand=True, fill='both', padx=10, pady=20)
entry_frame2.pack(side='left', expand=True, fill='both', padx=10, pady=20)

main_label1.pack(expand=True, fill='both')
main_button1.pack(expand=True, fill='both')

main_label2.pack(expand=True, fill='both')
main_button2.pack(expand=True, fill='both')


root.mainloop()
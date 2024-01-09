import tkinter as tk
from tkinter import ttk
from random import randint, choice

root = tk.Tk()
root.title("Mium mium")
root.geometry("640x480+400+200")

canvas = tk.Canvas(root, bg='white', scrollregion=(0,0,2000,5000))
canvas.create_line(0,0,2000,5000, fill = 'green', width=10)
for i in range(100):
    l = randint(0, 2000)
    t = randint(0, 5000)
    r = l + randint(10, 500)
    b = t + randint(10, 500)
    color = choice(('red', 'green', 'blue', 'yellow', 'orange'))
    canvas.create_rectangle(l,t,r,b, fill=color) 
canvas.pack(expand=True, fill='both')

# mouse whell scrolling
def scroll(event):
    if not event.state:
        return canvas.yview_scroll(-int(event.delta), 'units')
    else:
        return canvas.xview_scroll(-int(event.delta), 'units')
canvas.bind('<MouseWheel>', lambda event: scroll(event))

# scrollbar
y_scrollbar = ttk.Scrollbar(root, orient='vertical', command=canvas.yview)
canvas.configure(yscrollcommand=y_scrollbar.set)
y_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')

x_scrollbar = ttk.Scrollbar(root, orient='horizontal', command=canvas.xview)
canvas.configure(xscrollcommand=x_scrollbar.set)
x_scrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')

root.mainloop()
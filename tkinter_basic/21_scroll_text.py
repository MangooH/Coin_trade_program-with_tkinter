import tkinter as tk
from tkinter import ttk
from random import randint, choice

root = tk.Tk()
root.title("Mium mium")
root.geometry("640x480+400+200")

# mouse whell scrolling
# def scroll(event):
#     if not event.state:
#         return canvas.yview_scroll(-int(event.delta), 'units')
#     else:
#         return canvas.xview_scroll(-int(event.delta), 'units')
# canvas.bind('<MouseWheel>', lambda event: scroll(event))

# # scrollbar
# y_scrollbar = ttk.Scrollbar(root, orient='vertical', command=canvas.yview)
# canvas.configure(yscrollcommand=y_scrollbar.set)
# y_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')

text = tk.Text(root)
for i in range(1, 200):
    text.insert(f'{i}.0', f'text: {i} \n')
text.pack(expand=True, fill='both')
text.config(state='disabled') #disable editing

scrollbar = ttk.Scrollbar(root, orient='vertical', command=text.yview)
text.configure(yscrollcommand=scrollbar.set)
scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')


root.mainloop()
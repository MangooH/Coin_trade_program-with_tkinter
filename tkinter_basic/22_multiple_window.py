import tkinter as tk
from tkinter import ttk, messagebox

def ask_yes_no():
    answer = messagebox.askquestion('Title', 'Body')
    print(answer)

def create_window():
    global extra_window
    extra_window = tk.Toplevel()
    extra_window.title('extra window')
    extra_window.geometry('300x300')

def close_window():
    extra_window.destroy()

root = tk.Tk()
root.title("Mium mium")
root.geometry("640x480+400+200")

# 버튼 위젯 생성
btn1 = tk.Button(root, text='Open main window', command=create_window)
btn1.pack(expand=True) 

# 패딩이 있는 버튼
btn2 = tk.Button(root, text='Close main window', command=close_window)
btn2.pack(expand=True) 

# 높이와 너비를 정해주는 버튼
btn3 = tk.Button(root, text='create yes no window', command=ask_yes_no)
btn3.pack(expand=True) 

root.mainloop()
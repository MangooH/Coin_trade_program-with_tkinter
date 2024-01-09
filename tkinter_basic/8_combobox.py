from tkinter import *
import tkinter.ttk as ttk

root = Tk()
root.title("Mium mium")
root.geometry("640x480+400+200")
 
values = [str(i) + "일" for i in range(1, 32)]
combobox = ttk.Combobox(root, height=5, values=values, state="readonly")
combobox.pack()
combobox.set("카드 결제일")


Label(root, text="카드 결제일을 선택하세요.").pack()
combobox2 = ttk.Combobox(root, height=10, values=values, state="readonly")
combobox2.current(0)
combobox2.pack() 

def change():
    print(combobox.get()) # 선택된 값표시

btn1 = Button(root, text="Click", command=change)
btn1.pack()

root.mainloop()
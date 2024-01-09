from tkinter import *
import tkinter.ttk as ttk
import time

root = Tk()
root.title("Mium mium")
root.geometry("640x480+400+200")

# pgbar = ttk.Progressbar(root, maximum=100, mode="determinate")
# pgbar.start(10) # 10ms 마다 움직임
# pgbar.pack()

# def change():
#     pgbar.stop() # 작동 중지

# btn1 = Button(root, text="Click", command=change)
# btn1.pack()

pg_var = DoubleVar()
pgbar = ttk.Progressbar(root, maximum=100, length=150, variable=pg_var)
pgbar.pack()

def btncmd():
    for i in range(1, 101):
        time.sleep(0.01)
        pg_var.set(i)
        pgbar.update() # GUI 업데이트.

btn = Button(root, text="시작", command=btncmd)
btn.pack()

root.mainloop()
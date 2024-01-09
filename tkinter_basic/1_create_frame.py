import tkinter as tk

root = tk.Tk()
# title 설정
root.title("Mium mium")
# 크기설정 : 가로 x 세로 / 위치 설정 : + x 위치, + y 위치 
root.geometry("640x480+400+200")
# 창 크기 조절 허용 x, y
root.resizable(False, False)

root.mainloop()
from tkinter import *

root = Tk()
root.title("Mium mium")
root.geometry("640x480+400+200")
 
cv = IntVar() # cv 에 int 형으로 값을 저장한다. 
cb = Checkbutton(root, text="오늘 하루 보지 않기", variable=cv)
cb.select() # 선택
cb.deselect() # 선택 해제
cb.pack()

def change():
    print(cv.get()) # 0: 체크해제, 1: 체크

btn1 = Button(root, text="Click", command=change)
btn1.pack()

root.mainloop()
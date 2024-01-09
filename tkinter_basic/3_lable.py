from tkinter import *

root = Tk()
root.title("Mium mium")
root.geometry("640x480+400+200")

lable1 = Label(root, text="안녕하세요")
lable1.pack()

photo = PhotoImage(file="tkinter_basic/check.png")
lable2 = Label(root, image=photo)
lable2.pack()

def change():
    lable1.config(text="또 만나요")

    # Garbage collector 가 이미지를 지움.
    global photo2
    photo2 = PhotoImage(file="tkinter_basic/x.png")
    lable2.config(image=photo2)

btn1 = Button(root, text="Click", command=change)
btn1.pack()

root.mainloop()
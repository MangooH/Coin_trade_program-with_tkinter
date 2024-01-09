from tkinter import *

root = Tk()
root.title("Mium mium")
root.geometry("640x480+400+200")
 
Label(root, text="메뉴를 선택하세요.").pack()

burger_var = IntVar()
btn_burger1 = Radiobutton(root, text="햄버거", value=1, variable=burger_var)
btn_burger1.select()
btn_burger1.pack() 
btn_burger2 = Radiobutton(root, text="치즈버거", value=2, variable=burger_var).pack()
btn_burger3 = Radiobutton(root, text="치킨버거", value=3, variable=burger_var).pack()

Label(root, text="음료를 선택하세요.").pack()

drink_var = StringVar()
btn_drink1 = Radiobutton(root, text="콜라", value="콜라", variable=drink_var)
btn_drink2 = Radiobutton(root, text="사이다", value="사이다", variable=drink_var)
btn_drink1.select()
btn_drink1.pack()
btn_drink2.pack()

def change():
    print(burger_var.get())
    print(drink_var.get())

btn1 = Button(root, text="Click", command=change)
btn1.pack()

root.mainloop()
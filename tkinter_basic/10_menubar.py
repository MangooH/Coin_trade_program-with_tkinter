from tkinter import *
import tkinter.ttk as ttk

root = Tk()
root.title("Mium mium")
root.geometry("640x480+400+200")
 


def create_new_file():
    print('새 파일 만들기')
    
menu = Menu(root)
menu_file = Menu(menu, tearoff=0)
menu_file.add_command(label = "New file", command=create_new_file)
menu_file.add_command(label = "New Window")
menu_file.add_separator()
menu_file.add_command(label="Open File...")
menu_file.add_separator()
menu_file.add_command(label="Save All", state="disable")
menu_file.add_separator()
menu_file.add_command(label="Exit", command=root.quit)
menu.add_cascade(label="File", menu=menu_file)

# Edit 메뉴 (빈값)
menu.add_cascade(label="Edit", menu=Menu(menu, tearoff=0))

# Language 메뉴 추가
menu_lang = Menu(menu, tearoff=0)
menu_lang.add_radiobutton(label="Python")
menu_lang.add_radiobutton(label="Java")
menu_lang.add_radiobutton(label="Cpp")
menu.add_cascade(label="Language", menu=menu_lang)

# View 메뉴 추가
menu_view = Menu(menu, tearoff=0)
menu_view.add_checkbutton(label="Show Minimap")
menu.add_cascade(label="View", menu=menu_view)

root.config(menu=menu)
root.mainloop()
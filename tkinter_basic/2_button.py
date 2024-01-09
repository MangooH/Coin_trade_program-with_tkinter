import tkinter as tk

root = tk.Tk()
root.title("Mium mium")

# 버튼 위젯 생성
btn1 = tk.Button(root, text='버튼1')
btn1.pack() # root 에 포함

# 패딩이 있는 버튼
btn2 = tk.Button(root, padx=5, pady=10, text='버튼2')
btn2.pack() # root 에 포함

# 높이와 너비를 정해주는 버튼
btn3 = tk.Button(root, width=10, height=3, text='버튼3')
btn3.pack() # root 에 포함

# 색상 지정
btn4 = tk.Button(root, padx=8, pady=8, fg="red", bg="yellow", text='버튼4')
btn4.pack()

# 아이콘 버튼
photo = tk.PhotoImage(file="tkinter_basic/check.png")
btn5 = tk.Button(root, image=photo)
btn5.pack()

# 버튼 동작
def btncmd():
    print('버튼이 클릭됨')
btn6 = tk.Button(root, text="동작하는 버튼", command=btncmd)
btn6.pack()

root.mainloop()
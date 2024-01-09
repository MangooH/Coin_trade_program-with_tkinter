import tkinter as tk

root = tk.Tk()
root.title("Mium mium")
root.geometry("640x480+400+200")

# 텍스트 입력 위젯 - 여러줄 입력 가능 
text = tk.Text(root, width=30, height=10)
text.pack()
text.insert(tk.END, '글자를 입력하세요')

# 엔트리 입력 위젯 - 한줄만 입력 가능 (Enter 키 불가)
e = tk.Entry(root, width=30)
e.pack()
e.insert(0, "한 줄만 입력하세요")

# Get text
def get_text():
    print(text.get("1.0", tk.END)) # "1.0" : '1' 첫 번째 줄의 '0'번째 column 부터 / END : 끝까지 가져와라 
    print(e.get())
btn1 = tk.Button(root, text="내용출력", command=get_text)
btn1.pack()

# Delete text()
def delete_text():
    text.delete("1.0", tk.END)
    e.delete(0, tk.END)
btn2 = tk.Button(root, text="내용삭제", command=delete_text)
btn2.pack()

root.mainloop()
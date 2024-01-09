from tkinter import *

root = Tk()
root.title("Mium mium")
root.geometry("640x480+400+200")

# height : 지정된 개수 만큼 (0: 모두)
# selectmode : single, exteneded
lb = Listbox(root, selectmode="extended", height=5)
for e in ["사과", "딸기", "포도", "수박", "바나나", "사과", "딸기", "포도", "수박", "바나나"]:
    lb.insert(END, e)
lb.pack()

def change():
    ## 삭제
    # lb.delete(END)
    # 개수 확인
    #print("리스트에는", lb.size(), '개가 있어요')
    # 항목 확인
    #print("첫 번째 부터 세 번째까지의 항목 : ", lb.get(0,2))
    # 선택된 항목 확인
    print("선택된 항목 : ", lb.curselection())
btn1 = Button(root, text="Click", command=change)
btn1.pack()

root.mainloop()
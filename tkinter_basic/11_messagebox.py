from tkinter import *
import tkinter.messagebox as msgbox

root = Tk()
root.title("Mium mium")
root.geometry("640x480+400+200")

def info():
    msgbox.showinfo("알림", "정상적으로 완료")

def warn():
    msgbox.showwarning("경고", "좌석이 매진되었습니다.")

def error():
    msgbox.showwarning("에러", "결제 오류 발생")

def okcancel():
    # msgbox.askokcancel("확인 / 취소", "해당 좌석은 유아 동반석. 예매할거냐?")
    # msgbox.askretrycancel("재시도 / 취소", "다시시도?")
    # msgbox.askyesno("예 / 취소", "예매할거냐?")
    msgbox.askyesnocancel(title=None, message="저장안됨")

Button(root, command=info, text="알림").pack()
Button(root, command=warn, text="경고").pack()
Button(root, command=error, text="에러").pack()
Button(root, command=okcancel, text="확인 취소").pack()



root.mainloop()
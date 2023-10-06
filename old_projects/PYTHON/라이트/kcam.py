import os
import time
import tkinter
import tkinter.messagebox
import pyautogui
import clipboard

def process():
    win = tkinter.Tk()
    win.title('KOS 2023')
    win.geometry('300x400+100+50')
    win.resizable(0,0)

    listbox = tkinter.Listbox( win, width=20,  height=9, font = ("맑은 고딕", 15) )
    listbox.place(x=10,y=10) #창이름 리스트

    off = True #창닫기
    def shutdown():
        nonlocal off
        off = False
        nonlocal win
        win.destroy()
    win.protocol('WM_DELETE_WINDOW', shutdown)

    locked = False #고정
    def lock():
        time.sleep(0.1)
        nonlocal locked
        nonlocal but0
        nonlocal win
        if locked:
            locked = False
            but0.configure(bg='gray50')
            win.wm_attributes("-topmost", 0)
        else:
            locked = True
            but0.configure(bg='lawn green')
            win.wm_attributes("-topmost", 1)
    but0 = tkinter.Button(win, text = 'LOCK', font = ("맑은 고딕", 14), command = lock, bg = 'gray50', fg = 'midnight blue')
    but0.place(x=10,y=340)

    title = [ ]
    def name():
        time.sleep(0.1)
        nonlocal title
        title = pyautogui.getAllWindows()
        title = [ i.title for i in title ]
        title = list( filter(lambda x : x != '',title) )
        nonlocal listbox
        listbox.delete( 0,listbox.size() )
        nonlocal win
        for i in title:
            if i != '':
                time.sleep(0.1)
                listbox.insert( listbox.size(),i )
                win.update()
    but1 = tkinter.Button(win, text = 'NAME', font = ("맑은 고딕", 14), command = name, bg = 'gray50', fg = 'midnight blue')
    but1.place(x=105,y=340)

    def copy():
        nonlocal title
        nonlocal listbox
        temp = listbox.curselection()[0]
        clipboard.copy( title[temp] )
    but2 = tkinter.Button(win, text = 'COPY', font = ("맑은 고딕", 14), command = copy, bg = 'gray50', fg = 'midnight blue')
    but2.place(x=210,y=340)
    win.update()

    win.mainloop()

time.sleep(0.5)

win = tkinter.Tk()
win.title('KOS 2023')
win.geometry('300x80+300+200')
win.resizable(0,0)

def go0():
    time.sleep(0.1)
    os.startfile('Kcam.exe')
but0 = tkinter.Button(win, text = '실행', font = ("맑은 고딕", 15), command = go0)
but0.place(x=10,y=10)

def go1():
    time.sleep(0.1)
    os.system('taskkill /f /im Kcam.exe')
but1 = tkinter.Button(win, text = '종료', font = ("맑은 고딕", 15), command = go1)
but1.place(x=80,y=10)

def go2():
    time.sleep(0.1)
    global win
    win.destroy()
    process()
but2 = tkinter.Button(win, text = '이름', font = ("맑은 고딕", 15), command = go2)
but2.place(x=150,y=10)

def go3():
    time.sleep(0.1)
    tkinter.messagebox.showinfo('도움말',' 현재 도움말을 제공하지 않습니다.\n 감사합니다. ')
but3 = tkinter.Button(win, text = '도움', font = ("맑은 고딕", 15), command = go3)
but3.place(x=220,y=10)

win.mainloop()
time.sleep(0.5)

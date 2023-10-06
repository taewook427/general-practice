# --hidden-import "pynput.keyboard._win32" --hidden-import "pynput.mouse._win32" //win

import pyautogui
import time
import tkinter
import keyboard

def work0(num):
    for i in range(0,num):
        pyautogui.click()
        time.sleep(0.03)
        pyautogui.click()
        time.sleep(0.05)
        pyautogui.hotkey('ctrl','tab')
        time.sleep(0.03)

def work1(num):
    for i in range(0,num):
        pyautogui.press('enter')
        time.sleep(0.03)
        pyautogui.press('enter')
        time.sleep(0.05)
        pyautogui.hotkey('ctrl','tab')
        time.sleep(0.03)

def work2(num):
    pyautogui.hotkey('ctrl','tab')
    time.sleep(0.05)
    pyautogui.click()
    time.sleep(0.03)
    pyautogui.click()
    time.sleep(0.03)

def work3(num):
    pyautogui.press('enter')
    time.sleep(0.03)
    pyautogui.press('enter')
    time.sleep(0.03)

win = tkinter.Tk()
win.title('test407')
win.geometry("400x300+200+150")
win.resizable(False, False)
win.update()

num = 10 #####

win.wm_attributes("-topmost", 1)
k = True
def shutdown():
    global k
    k = False
    global win
    win.destroy()
win.protocol('WM_DELETE_WINDOW', shutdown)

status = tkinter.StringVar()
status.set('OFF')

label1 = tkinter.Label(win, textvariable = status, font=('Consolas',30) )
label1.place(x=15,y=15)
win.update()

exp = '''a : 클릭 클릭 탭  
s : 엔터 엔터 탭  
d : 탭 클릭 클릭
w : 엔터 엔터
e : 종료          
'''
label2 = tkinter.Label(win, text = exp, font=('Consolas',20) )
label2.place(x=15,y=80)
win.update()

pyautogui.PAUSE = 0.001
while k:
    time.sleep(0.01)
    
    if keyboard.is_pressed('a'):
        status.set('ON a')
        win.update()
        work0(num)
        time.sleep(0.01)
        status.set('OFF')
        win.update()

    elif keyboard.is_pressed('s'):
        status.set('ON s')
        win.update()
        work1(num)
        time.sleep(0.01)
        status.set('OFF')
        win.update()

    elif keyboard.is_pressed('d'):
        status.set('ON d')
        win.update()
        time.sleep(0.01)
        work2(num)
        status.set('OFF')
        win.update()

    elif keyboard.is_pressed('w'):
        status.set('ON w')
        win.update()
        time.sleep(0.01)
        work3(num)
        status.set('OFF')
        win.update()

    elif keyboard.is_pressed('e'):
        time.sleep(0.1)
        k = False
        win.destroy()

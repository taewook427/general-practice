# --hidden-import "pynput.keyboard._win32" --hidden-import "pynput.mouse._win32" //win
# --hidden-import "pynput.keyboard._xorg" --hidden-import "pynput.mouse._xorg" //linux

import time
import tkinter
import tkinter.font
import pyautogui

win = tkinter.Tk()
win.title('Rubidium')
win.geometry("600x300+200+150")
win.resizable(False, False)
win.configure(bg='navy')
font = tkinter.font.Font(family="Consolas", size=20)
win.update()

height = pyautogui.size()[1] #y
width = pyautogui.size()[0] #x
txt0 = ' < 현재 디스플레이 해상도 >\n X : ' + str(width) + '   Y : ' + str(height)

label0 = tkinter.Label(win, text = txt0, font = font, bg='navy', fg='cyan2')
label0.place(x=5,y=10)
win.update()

txt1 = tkinter.StringVar()

temp = pyautogui.position()
currentx = temp[0] #x
currenty = temp[1] #y
txt1.set(' < 현재 마우스 위치 >\n X : '+str(currentx)+'   Y : '+str(currenty))

label1 = tkinter.Label(win, textvariable = txt1, font = font, bg='navy', fg='cyan2')
label1.place(x=5,y=150)
win.update()

k = True
def shutdown():
    global k
    k = False
    global win
    win.destroy()
win.protocol('WM_DELETE_WINDOW', shutdown)

locked = False
def lock():
    time.sleep(0.05)
    global locked
    global but0
    global win
    if locked:
        locked = False
        but0.configure(bg='gray50')
        win.wm_attributes("-topmost", 0)
    else:
        locked = True
        but0.configure(bg='lawn green')
        win.wm_attributes("-topmost", 1)
but0 = tkinter.Button(win, text = 'LOCK', font = ("맑은 고딕", 10), command = lock, bg = 'gray50', fg = 'midnight blue')
but0.place(x=500,y= 180)

while k:
    time.sleep(0.015)
    temp = pyautogui.position()
    currentx = temp[0] #x
    currenty = temp[1] #y
    txt1.set(' < 현재 마우스 위치 >\n X : '+str(currentx)+'   Y : '+str(currenty))
    win.update()
time.sleep(0.5)

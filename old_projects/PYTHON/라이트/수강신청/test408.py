# --hidden-import "pynput.keyboard._win32" --hidden-import "pynput.mouse._win32" //win

import pyautogui
import time
import tkinter
import keyboard
from threading import Thread

def work():
    time.sleep(0.001)
    global var
    global k
    while k:
        time.sleep(0.001)
        while var:
            #pyautogui.click()
            #time.sleep(0.001)
            pyautogui.press('enter')
            #time.sleep(0.001)

win = tkinter.Tk()
win.title('test407')
win.geometry("400x300+200+150")
win.resizable(False, False)
win.update()

win.wm_attributes("-topmost", 1)
k = True
var = False
def shutdown():
    global k
    global var
    var = False
    k = False
    global win
    win.destroy()
win.protocol('WM_DELETE_WINDOW', shutdown)

status = tkinter.StringVar()
status.set('OFF')

label1 = tkinter.Label(win, textvariable = status, font=('Consolas',30) )
label1.place(x=15,y=15)
win.update()

th1 = Thread(target = work)
th1.start()

while k:
    time.sleep(0.01)
    if keyboard.is_pressed('a'):
        if var:
            var = False
            status.set('OFF')
        else:
            var = True
            status.set('ON')
        win.update()
        time.sleep(0.1)

    elif keyboard.is_pressed('e'):
        time.sleep(0.1)
        k = False
        win.destroy()

th1.join()

# --hidden-import "pynput.keyboard._win32" --hidden-import "pynput.mouse._win32" //win

import pyautogui
import time
import tkinter
import keyboard

def work():
    pyautogui.hotkey('ctrl','tab')
    time.sleep(0.01)
    pyautogui.click()
    time.sleep(0.03)
    pyautogui.click()
    time.sleep(0.05)
    pyautogui.press('enter')
    time.sleep(0.03)
    pyautogui.press('enter')

win = tkinter.Tk()
win.title('test407')
win.geometry("400x300+200+150")
win.resizable(False, False)
win.update()

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

pyautogui.PAUSE = 0.001
while k:
    time.sleep(0.01)
    
    if keyboard.is_pressed('a'):
        status.set('ON')
        win.update()
        work()
        time.sleep(0.01)
        status.set('OFF')
        win.update()

    elif keyboard.is_pressed('e'):
        time.sleep(0.1)
        k = False
        win.destroy()

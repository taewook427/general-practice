from time import strftime
from time import localtime
from time import time
from time import sleep
from tkinter import Tk
from tkinter import StringVar
from tkinter import Label
from tkinter import Button

def gettime():
    cal = ['월요일','화요일','수요일','목요일','금요일','토요일','일요일']
    temp = time()
    now = localtime( temp )
    hour = int( strftime( '%H' , now ) )
    if hour >= 12:
        ap = '오후 '
    else:
        ap = '오전 '
    hour = hour % 12
    if hour == 0:
        hour = 12
    temp = str( temp - int(temp) )[2] #소숫점 첫째자리
    sec = ap + str(hour) + ':' + strftime( '%M:%S' , now ) + '.' + temp
    m = str( int( strftime( '%m' , now ) ) ) + '월 '
    d = str( int( strftime( '%d' , now ) ) ) + '일 '
    y = str( int( strftime( '%Y' , now ) ) ) + '년 '
    day = y + m + d + cal[now.tm_wday]
    return [sec,day] #시분초 / 날짜

font0 = ("Consolas", 40)
font1 = ("맑은 고딕", 20)
font2 = ("맑은 고딕", 10)
color0 = 'deep sky blue'
color1 = 'midnight blue'
color2 = 'gray50'
color3 = 'lawn green'
locked = False

win = Tk()
win.title("Argon")
win.geometry("440x130+300+200")
win.resizable(0,0)
win.configure(bg=color1)

txt0 = StringVar()
txt0.set('오전 12:00:00.0')
label0 = Label(win, textvariable = txt0, bg=color1, fg=color0, font=font0)
label0.place(x=0,y=5)

txt1 = StringVar()
txt1.set('2022년 12월 31일 일요일')
label1 = Label(win, textvariable = txt1, bg=color1, fg=color0, font=font1)
label1.place(x=0,y=70)

off = True
def shutdown():
    global off
    off = False
    global win
    win.destroy()
win.protocol('WM_DELETE_WINDOW', shutdown)
win.update()

def lock():
    sleep(0.05)
    global locked
    global but0
    global win
    if locked:
        locked = False
        but0.configure(bg=color2)
        win.wm_attributes("-topmost", 0)
    else:
        locked = True
        but0.configure(bg=color3)
        win.wm_attributes("-topmost", 1)
but0 = Button(win, text = '  LOCK  ', font = font2, command = lock, bg = color2, fg = color1)
but0.place(x=350,y=80)

while off:
    sleep(0.03)
    temp = gettime()
    txt0.set(temp[0])
    txt1.set(temp[1])
    win.update()
sleep(0.5)

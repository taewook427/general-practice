from time import strftime
from time import localtime
from time import time
from time import sleep

from tkinter import Tk
from tkinter import StringVar
from tkinter import Label

win = Tk()
win.title("CLOCK")
win.geometry("300x100+300+200")
win.resizable(0,0)

bigtxt = StringVar()
bigtxt.set("CLOCK for win11")
label0 = Label(win,textvariable = bigtxt)
label0.pack()
label0.configure(font=("Consolas", 30))

smalltxt = StringVar()
smalltxt.set("made by kos")
label1 = Label(win,textvariable = smalltxt)
label1.pack()
label1.configure(font=("Consolas", 15))

cal = ['월요일','화요일','수요일','목요일','금요일','토요일','일요일']
i = 0
while i < 216000:
    
    sleep(0.1)
    i = i + 1
    
    now = localtime( time() )
    hour = int( strftime( '%H' , now ) )
    
    if hour >= 12:
        ap = '오후 '
    else:
        ap = '오전 '
    hour = hour % 12
    if hour == 0:
        hour = 12
        
    sec = ap + str(hour) + ':' + strftime( '%M:%S' , now )
    m = str( int( strftime( '%m' , now ) ) ) + '월 '
    d = str( int( strftime( '%d' , now ) ) ) + '일 '
    y = str( int( strftime( '%Y' , now ) ) ) + '년 '
    day = y + m + d + cal[now.tm_wday]

    try:
        bigtxt.set(sec)
        smalltxt.set(day)
        win.update()
    except:
        sleep(0.5)
        i = 216000

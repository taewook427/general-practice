# 수강 신청 --hidden-import "pynput.keyboard._win32" --hidden-import
# "pynput.mouse._win32" //win

import pyautogui
import time
import tkinter
import tkinter.ttk
import keyboard
from PIL import ImageGrab
from PIL import ImageTk
from PIL import Image

def work(): # 다중탭 단일 신청
    pyautogui.click()
    time.sleep(0.03)
    pyautogui.click()
    time.sleep(0.05)
    
    pyautogui.press('enter')
    time.sleep(0.03)
    pyautogui.press('enter')
    time.sleep(0.03)

    pyautogui.hotkey('ctrl','tab')
    time.sleep(0.05)

def timing(): # 시차 맞추기
    global win
    global image
    
    img = ImageGrab.grab()
    t0 = time.time() # 컴퓨터 시간 save
    img.save('temp.png') # 서버 시간 save
    t1 = time.localtime(t0)
    show = time.strftime('%Y년 %m월 %d일\n%H시 %M분 %S', t1)
    t2 = f'{t0:.3f}'
    show = show + t2[t2.find('.'):] + '초' # 컴퓨터 시간

    new = tkinter.Toplevel()
    new.title('timing')
    new.geometry("600x500+1500+150")
    new.resizable(False, False)
    label2 = tkinter.Label(new, text = show, font=('Consolas',15) )
    label2.place(x=25,y=430)
    image = Image.open('temp.png').resize( (500,400) )
    image = ImageTk.PhotoImage(image)
    label3 = tkinter.Label(new, image = image)
    label3.pack()

    label4 = tkinter.Label( new, text = '00:00:00.000 사진시각', font=('Consolas',15) )
    label4.place(x=300,y=410)
    entry0 = tkinter.Entry(new, font=('Consolas',15) )
    entry0.place(x=300,y=450)

    var = 3600.0
    def go():
        temp = entry0.get()
        t10 = 3600 * int( time.strftime('%H', t1) ) + 60 * int( time.strftime('%M', t1) ) + int( time.strftime('%S', t1) ) + float( '0' + t2[t2.find('.'):] )
        # 컴퓨터 환산 시각
        t20 = 3600 * int( temp[0:2] ) + 60 * int( temp[3:5] ) + int( temp[6:8] ) + float( '0' + temp[8:] )
        # 서버 환산 시각
        global tconst
        tconst = t10 - t20 # 이 수치만큼 내 컴퓨터 시간이 빠르다. ex tconst = 1.0, my = 1s, ser = 0s
        new.destroy()
        status.set( f'{tconst:.3f} 빠름' )
        win.update()
    but1 = tkinter.Button(new, text = '>', font=('Consolas',15), command = go)
    but1.place(x=5,y=5)

win = tkinter.Tk()
win.title('XX대학XXXXXX')
win.geometry("400x300+200+150")
win.resizable(False, False)
win.update()

win.wm_attributes("-topmost", 1)
status = tkinter.StringVar()
status.set('IDLE')
label1 = tkinter.Label(win, textvariable = status, font=('Consolas',30) )
label1.place(x=15,y=15)
win.update()

tconst = 0.0 # 시차 상수
def tf():
    timing()
but0 = tkinter.Button(win, text = '시차 맞추기', font=('Consolas',15), command = tf)
but0.place(x=15,y=230)
win.update()

entry1 = tkinter.Entry(win, width = 6, font=('Consolas',15) )
entry1.place(x=300,y=230) # 시작 시간
label2 = tkinter.Label(win, text = '00:00\n시, 분', font=('Consolas',15) )
label2.place(x=180,y=230)

entry2 = tkinter.Entry(win, width = 3, font=('Consolas',15) )
entry2.place(x=330,y=170) # 신청 개수 (실개수 + 1)
label3 = tkinter.Label(win, text = '신청수(n+1)', font=('Consolas',15) )
label3.place(x=150,y=170)

def func():
    temp = entry1.get()
    st = 3600 * int( temp[0:2] ) + 60 * int( temp[3:5] ) # 시작 시점
    num = int( entry2.get() ) # 신청 개수
    de = 0.05 # 0.05s 전 시작

    it = time.time()
    iit = f'{it:.3f}'
    temp = time.localtime( it )
    the = 3600 * int( time.strftime('%H', temp) ) + 60 * int( time.strftime('%M', temp) ) + int( time.strftime('%S', temp) ) + float( '0' + iit[iit.find('.'):] )
    the = the - tconst + de # 환산 보정 시각

    while the < st:
        time.sleep(0.01)
        it = time.time()
        iit = f'{it:.3f}'
        temp = time.localtime( it )
        the = 3600 * int( time.strftime('%H', temp) ) + 60 * int( time.strftime('%M', temp) ) + int( time.strftime('%S', temp) ) + float( '0' + iit[iit.find('.'):] )
        the = the - tconst + de # 환산 보정 시각
        status.set(f'{st - the:.3f}')
        win.update()

    for i in range(1,num+1):
        work()
        status.set(f'tgt : {i}')
        win.update()
    
but1 = tkinter.Button(win, text = 'EXE', font=('Consolas',15), command = func)
but1.place(x=330,y=100)

pyautogui.PAUSE = 0.001
win.mainloop()

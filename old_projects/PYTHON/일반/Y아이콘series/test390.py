# 버스 예약
# --hidden-import "pynput.keyboard._win32" --hidden-import "pynput.mouse._win32"
# windows

import pyautogui
import time
import tkinter
import tkinter.ttk
import tkinter.messagebox
import keyboard
from PIL import ImageGrab
from PIL import ImageTk
from PIL import Image

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
win.title('연세XXXXXXXX')
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

def readset():
    with open('test390.txt', 'r', encoding='utf-8') as f:
        raw = [ x.strip() for x in f.readlines() ]
        raw = [x.replace(' ','') for x in raw if x != '']
        raw = [x for x in raw if x[0] != '#']
    # 시작시간, 예약버튼위치, 예약일자선택위치, 달력선택위치, 스크롤
    out = [0] * 5
    for i in raw:
        order = i[0:i.find('=')]
        element = i[i.find('=')+1:]
        if order == 'start':
            out[0] = 3600 * int( element[0:2] ) + 60 * int( element[3:5] )
        elif order == 'reserve':
            temp = element.split(',')
            out[1] = [ int( temp[0] ), int( temp[1] ) ]
        elif order == 'date':
            temp = element.split(',')
            out[2] = [ int( temp[0] ), int( temp[1] ) ]
        elif order == 'select':
            temp = element.split(',')
            out[3] = [ int( temp[0] ), int( temp[1] ) ]
        elif order == 'scroll':
            out[4] = int(element)
    return out

def func():
    setting = readset()
    tkinter.messagebox.showinfo('설정데이터',f' 시작시간, 예약버튼위치, 예약일자선택위치, 달력선택위치, 스크롤 \n {setting} ')
    de = -0.05 # 0.05s 후 시작

    st = setting[0]

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

    pyautogui.press('f5')
    status.set('A 누르기')
    win.update()

    process = True
    while process:
        time.sleep(0.01)
        if keyboard.is_pressed('a'):
            process = False
        win.update()

    pyautogui.moveTo( setting[1][0], setting[1][1], 0.01 )
    pyautogui.click()
    status.set('예약 버튼')
    win.update()
    time.sleep(0.1)
    
    process = True
    while process:
        time.sleep(0.01)
        if keyboard.is_pressed('a'):
            process = False
        win.update()

    pyautogui.moveTo( setting[2][0], setting[2][1], 0.01 )
    pyautogui.click()
    status.set('달력 버튼')
    win.update()
    time.sleep(0.1)

    process = True
    while process:
        time.sleep(0.01)
        if keyboard.is_pressed('a'):
            process = False
        win.update()

    pyautogui.moveTo( setting[3][0], setting[3][1], 0.01 )
    pyautogui.click()
    status.set('날자 선택')
    win.update()
    time.sleep(0.1)
    
    process = True
    while process:
        time.sleep(0.01)
        if keyboard.is_pressed('a'):
            process = False
        win.update()

    pyautogui.scroll(setting[4])
    status.set('스크롤 내림')
    win.update()
    time.sleep(0.1)
    status.set('완료')
    
but1 = tkinter.Button(win, text = 'EXE', font=('Consolas',15), command = func)
but1.place(x=250,y=230)

pyautogui.PAUSE = 0.001
win.mainloop()

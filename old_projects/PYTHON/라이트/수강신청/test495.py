# 수강 신청 //win
# --hidden-import "pynput.keyboard._win32"
# --hidden-import "pynput.mouse._win32"

import os
import pyautogui
import time
import tkinter
import tkinter.ttk
import keyboard
from PIL import ImageGrab
from PIL import ImageTk
from PIL import Image

temp = input('작동 시각 시:분:초 (ex 09:00:00) >>> ').split(':')
time0 = 3600 * int( temp[0] ) + 60 * int( temp[1] ) + 1 * int( temp[2] ) # 시작 시각
waypoint = [ (0, 0) ] * int( input('웨이포인트 수 (ex 7) >>> ') ) # 위치 데이터
for i in range(0, len(waypoint) ):
    input(f'wp{i} 위치에 마우스 올리고 엔터')
    temp = pyautogui.position()
    waypoint[i] = ( temp[0], temp[1] )
print(f'wp : {waypoint}')
input('press ENTER to continue... ')

img = ImageGrab.grab()
t0 = time.time() # 컴퓨터 시간 save
img.save('temp.png') # 서버 시간 save
t1 = time.localtime(t0)
show = time.strftime('%Y년 %m월 %d일 %H시 %M분 %S', t1)
t2 = f'{t0:.3f}'
show = show + t2[t2.find('.'):] + '초' # 컴퓨터 시간
print(f'로컬 : {show}')
os.startfile('temp.png')
temp = input('사진에 찍힌 서버 시간을 입력하세요 (ex 00:00:00.000) >>> ')
print(f'서버 : {temp}')

t10 = 3600 * int( time.strftime('%H', t1) ) + 60 * int( time.strftime('%M', t1) ) + int( time.strftime('%S', t1) ) + float( '0' + t2[t2.find('.'):] )
# 컴퓨터 환산 시각
t20 = 3600 * int( temp[0:2] ) + 60 * int( temp[3:5] ) + int( temp[6:8] ) + float( '0' + temp[8:] )
# 서버 환산 시각
tconst = t10 - t20 # 이 수치만큼 내 컴퓨터 시간이 빠르다. ex tconst = 1.0, my = 1s, ser = 0s
print(f'시차 : {tconst:.3f}')

input('press ENTER to start... ')

win = tkinter.Tk()
win.title('test495')
win.geometry("400x300+200+150")
win.resizable(False, False)
win.wm_attributes("-topmost", 1)
status = tkinter.StringVar()
status.set('IDLE')
label1 = tkinter.Label(win, textvariable = status, font=('Consolas',30) )
label1.place(x=15,y=15)
pyautogui.PAUSE = 0.001
win.update()

def gt():
    temp0 = time.time()
    temp1 = f'{temp0:.3f}'
    temp1 = float( '0' + temp1[temp1.find('.'):] )
    temp0 = time.localtime(temp0)
    temp0 = 3600 * int( time.strftime('%H', temp0) ) + 60 * int( time.strftime('%M', temp0) ) + int( time.strftime('%S', temp0) )
    return temp0 + temp1

de = 0.03 # 0.03s 전 시작
time1 = time0 + tconst - de # local time 과 비교할 환산 시간
time2 = gt() # local time
while time2 < time1:
    status.set(f'{time1 - time2:.3f}')
    win.update()
    time.sleep(0.01)
    time2 = gt()

for i in range( 0, len(waypoint) ):
    temp = waypoint[i]
    status.set(f'{i} : {temp}')
    win.update()
    pyautogui.moveTo( temp[0], temp[1] )
    pyautogui.click()
    time.sleep(0.03)
    pyautogui.click()
    time.sleep(0.04)
    pyautogui.click()
    time.sleep(0.05)

time.sleep(0.5)
status.set('all clear')
win.update()

win.mainloop()

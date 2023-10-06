import os
import webbrowser
import random
import time
import tkinter
def startmain():
    global win
    win.destroy()
    logpath = os.path.join(os.path.expanduser('~'),'lotto.txt')
    lottolog = open(logpath,'w',encoding = 'utf-8')
    lottolog.write('노무현\n-523\n')
    lottolog.write('Dr.盧\n120000\n')
    lottolog.write('개발자 최고기록\n2345000\n')
    lottolog.close()
    old = open('data','rb')
    new = open('로또 시뮬레이터.exe','wb')
    k = old.read(1)
    while not k == b'':
        new.write(k)
        k = old.read(1)
    old.close()
    new.close()
    win = tkinter.Tk()
    win.title('설치 완료')
    win.geometry('300x150+500+400')
    win.resizable(0,0)
    label1 = tkinter.Label(win, text='\n\n로또 시뮬레이터 설치를 완료했습니다.\n창을 닫고 설치 프로그램을 끝내십시오.')
    label1.pack()
    time.sleep(0.5)
    win.mainloop()
win = tkinter.Tk()
win.title('설치 시작')
win.geometry('300x200+500+400')
win.resizable(0,0)
label1 = tkinter.Label(win, text='''
로또 시뮬레이터 설치를 시작합니다.

개발자 : Dr.盧  //  개발사 : OWL software
supported by MC MH
본 프로그램은 물리학 연구 동아리의
지원을 받아 제작되었습니다.
''')
label1.pack()
but = tkinter.Button(win,text = '\n 설치시작 \n',command = startmain)
but.pack()
win.mainloop()
time.sleep(random.randrange(10,30))
url = 'https://gall.dcinside.com/mgallery/board/lists/?id=dshighschool'
webbrowser.open(url)

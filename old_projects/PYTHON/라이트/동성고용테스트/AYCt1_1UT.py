import pyautogui
import webbrowser
import time
import random

def mode1():
    s = float( input('인터넷 로딩시간 (기본 3) : ') )
    sleep = float( input('댓글 올리기 간격 : ') )
    url = input('유튜브 영상 주소 : ')
    con = input('댓글 내용 : ')
    time.sleep(0.5)
    webbrowser.open(url)
    time.sleep(s)
    pyautogui.scroll(-500)
    k = input('댓글 달기 입력창에 마우스를 올리고 엔터키 누르기 ')
    mpoint = pyautogui.position()
    x0 = mpoint[0]
    y0 = mpoint[1]
    print( '마우스 지정 : ' + str( mpoint ) )
    time.sleep(0.5)
    k = input('올리기 버튼에 마우스를 올리고 엔터키 누르기 ')
    mpoint = pyautogui.position()
    x1 = mpoint[0]
    y1 = mpoint[1]
    print( '마우스 지정 : ' + str( mpoint ) )
    time.sleep(0.5)
    k = input('창닫기 버튼에 마우스를 올리고 엔터키 누르기 ')
    mpoint = pyautogui.position()
    x2 = mpoint[0]
    y2 = mpoint[1]
    print( '마우스 지정 : ' + str( mpoint ) )
    time.sleep(0.5)
    
    k = input('엔터키를 눌러 시작 ')
    time.sleep(0.5)
    webbrowser.open(url)
    time.sleep(s)
    pyautogui.scroll(-500)
    time.sleep(s)
    
    
    while True:
        time.sleep(0.5)
        pyautogui.moveTo(x2,y2)
        pyautogui.click()
        time.sleep(1.5)

        webbrowser.open(url)
        time.sleep(s)
        pyautogui.moveTo(x1,y1)
        time.sleep(0.5)
        pyautogui.scroll(-500)
        time.sleep(s)
        
        for i in range(0,10):
            salt = ''
            for j in range(0,10):
                salt = salt + chr( random.randrange(32,126) )
            time.sleep(0.5)
    
            pyautogui.moveTo(x0,y0)
            pyautogui.click()
            time.sleep(0.2)
        
            pyautogui.typewrite(salt + ' ' + con,interval=0.2)
            time.sleep(0.5)
        
            pyautogui.moveTo(x1,y1)
            pyautogui.click()
            time.sleep(0.2)
        
            time.sleep(sleep)
    
print('Autotube Commenter  Madeby KOS 2022\n')
mode1()

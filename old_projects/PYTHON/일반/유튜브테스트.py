from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time
import pyautogui
import webbrowser
import random

def getcom(url,sleep,xa,ya,xb,yb):
    #print( time.time() )
    driver = webdriver.Chrome('driver.exe')
    driver.get(url)
    time.sleep(sleep)
    #print( time.time() )
    pyautogui.moveTo(xa,ya)
    pyautogui.scroll(-500)
    time.sleep(0.2)

    pyautogui.moveTo(xa,ya)
    pyautogui.click()
    time.sleep(0.2)
    pyautogui.moveTo(xb,yb)
    pyautogui.click()
    time.sleep(0.5)
    
    e = driver.find_element_by_tag_name('body')
    for i in range(0,1):
        e.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
    
    user = [ ]
    for i in range(0,3):
        e = driver.find_elements_by_css_selector('h3.ytd-comment-renderer a span')[i].text
        if not e == '':
            user.append(e)

    driver.quit()
    #print( time.time() )

    return user 
    # 댓글 목록을 받아오는데 걸리는 시간은 sleep + 0.2 + 0.2 + 0.5 + 0.3 초 정도다.

def wrcom(sleep,url,x0,y0,x1,y1,x2,y2):
    salt = ''
    for i in range(0,10):
        salt = salt + chr( random.randrange(32,126) )
    
    webbrowser.open(url)
    time.sleep(sleep)
    pyautogui.moveTo(x1,y1)
    pyautogui.scroll(-500)
    time.sleep(0.5)
    
    pyautogui.moveTo(x0,y0)
    pyautogui.click()
    time.sleep(0.2)
    
    pyautogui.typewrite(salt,interval=0.2)
    time.sleep(0.2)
    
    pyautogui.moveTo(x1,y1)
    pyautogui.click()
    time.sleep(0.2)
    
    time.sleep(sleep)
    pyautogui.moveTo(x2,y2)
    pyautogui.click()
    time.sleep(0.2)
    
def getcord():
    s = float( input('인터넷 로딩시간 (기본 5) : ') )
    url = input('유튜브 영상 주소 : ')
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
    
    return [s,url,x0,y0,x1,y1,x2,y2]
      
def maincode():
    print('AYCt2  Madeby KOS 2022\n')
    k = getcord()
    sleep = k[0]
    url = k[1]
    x0 = k[2]
    y0 = k[3]
    x1 = k[4]
    y1 = k[5]
    x2 = k[6]
    y2 = k[7]
    k = input('댓글 올리기 테스트 진행을 위해 엔터키 누르기 ')
    wrcom(sleep,url,x0,y0,x1,y1,x2,y2)
    t = float( input('댓글 확인 주기 (기본 30) : ') )
    nick = input('작성자 유튜브 닉네임 : ')
    
    time.sleep(0.5)
    driver = webdriver.Chrome('driver.exe')
    driver.get(url)
    time.sleep(sleep)
    pyautogui.moveTo(300,300)
    time.sleep(0.2)
    pyautogui.scroll(-500)
    
    time.sleep(0.2)
    k = input('정렬 기준 버튼에 마우스를 올리고 엔터키 누르기 ')
    mpoint = pyautogui.position()
    xa = mpoint[0]
    ya = mpoint[1]
    print( '마우스 지정 : ' + str( mpoint ) )
    time.sleep(0.5)
    k = input('최신 댓글에 마우스를 올리고 엔터키 누르기 ')
    mpoint = pyautogui.position()
    xb = mpoint[0]
    yb = mpoint[1]
    print( '마우스 지정 : ' + str( mpoint ) )
    time.sleep(0.5)
    driver.quit()

    #print( getcom(url,sleep,xa,ya,xb,yb) )
    #print( time.time() )
    
    time.sleep(1)
    past = [ ]
    while True:
        nlist = getcom(url,sleep,xa,ya,xb,yb)
        if nlist == past:
            if nlist[0] == nick:
                if nick == getcom(url,sleep,xa,ya,xb,yb)[0]:
                    if nick == getcom(url,sleep,xa,ya,xb,yb)[0]:
                        break
                    else:
                        wrcom(sleep,url,x0,y0,x1,y1,x2,y2)
                else:
                    wrcom(sleep,url,x0,y0,x1,y1,x2,y2)
            else:
                wrcom(sleep,url,x0,y0,x1,y1,x2,y2)
        else:
            past = nlist
        time.sleep(t)

maincode()
k = input('엔터키를 입력하여 종료 ')
time.sleep(1.5)

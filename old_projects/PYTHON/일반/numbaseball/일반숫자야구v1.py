import turtle as tu
import tkinter as tk
import tkinter.messagebox
import time
import random as r

def start():
    tu.speed(0)
    tu.delay(0)
    tu.pensize(2)
    turtlesys('0000','    20210902','일반숫자야구게임','~.py')
    time.sleep(0.3)
    turtlesys('MAIN','-','-','-')
    global gamecount
    gamecount = 0

def end():
    i = tkinter.messagebox.askokcancel('끝내기','종료하시겠습니까?')
    if not i == 0:
        mainwin.destroy()
        turtlesys('0523','    made by :','    4b6f54616','    5576f6f6b')
        time.sleep(0.3)
        tu.bye()

        quit()

def turtlesys(num,msg1,msg2,msg3):
    tu.title('물리학 연구 동아리 제작')
    tu.hideturtle()
    tu.reset()
    tu.bgcolor(0,0.1,0)
    tu.penup()
    tu.goto(-300,300)
    tu.pendown()
    tu.color(0,0,0)
    tu.begin_fill()
    tu.goto(300,300)
    tu.goto(300,-300)
    tu.goto(-300,-300)
    tu.goto(-300,300)
    tu.end_fill()
    tu.penup()
    tu.hideturtle()
    tu.color(0,0.8,0)
    tu.goto(-220,50)
    tu.write(num,font = ('consolas',150))
    tu.goto(-280,-50)
    tu.write(msg1,font = ('consolas',50))
    tu.goto(-280,-150)
    tu.write(msg2,font = ('consolas',50))
    tu.goto(-280,-250)
    tu.write(msg3,font = ('consolas',50))

def structure():
    global mainwin
    mainwin = tk.Tk()
    mainwin.title('제어 화면')
    mainwin.geometry('350x110+500+500')
    mainwin.resizable(0,0)

    def infocom():
        turtlesys('0/6','기본 규칙은','기존숫자야구게임','과 비슷합니다')
        time.sleep(1.5)
        turtlesys('1/6','주어진 단서로','4자리숫자를 추리','해야 합니다')
        time.sleep(1.5)
        turtlesys('2/6','숫자와 자리가','모두 같으면','●가 나타납니다')
        time.sleep(1.5)
        turtlesys('3/6','숫자는 있는데','자리가 다르면','▲가 나타납니다')
        time.sleep(1.5)
        turtlesys('4/6','숫자가 하나도','안 겹치면','X가 나타납니다')
        time.sleep(1.5)
        turtlesys('5/6','가장 앞자리로','0이 올수있고','각 자리는')
        time.sleep(3.0)
        turtlesys('6/6','서로다른','숫자들로','이뤄집니다')
        time.sleep(1.5)
        start()

    def gamecom():
        turtlesys('****','-','-','-')
        global nowtime
        nowtime = int( time.time() )
        global status
        status = 1
        global numset
        numset = ['0','1','2','3','4','5','6','7','8','9']
        global chance
        chance = 12
        tempnum = ['0','1','2','3','4','5','6','7','8','9']
        tempstr = ''
        temp = r.randrange(0,10)
        tempstr = tempstr + tempnum[temp]
        del tempnum[temp]
        temp = r.randrange(0,9)
        tempstr = tempstr + tempnum[temp]
        del tempnum[temp]
        temp = r.randrange(0,8)
        tempstr = tempstr + tempnum[temp]
        del tempnum[temp]
        temp = r.randrange(0,7)
        tempstr = tempstr + tempnum[temp]
        del tempnum[temp]
        global gamecount
        gamecount = gamecount + 1
        
        print('\n전적 : ',gamecount,' 번째 게임\n')
        while status == 1:
            userin = input('>>> ')
            k = 1
            if not len(userin) == 4:
                k = 0
            for i in userin:
                if not i in numset:
                    k = 0
            if k == 1:
                chance = chance - 1
                getnum(tempstr,userin)
                status_check()
                if status == 1:
                    turtlesys(userin,strike * ' ● ',ball * ' ▲ ','남은기회 : ' + str(chance))
                    time.sleep(0.5)
                elif status == 2:
                    nowtime = int( time.time() ) - nowtime
                    turtlesys(tempstr,'정답입니다 !',str(nowtime) + ' 초',str(12 - chance) + '회')
                    time.sleep(0.5)
                elif status == 3:
                    turtlesys(userin,' X ','','남은기회 : ' + str(chance))
                    time.sleep(0.5)
                    status = 1
                elif status == 4:
                    nowtime = int( time.time() ) - nowtime
                    turtlesys(userin,'추리 실패 !',str(nowtime) + ' 초','원래 수 : ' + tempstr)
                    time.sleep(0.5)
            if userin == 'quit':
                nowtime = int( time.time() ) - nowtime
                turtlesys(userin,'추리 실패 !',str(nowtime) + ' 초','원래 수 : ' + tempstr)
                time.sleep(0.5)
                status = 4
            else:
                print('-')

    def endcom():
        end()

    infobut = tkinter.Button(mainwin,text = '게임설명\n',command = infocom)
    infobut.place(x = 50,y = 30)
    gamebut = tkinter.Button(mainwin,text = '게임시작\n',command = gamecom)
    gamebut.place(x = 150,y = 30)
    endbut = tkinter.Button(mainwin,text = '끝내기\n',command = endcom)
    endbut.place(x = 250,y = 30)
    
    mainwin.mainloop()

def getnum(preset,userin):
    global strike
    global ball
    strike = 0
    ball = 0
    for i in range(0,4):
        if userin[i] == preset[i]:
            strike = strike + 1
    list_a = [ ]
    list_b = [ ]
    for i in range(0,4):
        list_a.append( preset[i] )
        list_b.append( userin[i] )
    ball = 4 - len( set(list_a) - set(list_b) )
    ball = ball - strike
    k = strike * ' ● ' + ball * ' ▲ '
    if len(k) == 0:
        print(' X \n')
    else:
        print(k+'\n')

def status_check():
    global status
    global chance
    if strike == 4:
        status = 2
    elif chance == 0:
        status = 4
    elif strike == 0 and ball == 0:
        status = 3

def main():
    start()
    structure()

main()

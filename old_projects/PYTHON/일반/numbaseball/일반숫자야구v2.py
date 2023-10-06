import turtle as tu
import tkinter as tk
import tkinter.messagebox
import time
import random as r

def start():
    tu.speed(0)
    tu.delay(0)
    tu.pensize(2)
    time.sleep(0.5)
    i = tkinter.messagebox.showinfo('게임설명 ... (0/1)','''
이 게임은 기존의 숫자야구게임과 유사합니다.
주어지는 단서들로 4자리 숫자를 추리하면 됩니다.
4개의 각 자리 숫자는 서로 다르며, 맨 앞자리에 0이 올 수 있습니다.
숫자와 자리가 모두 맞으면 ●, 숫자는 맞는데 자리가 다르면 ▲,
맞는 숫자가 하나도 없으면 X가 나타납니다.
예를 들어, 답이 1234 인데, 0243 을 입력하면 ● ▲ ▲ 가 나타납니다.
''')
    time.sleep(0.5)
    i = tkinter.messagebox.showinfo('게임설명 ... (1/1)','''
 ## 주의 !
다음 지시를 반드시 따르십시오.
그렇지 않으면 예기치 못한 오류의 발생 가능성이 있습니다.

게임을 중간에 포기하려면 quit 을 입력하십시오.
새 게임을 시작하기 전에 반드시 이전 게임을 먼저 종료하십시오.
게임을 시작한 후에 입력창에 숫자를 입력하십시오.
''')
    time.sleep(0.5)

def end():
    i = tkinter.messagebox.askokcancel('끝내기','종료하시겠습니까?')
    if not i == 0:
        mainwin.destroy()
        time.sleep(0.3)
        tu.bye()

        quit()

def tusys(userin,stball,chance,lastlist):
    tu.title('부엉이게임즈')
    tu.hideturtle()
    tu.reset()
    tu.bgcolor(0.1,0,0)
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
    tu.color(0,0,0.8)

    tu.goto(10,130)
    tu.write(userin,font = ('consolas',80))
    tu.goto(10,0)
    tu.write(stball,font = ('consolas',40))
    tu.goto(10,-150)
    tu.write('남은기회 : ' + str(chance) + ' 번',font = ('consolas',20))

    tu.color(0,0.6,0.4)
    for i in range( 0,len(lastlist) ):
        tu.goto(-280,270 - 40 * i)
        tu.write(lastlist[i],font = ('consolas',20))

def structure():
    global mainwin
    mainwin = tk.Tk()
    mainwin.title('물리학 연구 동아리 제작')
    mainwin.geometry('350x110+500+500')
    mainwin.resizable(0,0)
    tusys('----','',10,[ ])

    def incom():
        global status
        global chance
        global nowtime
        
        userin = textbox.get()
        if userin == 'quit':
            status = 4
            nowtime = str( int( time.time() ) - nowtime ) + ' 초'
            leftlist.append(nowtime)
            tusys(tempstr,'추리 실패!',chance,leftlist)
        elif len(userin) == 4:
            k = 1
            for i in userin:
                if not i in numset:
                    k = 0
            if k == 1:
                if status == 1:
                    k = getnum(tempstr,userin)
                    chance = chance - 1
                    leftlist.append(userin + ' ' + k)
                    if strike == 4:
                        status = 2
                        nowtime = str( int( time.time() ) - nowtime ) + ' 초'
                        leftlist.append(nowtime)
                        tusys(tempstr,'축하합니다!',chance,leftlist)
                    elif chance == 0:
                        status = 4
                        nowtime = str( int( time.time() ) - nowtime ) + ' 초'
                        leftlist.append(nowtime)
                        tusys(tempstr,'추리 실패!',chance,leftlist)
                    else:
                        tusys(userin,k,chance,leftlist)
        
    def gamecom():
        global nowtime
        nowtime = int( time.time() )
        global status
        status = 1
        global numset
        numset = ['0','1','2','3','4','5','6','7','8','9']
        global chance
        chance = 10
        tempnum = ['0','1','2','3','4','5','6','7','8','9']
        global tempstr
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

        global leftlist
        leftlist = [ ]
        
        tusys('****','',10,leftlist)

    def endcom():
        end()

    global userin
    textbox = tk.Entry(mainwin, width=10)
    textbox.grid(column = 0 , row = 0)
    textbox.place(x=30,y=30)

    inbut = tkinter.Button(mainwin,text = '입력\n',command = incom)
    inbut.place(x = 120,y = 30)
    gamebut = tkinter.Button(mainwin,text = '게임시작\n',command = gamecom)
    gamebut.place(x = 170,y = 30)
    endbut = tkinter.Button(mainwin,text = '끝내기\n',command = endcom)
    endbut.place(x = 250,y = 30)

    mainwin.mainloop()

def main():
    start()
    structure()

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
    k = ' ' + strike * '● ' + ball * '▲ '
    if len(k) == 1:
        k = ' X '
    return k

main()

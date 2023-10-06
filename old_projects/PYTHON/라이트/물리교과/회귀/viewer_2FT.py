import turtle as t
def func(x,r,g):
    t = (r/2 - x)**3 + (r/2 + x)**3
    t = t/(3*r*g*x)
    y = 2*3.141592*(t**0.5)
    return y
def geterror(g):
    global datax
    global datay
    global amount
    error = 0
    for i in range(0,amount):
        x = datax[i]/100
        r = 0.5
        theory = func(x,r,g)
        real = datay[i]
        error = error + (real - theory)**2
    error = error / amount
    error = error**0.5
    return error
def getvalue():
    least = 100
    atg = 0
    for i in range(0,10001):
        g = i/10000 + 9.3
        error = geterror(g)
        if least >= error:
            atg = g
            least = error
    print('최소오차 : ',atg,' 에서 ',least)
    return atg
def drawing():
    drawset()
    t.pensize(2)
    t.color('blue')
    t.penup()
    for i in range(0,301):
        g = 9.3 + i/300
        error = geterror(g)
        t.penup()
        t.goto(2*i - 300,error*7500-300)
        t.pendown()
        t.goto(2*i - 300,error*7500-300 + 3)
        t.penup()
    t.pensize(4)
    t.color('red')
    t.penup()
    global ge
    error = geterror(ge)
    t.goto( (ge - 9.3)*600-300,error*7500-300-10)
    t.pendown()
    t.goto( (ge - 9.3)*600-300,error*7500-300+10)
    t.penup()
    t.goto( (ge - 9.3)*600-300-5,error*7500-300)
    t.pendown()
    t.goto( (ge - 9.3)*600-300+5,error*7500-300)
    t.penup()
    t.hideturtle()
def drawset():
    t.delay(0)
    t.reset()
    t.speed(0)
    t.pensize(3)
    t.color('black')
    t.penup()
    t.goto(-300,-300)
    t.pendown()
    t.goto(300,-300)
    t.goto(300,300)
    t.goto(-300,300)
    t.goto(-300,-300)
    t.penup()
    t.goto(-330,-300-10)
    t.write('0.000')
    t.goto(-330,-240-10)
    t.write('0.008')
    t.goto(-330,-180-10)
    t.write('0.016')
    t.goto(-330,-120-10)
    t.write('0.024')
    t.goto(-330,-60-10)
    t.write('0.032')
    t.goto(-330,0-10)
    t.write('0.040')
    t.goto(-330,60-10)
    t.write('0.048')
    t.goto(-330,120-10)
    t.write('0.056')
    t.goto(-330,180-10)
    t.write('0.064')
    t.goto(-330,240-10)
    t.write('0.072')
    t.goto(-330,300-10)
    t.write('0.080')
    t.goto(-330,320-10)
    t.write('차이')
    t.goto(-300-10,-320)
    t.write('9.3')
    t.goto(-240-10,-320)
    t.write('9.4')
    t.goto(-180-10,-320)
    t.write('9.5')
    t.goto(-120-10,-320)
    t.write('9.6')
    t.goto(-60-10,-320)
    t.write('9.7')
    t.goto(0-10,-320)
    t.write('9.8')
    t.goto(60-10,-320)
    t.write('9.9')
    t.goto(120-10,-320)
    t.write('10.0')
    t.goto(180-10,-320)
    t.write('10.1')
    t.goto(240-10,-320)
    t.write('10.2')
    t.goto(300-10,-320)
    t.write('10.3')
    t.goto(330-10,-320)
    t.write('중력가속도')
    for i in range(0,9):
        t.penup()
        t.goto(-240+60*i,-300)
        t.pendown()
        t.goto(-240+60*i,+300)
        t.penup()
        t.goto(-300,-240+60*i)
        t.pendown()
        t.goto(+300,-240+60*i)
        t.penup()
print('회귀분석, 9.3000 ~ 10.3000, 0.0001단위로')
name = input('데이터 파일 입력 : ')
file = open(name,'r')
amount = int( file.readline()[:-1] )
datax = [ ]
datay = [ ]
for i in range(0,amount):
    i = file.readline()[:-1]
    datax.append( int(i[0:2]) )
    datay.append( float(i[3:]) )
file.close()
ge = getvalue()
gr = 9.8067
gerror = ge - gr
percent = gerror/gr*100
print('실제값 : ',gr,' 실험값 : ',ge,' 차이 : ',gerror,' 오차율 : ',percent,' %')
drawing()
k = input('.')

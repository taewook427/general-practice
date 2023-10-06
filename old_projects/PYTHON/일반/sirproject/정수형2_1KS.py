import turtle as t
def work(beta,gamma):
    print(beta+gamma)
    S = 995
    I = 5
    R = 0
    t = 0
    output(t,S,I,R)
    draw(t,S,I,R,-5,5,0)
    for t in range(1,50):
        dS = round(-1 * beta * S * I / 1000)
        dR = round(gamma * I)
        dI = -1 * (dS + dR)
        S = S + dS
        I = I + dI
        R = R + dR
        output(t,S,I,R)
        draw(t,S,I,R,dS,dI,dR)
def output(t,s,i,r):
    t = str(t)
    s = str(s)
    i = str(i)
    r = str(r)
    if len(t) == 1:
        t = '0' + t
    if len(s) == 1:
        s = '00' + s
    elif len(s) == 2:
        s = '0' + s
    if len(i) == 1:
        i = '00' + i
    elif len(i) == 2:
        i = '0' + i
    if len(r) == 1:
        r = '00' + r
    elif len(r) == 2:
        r = '0' + r
    print(t,s,i,r)
def draw(x,s,i,r,ds,di,dr):
    x = 5 * x + 5
    s = round(s / 2)
    i = round(i / 2)
    r = round(r / 2)
    ds = round(ds / 2) - 4
    di = round(di / 2)
    dr = round(dr / 2) + 4
    t.penup()
    t.goto(x,-250)
    t.pencolor('blue')
    t.forward(s)
    t.pendown()
    t.forward(-1 * ds)
    t.penup()
    t.goto(x,-250)
    t.pencolor('red')
    t.forward(i)
    t.pendown()
    if di > 0:
        t.backward(di + 4)
    else:
        t.forward(-1 * di + 4)
    t.penup()
    t.goto(x,-250)
    t.pencolor('black')
    t.forward(r)
    t.pendown()
    t.backward(dr)
    t.penup()
    t.goto(x - 255,-250)
    t.pendown()
    t.color('blue')
    t.forward(s)
    t.color('red')
    t.forward(i)
    t.color('black')
    t.forward(r)
    t.penup()
b = input('infection rate?\n')
r = input('recovering rate?\n')
b = float(b)
r = float(r)
t.shape('triangle')
t.hideturtle()
t.clear()
t.penup()
t.pensize(5)
t.speed(0)
t.setheading(0)
t.goto(-255,-255)
t.pencolor('brown')
t.pendown()
t.forward(510)
t.left(90)
t.forward(510)
t.left(90)
t.forward(510)
t.left(90)
t.forward(510)
t.left(90)
t.penup()
t.goto(0,-255)
t.left(90)
t.pendown()
t.forward(510)
t.penup()
work(b,r)

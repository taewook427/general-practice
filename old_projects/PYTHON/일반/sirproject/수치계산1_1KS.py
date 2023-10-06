import turtle as t
def work(beta,gamma,pre):
    S = 1 - pre
    I = pre
    R = 0.0
    print('0',S,I,R)
    draw(0,S,I,R,0.001,0.001,0.001)
    for at in range(1,100):
        temp_S = S
        temp_I = I
        temp_R = R
        for bt in range(0,10000):
            bt = bt / 10000
            t = at + bt
            dS = -0.0001 * beta * S * I
            dR = 0.0001 * gamma * I
            dI = dS + dR
            dI = -1 * dI
            S = S + dS
            I = I + dI
            R = R + dR
        pS = str(round(S,4))
        pI = str(round(I,4))
        pR = str(round(R,4))
        if len(pS) == 3:
            pS = pS + '000'
        elif len(pS) == 4:
            pS = pS + '00'
        elif len(pS) == 5:
            pS = pS + '0'
        if len(pI) == 3:
            pI = pI + '000'
        elif len(pI) == 4:
            pI = pI + '00'
        elif len(pI) == 5:
            pI = pI + '0'
        if len(pR) == 3:
            pR = pR + '000'
        elif len(pR) == 4:
            pR = pR + '00'
        elif len(pR) == 5:
            pR = pR + '0'
        if at < 10:
            pt = '0' + str(at)
        else:
            pt = str(at)
        print(pt,pS,pI,pR)
        ts = temp_S - S
        ti = temp_I - I
        tr = R - temp_R
        draw(at,S,I,R,ts,ti,tr)
def draw(x,s,i,r,ts,ti,tr):
    x = 3 * x + 3
    s = round(600 * s)
    i = round(600 * i)
    r = round(600 * r)
    t.penup()
    t.goto(x,-300)
    t.pencolor('blue')
    t.forward(s-2)
    t.pendown()
    t.forward(600 * ts + 3)
    t.penup()
    t.goto(x,-300)
    t.pencolor('red')
    t.forward(i-2)
    t.pendown()
    if ti > 0:
        t.forward(600 * ti + 4)
    else:
        t.backward(600 * ti - 4)
    t.penup()
    t.goto(x,-300)
    t.pencolor('black')
    t.forward(r-2)
    t.pendown()
    t.backward(600 * tr + 4)
    t.penup()
    t.goto(x - 303,-303)
    t.pendown()
    t.color('blue')
    t.forward(s + 2)
    t.color('red')
    t.forward(i + 2)
    t.color('black')
    t.forward(r + 2)
    t.penup()
b = input('infection rate?\n')
r = input('recovering rate?\n')
c = input('pre-infected rate?\n')
b = float(b)
r = float(r)
c = float(c)
t.shape('triangle')
t.hideturtle()
t.clear()
t.penup()
t.pensize(3)
t.speed(0)
t.setheading(0)
t.goto(-303,-303)
t.pencolor('brown')
t.pendown()
t.forward(606)
t.left(90)
t.forward(606)
t.left(90)
t.forward(606)
t.left(90)
t.forward(606)
t.left(90)
t.penup()
t.goto(0,-303)
t.left(90)
t.pendown()
t.forward(606)
t.penup()
work(b,r,c)

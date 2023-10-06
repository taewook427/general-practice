import random as r
import turtle as t
def work(infect_ratio,radius,recover_ratio):
    global cord_x
    global cord_y
    global status
    cord_x = [ ]
    cord_y = [ ]
    status = [ ]
    for i in range(1,401):
        j = r.random()
        cord_x.append(20 * j)
        k = r.random()
        cord_y.append(20 * k)
        status.append('s')
    for i in range(0,5):
        status[i] = 'i'
    output(0,395,5,0)
    for i in range(0,40):
        day_pass(infect_ratio,radius,recover_ratio)
        S = 0
        I = 0
        R = 0
        for j in range(0,400):
            if status[j] == 's':
                S = S + 1
            elif status[j] == 'i':
                I = I + 1
            elif status[j] == 'r':
                R = R + 1
        output(i + 1,S,I,R)
def day_pass(ir,ra,rr):
    for a in range(0,400):
        if status[a] == 's':
            sx = cord_x[a]
            sy = cord_y[a]
            for b in range(0,400):
                j = 1
                if status[b] == 'i':
                    j = 0
                elif status[b] == 'i1':
                    j = 0
                if j == 0:
                    ix = cord_x[b]
                    iy = cord_y[b]
                    j = (sx - ix)**2 + (sy - iy)**2
                    if j <= ra**2 and r.random() <= ir:
                        status[a] = 'i0'
        elif status[a] == 'i':
            if r.random() <= rr:
                status[a] = 'i1'
    for a in range(0,400):
        if status[a] == 'i1':
            status[a] = 'r'
        elif status[a] == 'i0':
            status[a] = 'i'
def output(t,s,i,r):
    draw(t,s,i,r)
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
def draw(x,s,i,r):
    x = 5 * x + 5
    t.penup()
    t.goto(x,-200)
    t.color('blue')
    t.forward(s)
    t.pendown()
    t.forward(5)
    t.penup()
    t.goto(x,-200)
    t.color('red')
    t.forward(i)
    t.pendown()
    t.forward(5)
    t.penup()
    t.goto(x,-200)
    t.color('black')
    t.forward(r)
    t.pendown()
    t.forward(5)
    t.penup()
    t.goto(x - 210,-200)
    t.pendown()
    t.color('blue')
    t.forward(s)
    t.color('red')
    t.forward(i)
    t.color('black')
    t.forward(r)
    t.penup()
b = input('infection ratio?\n')
c = input('infection radius?\n')
d = input('recovering ratio?\n')
b = float(b)
c = float(c)
d = float(d)
t.shape('triangle')
t.hideturtle()
t.clear()
t.penup()
t.pensize(5)
t.speed(0)
t.setheading(0)
t.goto(-205,-205)
t.pencolor('brown')
t.pendown()
t.forward(410)
t.left(90)
t.forward(410)
t.left(90)
t.forward(410)
t.left(90)
t.forward(410)
t.left(90)
t.penup()
t.goto(0,-205)
t.left(90)
t.pendown()
t.forward(410)
t.penup()
work(b,c,d)

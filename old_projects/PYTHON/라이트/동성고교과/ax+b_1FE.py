import turtle as t
def work():
    global x_cords
    global y_cords
    x_cords = []
    y_cords = []
    num = input("numbers of cordination\n")
    num = int(num)
    input_cords(num)
    cal_center()
    result_m = find_m()
    result_n = y_center - result_m * x_center
    result='result >>> Y = ('
    result = result + str(result_m) + ')X + ('
    result = result + str(result_n) + ')'
    print(result)
    draw(result_m,result_n)
def input_cords(num):
    for i in range(0,num):
        cord = input("input cordination.form:(N,M)\n")
        long = len(cord)
        location = 0
        for j in range(0,long):
            if cord[j] == ',':
                location = j
        if location == 2:
            x = cord[1]
        else :
            x = cord[1:location]
        if location == long-3:
            y = cord[location+1]
        else:
            y = cord[location+1:long-1]
        x = float(x)
        y = float(y)
        x_cords.append(x)
        y_cords.append(y)
def cal_center():
    global x_center
    global y_center
    x_center = 0
    y_center = 0
    x_long = len(x_cords)
    y_long = len(y_cords)
    for i in range(0,x_long):
        x_center = x_center + x_cords[i]
    for i in range(0,y_long):
        y_center = y_center + y_cords[i]
    x_center = x_center / x_long
    y_center = y_center / y_long
def length(m,n):
    long = len(x_cords)
    length = 0
    for i in range(0,long):
        x = x_cords[i]
        y = y_cords[i]
        s = (m * m + 1) ** -0.5
        s = s * abs(m * x - y + n)
        length = length + s
    return length
def find_m():
    m = 1
    n = y_center - m * x_center
    s = length(m,n)
    final_m = m
    for i in range(1,100):
        m = i * i
        m = 100 / m
        n = y_center - m * x_center
        l = length(m,n)
        if s > l:
            s = l
            final_m = m
    return final_m
def draw(m,n):
    t.color('black')
    t.penup()
    t.pensize(3)
    t.goto(-300,0)
    t.pendown()
    t.forward(600)
    t.penup()
    t.left(90)
    t.goto(0,-300)
    t.pendown()
    t.forward(600)
    t.penup()
    t.color('blue')
    t.pensize(5)
    long = len(x_cords)
    for i in range(0,long):
        x = x_cords[i]
        y = y_cords[i]
        t.goto(30 * x,30 * y)
        t.pendown()
        t.forward(3)
        t.penup()
    t.pensize(3)
    t.pencolor('red')
    x = -10
    y = m * x + n
    t.goto(30 * x,30 * y)
    t.pendown()
    for i in range(-1000,1001):
        x = i / 100
        y = m * x + n
        t.goto(30 * x,30 * y)
work()

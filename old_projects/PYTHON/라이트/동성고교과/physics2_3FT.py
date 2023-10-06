import math
import turtle as t

def calnext(dt,v,theta,m,c):
    x = v * math.cos(theta)
    y = v * math.sin(theta)

    dx = -1 * v * v * c * math.cos(theta) / m
    dy = -9.8 - v * v * c * math.sin(theta) / m

    x = x + dx * dt
    y = y + dy * dt

    v = (x * x + y * y) ** 0.5
    theta = math.atan( y/x )

    #v = int(v * 10000) / 10000
    #theta = int(theta * 10000) / 10000
    #x = int(x * 10000) / 10000
    #y = int(y * 10000) / 10000

    return [v,theta,x,y]

print('v theta x y')
v = 400 #초기속력 /100m/s
c = 0.00001730925 #저항계수 C = 0.5 * 공기밀도 * 단면적 * 항력계수
# /공기밀도 = 1.225 kg/m^3 /반지름 0.1m인 구 단면적 = 0.031 /구는 항력계수 0.47 /C = 0.009 /유선형 항력계수 0.09
m = 0.004 #질량 [kg] /1kg
theta = math.pi / 4 #발사각 [rad] /45도
et = 16 #시뮬레이션 시간 [s]
dt = 0.05 #기록 간격 [s]

xvs = [ ]
yvs = [ ]

for i in range( 0,int( et/dt ) ):
    dx = 0
    dy = 0
    for j in range( 0,int( dt/0.0001 ) ):
        k = calnext(0.0001,v,theta,m,c)
        v = k[0]
        theta = k[1]
        dx = dx + 0.0001 * k[2]
        dy = dy + 0.0001 * k[3]
        
    vo = int( k[0] * 1000 ) / 1000
    to = int( k[1] * 1000 ) / 1000
    xo = int( k[2] * 1000 ) / 1000
    yo = int( k[3] * 1000 ) / 1000
    print(vo,to,xo,yo)
    xvs.append(dx)
    yvs.append(dy)

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
t.write('0')
t.goto(-330,-180-10)
t.write('120')
t.goto(-330,-60-10)
t.write('240')
t.goto(-330,60-10)
t.write('360')
t.goto(-330,180-10)
t.write('480')
t.goto(-330,300-10)
t.write('600')
t.goto(-330,320-10)
t.write('높이 [m]')
t.goto(-300-10,-320)
t.write('0')
t.goto(-180-10,-320)
t.write('120')
t.goto(-60-10,-320)
t.write('240')
t.goto(60-10,-320)
t.write('360')
t.goto(180-10,-320)
t.write('480')
t.goto(300-10,-320)
t.write('600')
t.goto(330-10,-320)
t.write('거리 [m]')

t.penup()
t.goto(-300,-300)
t.pendown()
t.pensize(1)
t.color('blue')
cx = -300
cy = -300

for i in range( 0,len(xvs) ):
    if i % int( 1 / dt ) == 0:
        t.dot(5,'red')
    
    cx = cx + xvs[i]
    cy = cy + yvs[i]
    t.goto(cx,cy)

k = input('press enter to exit ')

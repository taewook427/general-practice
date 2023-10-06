import turtle as t
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
    t.write('1.0')
    t.goto(-330,-180-10)
    t.write('1.4')
    t.goto(-330,-60-10)
    t.write('1.8')
    t.goto(-330,60-10)
    t.write('2.2')
    t.goto(-330,180-10)
    t.write('2.6')
    t.goto(-330,300-10)
    t.write('3.0')
    t.goto(-330,320-10)
    t.write('주기 [s]')
    t.goto(-300-10,-320)
    t.write('0.00')
    t.goto(-180-10,-320)
    t.write('0.05')
    t.goto(-60-10,-320)
    t.write('0.10')
    t.goto(60-10,-320)
    t.write('0.15')
    t.goto(180-10,-320)
    t.write('0.20')
    t.goto(300-10,-320)
    t.write('0.25')
    t.goto(330-10,-320)
    t.write('축-중심 거리 [m]')
    for i in range(0,5):
        t.penup()
        t.goto(-180+120*i,-300)
        t.pendown()
        t.goto(-180+120*i,+300)
        t.penup()
        t.goto(-300,-180+120*i)
        t.pendown()
        t.goto(+300,-180+120*i)
        t.penup()
def getdata(name,amount):
    file = open(name,'r',encoding = 'utf-8')
    file.readline()
    file.readline()
    file.readline()
    lists = [ ]
    for i in range(0,amount):
        lists.append( file.readline()[:-1] )
    datax = [ ]
    datay = [ ]
    for i in lists:
        datax.append( int( i[0:2] ) )
        datay.append( float( i[3:] ) )
    file.close()
    output = [ ]
    output.append(datax)
    output.append(datay)
    return output
def drawdata(name,color,amount,datax,datay,k):
    t.pensize(2)
    t.color(color)
    t.penup()
    t.goto(320,-300+30+30*k)
    t.stamp()
    t.goto(330,-300+30+30*k)
    t.write(name)
    t.penup()
    t.goto(24*datax[0]-300,300*(datay[0]-1)-300)
    for i in range(0,amount):
        t.pensize(2)
        t.pendown()
        t.goto(24*datax[i]-300,300*(datay[i]-1)-300)
        t.pensize(4)
        t.penup()
        t.goto(24*datax[i]-300-3,300*(datay[i]-1)-300)
        t.pendown()#d
        t.goto(24*datax[i]-300+3,300*(datay[i]-1)-300)
        t.penup()
        t.goto(24*datax[i]-300,300*(datay[i]-1)-300-6)
        t.pendown()#d
        t.goto(24*datax[i]-300+2,300*(datay[i]-1)-300+6)
        t.pensize(2)
        t.penup()
        t.goto(24*datax[i]-300,300*(datay[i]-1)-300)
print('그래프')
file_amount = int(input('그릴 데이터 개수 : '))
file_name = [ ]
for i in range(0,file_amount):
    name = input('데이터 파일 이름 : ')
    file_name.append(name)
drawset()
k = 0
for file in file_name:
    txt = open(file,'r',encoding = 'utf-8')
    data_name = txt.readline()[:-1]
    data_color = txt.readline()[:-1]
    data_amount = int( txt.readline()[:-1] )
    txt.close()
    rawlist = getdata(file,data_amount)
    datax = rawlist[0]
    datay = rawlist[1]
    drawdata(data_name,data_color,data_amount,datax,datay,k)
    k = k + 1
t.hideturtle()
print('완료')
k = input('.')

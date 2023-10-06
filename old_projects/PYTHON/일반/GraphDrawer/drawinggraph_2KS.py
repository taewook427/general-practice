import turtle
import math
def cal_par(start,end):
    list_cal_par=[]
    for temp1 in range(start+1,end):
        list_cal_par.append(list_cal_equ[temp1])
    del list_cal_equ[start:end+1]
    cal_par_result=0
    cal_par_defined=1
    while len(list_cal_par)>1:
        cal_par_operand1=0
        cal_par_operand2=0
        if list_cal_par.count('^')>0:
            temp1=list_cal_par.index('^')
            cal_par_operand1=list_cal_par[temp1-1]
            cal_par_operand2=list_cal_par[temp1+1]
            del list_cal_par[temp1-1]
            del list_cal_par[temp1-1]
            del list_cal_par[temp1-1]
            if cal_par_operand1>0:
                cal_par_result=cal_par_operand1**cal_par_operand2
                list_cal_par.insert(temp1-1,cal_par_result)
            elif cal_par_operand2==int(cal_par_operand2):
                cal_par_result=cal_par_operand1**cal_par_operand2
                list_cal_par.insert(temp1-1,cal_par_result)
            else:
                cal_par_defined=0
                cal_par_result=0
                list_cal_par.insert(temp1-1,cal_par_result)
        elif list_cal_par.count("*")>0 or list_cal_par.count('/')>0:
            temp1=0
            temp2=-1
            while temp1==0:
                temp2=temp2+1
                if list_cal_par[temp2]=='*'or list_cal_par[temp2]=='/':
                    temp1=1
            if list_cal_par[temp2]=='*':
                cal_par_operand1=list_cal_par[temp2-1]
                cal_par_operand2=list_cal_par[temp2+1]
                del list_cal_par[temp2-1]
                del list_cal_par[temp2-1]
                del list_cal_par[temp2-1]
                cal_par_result=cal_par_operand1*cal_par_operand2
                list_cal_par.insert(temp2-1,cal_par_result)
            elif list_cal_par[temp2]=='/':
                cal_par_operand1=list_cal_par[temp2-1]
                cal_par_operand2=list_cal_par[temp2+1]
                del list_cal_par[temp2-1]
                del list_cal_par[temp2-1]
                del list_cal_par[temp2-1]
                if cal_par_operand2 == 0:
                    cal_par_result=0
                    cal_par_defined=0
                else:
                    cal_par_result=cal_par_operand1/cal_par_operand2
                list_cal_par.insert(temp2-1,cal_par_result)
        elif list_cal_par.count("+")>0 or list_cal_par.count('-')>0:
            temp1=0
            temp2=-1
            while temp1==0:
                temp2=temp2+1
                if list_cal_par[temp2]=='+'or list_cal_par[temp2]=='-':
                    temp1=1
            if list_cal_par[temp2]=='+':
                cal_par_operand1=list_cal_par[temp2-1]
                cal_par_operand2=list_cal_par[temp2+1]
                del list_cal_par[temp2-1]
                del list_cal_par[temp2-1]
                del list_cal_par[temp2-1]
                cal_par_result=cal_par_operand1+cal_par_operand2
                list_cal_par.insert(temp2-1,cal_par_result)
            elif list_cal_par[temp2]=='-':
                cal_par_operand1=list_cal_par[temp2-1]
                cal_par_operand2=list_cal_par[temp2+1]
                del list_cal_par[temp2-1]
                del list_cal_par[temp2-1]
                del list_cal_par[temp2-1]
                cal_par_result=cal_par_operand1-cal_par_operand2
                list_cal_par.insert(temp2-1,cal_par_result)
    global cal_equ_defined
    cal_equ_defined=cal_equ_defined*cal_par_defined
    temp1=list_cal_par[0]
    list_cal_equ.insert(start,temp1)
def cal_func(func_type,operand):
    global cal_func_result
    global cal_equ_defined
    cal_func_defined=1
    cal_func_result=0
    if func_type=='round':
        if math.ceil(operand)-operand>0.5:
            cal_func_result=math.floor(operand)
        else:
            cal_func_result=math.ceil(operand)
    elif func_type=='abs':
        cal_func_result=math.fabs(operand)
    elif func_type=='up':
        cal_func_result=math.ceil(operand)
    elif func_type=='down':
        cal_func_result=math.floor(operand)
    elif func_type=='root':
        if operand>=0:
            cal_func_result=operand**0.5
        else:
            cal_func_result=0
            cal_func_defined=0
    elif func_type=='sin':
        cal_func_result=math.sin(operand)
    elif func_type=='cos':
        cal_func_result=math.cos(operand)
    elif func_type=='tan':
        cal_func_result=math.tan(operand)
    elif func_type=='asin':
        if -1<=operand<=1:
            cal_func_result=math.asin(operand)
        else:
            cal_func_result=0
            cal_func_defined=0
    elif func_type=='acos':
        if -1<=operand<=1:
            cal_func_result=math.acos(operand)
        else:
            cal_func_result=0
            cal_func_defined=0
    elif func_type=='atan':
        cal_func_result=math.atan(operand)
    elif func_type=='ln':
        if operand>0:
            cal_func_result=math.log(operand)
        else:
            cal_func_result=0
            cal_func_defined=0
    elif func_type=='log':
        if operand>0:
            cal_func_result=math.log10(operand)
        else:
            cal_func_result=0
            cal_func_defined=0
    cal_equ_defined=cal_equ_defined*cal_func_defined
def find_par():
    global find_par_site1
    global find_par_site2
    find_par_site1=0
    find_par_site2=0
    temp1=0
    temp2=1
    if list_cal_equ.count(')')>0:
        find_par_site2=list_cal_equ.index(')')
        temp1=find_par_site2
        while temp2==1:
            temp1=temp1-1
            if list_cal_equ[temp1]=='(':
                temp2=0
        find_par_site1=temp1
    else:
        find_par_site1=0
        find_par_site2=len(list_cal_equ)-1
def cal_equ(x_input,y_input):
    cal_equ_result=0
    global cal_equ_defined
    cal_equ_defined=1
    global list_cal_equ
    list_cal_equ=[]
    list_operator=['(',')','+','-','*','/','^']
    list_function1=['round','abs','up','down','root','ln','log']
    list_function2=['sin','cos','tan','asin','acos','atan']
    for temp1 in list_equ_input:
        if temp1=='x':
            list_cal_equ.append(x_input)
        elif temp1=='y':
            list_cal_equ.append(y_input)
        elif temp1=='pi':
            list_cal_equ.append(math.pi)
        elif temp1=='e':
            list_cal_equ.append(math.e)
        elif temp1 in list_operator:
            list_cal_equ.append(temp1)
        elif temp1 in list_function1:
            list_cal_equ.append(temp1)
        elif temp1 in list_function2:
            list_cal_equ.append(temp1)
        else:
            temp1=float(temp1)
            list_cal_equ.append(temp1)
    while len(list_cal_equ)>1:
        find_par()
        if find_par_site1==0:
            cal_par(find_par_site1,find_par_site2)
        elif list_cal_equ[find_par_site1-1] in list_operator:
            cal_par(find_par_site1,find_par_site2)
        elif list_cal_equ[find_par_site1-1] in list_function1:
            temp3=list_cal_equ[find_par_site1-1]
            cal_par(find_par_site1,find_par_site2)
            temp4=list_cal_equ[find_par_site1]
            cal_func(temp3,temp4)
            del list_cal_equ[find_par_site1-1]
            del list_cal_equ[find_par_site1-1]
            list_cal_equ.insert(find_par_site1-1,cal_func_result)
        elif list_cal_equ[find_par_site1-1] in list_function2:
            temp3=list_cal_equ[find_par_site1-1]
            cal_par(find_par_site1,find_par_site2)
            temp4=list_cal_equ[find_par_site1]
            cal_func(temp3,temp4)
            del list_cal_equ[find_par_site1-1]
            del list_cal_equ[find_par_site1-1]
            list_cal_equ.insert(find_par_site1-1,cal_func_result)
    return list_cal_equ[0]
def equ_input():
    global list_equ_input
    global real_input
    global equal_sign
    list_equ_input=[]
    list_operator=['(',')','+','-','*','/','^']
    real_input=input('그래프를 그릴 방정식을 입력하세요.\n')
    temp1=-1
    temp2=0
    while temp2==0:
        temp1=temp1+1
        if real_input[temp1]=='=':
            temp2=1
            equal_sign=0
        elif real_input[temp1]=='<':
            temp2=1
            equal_sign=-1
        elif real_input[temp1]=='>':
            temp2=1
            equal_sign=1
    temp2=len(real_input)
    if temp1==1:
        equ_input_part1=real_input[0]
    else:
        equ_input_part1=real_input[:temp1]
    if temp1==temp2-2:
        equ_input_part2=real_input[temp2-1]
    else:
        equ_input_part2=real_input[temp1+1:]
    raw_input='('
    raw_input=raw_input+equ_input_part1
    raw_input=raw_input+'-('
    raw_input=raw_input+equ_input_part2
    raw_input=raw_input+')'
    raw_input=raw_input+')'
    temp2=''
    for temp1 in raw_input:
        if temp1 in list_operator:
            if temp2=='':
                list_equ_input.append(temp1)
            else:
                list_equ_input.append(temp2)
                list_equ_input.append(temp1)
                temp2=''
        else:
            temp2=temp2+temp1
def draw_line(x_part):
    turtle.penup()
    turtle.goto(5*x_part,-300)
    turtle.pendown()
    for y_part in range(-60,60):
        draw_result=cal_equ(x_part,y_part)
        if cal_equ_defined==0:
            turtle.color('rosybrown')
        else:
            if equal_sign==0:
                if -1*pen_size<draw_result<pen_size:
                    turtle.color('blue')
                else:
                    turtle.color('silver')
            elif equal_sign==-1:
                if draw_result<0:
                    turtle.color('blue')
                else:
                    turtle.color('silver')
            elif equal_sign==1:
                if draw_result>0:
                    turtle.color('blue')
                else:
                    turtle.color('silver')
        turtle.forward(5)
def draw_all():
    turtle.penup()
    turtle.reset()
    turtle.speed(0)
    turtle.pensize(6)
    turtle.left(90)
    for x_cord in range(-60,60):
        draw_line(x_cord)
    x_cord=input('그래프 그리기가 끝났습니다. 아무 키를 눌러 종료하십시오.\n')
print('이 프로그램은 방정식의 그래프를 그리는 프로그램입니다.\n')
equ_input()
if equal_sign==0:
    pen_size=input('등호 계산시 허용 범위를 정해주세요.\n')
    pen_size=float(pen_size)
else:
    pen_size=1.5
turtle.title("KoTaewook's Equation Graphic Module")
turtle.delay(0)
draw_all()

import random
from tkinter import filedialog
import tkinter
import os

def preset():
    try:
        mainwin = tkinter.Tk()
        mainwin.title('FR2')
        mainwin.geometry('20x20+10+10')
        mainwin.resizable(0,0)
        #path = os.path.join(os.path.expanduser('~'),'Desktop')
        path = os.getcwd()
        file = filedialog.askopenfile( initialdir=path, title='실행할 코드 선택', filetypes=( ('txt files', '*.txt'),('all files', '*.*') ) )
        txtname = file.name
        mainwin.destroy()
        
        file = open(txtname,'r',encoding='utf-8')
        rawcode = file.readlines()
        if not rawcode[-1][-1] == '\n':
            rawcode[-1] = rawcode[-1] + '\n'
        for i in range( 0,len(rawcode) ):
            rawcode[i] = rawcode[i][0:-1]
        file.close()
        return rawcode
    except:
        print('문제 : 실행할 텍스트 파일을 찾을 수 없습니다.')
        return [ ]

def start(script,ifloc,whileloc):
    nowpoint = 0
    endpoint = len(script)
    varlist = [ ]
    for i in range(0,100):
        varlist.append(0)

    while not nowpoint == endpoint:
        cmd = script[nowpoint]
        try:
            if cmd[0:2] == 'BK':
                tgtvar = int( cmd[2:4] )
                oper = cmd[4]
                if oper == '!':
                    varlist[tgtvar] = varlist[tgtvar] + 1

                elif oper == '?':
                    varlist[tgtvar] = varlist[tgtvar] - 1

                elif oper == '=':
                    bckcmd = cmd[5:cmd.find(':')]
                    if bckcmd == '공부안해?':
                        var1 = cmd[cmd.find(':')+1:cmd.find(':')+5]
                        var2 = cmd[cmd.find(':')+6:cmd.find(':')+10]
                        if not var1[0:2] == 'BK' and var2[0:2] == 'BK':
                            print('문제 : 잘못된 변수명 ',cmd)
                        else:
                            var1 = str( varlist[ int( var1[2:4] ) ] )
                            var2 = str( varlist[ int( var2[2:4] ) ] )
                            varlist[tgtvar] = var1 + var2

                    elif bckcmd == '여러분 맞습니까?':
                        strvar = cmd[cmd.find(':')+1:]
                        print('콘솔 : ',strvar)
                        userin = input('유저 : ')
                        try:
                            varlist[tgtvar] = int( userin )
                        except:
                            varlist[tgtvar] = userin

                    elif bckcmd == '주옥같은 기출문제 풀어보세요':
                        var1 = cmd[cmd.find(':')+1:cmd.find(':')+5]
                        var2 = cmd[cmd.find(':')+6:cmd.find(':')+10]
                        cal = cmd[cmd.find(':')+5]
                        if not var1[0:2] == 'BK' and var2[0:2] == 'BK':
                            print('문제 : 잘못된 변수명 ',cmd)
                        else:
                            var1 = varlist[ int( var1[2:4] ) ]
                            var2 = varlist[ int( var2[2:4] ) ]
                            if not cal in ['+','-','*','/','^','%']:
                                print('문제 : 사용할 수 없는 연산자 ',cmd)
                            else:
                                try:
                                    if cal == '+':
                                        varlist[tgtvar] = var1 + var2
                                    elif cal == '-':
                                        varlist[tgtvar] = var1 - var2
                                    elif cal == '*':
                                        varlist[tgtvar] = var1 * var2
                                    elif cal == '/':
                                        varlist[tgtvar] = int( var1 / var2 )
                                    elif cal == '^':
                                        varlist[tgtvar] = var1 ** var2
                                    elif cal == '%':
                                        varlist[tgtvar] = var1 % var2
                                except:
                                    print('문제 : 계산 불가 ',cmd)

                    else:
                        print('문제 : 존재하지 않는 명령 ',cmd)

                else:
                    print('문제 : 존재하지 않는 명령 ',cmd)
                nowpoint = nowpoint + 1
            
            else:
                cmdset = cmd[0:cmd.find(':')]
                if cmdset == '표현력':
                    cmdvar = cmd[cmd.find(':')+1:]
                    if cmdvar[0:2] == 'BK':
                        var = varlist[ int( cmdvar[2:4] ) ]
                        print('콘솔 : ',var)
                    else:
                        print('문제 : 잘못된 변수명 ',cmd)
                    nowpoint = nowpoint + 1
                    
                elif cmdset == '자 앉아보세요':
                    cmdvar = cmd[cmd.find(':')+1:cmd.find('=')]
                    cmdstr = cmd[cmd.find('=')+1:]
                    if cmdvar[0:2] == 'BK':
                        try:
                            cmdstr = int( cmdstr )
                            varlist[ int( cmdvar[2:4] ) ] = cmdstr
                        except:
                            varlist[ int( cmdvar[2:4] ) ] = cmdstr
                    else:
                        print('문제 : 잘못된 변수명 ',cmd)
                    nowpoint = nowpoint + 1
                
                elif cmdset == '1/3법칙':
                    cmdvar = cmd[cmd.find(':')+1:]
                    if cmdvar[0:2] == 'BK':
                        varlist[ int( cmdvar[2:4] ) ] = random.randrange(1,4)
                    else:
                        print('문제 : 잘못된 변수명 ',cmd)
                    nowpoint = nowpoint + 1
                
                elif cmdset == '불광동':
                    cmdvar = cmd[cmd.find(':')+1:]
                    if cmdvar[0:2] == 'BK':
                        try:
                            varlist[ int( cmdvar[2:4] ) ] = int( float( varlist[ int( cmdvar[2:4] ) ] ) )
                        except:
                            print('문제 : 정수형 변환불가 ',cmd)
                    else:
                        print('문제 : 잘못된 변수명 ',cmd)
                    nowpoint = nowpoint + 1
                
                elif cmdset == '따라오니':
                    stpos = nowpoint
                    curpos = nowpoint
                    enpos = 0
                    temp = 1
                    while not temp == 0:
                        curpos = curpos + 1
                        temp = temp + ifloc[curpos]
                    enpos = curpos
                    cmdvar = cmd[cmd.find(':')+1:]
                    var1 = varlist[ int( cmdvar[2:4] ) ]
                    var2 = varlist[ int( cmdvar[7:9] ) ]
                    com = cmdvar[4]
                    if com == '=':
                        if var1 == var2:
                            nowpoint = nowpoint + 1
                        else:
                            nowpoint = enpos + 1
                    elif com == '>':
                        if var1 > var2:
                            nowpoint = nowpoint + 1
                        else:
                            nowpoint = enpos + 1
                    elif com == '<':
                        if var1 < var2:
                            nowpoint = nowpoint + 1
                        else:
                            nowpoint = enpos + 1
                    else:
                        print('문제 : 조건 비교 불가 ',cmd)
                        nowpoint = nowpoint + 1
                
                elif cmdset == '여러분 이러면 안됩니다':
                    nowpoint = nowpoint + 1
                
                elif cmdset == '자 문제 한번 풀어보세요':
                    stpos = nowpoint
                    curpos = nowpoint
                    enpos = 0
                    temp = 1
                    while not temp == 0:
                        curpos = curpos + 1
                        temp = temp + whileloc[curpos]
                    enpos = curpos
                    cmdvar = cmd[cmd.find(':')+1:]
                    var1 = varlist[ int( cmdvar[2:4] ) ]
                    var2 = varlist[ int( cmdvar[7:9] ) ]
                    com = cmdvar[4]
                    if com == '=':
                        if var1 == var2:
                            nowpoint = nowpoint + 1
                        else:
                            nowpoint = enpos + 1
                    elif com == '>':
                        if var1 > var2:
                            nowpoint = nowpoint + 1
                        else:
                            nowpoint = enpos + 1
                    elif com == '<':
                        if var1 < var2:
                            nowpoint = nowpoint + 1
                        else:
                            nowpoint = enpos + 1
                    else:
                        print('문제 : 조건 비교 불가 ',cmd)
                        nowpoint = nowpoint + 1
                
                elif cmdset == '교과서 수준 문제':
                    stpos = nowpoint
                    curpos = nowpoint
                    enpos = nowpoint
                    temp = -1
                    while not temp == 0:
                        curpos = curpos - 1
                        temp = temp + whileloc[curpos]
                    stpos = curpos
                    nowpoint = stpos
                
                else:
                    print('문제 : 존재하지 않는 명령 ',cmd)
                    nowpoint = nowpoint + 1
        except:
            print('문제 : 알수없는 오류 발생 ',cmd)
            nowpoint = nowpoint + 1

def main():
    rawcode = preset()
    if not rawcode == [ ]:
        if not '안녕 얘들아' in rawcode:
            print('문제 : 시작 구문이 없습니다.')
        elif not '오늘 수업 여기까지' in rawcode:
            print('문제 : 종료 구문이 없습니다.')
        else:
            converted = [ ]
            tempa = 0
            tempb = 1
            for i in range( 0,len(rawcode) ):
                if not rawcode[i] == '':
                    if not rawcode[i][0:3] == '에헤이':
                        if rawcode[i] == '안녕 얘들아':
                            tempa = 1
                        elif rawcode[i] == '오늘 수업 여기까지':
                            tempb = 0
                        elif tempa * tempb == 1:
                            converted.append( rawcode[i] )

            ifconfig = [ ]
            for i in range( 0,len(converted) ):
                try:
                    if converted[i][0:4] == '따라오니':
                        ifconfig.append(1)
                    elif converted[i][0:12] == '여러분 이러면 안됩니다':
                        ifconfig.append(-1)
                    else:
                        ifconfig.append(0)
                except:
                    ifconfig.append(0)

            whileconfig = [ ]
            for i in range( 0,len(converted) ):
                try:
                    if converted[i][0:13] == '자 문제 한번 풀어보세요':
                        whileconfig.append(1)
                    elif converted[i][0:9] == '교과서 수준 문제':
                        whileconfig.append(-1)
                    else:
                        whileconfig.append(0)
                except:
                    whileconfig.append(0)

            temp1 = 0
            for i in ifconfig:
                temp1 = temp1 + i
            temp2 = 0
            for i in whileconfig:
                temp2 = temp2 + i
            if not temp1 == 0:
                print('문제 : 조건문 시작-끝 조합이 맞지 않습니다.')
            elif not temp2 == 0:
                print('문제 : 반복문 시작-끝 조합이 맞지 않습니다.')
            else:          
                print('\n< 변환된 코드 >')
                for i in converted:
                    print(i)
                k = input('\n엔터키를 눌러 실행 ')
                start(converted,ifconfig,whileconfig)

print('BKscript   이 프로그램을 동성고 실세 김병관 선생님께 바칩니다.')    
main()
k = input('\npress enter to exit... ')

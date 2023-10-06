import time
import os
import sys
import sei

def dos(k,win,listbox): #shutdown return T/F
    helptxt = '''
< 사용 가능한 명령어 모음 >
'help' : 도움말
'exit' : 명령어 모드 종료
'shutdown' : 전체 종료
'print A' : A 출력
'exe A' : A 문자열 실행 후 결과 리턴
'txt' : 텍스트 파일 열기
'bin' : 이진 파일 열기
'open' : 기록 보기
'cut A B' : 일정 기간보다 오래된 기록 지우기
A - y / d / s, B - 숫자
'edit' : 기록 직접 수정
'delete' : 기록 파일 삭제
'''
    k.print(win,listbox,'===== KDOS CONSOLE =====\n')
    dos = True
    while dos:
        k.print(win,listbox,'_')
        order = k.input0(win)
        k.erase(win,listbox)
        k.print(win,listbox,'>>> '+order)
        
        try:
            #order 실행
            if order == 'help':
                k.print(win,listbox,helptxt)
            elif order == 'exit':
                k.print(win,listbox,'명령어 모드 종료')
                dos = False
            elif order == 'shutdown':
                k.print(win,listbox,'전체 종료')
                dos = False
                
            elif order == 'txt':
                k.print(win,listbox,'열기를 진행할 텍스트 파일 선택')
                path = k.select('file') #txt path
                if os.path.getsize(path) > 1048576: #1MB
                    k.msg('경고','크기가 1MB보다 큰 파일은 열 수 없습니다.','info')
                    raise Exception ('File Too Big')
                f = open(path,'r',encoding='utf-8')
                temp = f.readlines()
                f.close()
                f = lambda x : x[0:-1] if x[-1] == '\n' else x
                for i in range(0,len(temp)):
                    temp[i] = f( temp[i] )#\n 제거된 리스트
                num = len(temp) #행 개수
                size = len( str(num) ) #번호 사이즈
                k.print(win,listbox,'T' * size + ' | ' + '0'*10 + '1'*10 + '2'*10 + '3'*10)
                k.print(win,listbox,'T' * size + ' | ' + '1234567890'*4)
                for i in range(0,num):
                    k.print( win, listbox, ('0' * size + str(i))[-size:] + ' | ' + temp[i] )
                k.print(win,listbox,' ')

            elif order == 'bin':
                k.print(win,listbox,'열기를 진행할 이진 파일 선택')
                path = k.select('file') #bin path
                if os.path.getsize(path) > 1048576: #1MB
                    k.msg('경고','크기가 1MB보다 큰 파일은 열 수 없습니다.','info')
                    raise Exception ('File Too Big')
                f = open(path,'rb')
                temp = f.read() #bin
                f.close()
                num = len(temp) #bin size int
                num16 = num // 16 #행 개수
                size = len( str(num16 + 1) ) #번호 사이즈
                k.print(win,listbox,'B' * size + ' | ' + '0001020304050607 08090A0B0C0D0E0F')
                for i in range(0,num16):
                    d0 = temp[16*i:16*i+16] #16B
                    d1 = [ ]
                    for j in range(0,16):
                        d2 = hex( d0[j] ) #0x0 0x11
                        if len(d2) == 4:
                            d1.append( d2[2:] )
                        else:
                            d1.append( '0' + d2[2] )
                    outt = ('0' * size + str(i))[-size:] + ' | ' + ''.join(d1[0:8]) + ' ' + ''.join(d1[8:16])
                    k.print( win, listbox, outt.upper() )
                if num % 16 != 0:
                    d0 = temp[-(num % 16):] #마지막 바이트 전부
                    d1 = [ ]
                    for j in range(0,len(d0)):
                        d2 = hex( d0[j] ) #0x0 0x11
                        if len(d2) == 4:
                            d1.append( d2[2:] )
                        else:
                            d1.append( '0' + d2[2] )
                    if len(d1) > 8:
                        out = ''.join(d1[0:8]) + ' ' + ''.join(d1[8:])
                    else:
                        out = ''.join(d1)
                    outt = ('0' * size + str(num16))[-size:] + ' | ' + out
                    k.print( win, listbox, outt.upper() )
                k.print(win,listbox,' ')

            elif order == 'open':
                try:
                    f = open('log307.txt','r',encoding='utf-8')
                    lines = [ x[0:-1] for x in f.readlines() ]
                    f.close() #기록표 구하기
                except:
                    lines = [ ]
                k.print(win,listbox,'현재까지의 데이터 기록입니다.')
                for i in lines:
                    k.print(win,listbox,i)
                k.print(win,listbox,' ')

            elif order == 'edit':
                k.print(win,listbox,'기록 직접수정 모드를 고르십시오.')
                k.print(win,listbox,'추가 모드로 수정하시겠습니까?\n예 : 추가 모드 / 아니오 : 새시작 모드')
                if k.ask2(win) == '0':
                    temp = k.input2(win) #추가 모드
                    if temp[-1] != '\n':
                        temp = temp + '\n'
                    f = open('log307.txt','a',encoding='utf-8')
                    f.write(temp)
                    f.close()
                else:
                    temp = k.input2(win) #새시작 모드
                    if temp[-1] != '\n':
                        temp = temp + '\n'
                    f = open('log307.txt','w',encoding='utf-8')
                    f.write(temp)
                    f.close()
                k.print(win,listbox,'기록이 수정되었습니다.')

            elif order == 'delete':
                k.print(win,listbox,'기록 삭제 준비')
                if k.msg('삭제 확인','정말 기록 파일을 삭제하시겠습니까?','ask'):
                    try:
                        os.remove('log307.txt')
                    except:
                        pass
                    k.print(win,listbox,'기록 파일이 삭제되었습니다.')
                else:
                    k.print(win,listbox,'기록 파일 삭제가 취소되었습니다.')

            else:
                temp = order.split(' ') #띄어쓰기 분할된 명령어
                if temp[0] == 'print':
                    k.print( win, listbox, ' '.join(temp[1:]) )
                elif temp[0] == 'exe':
                    k.print( win, listbox, str( eval( ' '.join(temp[1:]) ) ) )
                    
                elif temp[0] == 'cut':
                    realtime = int( time.time() ) #정수 유닉스 시간
                    nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) ) #시간 구조
                    k.print(win,listbox,'현재시간 : '+nowtime)
                    d1 = temp[1] #날짜 식별자
                    d2 = int( temp[2] ) #숫자
                    try:
                        f = open('log307.txt','r',encoding='utf-8')
                        lines = [ x[0:-1] for x in f.readlines() ]
                        f.close() #기록표 구하기
                    except:
                        lines = [ ]
                    if d1 == 'y':
                        t = 31536000
                    elif d1 == 'd':
                        t = 86400
                    elif d1 == 's':
                        t = 1
                    else:
                        raise Exception ('알 수 없는 시간 모드')
                    #lines txt update
                    newlines = [ ]
                    for i in lines:
                        temp = i.split('#')
                        a = temp[0]
                        b = temp[1]
                        c = temp[2]
                        if realtime - int(b) < t * d2:
                            newlines.append( a + '#' + b+ '#' + c )
                    f = open('log307.txt','w',encoding='utf-8')
                    for i in newlines:
                        f.write(i + '\n')
                    f.close()
                    k.print(win,listbox,'처리되었습니다.')

                else:
                    k.print(win,listbox,'알 수 없는 명령어입니다.\nhelp를 입력해 명령어 목록을 보십시오.')
                
        except Exception as e:
            k.print(win,listbox,'예외 발생 : '+str(e))
            
    if order == 'shutdown':
        for i in range(0,3):
            k.print(win,listbox,'/')
            time.sleep(0.3)
            k.erase(win,listbox)
            k.print(win,listbox,' ')
            time.sleep(0.3)
            k.erase(win,listbox)
        k.end(win)
        return True
    else:
        return False

def console(k):
    p = k.init('KDOS')
    win = p[0]
    listbox = p[1]
    try:
        f = open('log307.txt','r',encoding='utf-8')
        lines = [ x[0:-1] for x in f.readlines() ]
        f.close() #기록표 구하기
    except:
        lines = [ ]
        
    k.print(win,listbox,'===== KDOS SYSTEM =====\n\n비밀번호를 입력하십시오.')
    while k.input1(win) != '0000':
        for i in range(1,36):
            k.print(win,listbox,'*'*i)
            time.sleep(0.03)
            k.erase(win,listbox)
        k.print(win,listbox,'비밀번호가 일치하지 않습니다.')
    for i in range(1,36):
        k.print(win,listbox,'*'*i)
        time.sleep(0.03)
        k.erase(win,listbox)
    k.print(win,listbox,'로그인 성공\n')

    k.print(win,listbox,'<단축키>\nA - 데이터 보기\nB - 데이터 정리\nC - 명령어 모드\nD - 종료\n')
    
    shutdown = False
    while not shutdown:
        init = k.ask4(win) #4개 단축키
        if init == '0':
            k.print(win,listbox,'현재까지의 데이터 기록입니다.')
            for i in lines:
                k.print(win,listbox,i)
            k.print(win,listbox,' ')
        elif init == '1':
            realtime = int( time.time() ) #정수 유닉스 시간
            nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) ) #시간 구조
            k.print(win,listbox,'현재시간 : '+nowtime)
            k.print(win,listbox,'몇 년 전까지의 기록만 남기겠습니까?')
            num = int( k.ask5(win) ) + 1 #12345
            #lines txt update
            newlines = [ ]
            for i in lines:
                temp = i.split('#')
                a = temp[0]
                b = temp[1]
                c = temp[2]
                if realtime - int(b) < 31536000 * num:
                    newlines.append( a + '#' + b+ '#' + c )
            lines = newlines
            f = open('log307.txt','w',encoding='utf-8')
            for i in lines:
                f.write(i + '\n')
            f.close()
            k.print(win,listbox,'처리되었습니다.\n')
        elif init == '2':
            shutdown = dos(k,win,listbox) #DOS mode
        else:
            shutdown = True
            k.print(win,listbox,'종료합니다.')
            k.ask2(win)
            k.end(win)

def counter(num):
    realtime = int( time.time() ) #정수 유닉스 시간
    nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) ) #시간 구조
    wr = nowtime + '#' + str(realtime) + '#' + str(num) + '\n' #기록할 문자열
    f = open('log307.txt','a',encoding='utf-8')
    f.write(wr)
    f.close()

k = sei.lite()
p = k.init('KDOS')
win = p[0]
listbox = p[1]

try:
    f = open('log307.txt','r',encoding='utf-8')
    lines = [ x[0:-1] for x in f.readlines() ]
    f.close() #기록표 구하기
except:
    lines = [ ]

try:
    k.print(win,listbox,'< 현재 기록 목록 >')
    for i in lines:
        k.print(win,listbox,i)
    if lines == [ ]:
        temp = 'None'
    else:
        temp = lines[-1].split('#')[2] #마지막 숫자
    k.print(win,listbox,'\n가장 최근 기록 : '+temp)
    
    k.print(win,listbox,'\n기록할 테스트 번호를 입력하십시오.\n미입력은 콘솔 모드입니다.')
    num = k.getnum(win) #문자열
except:
    try:
        k.print(win,listbox,'\n< 복구 모드 >\n기록 파일에 문제가 발생했습니다.\n콘솔 복구 모드로 진입합니다.\n')
        num = ''
        for i in range(0,7):
            k.print(win,listbox,'/')
            time.sleep(0.3)
            k.erase(win,listbox)
            k.print(win,listbox,' ')
            time.sleep(0.3)
            k.erase(win,listbox)
    except:
        sys.exit(0)

if num == '': #콘솔 열기
    k.end(win)
    console(k)
else:
    counter( int(num) )
    k.print(win,listbox,'기록됨 : '+num)
    k.print(win,listbox,'종료합니다.')
    for i in range(0,3):
        k.print(win,listbox,'/')
        time.sleep(0.3)
        k.erase(win,listbox)
        k.print(win,listbox,' ')
        time.sleep(0.3)
        k.erase(win,listbox)
    k.end(win)

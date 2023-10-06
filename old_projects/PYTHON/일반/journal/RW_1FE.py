import getpass
import time
import os
def work():
    file = open('crypt.txt','r',encoding = 'cp949')
    rawtxt = file.readlines()
    file.close()
    volume0 = rawtxt[0:5]
    volumeE = rawtxt[5:]
    volume0 = readhead(volume0)
    password = ask(volume0[0],volume0[1])
    if len(password) > 2:
        passwordout = password[0] + '*' * (len(password)-2) + password[-1]
    else:
        passwordout = '-'
    print('비밀번호 : ' + passwordout)
    print('마지막 비밀번호 변경 시간 : ' + volume0[2])
    print('마지막 볼륨 내용  변경 시간 : ' + volume0[3])
    print('마지막 접근 시간 : ' + volume0[4] )
    print("가용 명령어 : 'end' 'reset' 'load' 'save' 'update'\n")
    key = makehash(password)
    volumeE_decoded = readtxt(key,volumeE)
    now = gettime()
    volume0[4] = now
    write(key,volume0,volumeE_decoded)
    print('')
    f = 0
    while f == 0:
        talk = input('작업 명령어 입력 : ')
        result = order(talk,password,volume0,volumeE_decoded)
        if result == 1:
            f = 1
            print('종료합니다\n')
        elif result == -1:
            f = 0
            print('잘못된 명령입니다\n')
        elif result == 2:
            file = open('crypt.txt','r',encoding = 'cp949')
            rawtxt = file.readlines()
            file.close()
            volume0 = rawtxt[0:5]
            volumeE = rawtxt[5:]
            volume0 = readhead(volume0)
            if len(password) > 2:
                passwordout = password[0] + '*' * (len(password)-2) + password[-1]
            else:
                passwordout = '-'
            password = ask(volume0[0],volume0[1])
            print('비밀번호 : ' + passwordout)
            print('마지막 비밀번호 변경 시간 : ' + volume0[2])
            print('마지막 볼륨 내용  변경 시간 : ' + volume0[3])
            print('마지막 접근 시간 : ' + volume0[4] )
            print("가용 명령어 : 'end' 'reset' 'load' 'save' 'update'\n")
            key = makehash(password)
            volumeE_decoded = readtxt(key,volumeE)
            now = gettime()
            volume0[4] = now
            write(key,volume0,volumeE_decoded)
            print('')
        else:
            f = 0
    f = input('아무 키나 입력하여 종료하십시오... ')
def makehash(word):
    chrnum = [ ]
    for i in range( 0,len(word) ):
        chrnum.append( ord(word[i]) )
    num = 16180339887498 * 4
    for i in chrnum:
        num = ( num * i + 31415926535897 + 27182818284590 ) % 100000000000000
    return num
def gettime():
    nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) )
    return nowtime
def encrypt(key,word):
    wordlist = [ ]
    for i in range( 0,len(word) ):
        wordlist.append( int(str(9999999 - ord( word[i] ))*2) )
    strkey = str(key)
    multi = 0
    for i in range( 0,len(strkey) ):
        multi = multi + int( strkey[i] )
    multi = ( multi % 9 ) + 1
    for i in range( 0,len(wordlist) ):
        wordlist[i] = multi * ( key + wordlist[i] )
    output = ''
    for i in wordlist:
        output = output + str(i) + ' '
    output = output[:-1]
    return output
def decrypt(key,word):
    wordlist = [ ]
    temp = ''
    for i in range( 0,len(word) ):
        if word[i] == ' ':
            wordlist.append( int(temp) )
            temp = ''
        else:
            temp = temp + word[i]
    wordlist.append( int(temp) )
    strkey = str(key)
    multi = 0
    for i in range( 0,len(strkey) ):
        multi = multi + int( strkey[i] )
    multi = ( multi % 9 ) + 1
    for i in range( 0,len(wordlist) ):
        wordlist[i] = int(wordlist[i] / multi) - key
    output = ''
    for i in range( 0,len(wordlist) ):
        output = output + chr( 9999999 - int(str(wordlist[i])[-7:]) )
    return output
def simplecrypt(mode,word):
    if mode == 1:
        wordlist = [ ]
        for i in range( 0,len(word) ):
            wordlist.append( ord( word[i] ) )
        output = ''
        for i in wordlist:
            output = output + str(i) + ' '
        output = output[:-1]
        return output
    else:
        wordlist = [ ]
        temp = ''
        for i in range( 0,len(word) ):
            if word[i] == ' ':
                wordlist.append( int(temp) )
                temp = ''
            else:
                temp = temp + word[i]
        wordlist.append( int(temp) )
        for i in range( 0,len(wordlist) ):
            wordlist[i] = chr( wordlist[i] )
        output = ''
        for i in wordlist:
            output = output + i
        return output
def readhead(wordlist):
    for i in range( 0,len(wordlist) ):
        wordlist[i] = simplecrypt(0,wordlist[i][1:])
    return wordlist
def ask(trihash,hint):
    print('KOs crypto program V2.0')
    print('비밀번호 힌트 : ' + hint)
    f = 0
    while f == 0:
        income = getpass.getpass('비밀번호를 입력하세요\n>>> ')
        incometri = income * 3
        if str(trihash) == str( makehash(incometri) ):
            f = 1
            return income
        else:
            print('비밀번호가 잘못됐습니다\n'+str(len(income))+'자 입력됨\n')
def readtxt(key,volume):
    decoded = [ ]
    for i in volume:
        i = i[:-1]
        if i == '':
            print('')
            decoded.append('')
        else:
            print(decrypt(key,i))
            decoded.append(decrypt(key,i))
    return decoded
def write(key,volume0,volumeE):
    lists = [ ]
    for i in volume0:
        lists.append('#' + simplecrypt(1,i) )
    for i in volumeE:
        if i == '':
            lists.append('')
        else:
            lists.append( encrypt(key,i) )
    file = open('crypt.txt','w')
    for i in lists:
        file.write(i + '\n')
    file.close()
def order(talk,password,header,volumeF):
    if talk == 'end':
        return 1
    elif talk == 'reset':
        if password == getpass.getpass('비밀번호를 입력하세요\n>>> '):
            new = input('새 비밀번호를 입력하세요\n>>>')
            hint = input('비밀번호 힌트를 입력하세요\n>>> ')
            header[0] = str( makehash(new * 3) )
            header[1] = hint
            header[2] = gettime()
            key = makehash(new)
            write(key,header,volumeF)
            print('비밀번호가 변경되었습니다\n')
            return 2
        else:
            print('비밀번호가 잘못되었습니다.\n')
            return 0
    elif talk == 'load':
        if password == getpass.getpass('비밀번호를 입력하세요\n>>>'):
            file = open('plain.txt','w')
            for i in volumeF:
                file.write(i + '\n')
            file.close()
            print('이제 볼륨 내용을 외부 텍스트 파일에서 수정할 수 있습니다\n')
            return 0
        else:
            print('비밀번호가 잘못되었습니다.\n')
            return 0
    elif talk == 'save':
        if password == getpass.getpass('비밀번호를 입력하세요\n>>> '):
            header[3] = gettime()
            filenew = open('plain.txt','r',encoding = 'cp949')
            volumeF = filenew.readlines()
            for i in range( 0,len(volumeF) ):
                volumeF[i] = volumeF[i][:-1]
            write(makehash(password),header,volumeF)
            filenew.close()
            filenew = open('plain.txt','w')
            for i in range(0,1000):
                filenew.write( str(i) * 100 + '\n' )
            filenew.close()
            os.remove('plain.txt')
            print('수정된 파일이 저장되었습니다\n')
            return 0
        else:
            print('비밀번호가 잘못되었습니다.\n')
            return 0
    elif talk == 'update':
        return 2
    else:
        return -1
work()

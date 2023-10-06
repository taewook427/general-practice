import tkinter
import tkinter.messagebox
import time
import random
import hashlib
import os

def main():

    def encrypt():
        filename = textbox0.get()
        try:
            def start_en():
                password = textbox1.get()
                i = tkinter.messagebox.askokcancel('비밀번호 확인','비밀번호를 다음과 같이 설정합니다 :\n' + password)
                if not i == 0:

                    def start_pack():
                        hint = textbox2.get()
                        hint_b = bytes(hint,'utf-8')
                        if len(hint_b) > 324:
                            i = tkinter.messagebox.showinfo('Error : 힌트크기','힌트 텍스트의 크기가 너무 큽니다.\n324바이트 이하로 적어 주십시오.\n( 영문 324자 / 한글 108자 )')
                        else:
                            i = tkinter.messagebox.askokcancel('비밀번호 힌트 확인','비밀번호 힌트를 다음과 같이 설정합니다 :\n' + hint)
                            if not i == 0:
                                hint = hint + ' '*324
                                hint_b = bytes(hint,'utf-8')
                                hint_b = hint_b[0:324]
                                time.sleep(0.5)
                                i = tkinter.messagebox.showinfo('변환 시작','파일 변환이 시작됩니다.\n파일이 위치한 폴더에 진행 사항이 표시됩니다.\n시간이 좀 걸릴 수 있습니다.')
                                hintwin.destroy()
                                encrypt_sys(filename,password,hint_b)
                                adwin = tkinter.Tk()
                                adwin.geometry('10x10+10+10')
                                time.sleep(0.5)
                                i = tkinter.messagebox.showinfo('변환 완료','파일 변환이 완료되었습니다.')
                                adwin.destroy()
                    
                    enwin.destroy()
                    time.sleep(0.5)
                    hintwin = tkinter.Tk()
                    hintwin.title('Cryptography V1')
                    hintwin.geometry('400x200+500+400')
                    hintwin.resizable(0,0)
                    label1 = tkinter.Label(hintwin, text='비밀번호 : ' + password)
                    label1.place(x = 30,y = 10)
                    label2 = tkinter.Label(hintwin, text='비밀번호 힌트 설정 :')
                    label2.place(x = 30,y = 50)
                    textbox2 = tkinter.Entry(hintwin, width=40)
                    textbox2.grid(column = 0 , row = 0)
                    textbox2.place(x=55,y=75)
                    putinbut = tkinter.Button(hintwin,text = '\n   입력   \n',command = start_pack)
                    putinbut.place(x = 170,y = 110)
                    
            f = open(filename)
            f.close()
            mainwin.destroy()
            time.sleep(0.5)
            enwin = tkinter.Tk()
            enwin.title('Cryptography V1')
            enwin.geometry('400x200+500+400')
            enwin.resizable(0,0)

            label1 = tkinter.Label(enwin, text='파일 : ' + filename)
            label1.place(x = 30,y = 10)
            label2 = tkinter.Label(enwin, text='비밀번호 설정 :')
            label2.place(x = 30,y = 50)
            textbox1 = tkinter.Entry(enwin, width=40)
            textbox1.grid(column = 0 , row = 0)
            textbox1.place(x=55,y=75)
            putinbut = tkinter.Button(enwin,text = '\n   입력   \n',command = start_en)
            putinbut.place(x = 170,y = 110)
            
            enwin.mainloop()
        except:
            i = tkinter.messagebox.showinfo('Error : 파일위치','파일을 찾을 수 없습니다.\n같은 폴더 내의 파일 이름과 확장자를 \n정확히 입력했는지 확인하십시오.')
        
    def decrypt():
        filename = textbox0.get()
        try:
            f = open(filename)
            f.close()

            raw = open(filename,'rb')
            magicnum_b = raw.read(4)
            salt_b = raw.read(40)
            hash1_b = raw.read(32)
            hint_b = raw.read(324)
            
            raw.close()

            if not magicnum_b == b'.kos':
                i = tkinter.messagebox.showinfo('Error : 파일손상','파일을 읽을 수 없습니다.\n파일 헤더가 손상되었는지 확인하십시오.')
            elif not filename[-2:] == '.k':
                i = tkinter.messagebox.showinfo('Error : 확장자 이상','파일 확장자가 .k 여야 합니다.\nExample.txt.k 와 같이 확장자를 변경해 주십시오.')
            else:
                salt = str( salt_b , 'utf-8' )
                hash1 = ''
                for i in hash1_b:
                    temp = hex(i)[2:]
                    if len(temp) == 1:
                        temp = '0' + temp
                    hash1 = hash1 + temp
                hint = str( hint_b , 'utf-8' )

                def decrypt():
                    time.sleep(0.2)
                    password = textbox3.get()
                    if hash1 == gethash1(salt + password):
                        key = gethash2( gethash1( password + salt ) , salt )
                        i = tkinter.messagebox.showinfo('변환 시작','파일 변환이 시작됩니다.\n파일이 위치한 폴더에 진행 사항이 표시됩니다.\n시간이 좀 걸릴 수 있습니다.')
                        dewin.destroy()
                        decrypt_sys(filename,key)
                        adwin = tkinter.Tk()
                        adwin.geometry('10x10+10+10')
                        time.sleep(0.5)
                        i = tkinter.messagebox.showinfo('변환 완료','파일 변환이 완료되었습니다.')
                        adwin.destroy()
                        
                    else:
                        i = tkinter.messagebox.showinfo('Error : 비밀번호 불일치','비밀번호가 일치하지 않습니다.\n다시 입력해 주십시오.')

                def seehint():
                    time.sleep(0.2)
                    i = tkinter.messagebox.showinfo('비밀번호 힌트보기',hint)

                mainwin.destroy()
                time.sleep(0.5)
                dewin = tkinter.Tk()
                dewin.title('Cryptography V1')
                dewin.geometry('400x200+500+400')
                dewin.resizable(0,0)
                label1 = tkinter.Label(dewin, text='비밀번호를 정확히 입력하세요')
                label1.place(x = 110,y = 10)
                textbox3 = tkinter.Entry(dewin, width=40)
                textbox3.grid(column = 0 , row = 0)
                textbox3.place(x=55,y=50)
                debut = tkinter.Button(dewin,text = '\n  입력  \n',command = decrypt)
                debut.place(x = 50,y = 110)
                hintbut = tkinter.Button(dewin,text = '\n 힌트보기 \n',command = seehint)
                hintbut.place(x = 270,y = 110)

                dewin.mainloop()
            
        except:
            i = tkinter.messagebox.showinfo('Error : 파일위치','파일을 찾을 수 없습니다.\n같은 폴더 내의 파일 이름과 확장자를 \n정확히 입력했는지 확인하십시오.')
        
    def endall():
        i = tkinter.messagebox.askokcancel('끝내기','종료하시겠습니까?')
        if not i == 0:
            mainwin.destroy()
            time.sleep(0.5)
            quit()
    
    mainwin = tkinter.Tk()
    mainwin.title('Cryptography V1')
    mainwin.geometry('400x200+500+400')
    mainwin.resizable(0,0)
    label1 = tkinter.Label(mainwin, text='파일이름을 확장자까지 정확하게 입력해 주세요')
    label1.place(x = 70,y = 10)
    textbox0 = tkinter.Entry(mainwin, width=40)
    textbox0.grid(column = 0 , row = 0)
    textbox0.place(x=55,y=50)
    enbut = tkinter.Button(mainwin,text = '\n 암호화 \n',command = encrypt)
    enbut.place(x = 50,y = 110)
    debut = tkinter.Button(mainwin,text = '\n 복호화 \n',command = decrypt)
    debut.place(x = 170,y = 110)
    endbut = tkinter.Button(mainwin,text = '\n 끝내기 \n',command = endall)
    endbut.place(x = 290,y = 110)
    
    mainwin.mainloop()

def encrypt_sys(filename,password,hint_b):
    salt = getsalt()
    hash1 = gethash1(salt + password)
    original = open(filename,'rb')
    new = open(filename+'.k','wb')
    new.write(b'.kos')
    new.write( bytes(salt,'utf-8') )
    new.write( bytes.fromhex(hash1) )
    new.write( hint_b )
    key = gethash2( gethash1( password + salt ),salt )

    converted = 0
    temp = original.read(1)
    f = open('0 MB','wb')
    f.close()
    k = '0'
    while not temp == b'':
        tempkey = key[ converted % 1024 ]
        towrite = plus(temp,tempkey)
        new.write(towrite)
        converted = converted + 1
        temp = original.read(1)
        if converted % (1048576*5) == 0:
            k = converted // 1048576
            j = k - 5
            k = str(k)
            j = str(j)
            os.remove(j + ' MB')
            f = open(k + ' MB','wb')
            f.close()

    os.remove(k + ' MB')
    original.close()
    new.close()
    global mainconst
    mainconst = 1

def decrypt_sys(filename,key):
    time.sleep(0.5)
    old = open(filename,'rb')
    new = open(filename[:-2],'wb')

    temp = old.read(400)
    converted = 0
    temp = old.read(1)
    f = open('0 MB','wb')
    f.close()
    k = '0'

    while not temp == b'':
        tempkey = key[ converted % 1024 ]
        towrite = minus(temp,tempkey)
        new.write(towrite)
        converted = converted + 1
        temp = old.read(1)
        if converted % (1048576*5) == 0:
            k = converted // 1048576
            j = k - 5
            k = str(k)
            j = str(j)
            os.remove(j + ' MB')
            f = open(k + ' MB','wb')
            f.close()

    os.remove(k + ' MB')
    old.close()
    new.close()
    global mainconst
    mainconst = 1

def getsalt():
    output = ''
    for i in range(0,40):
        output = output + chr(random.randrange(32,126))
    return output

def gethash1(letter):
    myhash = hashlib.sha256( ( letter ).encode( 'utf-8' ) ).hexdigest()
    return myhash

def gethash2(hashin,salt):
    output = [ ]
    rawhash = [ ]
    for i in range(0,32):
        rawhash.append( hashin[ 2 * i : 2 * i + 2 ] )
    for i in rawhash:
        temp = gethash1(i + salt)
        for j in range(0,32):
            output.append( temp[ 2 * j : 2 * j + 2 ] )
    return output

def plus(a,b):
    c = int.from_bytes(a,byteorder = 'big')
    d = int(b,base = 16)
    e = (c + d) % 256
    e = hex(e)[2:]
    if len(e) == 1:
        e = '0' + e
    return bytes.fromhex(e)

def minus(a,b):
    c = int.from_bytes(a,byteorder = 'big')
    d = int(b,base = 16)
    e = (c - d) % 256
    e = hex(e)[2:]
    if len(e) == 1:
        e = '0' + e
    return bytes.fromhex(e)

global mainconst
mainconst = 1
while mainconst == 1:
    mainconst = 0
    time.sleep(0.5)
    main()

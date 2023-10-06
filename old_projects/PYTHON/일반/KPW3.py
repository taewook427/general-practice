import os
import shutil
import time

import random
import secrets
from Cryptodome.Cipher import AES
import hashlib
from zlib import crc32
import base64

from PIL import Image

import tkinter
import tkinter.ttk
from tkinter import filedialog

import oreo

class infunc:

    def en(self,number,length): #리틀 엔디안 인코딩
        k = [ ]
        for i in range( 0,length ):
            k.append( number % 256 )
            number = number // 256
        j = bytes( { k[0] } )
        for i in range( 1,len(k) ):
            j = j + bytes( { k[i] } )
        return j

    def de(self,binary): #리틀 엔디안 디코딩
        value = 0
        for i in range( 0,len(binary) ):
            k = 256 ** i
            k = k * binary[i]
            value = value + k
        return value

    def getpwhash(self,salt,kf,pw): #salt 바이트 keyfile 바이트 pw str
        pw = bytes(pw,encoding='utf-8') #pw 바이트
        tool = infunc()
        func = tool.gethash
        init = pw #init byte
        for i in range(0,100):
            init = func(init + kf,'sha3512')
            for j in range(0,5000):
                init = func(salt + init,'sha3512')
                init = func(init + salt,'sha3512')
        return init #64 바이트

    def getmasterkey(self,salt,kf,pw): #salt 바이트 keyfile 바이트 pw str
        pw = bytes(pw,encoding='utf-8') #pw 바이트
        tool = infunc()
        func = tool.gethash
        pw = bytes( reversed(pw) )
        salt = bytes( reversed(salt) )
        kf = bytes( reversed(kf) )
        init = pw #init byte
        for i in range(0,10):
            init = func(init + kf,'sha3512')
            for j in range(0,5000):
                init = func(salt + init,'sha3512')
                init = func(init + salt,'sha3512')
        return init #64 바이트

    def enshort(self,key,iv,data): #짧은 데이터 암호화, 입력은 바이트, 패딩 있음
        num = len(data)//16 #16바이트 num개 블록 + 추가 1 블록 패딩
        out = [0] * (num + 1) * 16
        func = AES.new(key,AES.MODE_CBC,iv)
        func = func.encrypt
        for i in range(0,num):
            ii = 16 * i
            iii = ii + 16
            out[ii:iii] = func( data[ii:iii] )
        pad = lambda x : x + bytes(chr(16 - len(x)),'utf-8') * (16 - len(x))
        out[16 * num : 16 * num + 16] = func( pad( data[16 * num:] ) )
        return bytes(out) #10MB당 1.4s 정도

    def deshort(self,key,iv,data): #짧은 데이터 복호화, 입력은 바이트, 패딩 있음
        num = ( len(data)//16 ) - 1 #non pad chunk + pad chunk 1
        out = [0] * num * 16
        func = AES.new(key,AES.MODE_CBC,iv)
        func = func.decrypt
        for i in range(0,num):
            ii = 16 * i
            iii = ii + 16
            out[ii:iii] = func( data[ii:iii] )
        unpad = lambda x : x[:-x[-1]]
        ii = 16 * num
        iii = ii + 16
        temp = unpad( func( data[ii:iii] ) )
        out = bytes(out) + temp
        return out #10MB당 1.4s 정도

    def getrandom(self,seed,size): #진짜 랜덤, 시드는 바이트, 사이즈는 정수
        tool = infunc()
        func = tool.gethash #해시 구하기
        rfunc = secrets.randbelow #랜덤 숫자 생성
        seed = func(seed*(rfunc(256)+256),'sha3512') #시드는 64바이트
        num = size // 32 #32바이트 끊기
        add = size % 32
        out = [0] * size
        for i in range(0,num):
            rdata = [0] * 64 #64바이트 난수 생성
            for j in range(0,64):
                rdata[j] = rfunc(256)
            rdata = bytes(rdata)
            r0 = rfunc(32)
            r1 = rfunc(32)
            r2 = rfunc(32)
            temp = func( rdata[r0:r0+32] + seed[r1:r1+32],'sha3512' )
            tempp = 32 * i
            out[tempp:tempp+32] = temp[r2:r2+32]
        if add != 0:
            rdata = [0] * 64 #64바이트 난수 생성
            for j in range(0,64):
                rdata[j] = rfunc(256)
            rdata = bytes(rdata)
            r0 = rfunc(32)
            r1 = rfunc(32)
            r2 = rfunc(32)
            temp = func( rdata[r0:r0+32] + seed[r1:r1+32],'sha3512' )
            tempp = 32 * num
            out[tempp:tempp+add] = temp[r2:r2+add]
        return bytes(out) #size 바이트 만큼 내보내기 10MB 당 17s 정도

    def gethash(self,data,mode): #해시구하기
        tp = type(data) #바이트, 문자열, 정수 등 받음
        if tp == str: #모드는 문자열
            data = bytes(data,encoding='utf-8')
        elif tp != bytes:
            data = bytes(str(data),encoding='utf-8')
        if mode == 'crc32':
            temp = crc32(data)
            out = [0,0,0,0]
            out[3] = temp % 256
            temp = temp // 256
            out[2] = temp % 256
            temp = temp // 256
            out[1] = temp % 256
            temp = temp // 256
            out[0] = temp % 256
            temp = temp // 256
            return bytes(out) #4바이트
        elif mode == 'sha3512':
            temp = hashlib.sha3_512(data).hexdigest()
            return bytes.fromhex(temp) #64바이트
        elif mode == 'sha2256':
            temp = hashlib.sha256(data).hexdigest()
            return bytes.fromhex(temp) #32바이트
        elif mode == 'sha2512':
            temp = hashlib.sha512(data).hexdigest()
            return bytes.fromhex(temp) #64바이트
        elif mode == 'md5':
            temp = hashlib.md5(data).hexdigest()
            return bytes.fromhex(temp) #16바이트
        else:
            return b'' #목록에 없음

    def b64en(self,data): #base64 인코딩, 입력은 바이트
        data = base64.b64encode(data) # +:$ /:% =:&
        data = str(data,encoding='utf-8')
        data = data.replace('+','$')
        data = data.replace('/','%')
        data = data.replace('=','&')
        return data #출려은 문자열

    def b64de(self,data): #base64 디코딩, 입력은 문자열
        data = data.replace('$','+') # +:$ /:% =:&
        data = data.replace('%','/')
        data = data.replace('&','=')
        data = base64.b64decode(data)
        return data #출력은 바이트

    def getkeyfile(self,path):
        try:
            with open(path,'rb') as f:
                temp = f.read()
        except:
            temp = b'580sd8gfgjf92fc3857fjj2309478572382390vjfjwifdjf8v3785249057vwdfj904689324n89k90fdkc73458k823475686890vmtjdfvg9k87b683489013458k90jgfdfiosjkv9f3498u23yubt98458'
        return temp

    def readpng(self,path): # png to data byte
        temp = Image.open(path)
        temp.save('bp.bmp')
        with open('bp.bmp','rb') as f:
            bmp = f.read() # bmp data
        os.remove('bp.bmp')
        size = bmp[10] + bmp[11] * 256 + bmp[12] * 65536 + bmp[13] * 16777216
        bmpmain = bmp[size:]
        size = len(bmpmain) // 4 #output size
        out = [0] * size
        for i in range(0,size):
            temp = i * 4
            out[i] = (bmpmain[temp] % 4) * 64 + (bmpmain[temp+1] % 4) * 16 + (bmpmain[temp+2] % 4) * 4 + (bmpmain[temp+3] % 4)
        return bytes(out)

    def writepng(self,path,data): #png path, short byte data
        data = list(data) # 0 ~ 255 int list
        size = len(data)
        tow = [0,0,0,0] * size #쓸 데이터
        for i in range(0,size):
            temp = data[i]
            t = 4 * i
            tow[t] = temp // 64
            temp = temp % 64
            tow[t + 1] = temp // 16
            temp = temp % 16
            tow[t + 2] = temp // 4
            temp = temp % 4
            tow[t + 3] = temp # 0 ~ 3 int list
        temp = Image.open('bp.png')
        temp.save('bp.bmp')
        with open('bp.bmp','rb') as f:
            bmp = f.read() #bmp file byte
        os.remove('bp.bmp')
        size = bmp[10] + bmp[11] * 256 + bmp[12] * 65536 + bmp[13] * 16777216
        bmphead = bmp[0:size]
        bmpmain = bmp[size:]
        tow = tow + [0] * ( len(bmpmain) - 4 * len(data) ) # tow padding
        new = [0] * len(bmpmain)
        for i in range( 0,len(bmpmain) ):
            new[i] = 4 * (bmpmain[i] // 4) + tow[i]
        with open('bp.bmp','wb') as f:
            f.write( bmphead + bytes(new) )
        temp = Image.open('bp.bmp')
        temp.save(path)
        os.remove('bp.bmp') # 2048 x 2048 -> ~3MB data

class mainclass:

    def init(self):
        tool = infunc()
        try:
            data = tool.readpng('k.png') # data byte
            if data[0:3] != b'KP3':
                raise Exception('Magic Num Err') # 매직넘버 불일치
            else:
                hs = tool.de( data[3:5] ) #헤더크기
                ds = tool.de( data[5:8] ) #데이터크기
                crc = data[8:12] #crc byte
                head = data[16:16+hs] #head byte
                data = data[16+hs:16+hs+ds] #data byte
                if tool.gethash(head + data,'crc32') != crc:
                    raise Exception('Hash Err') # 해시값 불일치
                else:
                    return [head,data]
        except Exception as e:
            pw = '0000' #기본 비밀번호
            kf = tool.getkeyfile('') #기본 키파일
            hint = '비밀번호 저장 파일이\n없거나 깨졌습니다.\n새 비밀번호 저장 파일이\n생성 되었습니다.\n초기 비밀번호 0000' #기본 힌트 H str
            ckey = b'\x00' * 32 # ckey
            salt = b'\x00' * 64 # salt H
            td = int( time.time() ) # time data H int
            pwhash = tool.b64en( tool.getpwhash(salt,kf,pw) ) #pw hash H str
            mkey = tool.getmasterkey(salt,kf,pw) #mkey dt
            content = tool.enshort( ckey, mkey[48:64], bytes('[data]{[num]{1}[0]{"welcome#nKOS#s2023#nKOS-KPW3"}}',encoding='utf-8') ) #실제 내묭 바이트
            ckeydt = tool.b64en( tool.enshort( mkey[0:32], mkey[32:48], ckey ) ) #ckeydt H str
            otool = oreo.toolbox()
            temp = otool.mkobj('header')
            otool.putdt(temp,'pwhash',pwhash)
            otool.putdt(temp,'hint',hint)
            otool.putdt( temp,'salt',tool.b64en(salt) ) #salt H str
            otool.putdt(temp,'ckeydt',ckeydt)
            otool.putdt(temp,'time',td)
            header = bytes( otool.rtoe( otool.wrcom(temp.data,True,True),'BKLOVE' ),encoding='utf-8' ) #실제 헤더 바이트
            temp = b'KP3' + tool.en(len(header),2) + tool.en(len(content),3) + tool.gethash(header + content,'crc32') + b'\x00\x00\x00\x00' + header + content #실제 기록 바이트
            tool.writepng('k.png',temp) #새로 기록
            return [header,content]

    def pwfunc(self,head,content): #비밀번호 입력
        otool = oreo.toolbox()
        head = otool.readstr( otool.etor( str(head,'utf-8'),'BKLOVE' ) )
        tool = infunc()
        pwhash = tool.b64de( head['header#pwhash'] ) #pwhash byte
        hint = head['header#hint'] #hint str
        salt = tool.b64de( head['header#salt'] ) #salt byte
        ckeydt = tool.b64de( head['header#ckeydt'] ) #ckeydt byte
        td = head['header#time'] #time int
        
        win = tkinter.Tk()
        win.title('KOS 2023')
        win.geometry("400x300+100+50")
        win.resizable(False, False)

        label0 = tkinter.Label( win, font=("맑은 고딕",14), text = hint )
        label0.place(x=5,y=5)

        in0 = tkinter.Entry(width=30, font = ("맑은 고딕",14), show = '●')
        in0.grid(column = 0 , row = 0)
        in0.place(x=5,y=205)

        wrong = 0
        def getdt():
            time.sleep(0.1)
            nonlocal in0
            nonlocal but0
            pw = in0.get() #password

            nonlocal wrong
            nonlocal pwhash
            nonlocal salt
            nonlocal ckeydt
            nonlocal td
            nonlocal content
            nonlocal hint
            nonlocal re
            nonlocal win

            tool = infunc()
            nonlocal kfpath
            kf = tool.getkeyfile( kfpath.get() ) #keyfile
            if pwhash == tool.getpwhash(salt,kf,pw):
                mkey = tool.getmasterkey(salt,kf,pw)
                ckey = tool.deshort(mkey[0:32],mkey[32:48],ckeydt)
                data = tool.deshort(ckey,mkey[48:64],content)
                re = [pw,kfpath.get(),hint,data,td]
                win.destroy()
            else:
                wrong = wrong + 1
                if wrong < 5:
                    time.sleep(1)
                else:
                    re = ['0000','기본키파일',hint,b'[data]{[num]{1}[0]{"top#ssecret#nfwb19010f9"}}',int(time.time())-7200] #pw kf hint content time
                    win.destroy()
            
        but0 = tkinter.Button(win, text = '입력', font = ("맑은 고딕",14), command = getdt)
        but0.place(x = 330,y = 200)

        def getkf():
            time.sleep(0.1)
            nonlocal kfpath
            try:
                kfpath.set( filedialog.askopenfile(title='파일 선택').name )
            except:
                kfpath.set('기본키파일')
            nonlocal win
            win.update()
            
        kfpath = tkinter.StringVar()
        kfpath.set('기본키파일')
        but1 = tkinter.Button(win, text = ' . . . ', font = ("맑은 고딕",14), command = getkf)
        but1.place(x = 330,y = 250)

        label1 = tkinter.Label( win, font=("맑은 고딕",14), textvariable = kfpath )
        label1.place(x=5,y=250)

        re = [ ]
        win.mainloop()
        return re

    def mainfunc(self,pw,kfp,hint,content,td):
        thumb = [ ] #썸네일
        for i in content:
            thumb.append( i.split('\n')[0] )
        
        win = tkinter.Tk()
        win.title('KOS 2023')
        win.geometry("700x600+100+50")
        win.resizable(False, False)

        frame = tkinter.Frame(win)
        frame.place(x=5,y=5)
        listbox = tkinter.Listbox( frame, width=40,  height=10, font = ("맑은 고딕",14) )
        listbox.pack(side="left", fill="y")
        scrollbar0 = tkinter.Scrollbar(frame, orient="vertical")
        scrollbar0.config(command=listbox.yview)
        scrollbar0.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar0.set)

        for i in thumb:
            listbox.insert( listbox.size(),i )

        view = tkinter.StringVar()
        view.set('') #표시 내용
        label0 = tkinter.Label( win, font = ("맑은 고딕",14), textvariable = view )
        label0.place(x=5,y=270)

        in0 = tkinter.Text( width=40, height=6, font = ("맑은 고딕",14) )
        in0.grid(column = 0 , row = 0)
        in0.place(x=5,y=430) #내용 입력창

        tstr = tkinter.StringVar()
        tstr.set( 'Last Save ' + time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( td ) ) ) #시간 문자열
        label1 = tkinter.Label( win, font = ("맑은 고딕",14), textvariable = tstr )
        label1.place(x=430,y=5) #마지막 저장 시간 표시

        pwstr = tkinter.StringVar()
        if len(pw) > 2:
            pwstr.set( 'PW ' + pw[0] + '●' * (len(pw)-2) + pw[-1] )
        else:
            pwstr.set( 'PW ' + '●' * len(pw) )
        label2 = tkinter.Label( win, font = ("맑은 고딕",14), textvariable = pwstr )
        label2.place(x=430,y=40) #비밀번호 표시

        in1 = tkinter.Entry( width=25, font = ("맑은 고딕",14), show = '●' )
        in1.grid(column = 0 , row = 0)
        in1.place(x=430,y=80) #pw 수정 입력

        def getkf():
            time.sleep(0.1)
            nonlocal kfpath
            try:
                kfpath.set( filedialog.askopenfile(title='파일 선택').name )
            except:
                kfpath.set('기본키파일')
            nonlocal win
            save()
            win.update()
            
        kfpath = tkinter.StringVar()
        kfpath.set(kfp)
        but1 = tkinter.Button(win, text = '. . .', font = ("맑은 고딕",14), command = getkf)
        but1.place(x = 430,y = 120)

        label3 = tkinter.Label( win, font = ("맑은 고딕",14), textvariable = kfpath )
        label3.place(x=480,y=125) #키 파일 경로 표시

        addnum = 0
        def but2ord():
            time.sleep(0.1)
            nonlocal win
            nonlocal thumb
            nonlocal content
            nonlocal listbox
            nonlocal addnum
            thumb = thumb + ['새 항목 '+str(addnum)]
            content = content + ['새 항목 '+str(addnum)]
            listbox.insert( listbox.size(),thumb[-1] )
            addnum = addnum + 1
            save()
        but2 = tkinter.Button(win, text = '항목추가', font = ("맑은 고딕",14), command = but2ord)
        but2.place(x = 430,y = 170)

        def but3ord():
            time.sleep(0.1)
            nonlocal win
            nonlocal thumb
            nonlocal content
            nonlocal listbox
            temp = listbox.curselection()[0]
            del thumb[temp]
            del content[temp]
            listbox.delete( temp,temp )
            save()
        but3 = tkinter.Button(win, text = '항목삭제', font = ("맑은 고딕",14), command = but3ord)
        but3.place(x = 550,y = 170)

        def but4ord():
            time.sleep(0.1)
            nonlocal in1 #pw in
            nonlocal in2 #hint
            nonlocal pwstr
            nonlocal hstr
            nonlocal pw
            pw = in1.get()
            nonlocal hint
            hint = in2.get('1.0','end')[0:-1]
            if len(pw) > 2:
                pwstr.set( 'PW ' + pw[0] + '●' * (len(pw)-2) + pw[-1] )
            else:
                pwstr.set( 'PW ' + '●' * len(pw) )
            hstr.set(hint)
            save()
        but4 = tkinter.Button(win, text = '암호수정', font = ("맑은 고딕",14), command = but4ord)
        but4.place(x = 430,y = 220)

        def but5ord():
            time.sleep(0.1)
            nonlocal thumb
            nonlocal content
            nonlocal listbox
            nonlocal view
            nonlocal in0
            temp = listbox.curselection()[0] #현재 항목 번호
            data = in0.get('1.0','end')[0:-1] #항목 값
            content[temp] = data
            thumb[temp] = data.split('\n')[0]
            view.set(data)
            listbox.delete( temp,temp )
            listbox.insert( temp,thumb[temp] )
            save()
        but5 = tkinter.Button(win, text = '항목저장', font = ("맑은 고딕",14), command = but5ord)
        but5.place(x = 550,y = 220)
        
        hstr = tkinter.StringVar()
        hstr.set(hint)
        label4 = tkinter.Label( win, font = ("맑은 고딕",14), textvariable = hstr )
        label4.place(x=430,y=270) #힌트 표시

        in2 = tkinter.Text( width=25, height=6, font = ("맑은 고딕",14) )
        in2.grid(column = 0 , row = 0)
        in2.place(x=430,y=430) #힌트 입력창

        def click(event):
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal view
            nonlocal content
            temp = listbox.curselection()[0]
            view.set( content[temp] )
            win.update()
        listbox.bind('<ButtonRelease-1>',click)

        def save():
            nonlocal td #td int
            td = int( time.time() )
            
            tool = infunc()
            otool = oreo.toolbox()
            nonlocal pw #pw str
            nonlocal kfpath
            kf = tool.getkeyfile( kfpath.get() ) #kf byte
            nonlocal hint #hint str
            ckey = tool.getrandom(bytes( str( int( time.time() ) ),encoding='utf-8' ),32) #ckey byte
            salt = tool.getrandom(bytes( str( int( time.time() ) ),encoding='utf-8' ),64) #salt byte
            pwhash = tool.b64en( tool.getpwhash(salt,kf,pw) ) #pw hash str
            mkey = tool.getmasterkey(salt,kf,pw) #mkey byte
            nonlocal content
            temp = otool.mkobj('data')
            for i in range( 0,len(content) ):
                otool.putdt( temp,str(i),content[i] )
            otool.putdt( temp,'num',len(content) )
            temp = otool.wrcom(temp.data,True,True)
            data = tool.enshort( ckey, mkey[48:64], bytes(temp,encoding='utf-8') ) #content byte
            ckeydt = tool.b64en( tool.enshort( mkey[0:32], mkey[32:48], ckey ) ) #ckeydt str
            temp = otool.mkobj('header')
            otool.putdt(temp,'pwhash',pwhash)
            otool.putdt(temp,'hint',hint)
            otool.putdt( temp,'salt',tool.b64en(salt) )
            otool.putdt(temp,'ckeydt',ckeydt)
            otool.putdt(temp,'time',td)
            header = bytes( otool.rtoe( otool.wrcom(temp.data,True,True),'BKLOVE' ),encoding='utf-8' ) #header byte
            temp = b'KP3' + tool.en(len(header),2) + tool.en(len(data),3) + tool.gethash(header + data,'crc32') + b'\x00\x00\x00\x00' + header + data #실제 기록 바이트
            tool.writepng('k.png',temp) #새로 기록

            nonlocal tstr
            tstr.set( 'Last Save ' + time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( td ) ) ) #시간 문자열
            nonlocal win
            win.update()
            
        win.mainloop()

k = mainclass()
p = k.init()
t = k.pwfunc( p[0], p[1] ) #pw kfpath hint content time
if t != [ ]:
    otool = oreo.toolbox()
    temp = otool.readstr( str(t[3],'utf-8') )
    num = temp['data#num']
    data = [ ]
    for i in range(0,num):
        data.append( temp['data#'+str(i)] )
    k.mainfunc(t[0],t[1],t[2],data,t[4])
time.sleep(0.5)

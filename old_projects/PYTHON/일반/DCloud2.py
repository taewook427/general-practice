import tkinter
import tkinter.messagebox
import tkinter.ttk
from tkinter import filedialog
import time
import random
import hashlib
import os
from Cryptodome.Cipher import AES
from PIL import Image
import shutil
import webbrowser

class mainsys:
    def mainsys(self):
        kvar = 1
    
        mainwin = tkinter.Tk()
        mainwin.title('DCloud V2')
        mainwin.geometry('200x200+500+400')
        mainwin.resizable(0,0)
        
        def info():
            
            infotitle = 'DCloud V2 INFO'
            infocontent = '''이 프로그램은 인터넷 커뮤니티의 게시판을 클라우드처럼 사용하는 것을 목표로 개발되었습니다. 사진 속에 데이터를 싣어서 커뮤니티 상에서 전송하고, 다시 사진을 받아 파일을 복구하세요. 파일 복구 시, 사진들은 모두 한 폴더 안에 모여 있어야 합니다.

이 프로그램으로 담을 수 있는 파일은 최대 100 MB 입니다. 변환 결과로 나오는 사진을 변경하고 싶다면, 프로그램이 위치한 곳에 있는 source.png 사진을 변경하십시오. 단, 전체 픽셀의 수는 짝수여야 합니다. 일부 사진은 작동에 오류를 일으킬 수 있습니다.

커뮤니티마다 사진 업로드 제한이 있으니, 이에 맞춰서 적당한 사진을 사용하시면 됩니다. 기본적으로 제공되는 사진은 2600 X 2600 픽셀로, 장당 최대 9.5 MB 를 저장 할 수 있습니다.

사진에서 파일 복구 시, 원래 결과물로 나온 사진의 이름과 해상도, 색상 등이 유지되어야 합니다. 사진을 다른 형식 (jpg 등) 으로 변경하면 데이터가 소실될 수 있습니다. 이 프로그램은 SHA3-512, AES-256을 사용해 암호화합니다. 비밀번호 분실 시 파일을 복구할 수 없으니, 파일 생성시 자신만 알도록 힌트를 잘 적어두시기 바랍니다.
\n>>> 인터넷을 시작할까요?\n
'''
            i = tkinter.messagebox.askokcancel(infotitle,infocontent)
            if not i == 0:
                time.sleep(0.5)
                if random.random() < 0.2:
                    url = 'https://gall.dcinside.com/mini/board/lists?id=soyuz'
                else:
                    url = 'https://gall.dcinside.com/mgallery/board/lists?id=djembe'
                webbrowser.open(url)
            
        def end():
            i = tkinter.messagebox.askokcancel('끝내기','종료하시겠습니까?')
            if not i == 0:
                nonlocal kvar
                kvar = 0
                mainwin.destroy()
                time.sleep(0.5)
                os.exit()
            
        def en():
            time.sleep(0.5)
            mainwin.destroy()
            
            enwin = tkinter.Tk()
            enwin.title('ENCRYPT')
            enwin.geometry('300x130+500+400')
            enwin.resizable(0,0)
            
            filename = tkinter.StringVar()
            fileloc = tkinter.StringVar()
            filename.set('-')
            fileloc.set('-')
            label0 = tkinter.Label(enwin, textvariable=fileloc)
            label0.place(x = 10,y = 10)
            label1 = tkinter.Label(enwin, textvariable=filename)
            label1.place(x = 10,y = 30)
            
            def sel():
                path = os.path.join(os.path.expanduser('~'),'Desktop')
                file = filedialog.askopenfile(initialdir=path, title='변환할 파일 선택', filetypes=(('all files', '*.*'),('png files', '*.png')))
                file = file.name
                k = file.rfind('/')
                fileloc.set(file[0:k+1])
                filename.set(file[k+1:])
                
            def gogo():
                floc = fileloc.get()
                fname = filename.get()
                pword = textbox0.get()
                hint = textbox1.get()
                if floc == '-':
                    time.sleep(0.5)
                    if pword == 'kos':
                        i = tkinter.messagebox.askokcancel('개발자',' K O S   2 0 2 2 \n\n>>> Go To Storage ?')
                        if not i == 0:
                            time.sleep(0.5)
                            url = 'https://gall.dcinside.com/mini/board/lists?id=soyuz'
                            webbrowser.open(url)
                else:
                    fsize = os.path.getsize(floc + fname) 
                    if fsize > 104857600:
                        i = tkinter.messagebox.showinfo('파일 크기 경고','파일 크기는 100 MB 이하여야 합니다.')
                    elif len( hint.encode('utf-8') ) > 60:
                        i = tkinter.messagebox.showinfo('힌트 길이 경고','힌트 길이는 60 바이트 이하여야 합니다.')
                    elif len( fname.encode('utf-8') ) > 64:
                        i = tkinter.messagebox.showinfo('파일명 길이 경고','파일 이름은 64 바이트 이하여야 합니다.')
                    else:
                        i = tkinter.messagebox.askokcancel('변환 준비','파일이 사진으로 변환됩니다.\n변환된 사진들은 바탕 화면에 한 폴더로 모입니다.\n이 작업은 시간이 걸릴 수 있습니다.')
                        if not i == 0:
                            enwin.destroy()
                            dowork = ensys()
                            dowork.mainsys(floc,fname,pword,hint)
            
            selbut = tkinter.Button(enwin,text = '. . .',command = sel)
            selbut.place(x = 10,y = 80)
            gobut = tkinter.Button(enwin,text = ' 변환 \n 진행 ',command = gogo)
            gobut.place(x = 240,y = 70)
            
            label0 = tkinter.Label(enwin, text='비밀번호')
            label0.place(x = 55,y = 70)
            textbox0 = tkinter.Entry(enwin, width=15)
            textbox0.grid(column = 0 , row = 0)
            textbox0.place(x=120,y=70)
            label1 = tkinter.Label(enwin, text='암호힌트')
            label1.place(x = 55,y = 95)
            textbox1 = tkinter.Entry(enwin, width=15)
            textbox1.grid(column = 0 , row = 0)
            textbox1.place(x=120,y=95)
            
        def de():
            time.sleep(0.5)
            mainwin.destroy()
            
            dewin = tkinter.Tk()
            dewin.title('DECRYPT')
            dewin.geometry('300x130+500+400')
            dewin.resizable(0,0)
            filename = tkinter.StringVar()
            fileloc = tkinter.StringVar()
            filename.set('0')
            fileloc.set('-')
            label0 = tkinter.Label(dewin, textvariable=fileloc)
            label0.place(x = 10,y = 10)
            label1 = tkinter.Label(dewin, textvariable=filename)
            label1.place(x = 10,y = 30)
            label2 = tkinter.Label(dewin, text='개 발견된 파일')
            label2.place(x = 30,y = 30)
            
            dovar = 0
            
            def sel():
                if dovar == 0:
                    path = os.path.join(os.path.expanduser('~'),'Desktop')
                    file = filedialog.askdirectory(initialdir=path, title='사진이 있는 폴더 선택')
                    fileloc.set(file)
                    
                    filenum = 0
                    k = 0
                    while k == 0:
                        try:
                            temp = open(file+'/'+str(filenum)+'.png','rb')
                            temp.close()
                            filenum = filenum + 1
                        except:
                            k = 1
                    filename.set( str(filenum) )
                
            def gogo():
                nonlocal dovar
                if dovar == 0:
                    floc = fileloc.get()
                    fnum = int( filename.get() )
                    if fnum == 0:
                        time.sleep(0.5)
                    else:
                        i = tkinter.messagebox.askokcancel('변환 준비','사진이 파일로 변환됩니다.\n변환된 파일은 바탕 화면에 표시됩니다.\n이 작업은 시간이 걸릴 수 있습니다.')
                        if not i == 0:
                            dovar = 1
                            os.mkdir('temp')
                            num3 = tkinter.DoubleVar()
                            var3 = tkinter.ttk.Progressbar(dewin,maximum=fnum,variable = num3,length=180)
                            var3.place(x = 50,y = 80)
                            dewin.update()
                            dowork = desys()
                            
                            for i in range(0,fnum):
                                fimage = Image.open(floc+'/'+str(i)+'.png')
                                fimage.save('temp\\'+str(i)+'.bmp')
                                dowork.mktemp(i)
                                num3.set(i+1)
                                dewin.update()
                                
                            time.sleep(0.5)
                            dewin.destroy()
                            dowork.mainsys()
            
            selbut = tkinter.Button(dewin,text = '. . .',command = sel)
            selbut.place(x = 10,y = 80)
            gobut = tkinter.Button(dewin,text = ' 변환 \n 진행 ',command = gogo)
            gobut.place(x = 240,y = 70)
            
        
        infobut = tkinter.Button(mainwin,text = '\n  INFO  \n',command = info)
        infobut.place(x = 30,y = 30)
        endbut = tkinter.Button(mainwin,text = '\n  END   \n',command = end)
        endbut.place(x = 30,y = 110)
        enbut = tkinter.Button(mainwin,text = '\n  toPIC  \n',command = en)
        enbut.place(x = 110,y = 30)
        debut = tkinter.Button(mainwin,text = '\n  toFile  \n',command = de)
        debut.place(x = 110,y = 110)
        
        mainwin.mainloop()
        return kvar
        
class ensys:
    def mainsys(self,floc,fname,pword,hint):
        pwin = tkinter.Tk()
        pwin.title('변환 중 . . .')
        pwin.geometry('200x120+500+400')
        pwin.resizable(0,0)
        label0 = tkinter.Label(pwin, text=floc)
        label0.pack()
        label1 = tkinter.Label(pwin, text=fname+'\n')
        label1.pack()
        txt2 = tkinter.StringVar()
        txt2.set('상태 : '+'준비 중 . . .')
        label2 = tkinter.Label(pwin, textvariable=txt2)
        label2.pack()
        pwin.update()
    
        os.mkdir('temp')
        
        hint = hint + ' '*60
        hint = hint.encode('utf-8')
        hint = hint[0:60]
        
        tool = utility()
        salt = tool.getsalt()
        pwhash = bytes.fromhex( tool.geth3512(pword + salt) )
        key = bytes.fromhex( tool.geth2256(salt + pword) )
        iv = bytes.fromhex( tool.gethmd5(salt) )
        
        maincon = tool.doen(floc + fname,key,iv)

        fname = fname + ' '*64
        fname = fname.encode('utf-8')
        fname = fname[0:64]
        fsize = len(maincon)
        fsize = tool.encode(fsize)
        salt = salt.encode('utf-8')
        header = salt + pwhash + hint + fname + fsize
        
        simg = Image.open('source.png')
        bperi = int( ( simg.size[0] * simg.size[1] ) * 3 / 2 )
        bext = ( bperi - ( ( len(header) + len(maincon) ) % bperi ) ) % bperi
        temp = header + maincon + b'\x00'*bext
        f = open('temp\\towrite','wb')
        f.write(temp)
        f.close()
        repeat = len(temp) // bperi
        temp = 0
        
        simg.save('temp\\source.bmp')
        f = open('temp\\source.bmp','rb')
        bmphead = f.read(10)
        bmphead = tool.decode( f.read(4) )
        f.close()
        f = open('temp\\source.bmp','rb')
        bmphead = f.read(bmphead)
        bmpmain = f.read()
        f.close()
        
        num3 = tkinter.DoubleVar()
        var3 = tkinter.ttk.Progressbar(pwin,maximum=repeat+2,variable = num3,length=150)
        var3.pack()
        
        f = open('temp\\towrite','rb')
        for i in range(0,repeat):
            txt2.set('상태 : '+str(i)+'.bmp')
            num3.set(i+1)
            pwin.update()
            
            temp = open('temp\\'+str(i)+'.bmp','wb')
            temp.write(bmphead)
            tow = f.read(bperi)
            for j in range(0,bperi):
                num = tow[j]
                loc1 = num // 16
                loc2 = num % 16
                tgt1 = bmpmain[j*2]
                tgt2 = bmpmain[j*2+1]
                wrt1 = bytes( { 16*(tgt1 // 16) + loc1} )
                wrt2 = bytes( { 16*(tgt2 // 16) + loc2} )
                temp.write(wrt1+wrt2)
            temp.close()
        f.close()
        
        temp = 0
        tow = 0
        path = os.path.join(os.path.expanduser('~'),'Desktop')
        txt2.set('상태 : '+'저장 중 . . .')
        num3.set(repeat+1)
        pwin.update()
        try:
            os.mkdir(path + '\\result')
            path = path + '\\result\\'
            k = 0
        except:
            os.mkdir('result')
            path = 'result\\'
            k = 1
        for i in range(0,repeat):
            temp = Image.open('temp\\'+str(i)+'.bmp')
            temp.save(path + str(i) + '.png')
        shutil.rmtree('temp')
        num3.set(repeat+2)
        pwin.update()
        if k == 0:
            i = tkinter.messagebox.showinfo('파일 변환 완료','바탕화면 result 폴더 안에 결과물 사진이 들어 있습니다.\n처음으로 돌아갑니다.')
        else:
            i = tkinter.messagebox.showinfo('파일 변환 완료','바탕화면에 접근할 수 없습니다.\n프로그램이 위치한 폴더 안의 result 디렉토리에 결과물 사진이 들어 있습니다.\n처음으로 돌아갑니다.')
        time.sleep(0.5)
        pwin.destroy()
        
class desys():
    def mktemp(self,num):
        f = open('temp\\'+str(num)+'.bmp','rb')
        tgt = open('temp\\temp','ab')
        tool = utility()
        bmphead = f.read(10)
        bmphead = tool.decode( f.read(4) )
        f.close()
        f = open('temp\\'+str(num)+'.bmp','rb')
        temp = f.read(bmphead)
        temp = f.read()
        
        for i in range( 0,int( len(temp)/2 ) ):
            loc1 = temp[i*2] % 16
            loc2 = temp[i*2 + 1] % 16
            num = bytes( {loc1*16 + loc2} )
            tgt.write(num)
        
        f.close()
        tgt.close()
    def mainsys(self):
        tool = utility()
        tgt = open('temp\\temp','rb')
        salt = str( tgt.read(64) , 'utf-8' )
        pwhash = tgt.read(64)
        hint = str( tgt.read(60) , 'utf-8' )
        filename = str( tgt.read(64) , 'utf-8' )
        filesize = tool.decode( tgt.read(4) )
        tgt.close()
        
        pwin = tkinter.Tk()
        pwin.title('비밀번호 입력')
        pwin.geometry('200x120+500+400')
        pwin.resizable(0,0)
        label0 = tkinter.Label(pwin, text=hint[0:15]+'\n'+hint[15:30]+'\n'+hint[30:45]+'\n'+hint[45:60])
        label0.place(x = 5,y = 5)
        textbox0 = tkinter.Entry(pwin, width=12)
        textbox0.grid(column = 0 , row = 0)
        textbox0.place(x=5,y=90)
        
        def gogo():
            pword = textbox0.get()
            hashb = bytes.fromhex( tool.geth3512(pword + salt) )
            key = bytes.fromhex( tool.geth2256(salt + pword) )
            iv = bytes.fromhex( tool.gethmd5(salt) )
            if hashb == pwhash:
                i = tkinter.messagebox.askokcancel('변환 준비','원본 파일이 생성됩니다.\n변환된 파일은 바탕 화면에 표시됩니다.\n이 작업은 시간이 걸릴 수 있습니다.')
                if not i == 0:
                    time.sleep(0.5)
                    pwin.destroy()
                    temp = tool.dode(filesize,key,iv)
                    
                    path = os.path.join(os.path.expanduser('~'),'Desktop')
                    try:
                        os.mkdir(path + '\\result')
                        path = path + '\\result\\'
                        f = open(path + filename,'wb')
                        f.write(temp)
                        f.close()
                        temp = 0
                        adwin = tkinter.Tk()
                        adwin.title('변환 완료')
                        adwin.geometry('20x20+20+20')
                        adwin.resizable(0,0)
                        i = tkinter.messagebox.showinfo('파일 변환 완료','바탕화면 result 폴더 안에 원본 파일이 들어 있습니다.\n처음으로 돌아갑니다.')
                    except:
                        os.mkdir('result')
                        path = 'result\\'
                        f = open(path + filename,'wb')
                        f.write(temp)
                        f.close()
                        temp = 0
                        adwin = tkinter.Tk()
                        adwin.title('변환 완료')
                        adwin.geometry('20x20+20+20')
                        adwin.resizable(0,0)
                        i = tkinter.messagebox.showinfo('파일 변환 완료','바탕화면에 접근할 수 없습니다.\n프로그램이 위치한 폴더 안의 result 디렉토리에 원본 파일이 들어 있습니다.\n처음으로 돌아갑니다.')
                    time.sleep(0.5)
                    adwin.destroy()
                    shutil.rmtree('temp')
                        
            else:
                i = tkinter.messagebox.showinfo('비밀번호 불일치','비밀번호가 일치하지 않습니다.\n다시 입력해 주십시오.')
            
        def cancel():
            i = tkinter.messagebox.askokcancel('변환 취소','사진 변환을 취소합니다.\n모든 임시 파일을 삭제합니다.\n처음으로 돌아갑니다.')
            if not i == 0:
                time.sleep(0.5)
                pwin.destroy()
                shutil.rmtree('temp')
        
        gobut = tkinter.Button(pwin,text = ' 입력 ',command = gogo)
        gobut.place(x = 100,y = 85)
        canbut = tkinter.Button(pwin,text = ' 취소 ',command = cancel)
        canbut.place(x = 150,y = 85)
        
        pwin.mainloop()
    
class utility:
    def getsalt(self):
        output = ''
        for i in range(0,64):
            output = output + chr(random.randrange(32,126))
        return output
    def geth3512(self,letter):
        out = letter.encode('utf-8')
        for i in range(0,1000000):
            out = hashlib.sha3_512( out ).hexdigest()
            out = bytes.fromhex(out)
        return hashlib.sha3_512( out ).hexdigest()
    def geth2256(self,letter):
        out = letter.encode('utf-8')
        for i in range(0,1000000):
            out = hashlib.sha256( out ).hexdigest()
            out = bytes.fromhex(out)
        return hashlib.sha256( out ).hexdigest()
    def gethmd5(self,letter):
        return hashlib.md5( ( letter ).encode( 'utf-8' ) ).hexdigest()
    def doen(self,file,key,iv):
        result = open('temp\\result','wb')
        aesset = aesf()
        aesset.set_cbc(key,iv)
        f = open(file,'rb')
        temp = 0
        while not temp == b'':
            temp = f.read(16)
            if len(temp) == 16:
                result.write( aesset.en_cbc(temp) )
            else:
                pad = lambda x : x + bytes(chr( 16 - len(x) ),'utf-8') * (16 - len(x))
                temp = pad(temp)
                result.write( aesset.en_cbc(temp) )
                temp = b''
        result.close()
        f.close()
        result = open('temp\\result','rb')
        k = result.read()
        result.close()
        return k
    def dode(self,filesize,key,iv):
        result = open('temp\\result','wb')
        aesset = aesf()
        aesset.set_cbc(key,iv)
        f = open('temp\\temp','rb')
        temp = f.read(256)
        for i in range(0,int( filesize/16 ) - 1 ):
            temp = f.read(16)
            result.write( aesset.de_cbc(temp) )
        temp = f.read(16)
        unpad = lambda x : x[:-x[-1]]
        temp = unpad( aesset.de_cbc(temp) )
        result.write(temp)
        
        result.close()
        f.close()
        result = open('temp\\result','rb')
        k = result.read()
        result.close()
        return k
    def encode(self,num):
        k = [ ]
        for i in range( 0,4 ):
            k.append( num % 256 )
            num = num // 256
        j = bytes( { k[0] } )
        for i in range( 1,len(k) ):
            j = j + bytes( { k[i] } )
        return j
    def decode(self,binary):
        value = 0
        for i in range( 0,len(binary) ):
            k = 256 ** i
            k = k * binary[i]
            value = value + k
        return value
    
class aesf:
    def set_cbc(self,key,iv):
        self.key = key
        self.iv = iv
        self.e_cipher = AES.new(self.key,AES.MODE_CBC,self.iv)
        self.d_cipher = AES.new(self.key,AES.MODE_CBC,self.iv)
    def en_cbc(self,data):
        return self.e_cipher.encrypt(data)
    def de_cbc(self,data):
        return self.d_cipher.decrypt(data)

kos = 1
while kos == 1:
    time.sleep(0.5)
    try:
        shutil.rmtree('temp')
    except:
        dowork = mainsys()
        kos = dowork.mainsys()
time.sleep(0.5)

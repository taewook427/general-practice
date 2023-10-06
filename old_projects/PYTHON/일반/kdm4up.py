import os
import shutil
import time
import hashlib

import tkinter
import tkinter.messagebox
from tkinter import filedialog
import tkinter.ttk

import mung2
import kaes4hy as en4

class infunc:

    def __init__(self):
        self.mtool = mung2.toolbox()
        self.etool = en4.toolbox()
        self.valid4 = self.etool.valid
        try:
            shutil.rmtree('temp493')
        except:
            pass
        os.mkdir('temp493')

    def view(self, path):
        return self.etool.view(path)

    def enfile(self, pwb, kfb, hintb, path):
        self.etool.enwhole(pwb, kfb, hintb, path)

    def defile(self, pwb, kfb, path):
        self.etool.dewhole(pwb, kfb, path)

    def enfolder(self, pwb, kfb, hintb, path):
        path = path.replace('/', '\\')
        self.mtool.pack(path, 'temp493/temp493.png', True)
        res = self.etool.enwhole(pwb, kfb, hintb, 'temp493/temp493.png')
        res = res.replace('\\', '/')
        path = path.replace('\\', '/')
        new = path[ 0:path.rfind('/') ] + res[res.rfind('/'):]
        shutil.move(res, new)
        os.remove('temp493/temp493.png')

    def defolder(self, pwb, kfb, path):
        self.etool.dewhole(pwb, kfb, path)
        path = path.replace('\\', '/')
        new = path[ 0:path.rfind('/') ]
        self.mtool.unpack(new + '/temp493.png')
        os.remove(new + '/temp493.png')
        for i in os.listdir('temp261'):
            shutil.move('temp261/' + i, new + '/' + i)
        shutil.rmtree('temp261')

    def delfile(self, path):
        size = os.path.getsize(path)
        with open(path, 'wb') as f:
            for i in range(0, size // 10485760):
                f.write( self.etool.genrandom(10485760) )
            f.write( self.etool.genrandom(size % 10485760) )
        os.remove(path)

    def delfolder(self, path):
        path = path.replace('\\', '/')
        temp = os.listdir(path)
        files = [ ]
        folders = [ ]
        for i in temp:
            if os.path.isdir(path + '/' + i):
                folders.append(i)
            else:
                files.append(i)
        for i in files:
            self.delfile(path + '/' + i)
        for i in folders:
            self.delfolder(path + '/' + i)
        shutil.rmtree(path)

class mainclass(infunc):

    def __init__(self):
        super().__init__()
        temp = self.dohash('kdm3/KDM.exe')
        keys = [6132056,
                b'A\x1a\x92\xecf\xf1sH\x0f"\xebz\x82>\xd5\xb5\x14\xa5} H\xb2\xf8\xe9\xa1k\x0b\x8c\x91\x1fB\xa4',
                b'\x97\x80\x81\x93\xf3\xdaz\xcc\xfe\xb0\xa3\x1d\x9a\xd9n)\x95{\xe8\xef\xe6:\xbaD\xc6\x83S\xe7N\x98;y']
    
        if temp == keys:
            self.valid3 = True
        else:
            self.valid3 = False

    def dohash(self, name):
        with open(name, 'rb') as f:
            dllbyte = f.read()
            rev = bytes( reversed(dllbyte) )

        keys = [ ]
        keys.append( len(dllbyte) )
        keys.append( hashlib.sha3_256(dllbyte).digest() )
        keys.append( hashlib.sha3_256(rev).digest() )

        return keys

    def mainfunc(self):
        win = tkinter.Tk()
        win.title('KOS Data Manager 4up')
        win.geometry("500x400+200+100")
        win.resizable(False, False)

        frame = tkinter.Frame(win)
        frame.place(x=10,y=10)
        listbox = tkinter.Listbox( frame, width=20,  height=15, font = ('Consolas', 15) )
        listbox.pack(side="left", fill="y")
        scrollbar0 = tkinter.Scrollbar(frame, orient="vertical")
        scrollbar0.config(command=listbox.yview)
        scrollbar0.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar0.set)
        win.update()

        dat0 = ['KAES4 File En', 'KAES4 File De', 'KAES4 Folder En', 'KAES4 Folder De', 'Universal Eraser', 'Compatibility Mode']
        dat1 = ['KAES4 hy를 사용하여\n파일을 암호화합니다.\n모드는 WHOLE입니다.',
                'KAES4 hy를 사용하여\n파일을 복호화합니다.\n모드는 WHOLE입니다.',
                'KAES4 hy를 사용하여\n폴더를 암호화합니다.\n모드는 WHOLE입니다.\n다른 기능과 혼용하여\n사용하지 마십시오.',
                'KAES4 hy를 사용하여\n폴더를 복호화합니다.\n모드는 WHOLE입니다.\n다른 기능과 혼용하여\n사용하지 마십시오.',
                'KAES4 hy Random\nGenerator를 사용하여\n파일 또는 폴더를\n삭제합니다.\n전체 크기만큼\n한 번 덮어씁니다.',
                'KOS Data Manager 3\n내장 KDM3를 실행합니다.\n구버전 호환성이\n필요한 경우\n사용할 수 있습니다.']

        time.sleep(0.2)
        for i in dat0:
            listbox.insert(listbox.size(), i)
            win.update()
            time.sleep(0.03)
        time.sleep(0.02)

        status = tkinter.StringVar()
        temp = ''
        if self.valid4:
            temp = temp + 'KAES4 hy dll 정상\n'
        else:
            temp = temp + 'critical warning\nKAES4 hy dll 손상\n'
        if self.valid3:
            temp = temp + 'KDM3 exe 정상\n'
        else:
            temp = temp + 'critical warning\nKDM3 exe 손상\n'
        status.set(temp)
        label0 = tkinter.Label(win, textvariable = status, font = ('Consolas', 15) )
        label0.place(x=260,y=10)
        win.update()

        last = -1
        def click(event):
            time.sleep(0.1)
            nonlocal listbox
            nonlocal last
            nonlocal status
            nonlocal win
            temp = listbox.curselection()[0]
            if last == temp:
                time.sleep(0.1)
                nonlocal win
                win.destroy()
                time.sleep(0.1)
                if last == 0:
                    self.mf0()
                elif last == 1:
                    self.mf1()
                elif last == 2:
                    self.mf2()
                elif last == 3:
                    self.mf3()
                elif last == 4:
                    self.mf4()
                elif last == 5:
                    self.mf5()
            else:
                last = temp
                status.set( dat1[last] )
                win.update()
        listbox.bind('<ButtonRelease-1>',click)

        def exitf(): # X 버튼
            global off
            off = False
            nonlocal win
            win.destroy()
        win.protocol('WM_DELETE_WINDOW', exitf)

        win.mainloop()

    def mf0(self):
        win = tkinter.Tk()
        win.title('KOS Data Manager 4up')
        win.geometry("500x400+200+100")
        win.resizable(False, False)

        var0 = tkinter.StringVar()
        var0.set('기본키파일') # 키 파일 경로
        def f0():
            time.sleep(0.1)
            nonlocal win
            nonlocal var0
            try:
                out = filedialog.askopenfile( title='키 파일 선택', filetypes=( ('all files', '*.*'),('jpg files', '*.jpg'),('png files', '*.png') ) )
                var0.set( out.name )
            except:
                var0.set('기본키파일')
            win.update()
        but0 = tkinter.Button(win, text = '...', font = ('Consolas',14), command = f0)
        but0.place(x = 10,y = 10) # 키 파일 설정

        label1 = tkinter.Label(win, font = ('Consolas',14), textvariable = var0)
        label1.place(x=60,y=15) # 키 파일 경로 표시

        frame2 = tkinter.Frame(win)
        frame2.place(x=10,y=55)
        listbox2 = tkinter.Listbox( frame2, width=45,  height=9, font = ('Consolas',14) )
        listbox2.pack(side="left", fill="y")
        scrollbar2 = tkinter.Scrollbar(frame2, orient="vertical")
        scrollbar2.config(command=listbox2.yview)
        scrollbar2.pack(side="right", fill="y")
        listbox2.config(yscrollcommand=scrollbar2.set)

        var3 = tkinter.IntVar() # 원본 삭제 여부, 0 : False, 1 : True
        but3 = tkinter.Checkbutton(win, text = '원본삭제', font = ('Consolas',14), variable = var3)
        but3.place(x = 5, y = 275)

        var4 = [ ] # files list
        def f4():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox2
            nonlocal var4
            var4 = [ ]
            listbox2.delete( 0,listbox2.size() )
            out = filedialog.askopenfiles( title='파일들 선택', filetypes=( ('all files', '*.*'),('png files', '*.png'),('k files', '*.k') ) )
            for i in out:
                var4.append(i.name)
                listbox2.insert( listbox2.size(),i.name )
            win.update()
        but4 = tkinter.Button(win, text = '파일선택', font = ('Consolas',14), command = f4)
        but4.place(x = 110,y = 270) # 파일 추가

        def f5():
            time.sleep(0.1)
            nonlocal win
            nonlocal var0 # kf path str
            nonlocal var3 # delete flag
            nonlocal var4 # files list
            nonlocal in6 # pw in A
            nonlocal in7 # pw in B
            nonlocal in8 # hint in
            
            pwa = in6.get() # pw str
            pwb = in7.get()
            hint = in8.get('1.0','end')
            kf = en4.getkf( var0.get() ) # key file
            flag = True if var3.get() == 1 else False # 원본 삭제 여부

            if pwa == pwb:
                spec = ' 파일 : ' + str( len(var4) ) + ' 개 \n 키 파일 크기 : ' + str( len(kf) ) + ' 바이트 \n 비밀번호 길이 : ' + str( len(pwa) ) + ' 글자 \n 다음과 같이 암호화를 진행합니다. '
                ask = tkinter.messagebox.askokcancel('변환 요소 확인',spec)
                if ask:
                    success = 0
                    fail = 0
                    for i in var4:
                        try:
                            self.enfile(bytes(pwa, 'utf-8'), kf, bytes(hint, 'utf-8'), i)
                            if flag:
                                os.remove(i)
                            success = success + 1
                            time.sleep(0.2)
                        except:
                            fail = fail + 1
                    tkinter.messagebox.showinfo('변환 완료',' 파일 암호화를 완료했습니다. \n 성공 : ' + str(success) + ' 실패 : ' + str(fail) + ' ')

            else:
                tkinter.messagebox.showinfo('비밀번호 불일치',' 비밀번호 - 비밀번호 확인이 불일치합니다. \n 다시 입력해 주십시오. ')
            win.update()
            
        but5 = tkinter.Button(win, text = '변환', font = ('Consolas',14), command = f5)
        but5.place(x = 210,y = 270) # 변환

        in6 = tkinter.Entry(width=25, font = ('맑은 고딕',14), show = '●')
        in6.grid(column = 0 , row = 0)
        in6.place(x=10,y=320) # pw in A

        in7 = tkinter.Entry(width=25, font = ('맑은 고딕',14), show = '●')
        in7.grid(column = 0 , row = 0)
        in7.place(x=10,y=360) # pw in B

        in8 = tkinter.Text( width=24, height=5, font = ('맑은 고딕',13) )
        in8.grid(column = 0 , row = 0)
        in8.place(x=270,y=270) # hint in

        win.mainloop()

    def mf1(self):
        win = tkinter.Tk()
        win.title('KOS Data Manager 4up')
        win.geometry("500x400+200+100")
        win.resizable(False, False)

        var0 = tkinter.StringVar()
        var0.set('기본키파일') # 키 파일 경로
        def f0():
            time.sleep(0.1)
            nonlocal win
            nonlocal var0
            try:
                out = filedialog.askopenfile( title='키 파일 선택', filetypes=( ('all files', '*.*'),('jpg files', '*.jpg'),('png files', '*.png') ) )
                var0.set( out.name )
            except:
                var0.set('기본키파일')
            win.update()
        but0 = tkinter.Button(win, text = '...', font = ('Consolas',14), command = f0)
        but0.place(x = 10,y = 10) # 키 파일 설정

        label1 = tkinter.Label(win, font = ('Consolas',14), textvariable = var0)
        label1.place(x=60,y=15) # 키 파일 경로 표시

        frame2 = tkinter.Frame(win)
        frame2.place(x=10,y=55)
        listbox2 = tkinter.Listbox( frame2, width=45,  height=9, font = ('Consolas',14) )
        listbox2.pack(side="left", fill="y")
        scrollbar2 = tkinter.Scrollbar(frame2, orient="vertical")
        scrollbar2.config(command=listbox2.yview)
        scrollbar2.pack(side="right", fill="y")
        listbox2.config(yscrollcommand=scrollbar2.set)

        var3 = tkinter.IntVar() # 원본 삭제 여부, 0 : False, 1 : True
        but3 = tkinter.Checkbutton(win, text = '원본삭제', font = ('Consolas',14), variable = var3)
        but3.place(x = 5, y = 275)

        var4 = [ ] # files list
        sel9 = 0 # 현재 힌트 보기 파일
        def f4():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox2
            nonlocal var4
            nonlocal var8
            nonlocal sel9
            var4 = [ ]
            listbox2.delete( 0,listbox2.size() )
            out = filedialog.askopenfiles( title='파일들 선택', filetypes=( ('all files', '*.*'),('png files', '*.png'),('k files', '*.k') ) )
            for i in out:
                var4.append(i.name)
                listbox2.insert( listbox2.size(),i.name )
            sel9 = 0
            try:
                temp = self.view( var4[sel9] )
                var8.set( str(temp, 'utf-8') )
            except:
                var8.set('Not Valid KAES4 File')
            win.update()
        but4 = tkinter.Button(win, text = '파일선택', font = ('Consolas',14), command = f4)
        but4.place(x = 110,y = 270) # 파일 추가

        def f9(event):
            time.sleep(0.1)
            nonlocal win
            nonlocal var4
            nonlocal sel9
            nonlocal var8
            nonlocal listbox2
            sel9 = listbox2.curselection()[0]
            try:
                temp = self.view( var4[sel9] )
                var8.set( str(temp, 'utf-8') )
            except:
                var8.set('Not Valid KAES4 File')
            win.update()
        listbox2.bind('<ButtonRelease-1>',f9)

        def f5():
            nonlocal win
            nonlocal var0 # kf path str
            nonlocal var3 # erase flag
            nonlocal var4 # files list
            nonlocal in6 # pw in A

            pwa = in6.get() # pw str A
            kf = en4.getkf( var0.get() ) # key file
            flag = True if var3.get() == 1 else False # 원본 삭제 여부

            countn = 0 # not kaes file
            countp = 0 # decode success
            countf = 0 # not valid pw
            spec = ' 파일 : ' + str( len(var4) ) + ' 개 \n 키 파일 크기 : ' + str( len(kf) ) + ' 바이트 \n 비밀번호 길이 : ' + str( len(pwa) ) + ' 글자 \n 다음과 같이 복호화를 진행합니다. '
            ask = tkinter.messagebox.askokcancel('변환 요소 확인',spec)
            if ask:
                for i in var4:
                    try:
                        self.defile(bytes(pwa, 'utf-8'), kf, i)
                        if flag:
                            os.remove(i)
                        countp = countp + 1
                        time.sleep(0.2)
                    except Exception as e:
                        if str(e) == 'invalidKEY':
                            countf = countf + 1
                        else:
                            countn = countn + 1
                tkinter.messagebox.showinfo('변환 완료',' 파일 복호화를 완료했습니다. \n P : ' + str(countp) + ' N : ' + str(countn) + ' F : ' + str(countf) + ' ')
            win.update()
            
        but5 = tkinter.Button(win, text = '변환', font = ('Consolas',14), command = f5)
        but5.place(x = 210,y = 270) # 변환

        in6 = tkinter.Entry(width=25, font = ('맑은 고딕',14), show = '●')
        in6.grid(column = 0 , row = 0)
        in6.place(x=10,y=320) # pw in A

        in7 = tkinter.Entry(width=25, font = ('맑은 고딕',14), show = '●', state='disabled')
        in7.grid(column = 0 , row = 0)
        in7.place(x=10,y=360) # pw in B

        var8 = tkinter.StringVar()
        var8.set('') # hint str
        label8 = tkinter.Label(win, font = ('맑은 고딕',13), textvariable=var8)
        label8.place(x=270,y=270) # 힌트 표시

        win.mainloop()

    def mf2(self):
        win = tkinter.Tk()
        win.title('KOS Data Manager 4up')
        win.geometry("500x400+200+100")
        win.resizable(False, False)

        var0 = tkinter.StringVar()
        var0.set('기본키파일') # 키 파일 경로
        def f0():
            time.sleep(0.1)
            nonlocal win
            nonlocal var0
            try:
                out = filedialog.askopenfile( title='키 파일 선택', filetypes=( ('all files', '*.*'),('jpg files', '*.jpg'),('png files', '*.png') ) )
                var0.set( out.name )
            except:
                var0.set('기본키파일')
            win.update()
        but0 = tkinter.Button(win, text = '...', font = ('Consolas',14), command = f0)
        but0.place(x = 10,y = 10) # 키 파일 설정

        label1 = tkinter.Label(win, font = ('Consolas',14), textvariable = var0)
        label1.place(x=60,y=15) # 키 파일 경로 표시

        frame2 = tkinter.Frame(win)
        frame2.place(x=10,y=55)
        listbox2 = tkinter.Listbox( frame2, width=45,  height=9, font = ('Consolas',14) )
        listbox2.pack(side="left", fill="y")
        scrollbar2 = tkinter.Scrollbar(frame2, orient="vertical")
        scrollbar2.config(command=listbox2.yview)
        scrollbar2.pack(side="right", fill="y")
        listbox2.config(yscrollcommand=scrollbar2.set)

        var3 = tkinter.IntVar() # 원본 삭제 여부, 0 : False, 1 : True
        but3 = tkinter.Checkbutton(win, text = '원본삭제', font = ('Consolas',14), variable = var3)
        but3.place(x = 5, y = 275)

        var4 = '' # folder path
        def f4():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox2
            nonlocal var4
            listbox2.delete( 0,listbox2.size() )
            var4 = filedialog.askdirectory(title='폴더 선택')
            listbox2.insert( listbox2.size(), var4 )
            win.update()
        but4 = tkinter.Button(win, text = '폴더선택', font = ('Consolas',14), command = f4)
        but4.place(x = 110,y = 270) # 폴더 추가

        def f5():
            time.sleep(0.1)
            nonlocal win
            nonlocal var0 # kf path str
            nonlocal var3 # delete flag
            nonlocal var4 # folder path str
            nonlocal in6 # pw in A
            nonlocal in7 # pw in B
            nonlocal in8 # hint in
            
            pwa = in6.get() # pw str
            pwb = in7.get()
            hint = in8.get('1.0','end')
            kf = en4.getkf( var0.get() ) # key file
            flag = True if var3.get() == 1 else False # 원본 삭제 여부

            if pwa == pwb:
                spec = ' 폴더 : ' + var4 + ' \n 키 파일 크기 : ' + str( len(kf) ) + ' 바이트 \n 비밀번호 길이 : ' + str( len(pwa) ) + ' 글자 \n 다음과 같이 암호화를 진행합니다. '
                ask = tkinter.messagebox.askokcancel('변환 요소 확인',spec)
                if ask:
                    try:
                        self.enfolder(bytes(pwa, 'utf-8'), kf, bytes(hint, 'utf-8'), var4)
                        if flag:
                            shutil.rmtree(var4)
                        time.sleep(0.2)
                        msg = ' converted successfully '
                    except Exception as e:
                        msg = f' {e} '
                    tkinter.messagebox.showinfo('변환 완료',' 폴더 암호화를 완료했습니다. \n' + msg)

            else:
                tkinter.messagebox.showinfo('비밀번호 불일치',' 비밀번호 - 비밀번호 확인이 불일치합니다. \n 다시 입력해 주십시오. ')
            win.update()
        but5 = tkinter.Button(win, text = '변환', font = ('Consolas',14), command = f5)
        but5.place(x = 210,y = 270) # 변환

        in6 = tkinter.Entry(width=25, font = ('맑은 고딕',14), show = '●')
        in6.grid(column = 0 , row = 0)
        in6.place(x=10,y=320) # pw in A

        in7 = tkinter.Entry(width=25, font = ('맑은 고딕',14), show = '●')
        in7.grid(column = 0 , row = 0)
        in7.place(x=10,y=360) # pw in B

        in8 = tkinter.Text( width=24, height=5, font = ('맑은 고딕',13) )
        in8.grid(column = 0 , row = 0)
        in8.place(x=270,y=270) # hint in

        win.mainloop()

    def mf3(self):
        win = tkinter.Tk()
        win.title('KOS Data Manager 4up')
        win.geometry("500x400+200+100")
        win.resizable(False, False)

        var0 = tkinter.StringVar()
        var0.set('기본키파일') # 키 파일 경로
        def f0():
            time.sleep(0.1)
            nonlocal win
            nonlocal var0
            try:
                out = filedialog.askopenfile( title='키 파일 선택', filetypes=( ('all files', '*.*'),('jpg files', '*.jpg'),('png files', '*.png') ) )
                var0.set( out.name )
            except:
                var0.set('기본키파일')
            win.update()
        but0 = tkinter.Button(win, text = '...', font = ('Consolas',14), command = f0)
        but0.place(x = 10,y = 10) # 키 파일 설정

        label1 = tkinter.Label(win, font = ('Consolas',14), textvariable = var0)
        label1.place(x=60,y=15) # 키 파일 경로 표시

        frame2 = tkinter.Frame(win)
        frame2.place(x=10,y=55)
        listbox2 = tkinter.Listbox( frame2, width=45,  height=9, font = ('Consolas',14) )
        listbox2.pack(side="left", fill="y")
        scrollbar2 = tkinter.Scrollbar(frame2, orient="vertical")
        scrollbar2.config(command=listbox2.yview)
        scrollbar2.pack(side="right", fill="y")
        listbox2.config(yscrollcommand=scrollbar2.set)

        var3 = tkinter.IntVar() # 원본 삭제 여부, 0 : False, 1 : True
        but3 = tkinter.Checkbutton(win, text = '원본삭제', font = ('Consolas',14), variable = var3)
        but3.place(x = 5, y = 275)

        var4 = [ ] # files list
        sel9 = 0 # 현재 힌트 보기 파일
        def f4():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox2
            nonlocal var4
            nonlocal var8
            nonlocal sel9
            var4 = [ ]
            listbox2.delete( 0,listbox2.size() )
            out = filedialog.askopenfiles( title='파일들 선택', filetypes=( ('all files', '*.*'),('png files', '*.png'),('k files', '*.k') ) )
            for i in out:
                var4.append(i.name)
                listbox2.insert( listbox2.size(),i.name )
            sel9 = 0
            try:
                temp = self.view( var4[sel9] )
                var8.set( str(temp, 'utf-8') )
            except:
                var8.set('Not Valid KAES4 File')
            win.update()
        but4 = tkinter.Button(win, text = '파일선택', font = ('Consolas',14), command = f4)
        but4.place(x = 110,y = 270) # 파일 추가

        def f9(event):
            time.sleep(0.1)
            nonlocal win
            nonlocal var4
            nonlocal sel9
            nonlocal var8
            nonlocal listbox2
            sel9 = listbox2.curselection()[0]
            try:
                temp = self.view( var4[sel9] )
                var8.set( str(temp, 'utf-8') )
            except:
                var8.set('Not Valid KAES4 File')
            win.update()
        listbox2.bind('<ButtonRelease-1>',f9)

        def f5():
            nonlocal win
            nonlocal var0 # kf path str
            nonlocal var3 # erase flag
            nonlocal var4 # files list
            nonlocal in6 # pw in A

            pwa = in6.get() # pw str A
            kf = en4.getkf( var0.get() ) # key file
            flag = True if var3.get() == 1 else False # 원본 삭제 여부

            countn = 0 # not kaes file
            countp = 0 # decode success
            countf = 0 # not valid pw
            spec = ' 파일 : ' + str( len(var4) ) + ' 개 \n 키 파일 크기 : ' + str( len(kf) ) + ' 바이트 \n 비밀번호 길이 : ' + str( len(pwa) ) + ' 글자 \n 다음과 같이 복호화를 진행합니다. '
            ask = tkinter.messagebox.askokcancel('변환 요소 확인',spec)
            if ask:
                for i in var4:
                    try:
                        self.defolder(bytes(pwa, 'utf-8'), kf, i)
                        if flag:
                            os.remove(i)
                        countp = countp + 1
                        time.sleep(0.2)
                    except Exception as e:
                        if str(e) == 'invalidKEY':
                            countf = countf + 1
                        else:
                            countn = countn + 1
                tkinter.messagebox.showinfo('변환 완료',' 파일 복호화를 완료했습니다. \n P : ' + str(countp) + ' N : ' + str(countn) + ' F : ' + str(countf) + ' ')
            win.update()
        but5 = tkinter.Button(win, text = '변환', font = ('Consolas',14), command = f5)
        but5.place(x = 210,y = 270) # 변환

        in6 = tkinter.Entry(width=25, font = ('맑은 고딕',14), show = '●')
        in6.grid(column = 0 , row = 0)
        in6.place(x=10,y=320) # pw in A

        in7 = tkinter.Entry(width=25, font = ('맑은 고딕',14), show = '●', state='disabled')
        in7.grid(column = 0 , row = 0)
        in7.place(x=10,y=360) # pw in B

        var8 = tkinter.StringVar()
        var8.set('') # hint str
        label8 = tkinter.Label(win, font = ('맑은 고딕',13), textvariable=var8)
        label8.place(x=270,y=270) # 힌트 표시

        win.mainloop()

    def mf4(self):
        win = tkinter.Tk()
        win.title('KOS Data Manager 4up')
        win.geometry("500x400+200+100")
        win.resizable(False, False)

        frame0 = tkinter.Frame(win)
        frame0.place(x=10,y=10)
        listbox0 = tkinter.Listbox( frame0, width=42,  height=7, font = ('Consolas',14) )
        listbox0.pack(side="left", fill="y")
        scrollbar0 = tkinter.Scrollbar(frame0, orient="vertical")
        scrollbar0.config(command=listbox0.yview)
        scrollbar0.pack(side="right", fill="y")
        listbox0.config(yscrollcommand=scrollbar0.set)

        label1 = tkinter.Label(win, text = '파일', font = ('Consolas',14) )
        label1.place(x = 450, y = 10)

        var2 = [ ] # files list
        def f2():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox0
            nonlocal var2
            out = filedialog.askopenfiles( title='파일들 선택', filetypes=( ('all files', '*.*'),('exe files', '*.exe') ) )
            for i in out:
                var2.append(i.name)
                listbox0.insert( listbox0.size(),i.name )
        but2 = tkinter.Button(win, text = 'ADD', font = ('Consolas',14), command = f2)
        but2.place(x = 450, y = 40) # 파일 추가

        var3 = '' # 현재 선택 번호
        def click3(event):
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox0
            nonlocal var3
            var3 = listbox0.curselection()[0]
            win.update()
        listbox0.bind('<ButtonRelease-1>', click3)

        def f3():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox0
            nonlocal var2
            nonlocal var3
            del var2[var3]
            listbox0.delete( var3, var3 )
            var3 = ''
            win.update()
        but3 = tkinter.Button(win, text = 'DEL', font = ('Consolas',14), command = f3)
        but3.place(x = 450, y = 85) # 항목 삭제

        def f4():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox0
            nonlocal var2
            nonlocal var3
            var2 = [ ]
            var3 = ''
            listbox0.delete( 0,listbox0.size() )
            win.update()
        but4 = tkinter.Button(win, text = 'CLR', font = ('Consolas',14), command = f4)
        but4.place(x = 450,y = 130) # 항목 초기화

        frame5 = tkinter.Frame(win)
        frame5.place(x=10,y=185)
        listbox5 = tkinter.Listbox( frame5, width=42,  height=7, font = ('Consolas',14) )
        listbox5.pack(side="left", fill="y")
        scrollbar5 = tkinter.Scrollbar(frame5, orient="vertical")
        scrollbar5.config(command=listbox5.yview)
        scrollbar5.pack(side="right", fill="y")
        listbox5.config(yscrollcommand=scrollbar5.set)

        label6 = tkinter.Label(win, text = '폴더', font = ('Consolas',14) )
        label6.place(x = 450, y = 185)

        var7 = [ ] # folders list
        def f7():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox5
            nonlocal var7
            out = filedialog.askdirectory(title='폴더 선택')
            var7.append(out)
            listbox5.insert( listbox5.size(),out )
        but7 = tkinter.Button(win, text = 'ADD', font = ('Consolas',14), command = f7)
        but7.place(x = 450, y = 215) # 폴더 추가

        var8 = '' # 현재 선택 번호
        def click8(event):
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox5
            nonlocal var8
            var8 = listbox5.curselection()[0]
            win.update()
        listbox5.bind('<ButtonRelease-1>', click8)

        def f8():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox5
            nonlocal var7
            nonlocal var8
            del var7[var8]
            listbox5.delete( var8, var8 )
            var8 = ''
            win.update()
        but8 = tkinter.Button(win, text = 'DEL', font = ('Consolas',14), command = f8)
        but8.place(x = 450, y = 260) # 항목 삭제

        def f9():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox5
            nonlocal var7
            nonlocal var8
            var7 = [ ]
            var8 = ''
            listbox5.delete( 0,listbox5.size() )
            win.update()
        but9 = tkinter.Button(win, text = 'CLR', font = ('Consolas',14), command = f9)
        but9.place(x = 450,y = 305) # 항목 초기화

        def f10():
            time.sleep(0.1)
            nonlocal win
            nonlocal var2
            nonlocal var7
            nonlocal var11
            for i in var2:
                var11.set(i)
                win.update()
                self.delfile(i)
            for i in var7:
                var11.set(i)
                win.update()
                self.delfolder(i)
            f4()
            f9()
            var11.set('all cleared')
            win.update()
        but10 = tkinter.Button(win, text = 'DEL', font = ('Consolas',14), command = f10)
        but10.place(x = 10,y = 355) # 삭제

        var11 = tkinter.StringVar()
        var11.set('')
        label11 = tkinter.Label(win, textvariable = var11, font = ('Consolas',14) )
        label11.place(x = 60, y = 360)

        win.mainloop()

    def mf5(self):
        global off
        off = False
        os.chdir( os.path.abspath("kdm3") )
        os.startfile('KDM.exe')

off = True
k = mainclass()
while off:
    time.sleep(0.1)
    k.mainfunc()
time.sleep(0.5)

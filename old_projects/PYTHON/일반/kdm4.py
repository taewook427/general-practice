import os
import time
import hashlib

import tkinter
import tkinter.messagebox
from tkinter import filedialog
import tkinter.ttk

import kaes4go as en4go

class mainclass:

    # module init
    def __init__(self):
        global mydll
        temp = self.dohash('./kdm3/KDM.exe')
        keys = [6132056,
                b'A\x1a\x92\xecf\xf1sH\x0f"\xebz\x82>\xd5\xb5\x14\xa5} H\xb2\xf8\xe9\xa1k\x0b\x8c\x91\x1fB\xa4',
                b'\x97\x80\x81\x93\xf3\xdaz\xcc\xfe\xb0\xa3\x1d\x9a\xd9n)\x95{\xe8\xef\xe6:\xbaD\xc6\x83S\xe7N\x98;y']
    
        if temp == keys:
            self.valid = True
        else:
            self.valid = False

    # 위변조 확인
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
        win.title('KOS Data Manager 4')
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

        time.sleep(0.2)
        listbox.insert( listbox.size(),'KAES4 encrypt' )
        win.update()
        time.sleep(0.03)
        listbox.insert( listbox.size(),'KAES4 decrypt' )
        win.update()
        time.sleep(0.03)
        listbox.insert( listbox.size(),'file deleter' )
        win.update()
        time.sleep(0.03)
        listbox.insert( listbox.size(),'execute KDM3' )
        time.sleep(0.05)

        status = tkinter.StringVar()
        status.set('')
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
                    k = kaes4()
                    if k.valid:
                        k.encrypt()
                    else:
                        tkinter.messagebox.showinfo('KAES4 invalid', ' 내장 KAES4 go dll 파일의 무결성이 훼손되었습니다. 이 파일을 실행할 수 없습니다. ')
                elif last == 1:
                    k = kaes4()
                    if k.valid:
                        k.decrypt()
                    else:
                        tkinter.messagebox.showinfo('KAES4 invalid', ' 내장 KAES4 go dll 파일의 무결성이 훼손되었습니다. 이 파일을 실행할 수 없습니다. ')
                elif last == 2:
                    k = kaes4()
                    if k.valid:
                        k.erase()
                    else:
                        tkinter.messagebox.showinfo('KAES4 invalid', ' 내장 KAES4 go dll 파일의 무결성이 훼손되었습니다. 이 파일을 실행할 수 없습니다. ')
                elif last == 3:
                    if self.valid:
                        global off
                        off = False
                        os.startfile('.\\kdm3\\KDM.exe')
                    else:
                        tkinter.messagebox.showinfo('KDM3 invalid', ' 내장 KDM3 exe 파일의 무결성이 훼손되었습니다. 이 파일을 실행할 수 없습니다. ')
            else:
                last = temp
                if last == 0:
                    msg = 'KAES4 파일 암호화\n모드는 WHOLE'
                elif last == 1:
                    msg = 'KAES4 파일 복호화\n모드는 WHOLE'
                elif last == 2:
                    msg = '파일들 안전 삭제'
                elif last == 3:
                    msg = 'KOS Data Manager 3\n구버전 실행'
                status.set(msg)
                win.update()
        listbox.bind('<ButtonRelease-1>',click)

        def exitf(): # X 버튼
            global off
            off = False
            nonlocal win
            win.destroy()
        win.protocol('WM_DELETE_WINDOW', exitf)

        win.mainloop()

class kaes4:

    def __init__(self):
        self.tool = en4go.toolbox()
        self.valid = self.tool.valid

    def erase(self):
        win = tkinter.Tk()
        win.title('KOS Data Manager 4')
        win.geometry("500x400+200+100")
        win.resizable(False, False)

        frame = tkinter.Frame(win)
        frame.place(x=10,y=10)
        listbox = tkinter.Listbox( frame, width=45,  height=14, font = ('Consolas',14) )
        listbox.pack(side="left", fill="y")
        scrollbar0 = tkinter.Scrollbar(frame, orient="vertical")
        scrollbar0.config(command=listbox.yview)
        scrollbar0.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar0.set)

        files = [ ] #파일 경로들

        current = '' # 현재 선택 항목
        def click(event):
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal current
            current = listbox.curselection()[0]
            win.update()
        listbox.bind('<ButtonRelease-1>',click)

        def but0f():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal files
            out = filedialog.askopenfiles( title='파일들 선택', filetypes=( ('all files', '*.*'),('exe files', '*.exe') ) )
            for i in out:
                files.append(i.name)
                listbox.insert( listbox.size(),i.name )
        but0 = tkinter.Button(win, text = 'ADD', font = ('Consolas',14), command = but0f)
        but0.place(x = 10,y = 350) # 파일 추가

        def but1f():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal files
            nonlocal current
            del files[current]
            listbox.delete( current,current )
            current = ''
            win.update()
        but1 = tkinter.Button(win, text = 'DEL', font = ('Consolas',14), command = but1f)
        but1.place(x = 70,y = 350) # 파일 삭제

        def but2f():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal files
            nonlocal current
            files = [ ]
            listbox.delete( 0,listbox.size() )
            current = ''
            win.update()
        but2 = tkinter.Button(win, text = 'CLR', font = ('Consolas',14), command = but2f)
        but2.place(x = 130,y = 350) # 파일 초기화

        def but3f():
            time.sleep(0.1)
            nonlocal win
            nonlocal files
            nonlocal listbox
            nonlocal combo0
            mode = combo0.get()[0][0]
            err = 0
            for i in range( 0, len(files) ):
                try:
                    if mode == '1':
                        size = os.path.getsize( files[i] )
                        with open(files[i], 'wb') as f:
                            for j in range(0, size // 10485760):
                                f.write( self.tool.genrandom(10485760) )
                            f.write( self.tool.genrandom(size % 10485760) )
                    elif mode == '2':
                        with open(files[i], 'wb') as f:
                            f.write( self.tool.genrandom(10485760) )
                    elif mode == '3':
                        size = os.path.getsize( files[i] )
                        with open(files[i], 'wb') as f:
                            for j in range(0, size // 10485760):
                                f.write(b'\x00' * 10485760)
                            f.write( b'\x00' * (size % 10485760) )
                    elif mode == '4':
                        with open(files[i], 'wb') as f:
                            f.write(b'\x00' * 10485760)
                    time.sleep(0.1)
                    os.remove( files[i] )
                    files[i] = '///CLEAR///'
                    listbox.delete(i)
                    listbox.insert(i, '///CLEAR///')
                except:
                    err = err + 1
                win.update()
            files =  [i for i in files if i != '///CLEAR///']
            listbox.delete( 0,listbox.size() )
            for i in files:
                listbox.insert( listbox.size(),i )
            win.update()
            tkinter.messagebox.showinfo('삭제 완료',' 파일 삭제를 완료했습니다. \n (' + str(err) + ') 개의 오류가 발생했습니다. ')
            
        but3 = tkinter.Button(win, text = 'COM', font = ('Consolas',14), command = but3f)
        but3.place(x = 190,y = 350) # 변환 진행

        modes = ['1) 완전난수 + 전체','2) 완전난수 + 부분','3) 제로패딩 + 전체','4) 제로패딩 + 부분']
        combo0 = tkinter.ttk.Combobox(win, width=20, font = ("Consolas",14), values = modes)
        combo0.set( modes[0] ) #모드
        combo0.place(x=250,y=355)

        win.mainloop()

    def encrypt(self):
        win = tkinter.Tk()
        win.title('KOS Data Manager 4')
        win.geometry("500x400+200+100")
        win.resizable(False, False)

        frame = tkinter.Frame(win)
        frame.place(x=60,y=10)
        listbox = tkinter.Listbox( frame, width=40,  height=7, font = ('Consolas',14) )
        listbox.pack(side="left", fill="y")
        scrollbar0 = tkinter.Scrollbar(frame, orient="vertical")
        scrollbar0.config(command=listbox.yview)
        scrollbar0.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar0.set)

        files = [ ] # 파일 목록
        def f0():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal files
            files = [ ]
            listbox.delete( 0,listbox.size() )
            out = filedialog.askopenfiles( title='파일들 선택', filetypes=( ('all files', '*.*'),('k files', '*.k') ) )
            for i in out:
                files.append(i.name)
                listbox.insert( listbox.size(),i.name )
            win.update()
        but0 = tkinter.Button(win, text = '...', font = ('Consolas',14), command = f0)
        but0.place(x = 10,y = 10) # 파일 추가

        mode1 = 'non' # 삭제 강도 'non' 'nor' 'adv'
        txt1 = tkinter.StringVar()
        txt1.set('DEL\nnon\n\n')
        def f1():
            time.sleep(0.1)
            nonlocal win
            nonlocal mode1
            nonlocal txt1
            if mode1 == 'non':
                mode1 = 'nor'
                txt1.set('DEL\n\nnor\n')
            elif mode1 == 'nor':
                mode1 = 'adv'
                txt1.set('DEL\n\n\nadv')
            else:
                mode1 = 'non'
                txt1.set('DEL\nnon\n\n')
            win.update()
        but1 = tkinter.Button(win, textvariable = txt1, font = ('Consolas',14), command = f1)
        but1.place(x = 10,y = 60) # 삭제 모드

        path2 = tkinter.StringVar()
        path2.set('기본키파일') # 키 파일 경로
        def f2():
            time.sleep(0.1)
            nonlocal win
            nonlocal path2
            try:
                out = filedialog.askopenfile( title='키 파일 선택', filetypes=( ('all files', '*.*'),('jpg files', '*.jpg'),('png files', '*.png') ) )
                path2.set( out.name )
            except:
                path2.set('기본키파일')
            win.update()
        but2 = tkinter.Button(win, text = '...', font = ('Consolas',14), command = f2)
        but2.place(x = 10,y = 180) # 키 파일 추가

        label3 = tkinter.Label(win, font = ('Consolas',14), textvariable=path2)
        label3.place(x=60,y=185) # 키 파일 경로 표시

        in4 = tkinter.Entry(width=25, font = ('맑은 고딕',14), show = '●')
        in4.grid(column = 0 , row = 0)
        in4.place(x=10,y=230) # pw in A

        in5 = tkinter.Entry(width=25, font = ('맑은 고딕',14), show = '●')
        in5.grid(column = 0 , row = 0)
        in5.place(x=10,y=270) # pw in B

        in6 = tkinter.Text( width=20, height=6, font = ('맑은 고딕',14) )
        in6.grid(column = 0 , row = 0)
        in6.place(x=280,y=230) # hint in

        mode7 = False # 원본 삭제 여부 T삭제 F유지
        txt7 = tkinter.StringVar()
        txt7.set('원본 : 유지')
        def f7():
            time.sleep(0.1)
            nonlocal win
            nonlocal mode7
            nonlocal txt7
            if mode7:
                mode7 = False
                txt7.set('원본 : 유지')
            else:
                mode7 = True
                txt7.set('원본 : 삭제')
            win.update()
        but7 = tkinter.Button(win, textvariable = txt7, font = ('Consolas',14), command = f7)
        but7.place(x = 10,y = 310) # 원본 삭제 여부


        def func():
            time.sleep(0.1)
            nonlocal win
            nonlocal files # 파일 목록
            nonlocal mode1 # 삭제 강도 'nor' 'adv'
            nonlocal path2 # 키 파일 경로
            nonlocal in4 # pw in A
            nonlocal in5 # pw in B
            nonlocal in6 # hint in
            nonlocal mode7 # 원본 삭제 여부 T삭제 F유지
            pwa = in4.get() # pw str
            pwb = in5.get()
            hint = in6.get('1.0','end')
            kf = en4go.getkf( path2.get() ) # key file
            if pwa == pwb:
                spec = ' 파일 : ' + str( len(files) ) + ' 개 \n 키 파일 크기 : ' + str( len(kf) ) + ' 바이트 \n 비밀번호 길이 : ' + str( len(pwa) ) + ' 글자 \n 다음과 같이 암호화를 진행합니다. '
                ask = tkinter.messagebox.askokcancel('변환 요소 확인',spec)
                if ask:
                    success = 0
                    fail = 0
                    for i in files:
                        try:
                            temp = self.tool.enwhole(bytes(pwa, 'utf-8'), kf, bytes(hint, 'utf-8'), i)
                            if mode7:
                                if mode1 == 'nor':
                                    size = os.path.getsize(i)
                                    with open(i, 'wb') as f:
                                        for j in range(0, size // 10485760):
                                            f.write(b'\x00' * 10485760)
                                        f.write( b'\x00' * (size % 10485760) )
                                elif mode1 == 'adv':
                                    size = os.path.getsize(i)
                                    with open(i, 'wb') as f:
                                        for j in range(0, size // 10485760):
                                            f.write( self.tool.genrandom(10485760) )
                                        f.write( self.tool.genrandom(size % 10485760) )
                                os.remove(i)
                            success = success + 1
                            time.sleep(0.2)
                        except:
                            fail = fail + 1
                    tkinter.messagebox.showinfo('변환 완료',' 파일 암호화를 완료했습니다. \n 성공 : ' + str(success) + ' 실패 : ' + str(fail) + ' ')
            else:
                tkinter.messagebox.showinfo('비밀번호 불일치',' 비밀번호 - 비밀번호 확인이 불일치합니다. \n 다시 입력해 주십시오. ')
            win.update()
        go = tkinter.Button(win, text = '< 변환 >', font = ('Consolas',14), command = func)
        go.place(x = 140,y = 310) # 변환 진행

        win.mainloop()

    def decrypt(self):
        win = tkinter.Tk()
        win.title('KOS Data Manager 4')
        win.geometry("500x400+200+100")
        win.resizable(False, False)

        frame = tkinter.Frame(win)
        frame.place(x=60,y=10)
        listbox = tkinter.Listbox( frame, width=40,  height=7, font = ('Consolas',14) )
        listbox.pack(side="left", fill="y")
        scrollbar0 = tkinter.Scrollbar(frame, orient="vertical")
        scrollbar0.config(command=listbox.yview)
        scrollbar0.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar0.set)

        files = [ ] # 파일 목록
        current = 0 # 현재 힌트 보기 파일
        def f0():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal files
            files = [ ]
            listbox.delete( 0,listbox.size() )
            out = filedialog.askopenfiles( title='파일들 선택', filetypes=( ('all files', '*.*'),('png files', '*.png'),('k files', '*.k') ) )
            for i in out:
                files.append(i.name)
                listbox.insert( listbox.size(),i.name )
            nonlocal hint5
            nonlocal current
            current = 0
            try:
                temp = self.tool.view( files[current] )
                hint5.set( str(temp, 'utf-8') )
            except:
                hint5.set('Not Valid KAES4 File')
            win.update()
        but0 = tkinter.Button(win, text = '...', font = ('Consolas',14), command = f0)
        but0.place(x = 10,y = 10) # 파일 추가

        mode1 = 'non' # 삭제 강도 'non' 'nor' 'adv'
        txt1 = tkinter.StringVar()
        txt1.set('DEL\nnon\n\n')
        def f1():
            time.sleep(0.1)
            nonlocal win
            nonlocal mode1
            nonlocal txt1
            if mode1 == 'non':
                mode1 = 'nor'
                txt1.set('DEL\n\nnor\n')
            elif mode1 == 'nor':
                mode1 = 'adv'
                txt1.set('DEL\n\n\nadv')
            else:
                mode1 = 'non'
                txt1.set('DEL\nnon\n\n')
            win.update()
        but1 = tkinter.Button(win, textvariable = txt1, font = ('Consolas',14), command = f1)
        but1.place(x = 10,y = 60) # 삭제 모드

        path2 = tkinter.StringVar()
        path2.set('기본키파일') # 키 파일 경로
        def f2():
            time.sleep(0.1)
            nonlocal win
            nonlocal path2
            try:
                out = filedialog.askopenfile( title='키 파일 선택', filetypes=( ('all files', '*.*'),('jpg files', '*.jpg'),('png files', '*.png') ) )
                path2.set( out.name )
            except:
                path2.set('기본키파일')
            win.update()
        but2 = tkinter.Button(win, text = '...', font = ('Consolas',14), command = f2)
        but2.place(x = 10,y = 180) # 키 파일 추가

        label3 = tkinter.Label(win, font = ('Consolas',14), textvariable=path2)
        label3.place(x=60,y=185) # 키 파일 경로 표시

        in4 = tkinter.Entry(width=25, font = ('맑은 고딕',14), show = '●')
        in4.grid(column = 0 , row = 0)
        in4.place(x=10,y=230) # pw in A

        hint5 = tkinter.StringVar()
        hint5.set('') # hint str
        label5 = tkinter.Label(win, font = ('맑은 고딕',14), textvariable=hint5)
        label5.place(x=280,y=230) # 키 파일 경로 표시

        mode6 = False # 원본 삭제 여부 T삭제 F유지
        txt6 = tkinter.StringVar()
        txt6.set('원본 : 유지')
        def f6():
            time.sleep(0.1)
            nonlocal win
            nonlocal mode6
            nonlocal txt6
            if mode6:
                mode6 = False
                txt6.set('원본 : 유지')
            else:
                mode6 = True
                txt6.set('원본 : 삭제')
            win.update()
        but6 = tkinter.Button(win, textvariable = txt6, font = ('Consolas',14), command = f6)
        but6.place(x = 10,y = 270) # 원본 삭제 여부

        def click(event):
            time.sleep(0.1)
            nonlocal win
            nonlocal files
            nonlocal current
            nonlocal hint5
            current = listbox.curselection()[0]
            try:
                temp = self.tool.view( files[current] )
                hint5.set( str(temp, 'utf-8') )
            except:
                hint5.set('Not Valid KAES4 File')
            win.update()
        listbox.bind('<ButtonRelease-1>',click)

        def func():
            time.sleep(0.1)
            nonlocal win
            nonlocal files # 파일 목록
            nonlocal mode1 # 삭제 강도 'nor' 'adv'
            nonlocal path2 # 키 파일 경로
            nonlocal in4 # pw in A
            nonlocal mode6 # 원본 삭제 여부
            pw = in4.get() # pw str
            kf = en4go.getkf( path2.get() ) # key file bytes
            countn = 0 # not kaes file
            countp = 0 # decode success
            countf = 0 # not valid pw
            spec = ' 파일 : ' + str( len(files) ) + ' 개 \n 키 파일 크기 : ' + str( len(kf) ) + ' 바이트 \n 비밀번호 길이 : ' + str( len(pw) ) + ' 글자 \n 다음과 같이 복호화를 진행합니다. '
            ask = tkinter.messagebox.askokcancel('변환 요소 확인',spec)
            if ask:
                for i in files:
                    try:
                        self.tool.dewhole(bytes(pw, 'utf-8'), kf, i)
                        if mode6:
                            if mode1 == 'nor':
                                size = os.path.getsize(i)
                                with open(i, 'wb') as f:
                                    for j in range(0, size // 10485760):
                                        f.write(b'\x00' * 10485760)
                                    f.write( b'\x00' * (size % 10485760) )
                            elif mode1 == 'adv':
                                size = os.path.getsize(i)
                                with open(i, 'wb') as f:
                                    for j in range(0, size // 10485760):
                                        f.write( self.tool.genrandom(10485760) )
                                    f.write( self.tool.genrandom(size % 10485760) )
                            os.remove(i)
                        countp = countp + 1
                        time.sleep(0.2)
                    except Exception as e:
                        if str(e) == 'invalidKEY':
                            countf = countf + 1
                        else:
                            countn = countn + 1
            tkinter.messagebox.showinfo('변환 완료',' 파일 복호화를 완료했습니다. \n P : ' + str(countp) + ' N : ' + str(countn) + ' F : ' + str(countf) + ' ')
            try:
                shutil.rmtree('temp271')
            except:
                pass
            win.update()
            
        go = tkinter.Button(win, text = '< 변환 >', font = ('Consolas',14), command = func)
        go.place(x = 140,y = 270) # 변환 진행

        win.mainloop()

off = True
k = mainclass()
while off:
    time.sleep(0.1)
    k.mainfunc()
time.sleep(0.5)
    

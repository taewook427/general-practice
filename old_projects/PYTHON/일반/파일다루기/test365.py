import os
import shutil
import time
import random

import multiprocessing as mp

import tkinter
import tkinter.messagebox
from tkinter import filedialog
import tkinter.ttk

import zipfile

import oreo
import kerbal
import mung2
import nox2
import test401

class mainclass:

    def mainfunc(self):
        win = tkinter.Tk()
        win.title('KOS 2023 - KDM')
        win.geometry("500x400+200+100")
        win.resizable(False, False)

        def but0f(): #zip release
            time.sleep(0.1)
            nonlocal win
            win.destroy()
            k = mainclass()
            k.zipre()
        but0 = tkinter.Button(win, text = 'ZIP release ', font = ('Consolas',20), command = but0f)
        but0.place(x = 10,y = 10)

        def but1f(): # file deleter
            time.sleep(0.1)
            nonlocal win
            win.destroy()
            k = mainclass()
            k.fdel()
        but1 = tkinter.Button(win, text = 'file deleter', font = ('Consolas',20), command = but1f)
        but1.place(x = 220,y = 10)

        def but2f(): # kzip pack
            time.sleep(0.1)
            nonlocal win
            win.destroy()
            k = kzip()
            k.pack()
        but2 = tkinter.Button(win, text = 'KZIP pack   ', font = ('Consolas',20), command = but2f)
        but2.place(x = 10,y = 80)

        def but3f(): # kzip unpack
            time.sleep(0.1)
            nonlocal win
            win.destroy()
            k = kzip()
            k.unpack()
        but3 = tkinter.Button(win, text = 'KZIP unpack ', font = ('Consolas',20), command = but3f)
        but3.place(x = 220,y = 80)

        def but4f(): # kpng pack
            time.sleep(0.1)
            nonlocal win
            win.destroy()
            k = kpng()
            k.pack()
        but4 = tkinter.Button(win, text = 'KPNG pack   ', font = ('Consolas',20), command = but4f)
        but4.place(x = 10,y = 150)

        def but5f(): # kpng unpack
            time.sleep(0.1)
            nonlocal win
            win.destroy()
            k = kpng()
            k.unpack()
        but5 = tkinter.Button(win, text = 'KPNG unpack ', font = ('Consolas',20), command = but5f)
        but5.place(x = 220,y = 150)

        def but6f(): # kaes pack
            time.sleep(0.1)
            nonlocal win
            win.destroy()
            k = kaes()
            k.pack()
        but6 = tkinter.Button(win, text = 'KAES pack   ', font = ('Consolas',20), command = but6f)
        but6.place(x = 10,y = 220)

        def but7f(): # kaes unpack
            time.sleep(0.1)
            nonlocal win
            win.destroy()
            k = kaes()
            k.unpack()
        but7 = tkinter.Button(win, text = 'KAES unpack ', font = ('Consolas',20), command = but7f)
        but7.place(x = 220,y = 220)

        def but8f(): # kaes old
            time.sleep(0.1)
            nonlocal win
            win.destroy()
            k = kaes()
            k.old()
        but8 = tkinter.Button(win, text = ' A ', font = ('Consolas',20), command = but8f)
        but8.place(x = 430,y = 10)

        def but9f(): # dcl old 2
            time.sleep(0.1)
            nonlocal win
            win.destroy()
            k = mainclass()
            k.dcl2()
        but9 = tkinter.Button(win, text = ' B ', font = ('Consolas',20), command = but9f)
        but9.place(x = 430,y = 80)

        def but10f(): # dcloud pack
            time.sleep(0.1)
            nonlocal win
            win.destroy()
            k = mainclass()
            k.dcl3pack()
        but10 = tkinter.Button(win, text = ' C ', font = ('Consolas',20), command = but10f)
        but10.place(x = 430,y = 150)

        def but11f(): # dcloud unpack
            time.sleep(0.1)
            nonlocal win
            win.destroy()
            k = mainclass()
            k.dcl3unpack()
        but11 = tkinter.Button(win, text = ' D ', font = ('Consolas',20), command = but11f)
        but11.place(x = 430,y = 220)

        def exitf(): # X 버튼
            global off
            off = False
            nonlocal win
            win.destroy()
        win.protocol('WM_DELETE_WINDOW', exitf)

        t = 'RZIP : 파일들 - *.png(ZIP)\nKZIP : 파일들/폴더 - *.png(kzip)\nKPNG : 파일들/폴더 - KZIP - *.png(PNG)\nKAES : 파일 - *.png(KAES)\n설정 : 프로그램 폴더 내 settings.txt 파일'
        label0 = tkinter.Label( win, text=t, font = ('Consolas',14) )
        label0.place(x=10,y=280)
        label1 = tkinter.Label( win, text='추가메뉴\nKAES old\nDcl old2\nDcl pack\nDcl unpk', font = ('Consolas',14) )
        label1.place(x=415,y=280)
        win.mainloop()

    def zipre(self):
        win = tkinter.Tk()
        win.title('KOS 2023 - KDM')
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
            nonlocal combo0
            otool = oreo.toolbox()
            settings = otool.readfile('settings.txt')
            mode = combo0.get()[0]
            if mode[0] == '1': #처음 사용자용 배포
                path = settings['settings#rzip#p0']
            else: #다목적 배포
                path = settings['settings#rzip#p1']
            try:
                shutil.rmtree('temp365')
            except:
                pass
            try:
                os.remove('temp365.zip')
            except:
                pass
            os.mkdir('temp365')
            names = [ ] # 단순 파일명
            for i in files:
                temp = i.replace('/','\\')
                names.append( temp[temp.rfind('\\')+1:] )
            for i in range( 0,len(files) ):
                shutil.copyfile(files[i], 'temp365\\' + names[i]) # 파일 복사

            out = os.path.join(os.path.expanduser('~'),'Desktop') + '\\' + str( random.randrange(100000,1000000) ) + '.png' # 결과 파일 이름
            temp = zipfile.ZipFile("temp365.zip", "w")
            for i in names:
                temp.write('temp365\\' + i, compress_type=zipfile.ZIP_DEFLATED)
            temp.close() # 임시 압축파일 생성

            with open(path,'rb') as f:
                pngdata = f.read() # png bytes ###
            with open('temp365.zip','rb') as f:
                binary = f.read() # tgt zip bytes
            cheadloc = decode( binary[-6:-2] ) # 중앙 헤더 위치
            num = decode( binary[-12:-10] ) # 파일 개수
            fdata = binary[0:cheadloc] # 압축된 데이터 바이트 ###
                          
            ehead = binary[-22:-6] + encode( len(pngdata) + cheadloc ) + binary[-2:] # end head ###
            chead = b'' # 중앙 헤더 ###
            temp = cheadloc
            for i in range(0,num):
                seta = binary[temp:temp+28]
                flen = decode( binary[temp+28:temp+30] ) # file name len
                setb = binary[temp+30:temp+42]
                start = encode( decode( binary[temp+42:temp+46] ) + len(pngdata) )
                fname = binary[temp+46:temp+46+flen]
                chead = chead + seta + binary[temp+28:temp+30] + setb + start + fname
                temp = temp + 46 + flen

            with open(out,'wb') as f:
                f.write(pngdata)
                f.write(fdata)
                f.write(chead)
                f.write(ehead)
            
            win.update()
            os.remove('temp365.zip')
            shutil.rmtree('temp365')
            tkinter.messagebox.showinfo('변환 완료',' png added zip 변환 완료 \n 바탕화면 ' + out + ' 생성되었습니다. ')
            
        but3 = tkinter.Button(win, text = 'COM', font = ('Consolas',14), command = but3f)
        but3.place(x = 190,y = 350) # 변환 진행

        modes = ['1) 처음 사용자용 배포','2) 일반 다목적 배포']
        combo0 = tkinter.ttk.Combobox(win, width=20, font = ("Consolas",14), values = modes)
        combo0.set( modes[0] ) #모드
        combo0.place(x=250,y=355)

        def encode(num): # 4 바이트 인코딩
            k = [ ]
            for i in range( 0,4 ):
                k.append( num % 256 )
                num = num // 256
            j = bytes( { k[0] } )
            for i in range( 1,len(k) ):
                j = j + bytes( { k[i] } )
            return j
        
        def decode(binary): # 디코딩
            value = 0
            for i in range( 0,len(binary) ):
                k = 256 ** i
                k = k * binary[i]
                value = value + k
            return value

        win.mainloop()

    def fdel(self):
        win = tkinter.Tk()
        win.title('KOS 2023 - KDM')
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
            ktool = kerbal.basic()
            mode = combo0.get()[0][0]
            ktool = kerbal.basic()
            err = 0
            otool = oreo.toolbox()
            temp = otool.readfile('settings.txt')
            core = temp['settings#fdel#core'] # core num
            for i in range( 0,len(files) ):
                try:
                    if mode == '1':
                        tool = mainclass()
                        tool.df(core,'1',files[i])
                        time.sleep(0.1)
                    elif mode == '2':
                        size = os.path.getsize(files[i])
                        f = open(files[i],'wb')
                        if size > 1048576:
                            f.write( ktool.getrandom( bytes( str( int( time.time() ) ),encoding='utf-8' ), 1048576 ) )
                        else:
                            f.write( ktool.getrandom( bytes( str( int( time.time() ) ),encoding='utf-8' ), size ) )
                        f.close()
                        time.sleep(0.1)
                        os.remove(files[i])
                    elif mode == '3':
                        tool = mainclass()
                        tool.df(core,'0',files[i])
                        time.sleep(0.1)
                    elif mode == '4':
                        size = os.path.getsize(files[i])
                        f = open(files[i],'wb')
                        tool = mainclass()
                        if size > 1048576:
                            f.write( tool.mkr('0',1048576) )
                        else:
                            f.write( tool.mkr('0',size) )
                        f.close()
                        time.sleep(0.1)
                        os.remove(files[i])
                    files[i] = '///CLEAR///'
                    listbox.delete(i)
                    listbox.insert( i,'///CLEAR///' )
                except Exception as e:
                    print(e)
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

        modes = ['1) 완전난수 + 전체','2) 완전난수 + 부분','3) 일반난수 + 전체','4) 일반난수 + 부분']
        combo0 = tkinter.ttk.Combobox(win, width=20, font = ("Consolas",14), values = modes)
        combo0.set( modes[0] ) #모드
        combo0.place(x=250,y=355)

        win.mainloop()

    def df(self,core,mode,path): # mode '0' 일반 '1' 보안
        size = os.path.getsize(path) # file size
        re = (size // 5242880) + 1 # 5MB * re
        numa = re // core
        numb = re % core
        os.remove(path)
        tool = mainclass()
        func = tool.mkr # r func
        f = open(path,'wb')
        p = mp.Pool(core)
        for i in range(0,numa):
            temp0 = [0] * core
            temp1 = [0] * core
            for j in range(0,core):
                temp0[j] = p.apply_async(func,(mode,5242880))
            for j in range(0,core):
                temp1[j] = temp0[j].get()
            f.write( b''.join(temp1) )
        temp0 = [0] * numb
        temp1 = [0] * numb
        for i in range(0,numb):
            temp0[i] = p.apply_async(func,(mode,5242880))
        for i in range(0,numb):
            temp1[i] = temp0[i].get()
        f.write( b''.join(temp1) )
        f.close()
        os.remove(path)
        p.close()
        p.join()

    def mkr(self,mode,size): # r data gen
        if mode == '0': # 일반
            numa = size // 20
            numb = size % 20
            seed = int( str( float( time.time() ) ).replace('.','0')[-6:] )
            if seed < 100000:
                seed = seed + 100000
            out = [''] * numa
            for i in range(0,numa):
                keya = random.randrange(10000000,100000000)
                keyb = random.randrange(10000000,100000000)
                temp = str( int( str(keya / keyb).replace('.','0') ) * seed )
                if len(temp) < 20:
                    temp = temp + ( 20 - len(temp) ) * '0'
                else:
                    temp = temp[-20:]
                out[i] = temp
            keya = random.randrange(10000000,100000000)
            keyb = random.randrange(10000000,100000000)
            temp = str( int( str(keya / keyb).replace('.','0') ) * seed )
            if len(temp) < 20:
                temp = temp + ( 20 - len(temp) ) * '0'
            else:
                temp = temp[-20:]
            temp = temp[0:numb]
            out.append(temp)
            temp = bytes(''.join(out),encoding='utf-8')
        elif mode == '1': # 보안
            ktool = kerbal.basic()
            temp = ktool.getrandom( bytes( str( int( time.time() ) ),encoding='utf-8' ), size )
        else:
            temp = b'\x00' * size
        return temp

    def dcl2(self):
        win = tkinter.Tk()
        win.title('KOS 2023 - KDM')
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

        path = '' # 폴더 위치
        num = 0 # 파일 개수
        salt = '' # salt
        pwhash = b'' # pwh
        fname = '' # f name
        fsize = 0 # f size
        def getpath():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal path
            nonlocal num
            path = filedialog.askdirectory(title='폴더 선택').replace('/','\\')
            num = 0
            while os.path.isfile(path + '\\' + str(num) + '.png'):
                num = num + 1
            listbox.delete( 0,listbox.size() )
            listbox.insert( 0,'폴더 위치 : '+path )
            listbox.insert( 1,'파일 개수 : '+str(num) )
            listbox.insert( 2,'. . .' )
            win.update()
            temp = test401.check(path,num)
            nonlocal salt
            nonlocal pwhash
            nonlocal fname
            nonlocal fsize
            salt = temp[0]
            pwhash = temp[1]
            hint = temp[2]
            fname = temp[3]
            fsize = temp[4]
            listbox.insert( 3,'salt str : '+salt )
            listbox.insert( 4,'pw hash : '+str(pwhash) )
            listbox.insert( 5,'file name : '+fname )
            listbox.insert( 6,'chunk size : '+str(fsize) )
            listbox.insert( 7,'. . .' )
            listbox.insert( 8,hint[0:32] )
            listbox.insert( 9,hint[32:64] )
            win.update()
        but0 = tkinter.Button(win, text = '...', font = ('Consolas',14), command = getpath)
        but0.place(x = 10,y = 350) # 파일 추가

        in0 = tkinter.Entry(width=35, font = ('맑은 고딕',14), show = '●')
        in0.grid(column = 0 , row = 0)
        in0.place(x=65,y=355) # pw in

        def gof():
            time.sleep(0.1)
            nonlocal win
            nonlocal path
            nonlocal num
            nonlocal salt
            nonlocal pwhash
            nonlocal fname
            nonlocal fsize
            if num == 0:
                tkinter.messagebox.showinfo('파일 없음',' DCloud2 사진화 데이터가 감지되지 않았습니다. \n 폴더를 다시 선택해 주십시오. ')
            else:
                nonlocal in0
                pw = in0.get() # pw str
                temp = test401.pw(salt,pw,pwhash)
                if temp[0] == 'P':
                    key = temp[1]
                    iv = temp[2]
                    test401.unpack(fname,fsize,key,iv)
                    tkinter.messagebox.showinfo('변환 완료',' 파일 디코딩이 완료되었습니다. \n 바탕화면에서 확인하십시오. ')
                else:
                    tkinter.messagebox.showinfo('비밀번호 불일치',' 파일 비밀번호가 일치하지 않습니다. \n 다시 입력해 주십시오. ')
            win.update()
            
        but1 = tkinter.Button(win, text = '진행', font = ('Consolas',14), command = gof)
        but1.place(x = 430,y = 350)

        win.mainloop()

    def dcl3pack(self):
        win = tkinter.Tk()
        win.title('KOS 2023 - KDM')
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

        path0 = [ ] # 파일/폴더 목록
        def f0():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal path0
            nonlocal mode1
            path0 = [ ]
            listbox.delete( 0,listbox.size() )
            if mode1 == 'file':
                temp = filedialog.askopenfiles( title='파일들 선택', filetypes=( ('all files', '*.*'),('exe files', '*.exe') ) )
                for i in temp:
                    path0.append(i.name)
            else:
                path0 = [ filedialog.askdirectory(title='폴더 선택') ]
            for i in path0:
                listbox.insert( listbox.size(),i )
            win.update()
        but0 = tkinter.Button(win, text = '...', font = ('Consolas',14), command = f0)
        but0.place(x = 10,y = 10) # 파일/폴더 추가

        txt1 = tkinter.StringVar()
        txt1.set('/M/\n\nfi \nle ')
        mode1 = 'file' # 파일/폴더 모드 'file' 'folder'
        def f1():
            time.sleep(0.1)
            nonlocal win
            nonlocal txt1
            nonlocal mode1
            if mode1 == 'file':
                mode1 = 'folder'
                txt1.set('/M/\n\nfol\nder')
            else:
                mode1 = 'file'
                txt1.set('/M/\n\nfi \nle ')
            nonlocal path0
            nonlocal listbox
            path0 = [ ]
            listbox.delete( 0,listbox.size() )
            win.update()
        but1 = tkinter.Button(win, textvariable = txt1, font = ('Consolas',14), command = f1)
        but1.place(x = 10,y = 60) # 파일/폴더 모드

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

        mode7 = True # 위장 여부 T위장 F일반
        txt7 = tkinter.StringVar()
        txt7.set('위장 : O')
        def f7():
            time.sleep(0.1)
            nonlocal win
            nonlocal mode7
            nonlocal txt7
            if mode7:
                mode7 = False
                txt7.set('위장 : X')
            else:
                mode7 = True
                txt7.set('위장 : O')
            win.update()
        but7 = tkinter.Button(win, textvariable = txt7, font = ('Consolas',14), command = f7)
        but7.place(x = 10,y = 310) # 위장 여부

        def func():
            time.sleep(0.1)
            nonlocal win
            nonlocal path0 # 파일/폴더 목록
            nonlocal mode1 # 파일/폴더 모드 'file' 'folder'
            nonlocal path2 # 키 파일 경로 get 주의!
            nonlocal in4 # pw in A
            nonlocal in5 # pw in B
            nonlocal in6 # hint in
            nonlocal mode7 # 위장 여부 T위장 F일반

            otool = oreo.toolbox()
            mtool = mung2.toolbox()
            ntool = nox2.toolbox()
            ktool = kerbal.toolbox()
            temp = otool.readfile('settings.txt')
            core = temp['settings#dcloud#core'] # core num
            chunk = temp['settings#dcloud#chunk'] # chunk size
            png = temp['settings#dcloud#p0'] # png path
            kf = ktool.getkeyfile( path2.get() ) # ketfile bytes
            pwa = in4.get() # pwa str
            pwb = in5.get() # pwb str
            hint = in6.get('1.0','end') # hint str

            if path0 == [ ]:
                tkinter.messagebox.showinfo('빈 리스트 경고',' 대상 파일/폴더가 없습니다. \n 변환할 파일/폴더를 선택하십시오. ')
                
            else:
                if pwa == pwb:
                    spec = ' 키 파일 크기 : ' + str( len(kf) ) + ' 바이트 \n 비밀번호 길이 : ' + str( len(pwa) ) + ' 글자 \n 다음과 같이 변환을 진행합니다. '
                    ask = tkinter.messagebox.askokcancel('변환 요소 확인',spec)
                    if ask:
                        try:
                            shutil.rmtree('temp365')
                        except:
                            pass
                        try:
                            shutil.rmtree('temp270')
                        except:
                            pass
                        os.mkdir('temp365')
                        temp = [ ]
                        for i in path0:
                            temp.append( i.replace('/','\\') )
                        if mode1 == 'file':
                            mtool.pack(temp,'temp365\\step0.dat','False')
                        else:
                            mtool.pack(temp[0],'temp365\\step0.dat','False') # user data -> kzip 변환

                        try:
                            shutil.rmtree('temp271')
                        except:
                            pass
                        try:
                            nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) ) #시간 구조
                            with open('temp400.txt','w',encoding='utf-8') as f:
                                f.write('kaes\n' + str(core) + '\n' + nowtime + '\n' + 'Encrypting User Data\n')
                            os.startfile('test400\\test400.exe')
                            time.sleep(0.3)
                        except:
                            pass
                        ktool.encryptall( os.path.abspath('temp365\\step0.dat').replace('/','\\'), pwa, hint, bytes(nowtime,encoding='utf-8'), 3, core, chunk, kf)
                        time.sleep(0.5) # kzip -> kaes

                        mtool.pack('temp365\\step0.dat.k','temp365\\step2.dat','False') # kaes -> kzip
                        time.sleep(0.2)

                        ntool.set(core,png)
                        try:
                            nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) ) #시간 구조
                            with open('temp400.txt','w',encoding='utf-8') as f:
                                f.write('kpng\n' + str(core) + '\n' + nowtime + '\n' + 'KPNG Encoding...\n')
                            os.startfile('test400\\test400.exe')
                            time.sleep(0.3)
                        except:
                            pass
                        temp = ntool.pack('temp365\\step2.dat',not(mode7),'png') # kzip -> kpng
                        time.sleep(0.5)
                        num = temp[0] # 개수
                        name = temp[1] #  일련번호

                        out = os.path.join(os.path.expanduser('~'),'Desktop') + '\\' + str( random.randrange(100000,1000000) ) # 바탕화면 폴더
                        try:
                            shutil.rmtree(out)
                        except:
                            pass
                        os.mkdir(out)
                        for i in range(0,num):
                            shutil.move('temp270\\' + name + str(i) + '.png', out + '\\' + name + str(i) + '.png')
                        try:
                            shutil.rmtree('temp270')
                        except:
                            pass
                        try:
                            shutil.rmtree('temp271')
                        except:
                            pass
                        try:
                            shutil.rmtree('temp365')
                        except:
                            pass
                        tkinter.messagebox.showinfo('변환 완료',' DCloud3 파일 패킹 완료 \n 바탕화면 ' + out + ' 생성되었습니다.\n 일련번호 : ' + name + ' 사진개수 : ' + str(num) + ' ')
                
                else:
                    tkinter.messagebox.showinfo('비밀번호 불일치',' 비밀번호 - 비밀번호 확인이 불일치합니다. \n 다시 입력해 주십시오. ')
            
            win.update()
            
        go = tkinter.Button(win, text = '< 변환 >', font = ('Consolas',14), command = func)
        go.place(x = 10,y = 355) # 변환 진행

        win.mainloop()

    def dcl3unpack(self):
        win = tkinter.Tk()
        win.title('KOS 2023 - KDM')
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

        def f0():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal mode1
            otool = oreo.toolbox()
            mtool = mung2.toolbox()
            ntool = nox2.toolbox()
            ktool = kerbal.toolbox()
            listbox.delete( 0,listbox.size() )
            temp = otool.readfile('settings.txt')
            core = temp['settings#dcloud#core'] # core num
            try:
                shutil.rmtree('temp365')
            except:
                pass
            os.mkdir('temp365')
            if mode1 == 'file':
                temp = filedialog.askopenfiles( title='파일들 선택', filetypes=( ('all files', '*.*'),('png files', '*.png') ) )
                raw = [ ] # 원본 파일 이름들
                for i in temp:
                    raw.append(i.name)
                for i in raw:
                    shutil.copyfile( i, 'temp365\\' + i[i.rfind('/')+1:] )
                temp = 'temp365'
            else:
                temp = filedialog.askdirectory(title='폴더 선택') # 폴더 이름
            listbox.insert( listbox.size(),'폴더 위치 : ' + temp )
            path = temp
            temp = ntool.detect(temp)
            listbox.insert( listbox.size(),'개수 : ' + str(temp[0]) + ' 일련번호 : ' + temp[1] + ' 형식 : ' + temp[2] )

            if temp[0] != 0:
                listbox.insert( listbox.size(),'...' )
                win.update()
                num = temp[0] # pic num
                name = temp[1] # pic name
                tp = temp[2] # pic type
                ntool.set(core,'')
                try:
                    shutil.rmtree('temp270')
                except:
                    pass
                try:
                    nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) ) #시간 구조
                    with open('temp400.txt','w',encoding='utf-8') as f:
                        f.write('kpng\n' + str(core) + '\n' + nowtime + '\n' + 'KPNG Dncoding...\n')
                    os.startfile('test400\\test400.exe')
                    time.sleep(0.3)
                except:
                    pass
                temp = ntool.unpack([path,num,name,tp])
                time.sleep(0.5)
                mtool.unpack('temp270\\result.dat')
                shutil.rmtree('temp270')
                time.sleep(0.2)
                #temp261\\step0.dat.k
                temp = ktool.checkall('temp261\\step0.dat.k')
                nonlocal hint6
                if temp[0] == 'V':
                    hint6.set( temp[1][6] )
                    listbox.insert( listbox.size(),'Ready To Unpack Dcl3 File' )
                else:
                    hint6.set('')
                    listbox.insert( listbox.size(),'Not Valid KAES-3 File' )
            try:
                shutil.rmtree('temp365')
            except:
                pass
            
            win.update()
        but0 = tkinter.Button(win, text = '...', font = ('Consolas',14), command = f0)
        but0.place(x = 10,y = 10) # 파일/폴더 추가

        txt1 = tkinter.StringVar()
        txt1.set('/M/\n\nfi \nle ')
        mode1 = 'file' # 파일/폴더 모드 'file' 'folder'
        def f1():
            time.sleep(0.1)
            nonlocal win
            nonlocal txt1
            nonlocal mode1
            if mode1 == 'file':
                mode1 = 'folder'
                txt1.set('/M/\n\nfol\nder')
            else:
                mode1 = 'file'
                txt1.set('/M/\n\nfi \nle ')
            nonlocal listbox
            listbox.delete( 0,listbox.size() )
            win.update()
        but1 = tkinter.Button(win, textvariable = txt1, font = ('Consolas',14), command = f1)
        but1.place(x = 10,y = 60) # 파일/폴더 모드

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

        hint6 = tkinter.StringVar()
        hint6.set('')
        label6 = tkinter.Label(win, font = ('맑은 고딕',14), textvariable=hint6)
        label6.place(x=280,y=230) # 힌트 표시

        mode7 = True # 풀기 위치 T 바탕화면 F 임시폴더
        txt7 = tkinter.StringVar()
        txt7.set('풀기 위치 : 바탕화면')
        def f7():
            time.sleep(0.1)
            nonlocal win
            nonlocal mode7
            nonlocal txt7
            if mode7:
                mode7 = False
                txt7.set('풀기 위치 : 임시폴더')
            else:
                mode7 = True
                txt7.set('풀기 위치 : 바탕화면')
            win.update()
        but7 = tkinter.Button(win, textvariable = txt7, font = ('Consolas',14), command = f7)
        but7.place(x = 10,y = 310) # 위장 여부

        def func():
            time.sleep(0.1)
            nonlocal win
            nonlocal path2 # 키 파일 경로
            nonlocal in4 # pw in A
            nonlocal mode7 # 풀기 위치 T 바탕화면 F 임시폴더
            ktool = kerbal.toolbox()
            pw = in4.get() # pw str
            kf = ktool.getkeyfile( path2.get() ) # key file bytes
            spec = ' 키 파일 크기 : ' + str( len(kf) ) + ' 바이트 \n 비밀번호 길이 : ' + str( len(pw) ) + ' 글자 \n 다음과 같이 복호화를 진행합니다. '
            ask = tkinter.messagebox.askokcancel('변환 요소 확인',spec)
            if ask:
                try:
                    shutil.rmtree('temp271')
                except:
                    pass
                temp = ktool.checkall('temp261\\step0.dat.k')
                fstart = temp[1][0]
                core = temp[1][1]
                chunk = temp[1][2]
                ckeydt = temp[1][3]
                salt = temp[1][4]
                pwhash = temp[1][5]
                tkeydt = temp[1][7]
                title = temp[1][8]
                temp = ktool.pwall(pw, kf, salt, pwhash, [ckeydt, tkeydt, title]) # pw check

                if temp[0] == 'V':
                    ckey = temp[1]
                    iv = temp[2]
                    fname = temp[3]
                    try:
                        nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) ) #시간 구조
                        with open('temp400.txt','w',encoding='utf-8') as f:
                            f.write('kaes\n' + str(core) + '\n' + nowtime + '\n' + 'Decrypting User Data\n')
                        os.startfile('test400\\test400.exe')
                        time.sleep(0.3)
                    except:
                        pass
                    ktool.decryptall(['temp261\\step0.dat.k',fstart,fname,core,chunk,ckey,iv])
                    time.sleep(0.5)

                    try:
                        shutil.rmtree('temp271')
                    except:
                        pass
                    try:
                        shutil.rmtree('temp365')
                    except:
                        pass
                    os.mkdir('temp365')

                    mtool = mung2.toolbox()
                    shutil.move('temp261\\step0.dat','temp365\\step0.dat')
                    mtool.unpack( os.path.abspath('temp365\\step0.dat') )
                    
                    shutil.rmtree('temp365')
                    if mode7:
                        out = os.path.join(os.path.expanduser('~'),'Desktop') + '\\' + str( random.randrange(100000,1000000) ) # 바탕화면 폴더
                        shutil.move('temp261',out)
                        tkinter.messagebox.showinfo('변환 완료',' Dcloud 3 파일 언패킹 완료 \n 바탕화면 ' + out + ' 생성되었습니다. ')
                    else:
                        tkinter.messagebox.showinfo('변환 완료',' Dcloud 3 파일 언패킹 완료 \n 프로그램 임시폴더 temp261 생성되었습니다. ')
                        time.sleep(0.1)
                        os.startfile('temp261')
                    
                else:
                    tkinter.messagebox.showinfo('비밀번호 불일치',' 비밀번호가 일치하지 않습니다. \n 비밀번호와 키 파일 경로를 확인하십시오. ')
            win.update()
            
        go = tkinter.Button(win, text = '< 변환 >', font = ('Consolas',14), command = func)
        go.place(x = 10,y = 355) # 변환 진행

        win.mainloop()

class kzip:

    def pack(self):
        win = tkinter.Tk()
        win.title('KOS 2023 - KDM')
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

        files = [ ] #파일/폴더 경로들
        mode = 'file' # mode file / folder
        png = True # png 위장

        def f0():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal files
            nonlocal mode
            files = [ ]
            listbox.delete( 0,listbox.size() )
            if mode == 'file':
                temp = filedialog.askopenfiles( title='파일들 선택', filetypes=( ('all files', '*.*'),('exe files', '*.exe') ) )
                for i in temp:
                    files.append(i.name)
            else:
                files = [ filedialog.askdirectory(title='폴더 선택') ]
            for i in files:
                listbox.insert( listbox.size(),i )
            win.update()
        but0 = tkinter.Button(win, text = '...', font = ('Consolas',14), command = f0)
        but0.place(x = 10,y = 350) # 파일/폴더 가져오기

        txt1 = tkinter.StringVar()
        txt1.set('모드 : 파일')
        def f1():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal files
            nonlocal txt1
            nonlocal mode
            files = [ ]
            listbox.delete( 0,listbox.size() )
            if mode == 'file':
                mode = 'folder'
                txt1.set('모드 : 폴더')
            else:
                mode = 'file'
                txt1.set('모드 : 파일')
            win.update()
        but1 = tkinter.Button(win, textvariable = txt1, font = ('Consolas',14), command = f1)
        but1.place(x = 110,y = 350) # 파일/폴더 선택

        txt2 = tkinter.StringVar()
        txt2.set('위장 : O')
        def f2():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal png
            nonlocal txt2
            if png:
                png = False
                txt2.set('위장 : X')
            else:
                png = True
                txt2.set('위장 : O')
            win.update()
        but2 = tkinter.Button(win, textvariable = txt2, font = ('Consolas',14), command = f2)
        but2.place(x = 290,y = 350) # 위장 선택

        def f3(): # 빈 file list 주의
            time.sleep(0.1)
            nonlocal win
            nonlocal files
            nonlocal mode
            nonlocal png
            mtool = mung2.toolbox()
            if files == [ ]:
                tkinter.messagebox.showinfo('빈 리스트 경고',' 대상 파일/폴더가 없습니다. \n 변환할 파일/폴더를 선택하십시오. ')
            else:
                out = os.path.join(os.path.expanduser('~'),'Desktop') + '\\' + str( random.randrange(100000,1000000) ) + '.png' # 결과 파일 이름
                temp = [ ]
                for i in files:
                    temp.append( i.replace('/','\\') )
                if mode == 'file':
                    mtool.pack(temp,out,png)
                else:
                    mtool.pack(temp[0],out,png)
                win.update()
                tkinter.messagebox.showinfo('변환 완료',' kzip 파일로 변환 완료 \n 바탕화면 ' + out + ' 생성되었습니다. ')
        but3 = tkinter.Button(win, text = '진행', font = ('Consolas',14), command = f3)
        but3.place(x = 430,y = 350) # 변환 진행

        win.mainloop()

    def unpack(self):
        win = tkinter.Tk()
        win.title('KOS 2023 - KDM')
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

        path = '' #kzip file path
        mode = True # T : 바탕화면 F : 임시폴더

        def f0():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal path
            mtool = mung2.toolbox()
            try:
                path = filedialog.askopenfile( title='파일 선택', filetypes=( ('all files', '*.*'),('png files', '*.png') ) )
                path = path.name
                size = os.path.getsize(path)
                temp = mtool.check(path)
                if temp[0] == 'N':
                    status = 'Not KZIP File'
                    chunk = 0
                elif temp[0] == 'E':
                    status = 'Broken KZIP File'
                    chunk = temp[1]
                else:
                    status = 'Valid KZIP File'
                    chunk = temp[1]
            except:
                path = ''
                size = 0
                status = 'File Not Selected'
                chunk = 0
            listbox.delete( 0,listbox.size() )
            listbox.insert( 0,path )
            listbox.insert( 1,'File Size : ' + str(size) + ' B' )
            listbox.insert( 2,'Status : ' + status )
            listbox.insert( 3,'Chunk Number : ' + str(chunk) )
            win.update()
        but0 = tkinter.Button(win, text = '...', font = ('Consolas',14), command = f0)
        but0.place(x = 10,y = 350) # 파일 가져오기
        
        txt1 = tkinter.StringVar()
        txt1.set('풀기 위치 : 바탕화면')
        def f1():
            time.sleep(0.1)
            nonlocal win
            nonlocal mode
            nonlocal txt1
            if mode:
                mode = False
                txt1.set('풀기 위치 : 임시폴더')
            else:
                mode = True
                txt1.set('풀기 위치 : 바탕화면')
            win.update()
        but1 = tkinter.Button(win, textvariable = txt1, font = ('Consolas',14), command = f1)
        but1.place(x = 130,y = 350) # 위장 선택

        def f2():
            time.sleep(0.1)
            nonlocal win
            nonlocal mode
            nonlocal path
            mtool = mung2.toolbox()
            if path != '':
                temp = mtool.check(path)
                if temp[0] != 'N':
                    out = mtool.unpack(path)
                    if out == 0:
                        if mode:
                            out = os.path.join(os.path.expanduser('~'),'Desktop') + '\\' + str( random.randrange(100000,1000000) ) # 바탕화면 폴더
                            shutil.move('temp261',out)
                            tkinter.messagebox.showinfo('변환 완료',' kzip 파일 언패킹 완료 \n 바탕화면 ' + out + ' 생성되었습니다. ')
                        else:
                            tkinter.messagebox.showinfo('변환 완료',' kzip 파일 언패킹 완료 \n 프로그램 임시폴더 temp261 생성되었습니다. ')
                            time.sleep(0.1)
                            os.startfile('temp261')
                    else:
                        tkinter.messagebox.showinfo('변환 중 오류',' kzip 파일 언패킹 중 오류 발생 \n CRC32 불일치로 파일 무결성이 훼손되었습니다. ')
            win.update()
        but2 = tkinter.Button(win, text = '진행', font = ('Consolas',14), command = f2)
        but2.place(x = 430,y = 350) # 변환 진행

        win.mainloop()

class kpng:

    def pack(self):
        win = tkinter.Tk()
        win.title('KOS 2023 - KDM')
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

        files = [ ] # 폴더 / 파일 경로들
        png = True # T : 위장, F : 전체저장
        size = '1' # 0소256 1중2600 2대4096
        mode = 'file' # 폴더 / 파일

        def f0():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal files
            nonlocal mode
            files = [ ]
            listbox.delete( 0,listbox.size() )
            if mode == 'file':
                temp = filedialog.askopenfiles( title='파일들 선택', filetypes=( ('all files', '*.*'),('png files', '*.png') ) )
                for i in temp:
                    files.append(i.name)
            else:
                files = [ filedialog.askdirectory(title='폴더 선택') ]
            for i in files:
                listbox.insert( listbox.size(),i )
            win.update()
        but0 = tkinter.Button(win, text = '...', font = ('Consolas',14), command = f0)
        but0.place(x = 10,y = 350) # 파일/폴더 가져오기

        txt1 = tkinter.StringVar()
        txt1.set('모드 : 파일')
        def f1():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal files
            nonlocal txt1
            nonlocal mode
            files = [ ]
            listbox.delete( 0,listbox.size() )
            if mode == 'file':
                mode = 'folder'
                txt1.set('모드 : 폴더')
            else:
                mode = 'file'
                txt1.set('모드 : 파일')
            win.update()
        but1 = tkinter.Button(win, textvariable = txt1, font = ('Consolas',14), command = f1)
        but1.place(x = 70,y = 350) # 파일/폴더 선택

        txt2 = tkinter.StringVar()
        txt2.set('위장 : O')
        def f2():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal png
            nonlocal txt2
            if png:
                png = False
                txt2.set('위장 : X')
            else:
                png = True
                txt2.set('위장 : O')
            win.update()
        but2 = tkinter.Button(win, textvariable = txt2, font = ('Consolas',14), command = f2)
        but2.place(x = 205,y = 350) # 위장 선택

        txt3 = tkinter.StringVar()
        txt3.set('사진 : 중')
        def f3():
            time.sleep(0.1)
            nonlocal win
            nonlocal size
            nonlocal txt3
            if size == '0':
                size = '1'
                txt3.set('사진 : 중')
            elif size == '1':
                size = '2'
                txt3.set('사진 : 대')
            else:
                size = '0'
                txt3.set('사진 : 소')
            win.update()
        but3 = tkinter.Button(win, textvariable = txt3, font = ('Consolas',14), command = f3)
        but3.place(x = 315,y = 350) # 위장 선택

        def f4():
            time.sleep(0.1)
            nonlocal win
            nonlocal files
            nonlocal png
            nonlocal size
            nonlocal mode
            otool = oreo.toolbox()
            ntool = nox2.toolbox()
            mtool = mung2.toolbox()
            temp = [ ]
            for i in files:
                temp.append( i.replace('/','\\') )
            try:
                os.remove('temp365.dat')
            except:
                pass
            if mode == 'file':
                mtool.pack(temp,'temp365.dat',False)
            else:
                mtool.pack(temp[0],'temp365.dat',False)
            settings = otool.readfile('settings.txt')
            core = settings['settings#kpng#core']
            p0 = settings['settings#kpng#p0']
            p1 = settings['settings#kpng#p1']
            p2 = settings['settings#kpng#p2']
            if size == '0':
                ntool.set(core,p0)
            elif size == '1':
                ntool.set(core,p1)
            else:
                ntool.set(core,p2)
            try:
                nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) ) #시간 구조
                with open('temp400.txt','w',encoding='utf-8') as f:
                    f.write('kpng\n' + str(core) + '\n' + nowtime + '\n' + 'KPNG Encoding...\n')
                os.startfile('test400\\test400.exe')
                time.sleep(0.3)
            except:
                pass
            temp = ntool.pack('temp365.dat',not(png),'png')
            time.sleep(0.5)
            num = temp[0] # 개수
            name = temp[1] #  일련번호
            out = os.path.join(os.path.expanduser('~'),'Desktop') + '\\' + str( random.randrange(100000,1000000) ) # 바탕화면 폴더
            try:
                shutil.rmtree(out)
            except:
                pass
            os.mkdir(out)
            for i in range(0,num):
                shutil.move('temp270\\' + name + str(i) + '.png', out + '\\' + name + str(i) + '.png')
            os.remove('temp365.dat')
            shutil.rmtree('temp270')
            tkinter.messagebox.showinfo('변환 완료',' kpng 파일 패킹 완료 \n 바탕화면 ' + out + ' 생성되었습니다.\n 일련번호 : ' + name + ' 사진개수 : ' + str(num) + ' ')
        but4 = tkinter.Button(win, text = '진행', font = ('Consolas',14), command = f4)
        but4.place(x = 430,y = 350) # 변환 진행

        win.mainloop()

    def unpack(self):
        win = tkinter.Tk()
        win.title('KOS 2023 - KDM')
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

        path = '' # 폴더 위치
        mode = True # T : 바탕화면 F : 임시폴더
        find = 'file' # 파일 탐색 / 폴더 탐색

        def f0():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal find
            nonlocal path
            ntool = nox2.toolbox()
            listbox.delete( 0,listbox.size() )
            if find == 'file':
                temp = filedialog.askopenfiles( title='파일들 선택', filetypes=( ('all files', '*.*'),('png files', '*.png') ) )
                raw = [ ] # 원본 파일 이름들
                for i in temp:
                    raw.append(i.name)
                try:
                    shutil.rmtree('temp365')
                except:
                    pass
                os.mkdir('temp365')
                for i in raw:
                    shutil.copyfile( i, 'temp365\\' + i[i.rfind('/')+1:] )
                temp = 'temp365'
            else:
                temp = filedialog.askdirectory(title='폴더 선택') # 폴더 이름
            listbox.insert( listbox.size(),'폴더 위치 : ' + temp )
            path = temp
            temp = ntool.detect(temp)
            listbox.insert( listbox.size(),'사진 개수 : ' + str(temp[0]) )
            listbox.insert( listbox.size(),'사진 일련번호 : ' + temp[1] )
            listbox.insert( listbox.size(),'사진 형식 : ' + temp[2] )
            win.update()
        but0 = tkinter.Button(win, text = '...', font = ('Consolas',14), command = f0)
        but0.place(x = 10,y = 350) # 파일 가져오기
        
        txt1 = tkinter.StringVar()
        txt1.set('풀기 : 바탕화면')
        def f1():
            time.sleep(0.1)
            nonlocal win
            nonlocal mode
            nonlocal txt1
            if mode:
                mode = False
                txt1.set('풀기 : 임시폴더')
            else:
                mode = True
                txt1.set('풀기 : 바탕화면')
            win.update()
        but1 = tkinter.Button(win, textvariable = txt1, font = ('Consolas',14), command = f1)
        but1.place(x = 70,y = 350) # 풀기 위치 정하기

        txt2 = tkinter.StringVar()
        txt2.set('탐색모드 : 파일')
        def f2():
            time.sleep(0.1)
            nonlocal win
            nonlocal txt2
            nonlocal find
            nonlocal listbox
            nonlocal path
            if find == 'file':
                find = 'folder'
                txt2.set('탐색모드 : 폴더')
            else:
                find = 'file'
                txt2.set('탐색모드 : 파일')
            listbox.delete( 0,listbox.size() )
            path = ''
            win.update()
        but2 = tkinter.Button(win, textvariable = txt2, font = ('Consolas',14), command = f2)
        but2.place(x = 250,y = 350) # 탐색 모드

        def f3():
            time.sleep(0.1)
            nonlocal win
            nonlocal path
            nonlocal mode
            nonlocal listbox
            otool = oreo.toolbox()
            mtool = mung2.toolbox()
            ntool = nox2.toolbox()
            if path != '':
                temp = otool.readfile('settings.txt')
                core = temp['settings#kpng#core'] # core num
                temp = ntool.detect(path)
                num = temp[0] # pic num
                name = temp[1] # pic name
                tp = temp[2] # pic type
                ntool.set(core,'')
                try:
                    nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) ) #시간 구조
                    with open('temp400.txt','w',encoding='utf-8') as f:
                        f.write('kpng\n' + str(core) + '\n' + nowtime + '\n' + 'KPNG Dncoding...\n')
                    os.startfile('test400\\test400.exe')
                    time.sleep(0.3)
                except:
                    pass
                temp = ntool.unpack([path,num,name,tp])
                time.sleep(0.5)
                mtool.unpack('temp270\\result.dat')
                shutil.rmtree('temp270')
                try:
                    shutil.rmtree('temp365')
                except:
                    pass
                if mode:
                    out = os.path.join(os.path.expanduser('~'),'Desktop') + '\\' + str( random.randrange(100000,1000000) ) # 바탕화면 폴더
                    shutil.move('temp261',out)
                    tkinter.messagebox.showinfo('변환 완료',' kpng 파일 언패킹 완료 \n 바탕화면 ' + out + ' 생성되었습니다. ')
                else:
                    tkinter.messagebox.showinfo('변환 완료',' kpng 파일 언패킹 완료 \n 프로그램 임시폴더 temp261 생성되었습니다. ')
                    time.sleep(0.1)
                    os.startfile('temp261')
            path = ''
            listbox.delete( 0,listbox.size() )
            win.update()
        but3 = tkinter.Button(win, text = '진행', font = ('Consolas',14), command = f3)
        but3.place(x = 430,y = 350) # 변환 진행

        win.mainloop()

class kaes:

    def old(self):
        win = tkinter.Tk()
        win.title('KOS 2023 - KDM')
        win.geometry("500x400+200+100")
        win.resizable(False, False)

        ktool = kerbal.old()

        def getfile():
            time.sleep(0.1)
            nonlocal path
            file = filedialog.askopenfile( title='파일 선택',filetypes=( ('all files', '*.*'),('k files', '*.k') ) )
            path.set( file.name )

            version = ktool.v1orv2( path.get() )
            nonlocal hint
            nonlocal salt
            nonlocal hash1
            if version == 1:
                result = ktool.v1check( path.get() )
                if result[0] == 'N':
                    hint.set('Error : Not Valid KAES V1 / V2 File')
                else:
                    salt = result[1]
                    hash1 = result[2]
                    txt = ''
                    for i in range(0,11):
                        txt = txt + result[3][30 * i:30 * i + 30] + '\n'
                    txt = txt[0:-1]
                    hint.set(txt)
            elif version == 2:
                result = ktool.v2check( path.get() )
                if result[0] == 'N':
                    hint.set('Error : Not Valid KAES V1 / V2 File')
                else:
                    salt = result[1]
                    hash1 = result[2]
                    txt = ''
                    for i in range(0,20):
                        txt = txt + result[3][30 * i:30 * i + 30] + '\n'
                    txt = txt[0:-1]
                    hint.set(txt)
                    nonlocal tdata
                    nonlocal tlen
                    nonlocal mode
                    tdata = result[4]
                    tlen = result[5]
                    mode = result[6]
            else:
                hint.set('Error : Not Valid KAES V1 / V2 File')
            nonlocal win
            win.update()
            
        but0 = tkinter.Button(win, text = '...', font = ('Consolas',14), command = getfile)
        but0.place(x = 10,y = 10)

        path = tkinter.StringVar()
        path.set('')
        label0 = tkinter.Label( win, textvariable=path, font = ('Consolas',14) )
        label0.place(x=60, y = 15)

        hint = tkinter.StringVar()
        hint.set('')
        label1 = tkinter.Label( win, textvariable=hint, font = ('Consolas',14) )
        label1.place(x=10, y = 60)

        salt = ''
        hash1 = ''
        tdata = ''
        tlen = ''
        mode = ''

        in0 = tkinter.Entry(width=40, font = ('맑은 고딕',14), show = '●')
        in0.grid(column = 0 , row = 0)
        in0.place(x=10,y=360)

        def gof():
            time.sleep(0.1)
            nonlocal salt
            nonlocal hash1
            nonlocal tdata
            nonlocal tlen
            nonlocal mode
            nonlocal in0
            nonlocal path
            pw = in0.get()
            ktool = kerbal.old()
            version = ktool.v1orv2( path.get() ) # 1 / 2
            
            if version == 1:
                result = ktool.v1pw(salt,hash1,pw)
                if result[0] == 'N':
                    tkinter.messagebox.showinfo('비밀번호 불일치',' 비밀번호가 일치하지 않습니다. ')
                else:
                    key = result[1] # v1 decrypt start
                    tkinter.messagebox.showinfo('디코딩 시작',' 비밀번호가 일치합니다.\n이 작업은 시간이 걸립니다. ')
                    ktool.v1decrypt(path.get(),key)
                    tkinter.messagebox.showinfo('디코딩 완료',' 디코딩을 완료했습니다.\n대상과 동일 폴더 내에 원본 파일이 생성되었습니다. ')
            else:
                result = ktool.v2pw([salt,hash1,pw,tdata,tlen,mode,path.get()])
                if result[0] == 'N':
                    tkinter.messagebox.showinfo('비밀번호 불일치',' 비밀번호가 일치하지 않습니다. ')
                else:
                    root = path.get()[0:path.get().rfind('/')+1] # result file path
                    root.replace('/','\\')
                    name = result[1].replace('/','\\')
                    name = name[name.rfind('\\')+1:] # result file name
                    ckey = result[2]
                    civ = result[3]
                    tkinter.messagebox.showinfo('디코딩 시작',' 비밀번호가 일치합니다.\n이 작업은 시간이 걸립니다. ')
                    ktool.v2decrypt(path.get(),root+name,ckey,civ)
                    tkinter.messagebox.showinfo('디코딩 완료',' 디코딩을 완료했습니다.\n대상과 동일 폴더 내에 원본 파일이 생성되었습니다. ')
            
        but1 = tkinter.Button(win, text = ' G O ', font = ('Consolas',14), command = gof)
        but1.place(x = 425,y = 355)

        win.mainloop()

    def pack(self):
        win = tkinter.Tk()
        win.title('KOS 2023 - KDM')
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

        mode1 = 'nor' # 삭제 강도 'nor' 'adv'
        txt1 = tkinter.StringVar()
        txt1.set('DEL\n\nnor\n')
        def f1():
            time.sleep(0.1)
            nonlocal win
            nonlocal mode1
            nonlocal txt1
            if mode1 == 'nor':
                mode1 = 'adv'
                txt1.set('DEL\n\nadv\n')
            else:
                mode1 = 'nor'
                txt1.set('DEL\n\nnor\n')
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

        mode8 = True # 위장 여부 T위장 F일반
        txt8 = tkinter.StringVar()
        txt8.set('위장 : O')
        def f8():
            time.sleep(0.1)
            nonlocal win
            nonlocal mode8
            nonlocal txt8
            if mode8:
                mode8 = False
                txt8.set('위장 : X')
            else:
                mode8 = True
                txt8.set('위장 : O')
            win.update()
        but8 = tkinter.Button(win, textvariable = txt8, font = ('Consolas',14), command = f8)
        but8.place(x = 140,y = 310) # 위장 여부

        mode9 = False # 이름 숨기기 여부 // T숨김 F공개
        txt9 = tkinter.StringVar()
        txt9.set('이름 : 공개')
        def f9():
            time.sleep(0.1)
            nonlocal win
            nonlocal mode9
            nonlocal txt9
            if mode9:
                mode9 = False
                txt9.set('이름 : 공개')
            else:
                mode9 = True
                txt9.set('이름 : 숨김')
            win.update()
        but9 = tkinter.Button(win, textvariable = txt9, font = ('Consolas',14), command = f9)
        but9.place(x = 10,y = 355) # 아름 숨김 여부

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
            nonlocal mode8 # 위장 여부 T위장 F일반
            nonlocal mode9 # 이름 숨기기 여부 // T숨김 F공개
            pwa = in4.get() # pw str
            pwb = in5.get()
            hint = in6.get('1.0','end')
            ktool = kerbal.toolbox()
            kf = ktool.getkeyfile( path2.get() ) # key file
            otool = oreo.toolbox()
            temp = otool.readfile('settings.txt')
            core = temp['settings#kaes#core'] # core num
            chunk = temp['settings#kaes#chunk'] # chunk size
            itool = mainclass()
            if pwa == pwb:
                spec = ' 파일 : ' + str( len(files) ) + ' 개 \n 키 파일 크기 : ' + str( len(kf) ) + ' 바이트 \n 비밀번호 길이 : ' + str( len(pwa) ) + ' 글자 \n 다음과 같이 암호화를 진행합니다. '
                ask = tkinter.messagebox.askokcancel('변환 요소 확인',spec)
                if ask:
                    success = 0
                    fail = 0
                    for i in files:
                        try:
                            try:
                                shutil.rmtree('temp271')
                            except:
                                pass
                            try:
                                nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) ) #시간 구조
                                with open('temp400.txt','w',encoding='utf-8') as f:
                                    f.write('kaes\n' + str(core) + '\n' + nowtime + '\n' + 'En ' + i[i.rfind('/')+1:] + '\n')
                                os.startfile('test400\\test400.exe')
                                time.sleep(0.3)
                            except:
                                pass
                            m = 0
                            if not(mode9):
                                m = m + 2
                            if not(mode8):
                                m = m + 1
                            ktool.encryptall( i.replace('/','\\'), pwa, hint, bytes(nowtime,encoding='utf-8'), m, core, chunk, kf)
                            time.sleep(0.5)
                            if mode7:
                                if mode1 == 'adv':
                                    itool.df(core,'0',i)
                                else:
                                    os.remove(i)
                            success = success + 1
                            time.sleep(0.2)
                        except:
                            fail = fail + 1
                    tkinter.messagebox.showinfo('변환 완료',' 파일 암호화를 완료했습니다. \n 성공 : ' + str(success) + ' 실패 : ' + str(fail) + ' ')
            else:
                tkinter.messagebox.showinfo('비밀번호 불일치',' 비밀번호 - 비밀번호 확인이 불일치합니다. \n 다시 입력해 주십시오. ')
            try:
                shutil.rmtree('temp271')
            except:
                pass
            win.update()
        go = tkinter.Button(win, text = '< 변환 >', font = ('Consolas',14), command = func)
        go.place(x = 140,y = 355) # 변환 진행

        win.mainloop()

    def unpack(self):
        win = tkinter.Tk()
        win.title('KOS 2023 - KDM')
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
            ktool = kerbal.toolbox()
            nonlocal hint5
            nonlocal current
            current = 0
            try:
                temp = ktool.checkall( files[current] )
                if temp[0] == 'V':
                    hint5.set( temp[1][6] )
                else:
                    hint5.set('Not Valid KAES-3 File')
            except:
                hint5.set('Not Valid KAES-3 File')
            win.update()
        but0 = tkinter.Button(win, text = '...', font = ('Consolas',14), command = f0)
        but0.place(x = 10,y = 10) # 파일 추가

        mode1 = 'nor' # 삭제 강도 'nor' 'adv'
        txt1 = tkinter.StringVar()
        txt1.set('DEL\n\nnor\n')
        def f1():
            time.sleep(0.1)
            nonlocal win
            nonlocal mode1
            nonlocal txt1
            if mode1 == 'nor':
                mode1 = 'adv'
                txt1.set('DEL\n\nadv\n')
            else:
                mode1 = 'nor'
                txt1.set('DEL\n\nnor\n')
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
            ktool = kerbal.toolbox()
            try:
                temp = ktool.checkall( files[current] )
                if temp[0] == 'V':
                    hint5.set( temp[1][6] )
                else:
                    hint5.set('Not Valid KAES-3 File')
            except:
                hint5.set('Not Valid KAES-3 File')
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
            ktool = kerbal.toolbox()
            itool = mainclass()
            pw = in4.get() # pw str
            kf = ktool.getkeyfile( path2.get() ) # key file bytes
            countn = 0 # not kaes file
            countp = 0 # decode success
            countf = 0 # not valid pw
            spec = ' 파일 : ' + str( len(files) ) + ' 개 \n 키 파일 크기 : ' + str( len(kf) ) + ' 바이트 \n 비밀번호 길이 : ' + str( len(pw) ) + ' 글자 \n 다음과 같이 복호화를 진행합니다. '
            ask = tkinter.messagebox.askokcancel('변환 요소 확인',spec)
            if ask:
                for i in files:
                    try:
                        try:
                            shutil.rmtree('temp271')
                        except:
                            pass
                        temp = ktool.checkall(i)
                        if temp[0] == 'V':
                            fstart = temp[1][0]
                            core = temp[1][1]
                            chunk = temp[1][2]
                            ckeydt = temp[1][3]
                            salt = temp[1][4]
                            pwhash = temp[1][5]
                            tkeydt = temp[1][7]
                            title = temp[1][8]
                            temp = ktool.pwall(pw, kf, salt, pwhash, [ckeydt, tkeydt, title]) # pw check
                            if temp[0] == 'V':
                                ckey = temp[1]
                                iv = temp[2]
                                fname = temp[3]
                                try:
                                    nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) ) #시간 구조
                                    with open('temp400.txt','w',encoding='utf-8') as f:
                                        f.write('kaes\n' + str(core) + '\n' + nowtime + '\n' + 'De ' + i[i.rfind('/')+1:] + '\n')
                                    os.startfile('test400\\test400.exe')
                                    time.sleep(0.3)
                                except:
                                    pass
                                ktool.decryptall([i.replace('/','\\'),fstart,fname,core,chunk,ckey,iv])
                                time.sleep(0.5)
                                if mode6:
                                    if mode1 == 'adv':
                                        itool.df(core,'0',i)
                                    else:
                                        os.remove(i)
                                countp = countp + 1
                            else:
                                countn = countn + 1
                        else:
                            countf = countf + 1
                        time.sleep(0.2)
                    except:
                        countf = countf + 1
            tkinter.messagebox.showinfo('변환 완료',' 파일 복호화를 완료했습니다. \n P : ' + str(countp) + ' N : ' + str(countn) + ' F : ' + str(countf) + ' ')
            try:
                shutil.rmtree('temp271')
            except:
                pass
            win.update()
            
        go = tkinter.Button(win, text = '< 변환 >', font = ('Consolas',14), command = func)
        go.place(x = 140,y = 270) # 변환 진행

        win.mainloop()

if __name__ == '__main__':
    global off
    off = True
    mp.freeze_support()
    k = mainclass()
    while off:
        time.sleep(0.1)
        k.mainfunc()
    time.sleep(0.5)

import os
import shutil
import time
import random

import multiprocessing as mp

import tkinter
import tkinter.messagebox
from tkinter import filedialog
import tkinter.ttk

import oreo
import kerbal
import mung2
import nox2

import kdcm3
import stream

class mainclass:

    def __init__(self):
        win = tkinter.Tk()
        win.title('KOS 2023 - DCL3')
        win.geometry("500x400+200+100")
        win.resizable(False, False)
        temp = '엣지 웹브라우저를\n최신 버전으로 유지하십시오.\n사람이 몰리는 저녁~새벽 시간에는\n오류 가능성이 높습니다.\n\n'
        label0 = tkinter.Label(win, text = temp + 'microsoft edge webdriver\n드라이버 업데이트 체크 중 ...', font = ('Consolas', 15) )
        label0.place(x=100,y=100)
        win.update()
        
        time.sleep(0.1)
        dct = kdcm3.toolbox()
        self.update = dct.update()

        time.sleep(0.1)
        win.destroy()

    def mainfunc(self):
        win = tkinter.Tk()
        win.title('KOS 2023 - DCL3')
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
        listbox.insert( listbox.size(),'encrypt' )
        win.update()
        time.sleep(0.03)
        listbox.insert( listbox.size(),'decrypt' )
        win.update()
        time.sleep(0.03)
        listbox.insert( listbox.size(),'upload' )
        win.update()
        time.sleep(0.03)
        listbox.insert( listbox.size(),'download' )
        win.update()
        time.sleep(0.03)
        listbox.insert( listbox.size(),'update(main)' )
        win.update()
        time.sleep(0.03)
        listbox.insert( listbox.size(),'update(sub)' )
        win.update()
        time.sleep(0.03)
        listbox.insert( listbox.size(),'update(bck)' )
        win.update()
        time.sleep(0.03)
        listbox.insert( listbox.size(),'upload test' )
        win.update()
        time.sleep(0.03)
        listbox.insert( listbox.size(),'erase' )
        win.update()
        time.sleep(0.05)

        if self.update != ['N','N','N']:
            try:
                with open('version.txt','r',encoding='utf-8') as f:
                    ver = f.read()
            except:
                ver = '자동 버전 식별에 실패함'
            time.sleep(0.2)
            tkinter.messagebox.showinfo('드라이버 업데이트',f' 드라이버가 자동 업데이트 되었습니다. \n 결과 : {self.update} \n 버전 : {ver} ')
            self.update = ['N','N','N']

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
                global setdata
                if last == 0:
                    k = conv()
                    k.en(setdata)
                elif last == 1:
                    k = conv()
                    k.de(setdata)
                elif last == 2:
                    k = web()
                    k.upload(setdata)
                elif last == 3:
                    k = web()
                    k.download(setdata)
                elif last == 4:
                    k = index()
                    k.get(setdata,'main')
                elif last == 5:
                    k = index()
                    k.get(setdata,'sub')
                elif last == 6:
                    k = index()
                    k.get(setdata,'bck')
                elif last == 7:
                    k = test()
                    k.do(setdata)
                elif last == 8:
                    k = addon()
                    k.erase(setdata)
            else:
                last = temp
                if last == 0:
                    msg = '프로필에 따라\n파일/폴더를 암호화하고\n사진으로 저장합니다.'
                elif last == 1:
                    msg = '프로필에 따라\n암호화된 사진을\n파일/폴더로 변환합니다.'
                elif last == 2:
                    msg = '설정된 저장소에\n사진을 자동으로\n게시합니다.'
                elif last == 3:
                    msg = '설정된 저장소의\n사진을 자동으로\n다운로드합니다.'
                elif last == 4:
                    msg = 'main 저장소에\n게시된 사진을\n인덱싱합니다.\n<주요 저장소>'
                elif last == 5:
                    msg = 'sub 저장소에\n게시된 사진을\n인덱싱합니다.\n<보조 저장소>'
                elif last == 6:
                    msg = 'bck 저장소에\n게시된 사진을\n인덱싱합니다.\n<백업 저장소>'
                elif last == 7:
                    msg = '설정된 저장소에\n글 올리기 테스트를\n자동으로 진행합니다.'
                elif last == 8:
                    msg = '중간 파일을 자동으로\n감지하고 삭제를\n진행 할 수 있습니다.'
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

class conv:

    def en(self,setdata):
        win = tkinter.Tk()
        win.title('KOS 2023 - DCL3')
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

        label2 = tkinter.Label(win, text = '프로필 : ', font = ('Consolas',14) )
        label2.place(x=10, y=200)
        profile = tkinter.StringVar()
        profile.set('-') #프로필
        label3 = tkinter.Label(win, textvariable = profile, font = ('Consolas',14) )
        label3.place(x=100, y=200)

        keys = [ ]
        for i in range( 0,len(setdata.profile) ):
            keys.append( str(i) + ') ' + setdata.profile[i][0] )
        combo4 = tkinter.ttk.Combobox(win, width=13, font = ("Consolas",15), values = keys)
        combo4.set( keys[0] ) #프로필 선택
        combo4.place(x=250,y=200)

        def f2():
            time.sleep(0.1)
            nonlocal win
            nonlocal profile
            nonlocal ptitle
            nonlocal ppw
            nonlocal pkf
            nonlocal combo4
            nonlocal setdata
            temp = int( combo4.get()[0] )
            ptitle = setdata.profile[temp][0]
            ppw = setdata.profile[temp][1]
            pkf = setdata.profile[temp][2]
            profile.set(ptitle)
            win.update()
            nonlocal select
            select = True
        but5 = tkinter.Button(win, text = 'set', font = ("Consolas",14), command = f2)
        but5.place(x=430,y=195) #선택 버튼
        ptitle = '' #프로필 이름
        ppw = '' #비밀번호
        pkf = '' #키파일 경로
        select = False #set 버튼 클릭 여부 

        mode6 = True # 위장 여부 T위장 F일반
        txt6 = tkinter.StringVar()
        txt6.set('위장 : O')
        def f6():
            time.sleep(0.1)
            nonlocal win
            nonlocal mode6
            nonlocal txt6
            if mode6:
                mode6 = False
                txt6.set('위장 : X')
            else:
                mode6 = True
                txt6.set('위장 : O')
            win.update()
        but6 = tkinter.Button(win, textvariable = txt6, font = ('Consolas',14), command = f6)
        but6.place(x = 10,y = 250) # 위장 여부

        def func():
            time.sleep(0.1)
            nonlocal win
            nonlocal setdata
            nonlocal mode1 # 파일/폴더 모드 'file' 'folder'
            nonlocal mode6 # 위장 여부 T위장 F일반
            nonlocal ptitle #프로필 이름
            nonlocal ppw #비밀번호
            nonlocal pkf #키 파일
            nonlocal path0 # 파일/폴더 목록

            otool = oreo.toolbox()
            mtool = mung2.toolbox()
            ntool = nox2.toolbox()
            ktool = kerbal.toolbox()
            # setdata.core setdata.chunk setdata.path
            kf = ktool.getkeyfile( pkf ) # ketfile bytes

            nonlocal select
            if select:
                
                if path0 != [ ]:
                    spec = ' 키 파일 크기 : ' + str( len(kf) ) + ' 바이트 \n 비밀번호 길이 : ' + str( len(ppw) ) + ' 글자 \n 다음과 같이 변환을 진행합니다. '
                    ask = tkinter.messagebox.askokcancel('변환 요소 확인',spec)
                    if ask:
                        try:
                            shutil.rmtree('temp366')
                        except:
                            pass
                        try:
                            shutil.rmtree('temp270')
                        except:
                            pass
                        os.mkdir('temp366')
                        temp = [ ]
                        for i in path0:
                            temp.append( i.replace('/','\\') )
                        if mode1 == 'file':
                            mtool.pack(temp,'temp366\\step0.dat','False')
                        else:
                            mtool.pack(temp[0],'temp366\\step0.dat','False') # user data -> kzip 변환

                        try:
                            shutil.rmtree('temp271')
                        except:
                            pass
                        try:
                            nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) ) #시간 구조
                            with open('temp400.txt','w',encoding='utf-8') as f:
                                f.write('kaes\n' + str(setdata.core) + '\n' + nowtime + '\n' + 'Encrypting User Data\n')
                            os.startfile('test400\\test400.exe')
                            time.sleep(0.3)
                        except:
                            pass
                        ktool.encryptall( os.path.abspath('temp366\\step0.dat').replace('/','\\'), ppw, '변환 프로필 : ' + ptitle, bytes(nowtime,encoding='utf-8'), 3, setdata.core, setdata.chunk, kf)
                        time.sleep(0.5) # kzip -> kaes

                        mtool.pack('temp366\\step0.dat.k','temp366\\step2.dat','False') # kaes -> kzip
                        time.sleep(0.2)

                        ntool.set(setdata.core,setdata.path)
                        try:
                            nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) ) #시간 구조
                            with open('temp400.txt','w',encoding='utf-8') as f:
                                f.write('kpng\n' + str(setdata.core) + '\n' + nowtime + '\n' + 'KPNG Encoding...\n')
                            os.startfile('test400\\test400.exe')
                            time.sleep(0.3)
                        except:
                            pass
                        temp = ntool.pack('temp366\\step2.dat',not(mode6),'png') # kzip -> kpng
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
                            shutil.rmtree('temp366')
                        except:
                            pass
                        tkinter.messagebox.showinfo('변환 완료',' DCloud3 파일 패킹 완료 \n 바탕화면 ' + out + ' 생성되었습니다.\n 일련번호 : ' + name + ' 사진개수 : ' + str(num) + ' ')
                
                else:
                    tkinter.messagebox.showinfo('빈 리스트 경고',' 대상 파일/폴더가 없습니다. \n 변환할 파일/폴더를 선택하십시오. ')

            else:
                tkinter.messagebox.showinfo('프로필 선택 경고',' 선택된 프로필이 없습니다. \n 변환 프로필을 선택하십시오. \n settings.txt에 저장된 프로필 항목을 참고하십시오. ')

            win.update()
            
        go = tkinter.Button(win, text = '< 변환 >', font = ('Consolas',14), command = func)
        go.place(x = 120,y = 250) # 변환 진행

        win.mainloop()

    def de(self,setdata):
        win = tkinter.Tk()
        win.title('KOS 2023 - DCL3')
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
                temp = filedialog.askopenfiles( title='파일들 선택', filetypes=( ('all files', '*.*'),('png files', '*.png') ) )
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

        label2 = tkinter.Label(win, text = '프로필 : ', font = ('Consolas',14) )
        label2.place(x=10, y=200)
        profile = tkinter.StringVar()
        profile.set('-') #프로필
        label3 = tkinter.Label(win, textvariable = profile, font = ('Consolas',14) )
        label3.place(x=100, y=200)

        keys = [ ]
        for i in range( 0,len(setdata.profile) ):
            keys.append( str(i) + ') ' + setdata.profile[i][0] )
        combo4 = tkinter.ttk.Combobox(win, width=13, font = ("Consolas",15), values = keys)
        combo4.set( keys[0] ) #프로필 선택
        combo4.place(x=250,y=200)

        def f2():
            time.sleep(0.1)
            nonlocal win
            nonlocal profile
            nonlocal ptitle
            nonlocal ppw
            nonlocal pkf
            nonlocal combo4
            nonlocal setdata
            temp = int( combo4.get()[0] )
            ptitle = setdata.profile[temp][0]
            ppw = setdata.profile[temp][1]
            pkf = setdata.profile[temp][2]
            profile.set(ptitle)
            win.update()
            nonlocal select
            select = True
        but5 = tkinter.Button(win, text = 'set', font = ("Consolas",14), command = f2)
        but5.place(x=430,y=195) #선택 버튼
        ptitle = '' #프로필 이름
        ppw = '' #비밀번호
        pkf = '' #키파일 경로
        select = False #set 버튼 클릭 여부

        def f6():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal path0
            listbox.delete( 0,listbox.size() )
            for i in path0:
                listbox.insert( listbox.size(), i )
                win.update()
                listbox.see( listbox.size() )
                time.sleep(0.05)
            win.update()
        but6 = tkinter.Button(win, text = '선택 목록 보기', font = ('Consolas',14), command = f6)
        but6.place(x = 10,y = 250) # 선택 목록 보기

        def func():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal setdata
            nonlocal mode1 # 파일/폴더 모드 'file' 'folder'
            nonlocal ptitle #프로필 이름
            nonlocal ppw #비밀번호
            nonlocal pkf #키 파일
            nonlocal path0 # 파일/폴더 목록
            otool = oreo.toolbox()
            mtool = mung2.toolbox()
            ntool = nox2.toolbox()
            ktool = kerbal.toolbox()
            # setdata.core setdata.chunk setdata.path
            kf = ktool.getkeyfile( pkf ) # ketfile bytes

            # 경고 / 사진 풀기
            try:
                shutil.rmtree('temp366')
            except:
                pass
            os.mkdir('temp366')
            nonlocal select
            if select:
                if path0 != [ ]:
                    spec = ' 키 파일 크기 : ' + str( len(kf) ) + ' 바이트 \n 비밀번호 길이 : ' + str( len(ppw) ) + ' 글자 \n 다음과 같이 변환을 진행합니다. '
                    ask = tkinter.messagebox.askokcancel('변환 요소 확인',spec)
                    if ask:

                        if mode1 == 'file':
                            for i in path0:
                                j = i.replace('/','\\')
                                shutil.copyfile(i, 'temp366\\' + j[j.rfind('\\')+1:] )
                            temp = 'temp366'
                        else:
                            temp = path0[0]
                        path = temp # raw file 폴더위치
                        temp = ntool.detect(temp) # ntool 감지

                        listbox.delete( 0,listbox.size() )
                        listbox.insert( listbox.size(),'개수 : ' + str(temp[0]) + ' 일련번호 : ' + temp[1] + ' 형식 : ' + temp[2] )
                        win.update()
                        time.sleep(0.3)

                        if temp[0] != 0: # 사진 존재
                            listbox.insert( listbox.size(), '. . .' )
                            win.update() # 상태 표시
                            num = temp[0] # pic num
                            name = temp[1] # pic name
                            tp = temp[2] # pic type

                            # png -> kzip -> kaes 변환 시작
                            try:
                                shutil.rmtree('temp270')
                            except:
                                pass
                            try:
                                nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) ) #시간 구조
                                with open('temp400.txt','w',encoding='utf-8') as f:
                                    f.write('kpng\n' + str(setdata.core) + '\n' + nowtime + '\n' + 'KPNG Decoding...\n')
                                os.startfile('test400\\test400.exe')
                                time.sleep(0.3)
                            except:
                                pass
                            ntool.set(setdata.core,'') # ntool png convert start
                            temp = ntool.unpack([path,num,name,tp])
                            time.sleep(0.5)
                            mtool.unpack('temp270\\result.dat')
                            shutil.rmtree('temp270')
                            time.sleep(0.2)
                            temp = ktool.checkall('temp261\\step0.dat.k') #temp261\\step0.dat.k
                            if temp[0] == 'V':
                                listbox.insert( listbox.size(),'Ready To Unpack Dcl3 File' )
                                listbox.insert( listbox.size(),'===== HINT =====' )
                                hint6 = temp[1][6].split('\n')
                                for i in hint6:
                                    listbox.insert( listbox.size(),i )
                            else:
                                listbox.insert( listbox.size(),'Not Valid KAES-3 File' )
                            try:
                                shutil.rmtree('temp365')
                            except:
                                pass
                            win.update()
                            time.sleep(0.3)

                            # kaes -> kzip -> user file
                            if temp[0] == 'V':
                                listbox.insert( listbox.size(), '. . .' )
                                win.update() # 상태 표시

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
                                temp = ktool.pwall(ppw, kf, salt, pwhash, [ckeydt, tkeydt, title]) # pw check

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
                                        shutil.rmtree('temp366')
                                    except:
                                        pass
                                    os.mkdir('temp366')

                                    # kzip -> user file
                                    mtool = mung2.toolbox()
                                    shutil.move('temp261\\step0.dat','temp366\\step0.dat')
                                    mtool.unpack( os.path.abspath('temp366\\step0.dat') ) #temp261

                                    listbox.insert( listbox.size(), '변환 완료' )
                                    win.update() # 상태 표시
                                    shutil.rmtree('temp366')
                                    out = os.path.join(os.path.expanduser('~'),'Desktop') + '\\' + str( random.randrange(100000,1000000) ) # 바탕화면 폴더
                                    shutil.move('temp261',out)
                                    tkinter.messagebox.showinfo('변환 완료',' Dcloud 3 파일 언패킹 완료 \n 바탕화면 ' + out + ' 생성되었습니다. ')

                                else:
                                    tkinter.messagebox.showinfo('잘못된 프로필',' 프로필 데이터가 일치하지 않습니다. \n settings.txt에 저장된 프로필 항목을 참고하십시오. ')
                                    listbox.insert( listbox.size(), '변환 실패' )
                                    win.update() # 상태 표시
                                
                            else:
                                tkinter.messagebox.showinfo('풀기 오류 경고',' 잘못된 암호화 파일입니다. \n 파일 생성 단계에서의 오류일 수 있습니다. ')
                                listbox.insert( listbox.size(), '변환 실패' )
                                win.update() # 상태 표시

                        else:
                            tkinter.messagebox.showinfo('대상 없음 경고',' 파일/폴더가 감지되지 않았습니다. \n 변환할 파일/폴더를 선택하십시오. ')

                else:
                    tkinter.messagebox.showinfo('빈 리스트 경고',' 대상 파일/폴더가 없습니다. \n 변환할 파일/폴더를 선택하십시오. ')

            else:
                tkinter.messagebox.showinfo('프로필 선택 경고',' 선택된 프로필이 없습니다. \n 변환 프로필을 선택하십시오. \n settings.txt에 저장된 프로필 항목을 참고하십시오. ')

            win.update()
            try:
                shutil.rmtree('temp261')
            except:
                pass
            try:
                shutil.rmtree('temp271')
            except:
                pass
            try:
                shutil.rmtree('temp366')
            except:
                pass
            
        go = tkinter.Button(win, text = '< 변환 >', font = ('Consolas',14), command = func)
        go.place(x = 170,y = 250) # 변환 진행

        win.mainloop()

class web:

    def upload(self,setdata):
        win = tkinter.Tk()
        win.title('KOS 2023 - DCL3')
        win.geometry("500x400+200+100")
        win.resizable(False, False)

        frame = tkinter.Frame(win)
        frame.place(x=10,y=10)
        listbox = tkinter.Listbox( frame, width=45,  height=7, font = ('Consolas',14) )
        listbox.pack(side="left", fill="y")
        scrollbar0 = tkinter.Scrollbar(frame, orient="vertical")
        scrollbar0.config(command=listbox.yview)
        scrollbar0.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar0.set)

        path0 = [ ] # 파일 목록
        def f0():
            time.sleep(0.1)
            nonlocal win
            nonlocal listbox
            nonlocal path0
            path0 = [ ]
            listbox.delete( 0,listbox.size() )
            temp = filedialog.askopenfiles( title='파일들 선택', filetypes=( ('png files', '*.png'), ('jpg files', '*.jpg'), ('webp files', '*.webp'), ('all files', '*.*') ) )
            for i in temp:
                path0.append(i.name)
            for i in path0:
                listbox.insert( listbox.size(),i )
            nonlocal txt2
            nonlocal txt4
            txt2.set('파일 개수 : ' + str( len(path0) ) )
            temp = 0
            for i in path0:
                temp = temp + os.path.getsize(i)
            txt4.set('파일 크기 : ' + str(temp) )
            win.update()
        but0 = tkinter.Button(win, text = '...', font = ('Consolas',14), command = f0)
        but0.place(x = 10,y = 180) # 파일 추가

        txt2 = tkinter.StringVar()
        txt2.set('파일 개수 : ' + '0') # 파일 개수
        label1 = tkinter.Label(win, textvariable = txt2, font = ('Consolas',14) )
        label1.place(x=60, y=185)
        txt4 = tkinter.StringVar()
        txt4.set('파일 크기 : ' + '0') # 파일 크기
        label3 = tkinter.Label(win, textvariable = txt4, font = ('Consolas',14) )
        label3.place(x=230, y=185)

        keys = [ ]
        for i in range( 0,len(setdata.profile) ):
            keys.append( str(i) + ') ' + setdata.profile[i][0] )
        combo5 = tkinter.ttk.Combobox(win, width=13, font = ("Consolas",15), values = keys)
        combo5.set( keys[0] ) #프로필 선택
        combo5.place(x=250,y=230)
        profile = tkinter.StringVar()
        profile.set('프로필 : -') #프로필
        label8 = tkinter.Label(win, textvariable = profile, font = ('Consolas',14) )
        label8.place(x=10, y=230)
        def f6():
            time.sleep(0.1)
            nonlocal win
            nonlocal profile
            nonlocal ptitle
            nonlocal combo5
            nonlocal setdata
            temp = int( combo5.get()[0] )
            ptitle = setdata.profile[temp][0]
            profile.set('프로필 : ' + ptitle)
            win.update()
            nonlocal select
            select = True
        but7 = tkinter.Button(win, text = 'set', font = ("Consolas",14), command = f6)
        but7.place(x=430,y=225) #선택 버튼
        ptitle = '' # 프로필 이름
        select = False #set 버튼 클릭 여부

        label9 = tkinter.Label(win, text = 'msg : ', font = ('Consolas',14) )
        label9.place(x=10, y=270)
        entry10 = tkinter.Entry(win, width = 40, font = ('Consolas',14) )
        entry10.place(x=70, y=275) # msg input

        mode11 = False # main upload T go F stop
        txt12 = tkinter.StringVar()
        txt12.set('main : X')
        def f7():
            time.sleep(0.1)
            nonlocal win
            nonlocal mode11
            nonlocal txt12
            if mode11:
                mode11 = False
                txt12.set('main : X')
            else:
                mode11 = True
                txt12.set('main : O')
            win.update()
        but13 = tkinter.Button(win, textvariable = txt12, font = ('Consolas',14), command = f7)
        but13.place(x = 10,y = 310)
        mode14 = False # sub upload T go F stop
        txt15 = tkinter.StringVar()
        txt15.set('sub : X')
        def f8():
            time.sleep(0.1)
            nonlocal win
            nonlocal mode14
            nonlocal txt15
            if mode14:
                mode14 = False
                txt15.set('sub : X')
            else:
                mode14 = True
                txt15.set('sub : O')
            win.update()
        but16 = tkinter.Button(win, textvariable = txt15, font = ('Consolas',14), command = f8)
        but16.place(x = 115,y = 310)
        mode17 = False # bck upload T go F stop
        txt18 = tkinter.StringVar()
        txt18.set('bck : X')
        def f9():
            time.sleep(0.1)
            nonlocal win
            nonlocal mode17
            nonlocal txt18
            if mode17:
                mode17 = False
                txt18.set('bck : X')
            else:
                mode17 = True
                txt18.set('bck : O')
            win.update()
        but19 = tkinter.Button(win, textvariable = txt18, font = ('Consolas',14), command = f9)
        but19.place(x = 210,y = 310)

        def func():
            time.sleep(0.1)
            nonlocal win
            nonlocal path0
            nonlocal ptitle
            nonlocal entry10 # msg input
            nonlocal select # set 버튼 클릭 여부
            nonlocal mode11 # main upload T go F stop
            nonlocal mode14 # sub upload T go F stop
            nonlocal mode17 # bck upload T go F stop
            nonlocal num20 # max 300
            nonlocal num22 # 대기 분
            nonlocal setdata
            num20.set(0)

            if select:
                
                if path0 != [ ]:
                    
                    if mode11 or mode14 or mode17:

                        try:
                            shutil.rmtree('temp366')
                        except:
                            pass
                        os.mkdir('temp366')
                        upnum = 0 # 쓸 글 수
                        tempsize = 0
                        os.mkdir('temp366\\0')
                        for i in path0:
                            if tempsize + os.path.getsize(i) > setdata.limit:
                                upnum = upnum + 1
                                os.mkdir( 'temp366\\' + str(upnum) )
                                tempsize = 0
                            j = i.replace('/','\\')
                            shutil.copyfile( i, 'temp366\\' + str(upnum) + '\\' + j[j.rfind('\\')+1:] )
                            tempsize = tempsize + os.path.getsize(i)

                        multi = 0 # 배수 결정
                        for i in [mode11, mode14, mode17]:
                            if i:
                                multi = multi + 1
                        multi = 3 / multi
                        temp = int( (upnum + 1) * (3 / multi) )
                        spec = f' 프로필 : {ptitle} 사진개수 : {len(path0)} 대기 : {num22} 분\n main : {mode11} sub : {mode14} bck : {mode17} \n'
                        spec = spec + f' 업로드 글 개수 : {temp} 예상시간 : {3*temp} 분 \n 다음과 같이 업로드를 진행합니다. '
                        ask = tkinter.messagebox.askokcancel('업로드 요소 확인',spec)
                        if ask:
                            temp = time.time()
                            while time.time() - temp < num22 * 60:
                                time.sleep(0.1)

                            var0m = 0 # 성공 수m
                            var1m = 0 # 시간초과 실패 수m
                            var2m = 0 # true 에러 실패 수m
                            var3m = 0 # 단순 업로드 실패 수m
                            var4m = 0 # 기타 실패 수m
                            if mode11:
                                gall = setdata.main
                                dtool = kdcm3.toolbox()
                                con = dtool.getconfig()
                                dtool.set(gall[0], gall[1], con)
                                rdata = str( hex( random.randrange(0,256) ) ) + '0'
                                rdata = rdata[2:4] # 2 글자 랜덤데이터
                                ktool = kerbal.basic()
                                for i in range(0,upnum + 1):
                                    uplist = list( os.path.abspath('temp366\\' + str(i) + '\\' + j) for j in os.listdir( 'temp366\\' + str(i) ) )
                                    title = f'{rdata} [DCL3] [{ptitle}] [{i}] [{upnum+1}] {str(random.randrange(1000,9000))}'
                                    body = f'{rdata} [{i}] [' + ktool.b64en( bytes( entry10.get(), 'utf-8') ) + f'] {str(random.randrange(1000,9000))}'
                                    try:
                                        dtool.write(gall[2], gall[3], title, body, uplist, True, True)
                                        try:
                                            new = dtool.getnum( gall[0] ) # 최신 글 번호
                                            response = dtool.gettxt( gall[4] + str(new) ) # [title, body]
                                            if ( f'[{i}] [{upnum+1}]' in response[0] ) and ( rdata in response[1] ):
                                                pass
                                            else:
                                                raise Exception('non detectable error')
                                        except:
                                            raise Exception('non detectable error')
                                        var0m = var0m + 1
                                    except:
                                        time.sleep(5)
                                        try:
                                            dtool.write(gall[2], gall[3], title, body, uplist, True, True)
                                            try:
                                                new = dtool.getnum( gall[0] ) # 최신 글 번호
                                                response = dtool.gettxt( gall[4] + str(new) ) # [title, body]
                                                if ( f'[{i}] [{upnum+1}]' in response[0] ) and ( rdata in response[1] ):
                                                    pass
                                                else:
                                                    raise Exception('non detectable error')
                                            except:
                                                raise Exception('non detectable error')
                                            var0m = var0m + 1
                                        except Exception as e:
                                            e = str(e)
                                            if e == 'timeout':
                                                var1m = var1m + 1
                                            elif e == 'true':
                                                var2m = var2m + 1
                                            elif e == 'non detectable error':
                                                var3m = var3m + 1
                                            else:
                                                var4m = var4m + 1
                                    num20.set( num20.get() + int( (1) / (upnum + 1) * 100 * multi ) )
                                    win.update()
                                    time.sleep(0.1)

                            var0s = 0 # 성공 수s
                            var1s = 0 # 시간초과 실패 수s
                            var2s = 0 # true 에러 실패 수s
                            var3s = 0 # 단순 업로드 실패 수s
                            var4s = 0 # 기타 실패 수s
                            if mode14:
                                gall = setdata.sub
                                dtool = kdcm3.toolbox()
                                con = dtool.getconfig()
                                dtool.set(gall[0], gall[1], con)
                                rdata = str( hex( random.randrange(0,256) ) ) + '0'
                                rdata = rdata[2:4] # 2 글자 랜덤데이터
                                ktool = kerbal.basic()
                                for i in range(0,upnum + 1):
                                    uplist = list( os.path.abspath('temp366\\' + str(i) + '\\' + j) for j in os.listdir( 'temp366\\' + str(i) ) )
                                    title = f'{rdata} [DCL3] [{ptitle}] [{i}] [{upnum+1}] {str(random.randrange(1000,9000))}'
                                    body = f'{rdata} [{i}] [' + ktool.b64en( bytes( entry10.get(), 'utf-8') ) + f'] {str(random.randrange(1000,9000))}'
                                    try:
                                        dtool.write(gall[2], gall[3], title, body, uplist, True, True)
                                        try:
                                            new = dtool.getnum( gall[0] ) # 최신 글 번호
                                            response = dtool.gettxt( gall[4] + str(new) ) # [title, body]
                                            if ( f'[{i}] [{upnum+1}]' in response[0] ) and ( rdata in response[1] ):
                                                pass
                                            else:
                                                raise Exception('non detectable error')
                                        except:
                                            raise Exception('non detectable error')
                                        var0s = var0s + 1
                                    except:
                                        time.sleep(5)
                                        try:
                                            dtool.write(gall[2], gall[3], title, body, uplist, True, True)
                                            try:
                                                new = dtool.getnum( gall[0] ) # 최신 글 번호
                                                response = dtool.gettxt( gall[4] + str(new) ) # [title, body]
                                                if ( f'[{i}] [{upnum+1}]' in response[0] ) and ( rdata in response[1] ):
                                                    pass
                                                else:
                                                    raise Exception('non detectable error')
                                            except:
                                                raise Exception('non detectable error')
                                            var0s = var0s + 1
                                        except Exception as e:
                                            e = str(e)
                                            if e == 'timeout':
                                                var1s = var1s + 1
                                            elif e == 'true':
                                                var2s = var2s + 1
                                            elif e == 'non detectable error':
                                                var3s = var3s + 1
                                            else:
                                                var4s = var4s + 1
                                    num20.set( num20.get() + int( (1) / (upnum + 1) * 100 * multi ) )
                                    win.update()
                                    time.sleep(0.1)

                            var0b = 0 # 성공 수b
                            var1b = 0 # 시간초과 실패 수b
                            var2b = 0 # true 에러 실패 수b
                            var3b = 0 # 단순 업로드 실패 수b
                            var4b = 0 # 기타 실패 수b
                            if mode17:
                                gall = setdata.bck
                                dtool = kdcm3.toolbox()
                                con = dtool.getconfig()
                                dtool.set(gall[0], gall[1], con)
                                rdata = str( hex( random.randrange(0,256) ) ) + '0'
                                rdata = rdata[2:4] # 2 글자 랜덤데이터
                                ktool = kerbal.basic()
                                for i in range(0,upnum + 1):
                                    uplist = list( os.path.abspath('temp366\\' + str(i) + '\\' + j) for j in os.listdir( 'temp366\\' + str(i) ) )
                                    title = f'{rdata} [DCL3] [{ptitle}] [{i}] [{upnum+1}] {str(random.randrange(1000,9000))}'
                                    body = f'{rdata} [{i}] [' + ktool.b64en( bytes( entry10.get(), 'utf-8') ) + f'] {str(random.randrange(1000,9000))}'
                                    try:
                                        dtool.write(gall[2], gall[3], title, body, uplist, True, True)
                                        try:
                                            new = dtool.getnum( gall[0] ) # 최신 글 번호
                                            response = dtool.gettxt( gall[4] + str(new) ) # [title, body]
                                            if ( f'[{i}] [{upnum+1}]' in response[0] ) and ( rdata in response[1] ):
                                                pass
                                            else:
                                                raise Exception('non detectable error')
                                        except:
                                            raise Exception('non detectable error')
                                        var0b = var0b + 1
                                    except:
                                        time.sleep(5)
                                        try:
                                            dtool.write(gall[2], gall[3], title, body, uplist, True, True)
                                            try:
                                                new = dtool.getnum( gall[0] ) # 최신 글 번호
                                                response = dtool.gettxt( gall[4] + str(new) ) # [title, body]
                                                if ( f'[{i}] [{upnum+1}]' in response[0] ) and ( rdata in response[1] ):
                                                    pass
                                                else:
                                                    raise Exception('non detectable error')
                                            except:
                                                raise Exception('non detectable error')
                                            var0b = var0b + 1
                                        except Exception as e:
                                            e = str(e)
                                            if e == 'timeout':
                                                var1b = var1b + 1
                                            elif e == 'true':
                                                var2b = var2b + 1
                                            elif e == 'non detectable error':
                                                var3b = var3b + 1
                                            else:
                                                var4b = var4b + 1
                                    num20.set( num20.get() + int( (1) / (upnum + 1) * 100 * multi ) )
                                    win.update()
                                    time.sleep(0.1)
                            
                            num20.set(300)
                            spec = f' 업로드가 완료되었습니다. \n main 성공({var0m}) 시간초과({var1m}) 서버이상({var2m}) 업로드불가({var3m}) 기타에러({var4m}) \n '
                            spec = spec + f'sub 성공({var0s}) 시간초과({var1s}) 서버이상({var2s}) 업로드불가({var3s}) 기타에러({var4s}) \n '
                            spec = spec + f'bck 성공({var0b}) 시간초과({var1b}) 서버이상({var2b}) 업로드불가({var3b}) 기타에러({var4b}) '
                            tkinter.messagebox.showinfo('업로드 완료',spec)

                        try:
                            shutil.rmtree('temp366')
                        except:
                            pass

                    else:
                        tkinter.messagebox.showinfo('대상 없음 경고',' 업로드할 저장소가 없습니다. \n 적어도 1개의 저장소를 업로드 대상으로 선택하십시오. ')

                else:
                    tkinter.messagebox.showinfo('빈 리스트 경고',' 대상 파일/폴더가 없습니다. \n 변환할 파일/폴더를 선택하십시오. ')
                
            else:
                tkinter.messagebox.showinfo('프로필 선택 경고',' 선택된 프로필이 없습니다. \n 변환 프로필을 선택하십시오. \n settings.txt에 저장된 프로필 항목을 참고하십시오. ')

            win.update()
            
        go = tkinter.Button(win, text = 'upload', font = ('Consolas',14), command = func)
        go.place(x = 400,y = 310) # upload

        num22 = 0 # 대기 분
        def f23():
            nonlocal win
            nonlocal num22
            nonlocal txt25
            time.sleep(0.1)
            data = [0,10,20,30,60,120,180,300,600]
            num22 = data[ (data.index(num22) + 1) % 9 ]
            txt25.set(f'slp{num22:>4}')
            win.update()
        txt25 = tkinter.StringVar()
        txt25.set('slp   0')
        but24 = tkinter.Button(win, textvariable = txt25, font = ('Consolas',14), command = f23)
        but24.place(x = 305,y = 310)

        num20 = tkinter.DoubleVar() # 진행바 변수 max 300
        bar21 = tkinter.ttk.Progressbar(win, maximum=300, variable = num20, length=450)
        bar21.place(x = 25,y = 360)
        win.update()

    def download(self,setdata):
        try:
            shutil.rmtree('temp366')
        except:
            pass

        win = tkinter.Tk()
        win.title('KOS 2023 - DCL3')
        win.geometry("500x400+200+100")
        win.resizable(False, False)

        frame = tkinter.Frame(win)
        frame.place(x=10,y=10)
        listbox = tkinter.Listbox( frame, width=45,  height=12, font = ('Consolas',14) )
        listbox.pack(side="left", fill="y")
        scrollbar0 = tkinter.Scrollbar(frame, orient="vertical")
        scrollbar0.config(command=listbox.yview)
        scrollbar0.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar0.set)

        list0 = [ ] # 표시될 리스트

        var1 = True # main 선택 여부
        def f1():
            time.sleep(0.1)
            nonlocal win
            nonlocal var1
            nonlocal but1
            var1 = not(var1)
            if var1:
                but1.configure(bg = 'lawn green')
            else:
                but1.configure(bg = 'gray95')
            win.update()
        but1 = tkinter.Button(win, text = 'main', font = ('Consolas',14), command = f1, bg = 'lawn green')
        but1.place(x = 10,y = 295) # main 선택

        var2 = True # sub 선택 여부
        def f2():
            time.sleep(0.1)
            nonlocal win
            nonlocal var2
            nonlocal but2
            var2 = not(var2)
            if var2:
                but2.configure(bg = 'lawn green')
            else:
                but2.configure(bg = 'gray95')
            win.update()
        but2 = tkinter.Button(win, text = ' sub', font = ('Consolas',14), command = f2, bg = 'lawn green')
        but2.place(x = 70,y = 295) # sub 선택

        var3 = True # bck 선택 여부
        def f3():
            time.sleep(0.1)
            nonlocal win
            nonlocal var3
            nonlocal but3
            var3 = not(var3)
            if var3:
                but3.configure(bg = 'lawn green')
            else:
                but3.configure(bg = 'gray95')
            win.update()
        but3 = tkinter.Button(win, text = ' bck', font = ('Consolas',14), command = f3, bg = 'lawn green')
        but3.place(x = 130,y = 295) # bck 선택

        mode = 'all' # all number profile message
        show = tkinter.StringVar()
        show.set('mode : ' + '    ' + mode)
        def f4():
            time.sleep(0.1)
            nonlocal win
            nonlocal mode
            nonlocal show
            temp = ['all','number','profile','message']
            mode = temp[(temp.index(mode) + 1) % 4]
            show.set('mode : ' + f'{mode:>7}')
            win.update()
        but4 = tkinter.Button(win, textvariable = show, font = ('Consolas',14), command = f4)
        but4.place(x = 190,y = 295) # view mode 선택

        keys = [ ]
        for i in range( 0,len(setdata.profile) ):
            keys.append( str(i) + ') ' + setdata.profile[i][0] )
        combo5 = tkinter.ttk.Combobox(win, width=15, font = ("Consolas",14), values = keys)
        combo5.set( keys[0] ) # 프로필 선택
        combo5.place(x=10,y=340)

        entry6 = tkinter.Entry(win, width = 15, font = ('Consolas',14) )
        entry6.place(x=190, y=340) # keyword input

        def f7():
            time.sleep(0.1)
            nonlocal win
            nonlocal mode # all number profile message
            nonlocal list0 # 표시될 리스트
            nonlocal var1 # main 선택 여부
            nonlocal var2 # sub 선택 여부
            nonlocal var3 # bck 선택 여부
            nonlocal combo5 # 프로필 선택
            nonlocal entry6 # keyword input
            nonlocal status # 현재 상태
            nonlocal datamain # main [ num, profile, msg, [urls] ]
            nonlocal datasub # sub [ num, profile, msg, [urls] ]
            nonlocal databck # bck [ num, profile, msg, [urls] ]
            nonlocal showmain # varify-id msg (num,profile)
            nonlocal showsub # varify-id msg (num,profile)
            nonlocal showbck # varify-id msg (num,profile)
            status.set('진행 : 키워드 탐색 진행 중')
            win.update()
            if mode == 'number':
                num = int( entry6.get() )
                list0 = [ ]
                if var1 and len(showmain) > num:
                    list0.append( showmain[num] )
                if var2 and len(showsub) > num:
                    list0.append( showsub[num] )
                if var3 and len(showbck) > num:
                    list0.append( showbck[num] )
            elif mode == 'profile':
                if entry6.get() == '':
                    nonlocal setdata
                    profile = setdata.profile[ int( combo5.get()[0] ) ][0]
                else:
                    profile = entry6.get()
                list0 = [ ]
                if var1:
                    for i in range( 0,len(showmain) ):
                        if profile == datamain[i][1]:
                            list0.append(showmain[i])
                if var2:
                    for i in range( 0,len(showsub) ):
                        if profile == datasub[i][1]:
                            list0.append(showsub[i])
                if var3:
                    for i in range( 0,len(showbck) ):
                        if profile == databck[i][1]:
                            list0.append(showbck[i])
            elif mode == 'message':
                temp = entry6.get()
                keywords = [temp] + [x for x in temp.split() if len(x) > 1]
                list0 = [ ]
                if var1:
                    for i in range( 0,len(showmain) ):
                        msg = datamain[i][2]
                        for j in keywords:
                            if j in msg:
                                list0.append(showmain[i])
                                break
                if var2:
                    for i in range( 0,len(showsub) ):
                        msg = datasub[i][2]
                        for j in keywords:
                            if j in msg:
                                list0.append(showsub[i])
                                break
                if var3:
                    for i in range( 0,len(showbck) ):
                        msg = databck[i][2]
                        for j in keywords:
                            if j in msg:
                                list0.append(showbck[i])
                                break
            else:
                list0 = [ ]
                if var1:
                    list0 = list0 + showmain
                if var2:
                    list0 = list0 + showsub
                if var3:
                    list0 = list0 + showbck
            nonlocal listbox
            listbox.delete( 0,listbox.size() )
            for i in list0:
                listbox.insert( listbox.size(),i )
            status.set('완료 : 탐색 완료. 화면에 표시됨.')
            win.update()
        but7 = tkinter.Button(win, text = ' search ', font = ('Consolas',14), command = f7)
        but7.place(x = 400,y = 295) # search

        def f8():
            time.sleep(0.1)
            nonlocal win
            nonlocal status # 현재 상태
            nonlocal datamain # main [ num, profile, msg, [urls] ]
            nonlocal datasub # sub [ num, profile, msg, [urls] ]
            nonlocal databck # bck [ num, profile, msg, [urls] ]
            nonlocal listbox
            nonlocal list0
            temp = listbox.curselection()[0] # selected position
            temp = list0[temp]
            num = int( temp[1:temp.find(' ')] ) # 청크 번호
            mode = temp[0] # 'm', 's', 'b'
            if mode == 'm':
                mode = 'main'
                profile = datamain[num][1]
                urls = datamain[num][3]
            elif mode == 's':
                mode = 'sub'
                profile = datasub[num][1]
                urls = datasub[num][3]
            else:
                mode = 'bck'
                profile = databck[num][1]
                urls = databck[num][3]
            i = tkinter.messagebox.askokcancel('다운로드 준비 완료',f' 번호 : {mode}-{num} 프로필 : {profile} 개수 : {len(urls)} 개 \n 해당 청크를 다운로드 하시겠습니까? ')
            if i:
                os.mkdir('temp366')
                var0 = 0 # success
                var1 = 0 # fail
                ktool = kdcm3.toolbox()
                for i in range( 0,len(urls) ):
                    status.set(f'진행 : {i+1} / {len(urls)} 사진 파일 다운로드 중')
                    win.update()
                    try:
                        temp = ktool.getpic(urls[i])
                        for j in temp:
                            shutil.move(j, 'temp366/' + j[j.find('/')+1:])
                        var0 = var0 + 1
                    except:
                        var1 = var1 + 1
                    try:
                        shutil.rmtree('temp306a')
                    except:
                        pass
                status.set(f'완료 : 다운로드 성공 {var0} 개 실패 {var1} 개')
                win.update()
                out = os.path.join(os.path.expanduser('~'),'Desktop') + '\\' + str( random.randrange(100000,1000000) ) # 바탕화면 폴더
                try:
                    shutil.rmtree(out)
                except:
                    pass
                shutil.move('temp366',out)
                tkinter.messagebox.showinfo('다운로드 완료',' 청크 사진 다운로드 완료 \n 바탕화면 ' + out + ' 생성되었습니다. ')
            win.update()
        but8 = tkinter.Button(win, text = 'download', font = ('Consolas',14), command = f8)
        but8.place(x = 400,y = 340) # download

        status = tkinter.StringVar()
        status.set('진행 : KSD 인덱스 파일 로딩 중') # 현재 상태
        label9 = tkinter.Label(win, textvariable = status, font = ('Consolas', 14) )
        label9.place(x=10,y=370)

        if os.path.isfile('main.ksd') and os.path.isfile('sub.ksd') and os.path.isfile('bck.ksd'):
            otool = oreo.toolbox()
            stool = stream.stream()
            stool.read('main.ksd')
            temp = len(stool.data)
            datamain = [0] * temp # main [ num, profile, msg, [urls] ]
            for i in range(0,temp):
                data = otool.readstr( str( stool.get(i), encoding='utf-8' ) )
                num = data['data#num'] # 글개수
                profile = data['data#profile'] # 프로필
                msg = data['data#msg'] # 메세지
                urls = [0] * num # url str 리스트
                for j in range(0,num):
                    urls[j] = data['data#urls#' + str(j)]
                datamain[i] = [num, profile, msg, urls]
            stool = stream.stream()
            stool.read('sub.ksd')
            temp = len(stool.data)
            datasub = [0] * temp # sub [ num, profile, msg, [urls] ]
            for i in range(0,temp):
                data = otool.readstr( str( stool.get(i), encoding='utf-8' ) )
                num = data['data#num'] # 글개수
                profile = data['data#profile'] # 프로필
                msg = data['data#msg'] # 메세지
                urls = [0] * num # url str 리스트
                for j in range(0,num):
                    urls[j] = data['data#urls#' + str(j)]
                datasub[i] = [num, profile, msg, urls]
            stool = stream.stream()
            stool.read('bck.ksd')
            temp = len(stool.data)
            databck = [0] * temp # bck [ num, profile, msg, [urls] ]
            for i in range(0,temp):
                data = otool.readstr( str( stool.get(i), encoding='utf-8' ) )
                num = data['data#num'] # 글개수
                profile = data['data#profile'] # 프로필
                msg = data['data#msg'] # 메세지
                urls = [0] * num # url str 리스트
                for j in range(0,num):
                    urls[j] = data['data#urls#' + str(j)]
                databck[i] = [num, profile, msg, urls]
            showmain = [0] * len(datamain) # varify-id msg (num,profile)
            for i in range( 0,len(datamain) ):
                temp = datamain[i]
                showmain[i] = f'm{i} {temp[2]} ({temp[0]},{temp[1]})'
            showsub = [0] * len(datasub) # varify-id msg (num,profile)
            for i in range( 0,len(datasub) ):
                temp = datasub[i]
                showsub[i] = f's{i} {temp[2]} ({temp[0]},{temp[1]})'
            showbck = [0] * len(databck) # varify-id msg (num,profile)
            for i in range( 0,len(databck) ):
                temp = databck[i]
                showbck[i] = f'b{i} {temp[2]} ({temp[0]},{temp[1]})'
            status.set('완료 : KSD 인덱스 파일 로딩됨')
            f7()
            
        else:
            status.set('경고 : KSD 인덱스 파일 존재하지 않음')

        win.mainloop()

class index:

    def get(self,setdata,mode):
        try:
            if os.path.isfile('mode.txt') and os.path.isfile('bcktxt.bck') and os.path.isfile('bckksd.bck'):
                with open('mode.txt','r',encoding='utf-8') as f:
                    temp = f.read()
                os.remove(temp + '.txt')
                os.remove(temp + '.ksd')
                os.rename('bcktxt.bck', temp + '.txt')
                os.rename('bckksd.bck', temp + '.ksd')
                os.remove('mode.txt')
        except:
            pass
        with open('mode.txt','w',encoding='utf-8') as f:
            f.write(mode)
        
        win = tkinter.Tk()
        win.title('KOS 2023 - DCL3')
        win.geometry("500x400+200+100")
        win.resizable(False, False)

        label0 = tkinter.Label(win, text = 'update mode : '+mode, font = ('Consolas', 15) )
        label0.place(x=10,y=10)
        if mode == 'main':
            temp = setdata.main[0]
        elif mode == 'sub':
            temp = setdata.sub[0]
        elif mode == 'bck':
            temp = setdata.bck[0]
        label1 = tkinter.Label(win, text = 'storage id : '+temp[temp.find('id=')+3:], font = ('Consolas', 15) )
        label1.place(x=10,y=40)

        num2 = -1 # 실시간 글 개수
        txt3 = tkinter.StringVar()
        txt3.set( 'realtime post num : ' + str(num2) )
        label4 = tkinter.Label(win, textvariable = txt3, font = ('Consolas', 15) )
        label4.place(x=10,y=70)

        num5 = -1 # 현재 카운트된 글 개수
        txt6 = tkinter.StringVar()
        txt6.set( 'counted post num : ' + str(num5) )
        label7 = tkinter.Label(win, textvariable = txt6, font = ('Consolas', 15) )
        label7.place(x=10,y=100)

        num8 = -1 # 저장 청크 개수
        txt9 = tkinter.StringVar()
        txt9.set( 'saved chunk num : ' + str(num8) )
        label10 = tkinter.Label(win, textvariable = txt9, font = ('Consolas', 15) )
        label10.place(x=10,y=130)

        status = tkinter.StringVar()
        status.set('업데이트 준비 중 . . .') # 현재 상태
        label11 = tkinter.Label(win, textvariable = status, font = ('Consolas', 15) )
        label11.place(x=10,y=170)

        num12 = tkinter.DoubleVar() # 진행바 변수
        bar13 = tkinter.ttk.Progressbar(win, maximum=1000, variable = num12, length=460) # max 1000
        bar13.place(x = 20,y = 320)
        win.update()

        try: # 기존 데이터 읽기
            otool = oreo.toolbox()
            stool = stream.stream()
            stool.read(mode + '.ksd')
            head = otool.readfile(mode + '.txt')
            url = head['header#url']
            num = head['header#num']
            if url != temp:
                raise Exception('url error')
            num5 = num
            num8 = len(stool.data)
        except: # 새로운 파일을 만들고 0 번째부터 시작
            otool = oreo.toolbox()
            stool = stream.stream()
            head = otool.mkobj('header')
            otool.putdt(head,'url',temp)
            otool.putdt(head,'num',0)
            head = otool.wrcom(head.data,True,False)
            with open(mode + '.txt', 'w', encoding='utf-8') as f:
                f.write(head)
            stool.write(mode + '.ksd','')
            num5 = 0
            num8 = 0
        txt6.set( 'counted post num : ' + str(num5) )
        txt9.set( 'saved chunk num : ' + str(num8) )
        win.update()

        shutil.copy(mode + '.txt','bcktxt.bck')
        shutil.copy(mode + '.ksd','bckksd.bck')

        ktool = kdcm3.toolbox()
        stool = stream.stream()
        otool = oreo.toolbox()
        k2tool = kerbal.basic()
        try:
            num2 = ktool.getnum(temp)
        except:
            num2 = 0
        txt3.set( 'realtime post num : ' + str(num2) )
        win.update()

        status.set('업데이트 시작')
        win.update()
        if mode == 'main':
            identify = setdata.main  # url 정보
        elif mode == 'sub':
            identify = setdata.sub
        elif mode == 'bck':
            identify = setdata.bck
        if num2 == 0:
            status.set('에러 : 인터넷 연결 불안정')
            win.update()
            os.remove('bcktxt.bck')
            os.remove('bckksd.bck')
        elif num2 == num5:
            status.set('종료 : 이미 최신 버전의 인덱스입니다')
            win.update()
            os.remove('bcktxt.bck')
            os.remove('bckksd.bck')
        else:
            status.set('진행 : title / body 데이터 수집 중 . . .')
            win.update()
            start = num5 + 1
            end = num2
            url = identify[4]

            output = [0] * (end - start + 1) # [title,body] 데이터, num5 + 1 ~ num2 포함
            for i in range(start, end + 1):
                if i % 100 == 0:
                    time.sleep(5)
                time.sleep(0.5)
                try:
                    temp = ktool.gettxt( url + str(i) )
                except:
                    try:
                        time.sleep(0.5)
                        temp = ktool.gettxt( url + str(i) )
                    except:
                        temp = ['','']
                output[i - start] = temp
                num12.set( int( (i - start + 1) / (end - start + 1) * 900) )
                win.update()

            status.set('진행 : DCL3 표지 분석 중 . . .')
            win.update()
            isupload = False # upload sequence 상태 판별
            upnum = 0 # sequence length
            upurls = [ ] # sequence urls
            temp = [ ] # register : rand data, varify, current num, msg
            stool.read(mode + '.ksd')
            # num2 실시간 글 개수
            # num5 현재 카운트된 글 개수
            # num8 저장 청크 개수
            endpoint = start # 기록상 종료점
            urladd = 0
            seqtotal = 0 # total number of sequence started
            seqend = 0 # total number of sequence ended
            for i in range(start, end + 1):
                title = output[i-start][0]
                body = output[i-start][1]
                if '[DCL3]' in title:
                    endpoint = i
                    try:
                        rand = title[0:2] # 처음 랜덤데이터
                        if not(rand in body):
                            raise Exception('non dcl3')
                        title = title[title.find(']') + 1:]
                        varify = title[title.find('[') + 1:title.find(']')] # 속성 str
                        title = title[title.find(']') + 1:]
                        thisnum = int( title[title.find('[') + 1:title.find(']')] ) # 현재 번호 int
                        title = title[title.find(']') + 1:]
                        entirenum = int( title[title.find('[') + 1:title.find(']')] ) # 전체 번호 int
                        if thisnum != int( body[body.find('[') + 1:body.find(']')] ):
                            raise Exception('non dcl3')
                        body = body[body.find(']') + 1:]
                        msg = body[body.find('[') + 1:body.find(']')] # 메세지 str

                        if thisnum == 0:
                            seqtotal = seqtotal + 1
                            isupload = True
                            upnum = entirenum
                            upurls.append( url + str(i) )
                            temp = [rand, varify, thisnum, msg]
                            if thisnum + 1 == upnum:
                                wrtemp = otool.mkobj('data')
                                otool.putdt(wrtemp, 'profile', temp[1])
                                otool.putdt(wrtemp, 'msg', str( k2tool.b64de( temp[3] ),'utf-8') )
                                otool.putdt(wrtemp, 'num', upnum)
                                ttt = otool.mkobj('urls')
                                for i in range(0,upnum):
                                    urladd = urladd + 1
                                    otool.putdt(ttt, str(i), upurls[i])
                                otool.putobj(wrtemp,ttt)
                                stool.append( bytes(otool.wrcom(wrtemp.data,True,True), encoding='utf-8') )
                                isupload = False
                                upnum = 0
                                upurls = [ ]
                                temp = [ ]
                                num8 = num8 + 1
                                seqend = seqend + 1
                                
                        elif isupload:
                            if (temp[0] == rand) and (temp[1] == varify) and (temp[2] + 1 == thisnum) and (temp[3] == msg):
                                temp[2] = thisnum
                                upurls.append( url + str(i) )
                                if thisnum + 1 == upnum:
                                    wrtemp = otool.mkobj('data')
                                    otool.putdt(wrtemp, 'profile', temp[1])
                                    otool.putdt(wrtemp, 'msg', str( k2tool.b64de( temp[3] ),'utf-8') )
                                    otool.putdt(wrtemp, 'num', upnum)
                                    ttt = otool.mkobj('urls')
                                    for i in range(0,upnum):
                                        urladd = urladd + 1
                                        otool.putdt(ttt, str(i), upurls[i])
                                    otool.putobj(wrtemp,ttt)
                                    stool.append( bytes(otool.wrcom(wrtemp.data,True,True), encoding='utf-8') )
                                    isupload = False
                                    upnum = 0
                                    upurls = [ ]
                                    temp = [ ]
                                    num8 = num8 + 1
                                    seqend = seqend + 1
                            else:
                                isupload = False
                                upnum = 0
                                upurls = [ ]
                                temp = [ ]
                        
                    except:
                        isupload = False
                        upnum = 0
                        upurls = [ ]
                        temp = [ ]
                        
            temp = otool.readfile(mode + '.txt')
            temp = temp['header']
            otool.revice(temp,'header#num',endpoint)
            temp = otool.wrcom(temp.data,True,False)
            with open(mode + '.txt', 'w', encoding='utf-8') as f:
                f.write(temp)
            status.set(f'기존 최신 번호 : {num5}\n저장될 최신 번호 : {endpoint}\n실제 최대 글 번호 : {num2}\n추가된 URL : {urladd}')
            num5 = endpoint
            txt6.set( 'counted post num : ' + str(num5) )
            txt9.set( 'saved chunk num : ' + str(num8) )
            num12.set(950)
            win.update()

            i = tkinter.messagebox.askokcancel('업데이트 초안 생성 완료',f' 업데이트 버전이 저장될 준비를 완료했습니다. \n 시작된 시퀀스 {seqtotal} 개, 완료된 시퀀스 {seqend} 개 \n 이 버전을 저장하시겠습니까? ')
            if i:
                os.remove('bcktxt.bck')
                os.remove('bckksd.bck')
            else:
                os.remove(mode + '.txt')
                os.remove(mode + '.ksd')
                os.rename('bcktxt.bck', mode + '.txt')
                os.rename('bckksd.bck', mode + '.ksd')
            num12.set(1000)
            win.update()

        os.remove('mode.txt')
        win.mainloop()

class test:

    def do(self,setdata):
        win = tkinter.Tk()
        win.title('KOS 2023 - DCL3')
        win.geometry("500x400+200+100")
        win.resizable(False, False)

        # upload 대상 선택
        label0 = tkinter.Label(win, text = '대상 : ', font = ('Consolas', 15) )
        label0.place(x=10,y=15)
        key1 = ['0) main', '1) sub', '2) bck']
        combo2 = tkinter.ttk.Combobox(win, width=13, font = ("Consolas",15), values = key1)
        combo2.set( key1[0] ) #프로필 선택
        combo2.place(x=210,y=15)
        def f3():
            time.sleep(0.1)
            nonlocal win
            nonlocal select0
            nonlocal select1
            nonlocal str5
            nonlocal combo2
            temp = combo2.get()[3:]
            select0 = True
            select1 = int( combo2.get()[0] )
            str5.set(temp)
            win.update()
        but4 = tkinter.Button(win, text = 'select', font = ("Consolas",14), command = f3)
        but4.place(x=400,y=10) #선택 버튼
        str5 = tkinter.StringVar()
        str5.set('-')
        label6 = tkinter.Label(win, textvariable = str5, font = ('Consolas', 15) )
        label6.place(x=80,y=15)
        select0 = False # 선택 여부
        select1 = -1 # upload 대상 번호

        # 테스트 모드 선택
        label7 = tkinter.Label(win, text = '모드 : ', font = ('Consolas', 15) )
        label7.place(x=10,y=75)
        key8 = ['0) 단순 텍스트', '1) 저용량 사진', '2) 고용량 사진']
        combo9 = tkinter.ttk.Combobox(win, width=13, font = ("Consolas",15), values = key8)
        combo9.set( key8[0] ) #모드 선택
        combo9.place(x=210,y=75)
        def f10():
            time.sleep(0.1)
            nonlocal win
            nonlocal select2
            nonlocal select3
            nonlocal str11
            nonlocal combo9
            temp = combo9.get()[3:]
            select2 = True
            select3 = int( combo9.get()[0] )
            str11.set(temp)
            win.update()
        but12 = tkinter.Button(win, text = 'select', font = ("Consolas",14), command = f10)
        but12.place(x=400,y=70) #선택 버튼
        str11 = tkinter.StringVar()
        str11.set('-')
        label13 = tkinter.Label(win, textvariable = str11, font = ('Consolas', 15) )
        label13.place(x=80,y=75)
        select2 = False # 선택 여부
        select3 = -1 # mode 번호

        def func():
            time.sleep(0.1)
            nonlocal win
            nonlocal select0 # tf
            nonlocal select1 # num
            nonlocal select2 # tf
            nonlocal select3 # num
            nonlocal num18
            nonlocal setdata
            nonlocal result
            ktool = kerbal.basic()
            ntool = nox2.toolbox()

            #초기화
            num18.set(0)
            result.set('-')
            win.update()
            time.sleep(0.1)

            if select0 and select2:
                rdata = str( hex( random.randrange(0,256) ) ) + '0'
                rdata = rdata[2:4] # 2 글자 랜덤데이터
                title = rdata + ' [DCL3] [test] [0] [1] 0001' # 글 제목
                body = rdata + ' [0] [' + ktool.b64en( bytes(f'upload test storage : {select1} mode : {select3}','utf-8') ) + '] 0001' # 글 본문
                num18.set(1)
                win.update()
                time.sleep(0.1)

                # 삽입할 사진 생성
                try:
                    shutil.rmtree('temp366')
                except:
                    pass
                os.mkdir('temp366')
                if select3 == 1:
                    shutil.copyfile(setdata.path,'temp366//test.png')
                elif select3 == 2:
                    wr = [0] * 83886080
                    for i in range(0,83886080):
                        wr[i] = random.randrange(0,256)
                    with open('temp366\\temp.dat','wb') as f:
                        wr = bytes(wr)
                        f.write( wr ) # wr : 80mb bytes
                    ntool.set(setdata.core,setdata.path)
                    temp = ntool.pack('temp366\\temp.dat',False,'png') # kpng pack
                    num = temp[0] # 개수
                    name = temp[1] #  일련번호
                    os.remove('temp366\\temp.dat')
                    for i in range(0,num):
                        shutil.move('temp270\\' + name + str(i) + '.png', 'temp366' + '\\' + name + str(i) + '.png')
                    shutil.rmtree('temp270')
                num18.set(2)
                win.update()
                time.sleep(0.1)

                # 업로드
                if select1 == 0:
                    gall = setdata.main
                elif select1 == 1:
                    gall = setdata.sub
                else:
                    gall = setdata.bck
                dtool = kdcm3.toolbox()
                con = dtool.getconfig() # config dict
                num18.set(3)
                win.update()
                time.sleep(0.1)
                dtool.set(gall[0], gall[1], con)
                try:
                    dtool.write(gall[2], gall[3], title, body, list( os.path.abspath('temp366\\' + i) for i in os.listdir('temp366') ), True, True )
                    err0 = '문제 없음' # 업로드 에러 코드
                except Exception as e:
                    e = str(e)
                    if e == 'timeout':
                        err0 = '문제/업로드 시간 초과'
                    elif e == 'true':
                        err0 = '문제/서버 상태 나쁨'
                    else:
                        err0 = '문제/' + e[0:15]
                num18.set(4)
                win.update()
                time.sleep(0.1)

                # 최신 글번호 확인
                time.sleep(2.5)
                num18.set(5)
                win.update()
                time.sleep(0.1)
                try:
                    new = dtool.getnum( gall[0] ) # 최신 글 번호
                    err1 = '문제 없음' # 최신글 에러 코드
                except Exception as e:
                    new = 0
                    err1 = '문제/' + str(e)[0:15]
                num18.set(6)
                win.update()
                time.sleep(0.1)

                # 텍스트 내용 확인
                try:
                    response = dtool.gettxt( gall[4] + str(new) ) # [title, body]
                    err2 = '문제 없음' # 텍스트 다운 에러 코드
                except Exception as e:
                    response = ['', '']
                    err2 = '문제/' + str(e)[0:15]
                if (rdata in response[0]) and (rdata in response[1]):
                    err3 = '문제 없음' # 텍스트 비교 에러 코드
                else:
                    err3 = '문제/내용 불일치'
                if ('[DCL3]' in response[0]) and ('[test]' in response[0]) and ('[0]' in response[0]) and ('[1]' in response[0]):
                    pass
                else:
                    err3 = '문제/내용 불일치'
                if body[ body.find('['):body.find(']') + 1 ] in response[1]:
                    pass
                else:
                    err3 = '문제/내용 불일치'
                num18.set(7)
                win.update()
                time.sleep(0.1)

                # 사진 다운로드
                try:
                    names = dtool.getpic( gall[4] + str(new) ) # 사진 파일 리스트
                except Exception as e:
                    names = [ ]
                    err4 = '문제/사진 다운로드 실패'
                num18.set(8)
                win.update()
                time.sleep(0.1)

                # 이진 내용 확인
                if select3 == 0:
                    err4 = '해당 사항 없음' # 이진 내용 일치 여부
                elif select3 == 1:
                    err4 = '문제/사진 다운로드 실패'
                    with open(setdata.path,'rb') as f:
                        wr = f.read() # 비교 데이터 bytes
                    for i in names:
                        with open(i,'rb') as f:
                            if f.read() == wr:
                                err4 = '문제 없음'
                else:
                    temp = ntool.detect('temp306a')
                    if temp[0] == 0:
                        err4 = '문제/사진 다운로드 실패'
                    else:
                        ntool.unpack( ['temp306a'] + temp )
                        with open('temp270\\result.dat','rb') as f:
                            if f.read()[0:83886080] == wr:
                                err4 = '문제 없음'
                            else:
                                err4 = '문제/사진 디코딩 실패'
                num18.set(9)
                win.update()
                time.sleep(0.1)

                # 폴더 정리
                try:
                    shutil.rmtree('temp270')
                except:
                    pass
                try:
                    shutil.rmtree('temp306a')
                except:
                    pass
                os.mkdir('temp306a')
                try:
                    shutil.rmtree('temp366')
                except:
                    pass
                win.update()

                temp = '업로드 : ' + err0 + '\n글번호 구하기 : ' + err1 + '\n텍스트 다운로드 : ' + err2 + '\n텍스트 비교 : ' + err3 + '\n이진 파일 비교 : ' + err4
                result.set(temp)
                num18.set(10)
                win.update()
                time.sleep(0.1)

            else:
                tkinter.messagebox.showinfo('선택 없음 경고',' 선택된 대상/모드가 없습니다. \n 테스트를 진행할 대상/모드를 선택하십시오. ')
            win.update()
        but14 = tkinter.Button(win, text = 'test', font = ("Consolas",14), command = func)
        but14.place(x=10,y=170) #go test 버튼

        label15 = tkinter.Label(win, text = '결과 >>>', font = ('Consolas', 15) )
        label15.place(x=10,y=220)
        result = tkinter.StringVar()
        result.set('-') # 결과 텍스트
        label16 = tkinter.Label(win, textvariable = result, font = ('Consolas', 15) )
        label16.place(x=120,y=175)

        num18 = tkinter.DoubleVar() # 진행바 변수
        bar17 = tkinter.ttk.Progressbar(win, maximum=10, variable = num18, length=460) # max ?
        bar17.place(x = 20,y = 320)
        win.update()

class settings:

    def __init__(self):
        tool = oreo.toolbox()
        temp = tool.readfile('settings.txt')
        self.core = temp['settings#core'] #프로세스 수
        self.chunk = temp['settings#chunk'] #청크 크기
        self.limit = temp['settings#limit'] #게시물당 크기 제한
        self.path = os.path.abspath( temp['settings#p0'] ) #가이드 사진 경로
        self.main = [ temp['settings#site0m'], temp['settings#site0w'], temp['settings#site0u'], temp['settings#site0p'], temp['settings#site0n'] ] #main 저장소 데이터
        self.sub = [ temp['settings#site1m'], temp['settings#site1w'], temp['settings#site1u'], temp['settings#site1p'], temp['settings#site1n'] ] #sub 저장소 데이터
        self.bck = [ temp['settings#site2m'], temp['settings#site2w'], temp['settings#site2u'], temp['settings#site2p'], temp['settings#site2n'] ] #bck 저장소 데이터
        end = True
        num = 0
        self.profile = [ ] #프로필 데이터 리스트
        while end:
            path = 'settings#profile#' + str(num)
            if path in temp:
                self.profile.append( [ temp[path + '#title'], temp[path + '#pw'], temp[path + '#kf'] ] )
            else:
                end = False
            num = num + 1

class addon:

    def erase(self,setdata):
        win = tkinter.Tk()
        win.title('KOS 2023 - DCL3')
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

        list0 = [ ] # 표시 리스트
        bg = os.path.join(os.path.expanduser('~'),'Desktop') # 바탕화면 경로
        dw = os.path.join(os.path.expanduser('~'),'Downloads') # 바탕화면 경로
        def show(): # 화면에 띄우기
            time.sleep(0.1)
            nonlocal win
            nonlocal list0
            nonlocal listbox
            nonlocal mask
            nonlocal folder
            bglist = os.listdir(bg) # 바탕화면 파일폴더
            dwlist = os.listdir(dw) # 다운로드 파일폴더
            list0 = [ ]
            if folder == 'bg':
                temp = bglist
            else:
                temp = dwlist
            for i in temp:
                if mask:
                    var = True
                    m = i
                    if '.' in i:
                        m = i[0:i.rfind('.')]
                    for j in list(m):
                        if not ( j in ['0','1','2','3','4','5','6','7','8','9'] ):
                            var = False
                    if var:
                        list0.append(i)
                else:
                    list0.append(i)
            listbox.delete( 0,listbox.size() )
            for i in list0:
                listbox.insert( listbox.size(),i )
            win.update()

        mask = True # mask 적용 여부
        def f1():
            time.sleep(0.1)
            nonlocal win
            nonlocal mask
            nonlocal but1
            mask = not(mask)
            if mask:
                but1.configure(bg = 'lawn green')
            else:
                but1.configure(bg = 'gray95')
            win.update()
            show()
        but1 = tkinter.Button(win, text = 'mask', font = ('Consolas',15), command = f1, bg = 'lawn green')
        but1.place(x = 10,y = 350)

        folder = 'bg' # 'bg' 'dw' 보여줄 폴더
        def f2():
            time.sleep(0.1)
            nonlocal win
            nonlocal folder
            nonlocal but2
            nonlocal but3
            folder = 'bg'
            but2.configure(bg = 'lawn green')
            but3.configure(bg = 'gray95')
            win.update()
            show()
        but2 = tkinter.Button(win, text = '바탕화면', font = ('Consolas',15), command = f2, bg = 'lawn green')
        but2.place(x = 110,y = 350)
        def f3():
            time.sleep(0.1)
            nonlocal win
            nonlocal folder
            nonlocal but2
            nonlocal but3
            folder = 'dw'
            but3.configure(bg = 'lawn green')
            but2.configure(bg = 'gray95')
            win.update()
            show()
        but3 = tkinter.Button(win, text = '다운로드', font = ('Consolas',15), command = f3, bg = 'gray95')
        but3.place(x = 215,y = 350)

        def f4():
            time.sleep(0.1)
            nonlocal win
            nonlocal folder
            nonlocal listbox
            nonlocal list0
            temp = list0[ listbox.curselection()[0] ]
            if folder == 'bg':
                temp = os.path.join(bg,temp)
            elif folder == 'dw':
                temp = os.path.join(dw,temp)
            out = f' 이 항목을 완전히 삭제할까요? \n {temp} \n'
            if os.path.isdir(temp):
                out = out + f' 하위 항목 : {len( os.listdir(temp) )} 개 '
            else:
                out = out + f' 파일 크기 : {os.path.getsize(temp)} 바이트 '
            i = tkinter.messagebox.askokcancel('파일/폴더 삭제',out)
            if i:
                if os.path.isdir(temp):
                    shutil.rmtree(temp)
                else:
                    os.remove(temp)
            show()
        but4 = tkinter.Button(win, text = 'erase', font = ('Consolas',15), command = f4)
        but4.place(x = 420,y = 350)

        show()
        win.mainloop()

if __name__ == '__main__':
    global off
    off = True
    mp.freeze_support()
    k = mainclass()
    global setdata
    setdata = settings()
    while off:
        time.sleep(0.1)
        k.mainfunc()
    time.sleep(0.5)

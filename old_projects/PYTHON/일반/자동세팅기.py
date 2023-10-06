import time
import os
import shutil
import winshell
from win32com.client import Dispatch

import tkinter
import tkinter.messagebox
from tkinter import filedialog
import tkinter.ttk

import mung2
import nox2
import oreo
import kdcm3

import multiprocessing as mp

class mainclass:

    def mainfunc(self):
        flist = os.listdir() #파일 리스트
        flist = [ i for i in flist if i[-4:] == '.kds' ]
        uselist = [ ] #실제 파일 이름
        tplist = [ ] #파일 종류 bytes
        headlist = [ ] #헤더 bytes
        infolist = [ ] #설명
        for i in flist:
            with open(i,'rb') as f:
                temp = f.read(4)
                if temp == b'KDS1':
                    temp = f.read(2)
                    if temp in [b'IE',b'FD']:
                        uselist.append(i)
                        tplist.append(temp)
                        size = f.read(1)[0] + f.read(1)[0] * 256
                        f.read(8)
                        temp = f.read(size)
                        headlist.append(temp)
                        try:
                            temp = str(temp,'utf-8') #str
                            otool = oreo.toolbox()
                            temp = otool.readstr(temp) #dict
                            info = temp['header#info']
                        except:
                            info = '이 파일에 대한 정보가 없습니다.'
                        infolist.append(info)
        
        win = tkinter.Tk()
        win.title('자동세팅')
        win.geometry("400x300+100+50")
        win.resizable(False, False)
        win.configure(bg='plum1')

        frame = tkinter.Frame(win)
        frame.place(x=10,y=10)
        listbox = tkinter.Listbox(
            frame, width=27,  height=7, font = ('Consolas', 15),
            bg='plum1', fg='purple1', selectbackground='purple1', selectforeground='plum1')
        listbox.pack(side="left", fill="y")
        scrollbar0 = tkinter.Scrollbar(frame, orient="vertical")
        scrollbar0.config(command=listbox.yview)
        scrollbar0.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar0.set)

        for i in range( 0,len(uselist) ):
            temp = str( tplist[i],'utf-8' ) + '* ' + uselist[i]
            listbox.insert( listbox.size(),temp )

        def extract(): #자동 사진 풀기 / 자동 설치
            time.sleep(0.1)
            nonlocal listbox
            nonlocal uselist
            nonlocal tplist
            nonlocal headlist
            temp = listbox.curselection()[0]
            k = userclass()
            nonlocal win
            nonlocal status
            status.set('추출/설치 진행중...')
            win.update()
            time.sleep(0.2)
            k.extfunc(uselist[temp],tplist[temp],headlist[temp])
            status.set('추출/설치 완료')
            win.update()
            tkinter.messagebox.showinfo('추출/설치 완료',' IE 타입의 경우 추출된 설치 파일을 이용해 설치 작업을 진행하십시오.\nFD 타입의 경우 설치된 프로그램을 사용할 수 있습니다. ')
        but0 = tkinter.Button(win, font = ('맑은 고딕', 14), text='풀기', bg='plum1', fg='purple1', command=extract)
        but0.place(x=340,y=20)

        def manual(): #수동 사진 풀기
            time.sleep(0.1)
            nonlocal win
            win.destroy()
            k = userclass()
            k.manualfunc()
        but1 = tkinter.Button(win, font = ('맑은 고딕', 14), text='수동', bg='plum1', fg='purple1', command=manual)
        but1.place(x=340,y=70)

        def zipf(): #배포
            time.sleep(0.1)
            nonlocal win
            win.destroy()
            k = mainclass()
            k.zipfunc()
        but2 = tkinter.Button(win, font = ('맑은 고딕', 14), text='묶기', bg='plum1', fg='purple1', command=zipf)
        but2.place(x=340,y=120)

        status = tkinter.StringVar()
        status.set('kds 확장자를 가진 데이터 파일을\n이 프로그램과 같은 폴더에 놓으십시오.\n이후 프로그램을 재시작하거나\n설치를 진행할 수 있습니다.')
        label0 = tkinter.Label(win, font = ('Consolas', 14), textvariable = status, bg='plum1', fg='purple1')
        label0.place(x=10,y=190)
        win.update()

        def click(event):
            time.sleep(0.1)
            nonlocal win
            nonlocal status
            nonlocal listbox
            nonlocal infolist
            temp = listbox.curselection()[0]
            status.set( infolist[temp] )
            win.update()
        listbox.bind('<ButtonRelease-1>',click)

        win.mainloop()

    def zipfunc(self):
        win = tkinter.Tk()
        win.title('자동세팅')
        win.geometry("500x200+100+50")
        win.resizable(False, False)

        status = tkinter.StringVar()
        status.set('개발자 모드 활성화됨')
        label0 = tkinter.Label(win, font = ('Consolas', 14), textvariable = status)
        label0.place(x=10,y=10)

        entry0 = tkinter.Entry(win, font = ('Consolas', 14), width=47)
        entry0.place(x=10,y=100)

        def inf():
            time.sleep(0.1)
            nonlocal win
            nonlocal status
            nonlocal entry0
            temp = entry0.get() #입력 명령
            if temp == 'ie':
                status.set('명령어 파일을 선택하십시오.')
                win.update()
                time.sleep(0.2)
                out0 = filedialog.askopenfile(title='파일 선택')
                out0 = out0.name.replace('/','\\') #명령어 txt
                size = os.path.getsize(out0) #헤더크기
                head = b'KDS1IE' + bytes( [ size % 256, size // 256 ] ) + bytes(8) #매직넘버
                with open('ieout.kds','wb') as f:
                    f.write(head)
                    with open(out0,'rb') as t:
                        f.write( t.read() )
                status.set('ieout.kds 파일로 변환되었습니다.')
                win.update()

            elif temp == 'fd':
                status.set('명령어 파일을 선택하십시오.')
                win.update()
                time.sleep(0.2)
                out0 = filedialog.askopenfile(title='파일 선택')
                out0 = out0.name.replace('/','\\') #명령어 txt
                time.sleep(0.5)
                status.set('데이터 파일을 선택하십시오.')
                win.update()
                time.sleep(0.2)
                out1 = filedialog.askopenfile(title='파일 선택')
                out1 = out1.name.replace('/','\\') #데이터
                size = os.path.getsize(out0) #헤더크기
                head = b'KDS1FD' + bytes( [ size % 256, size // 256 ] ) + bytes(8) #매직넘버
                with open('fdout.kds','wb') as f:
                    f.write(head)
                    with open(out0,'rb') as t:
                        f.write( t.read() )
                    with open(out1,'rb') as t:
                        temp = ''
                        while temp != b'':
                            temp = t.read(100000000)
                            f.write(temp)
                status.set('fdout.kds 파일로 변환되었습니다.')
                win.update()

            elif temp == 'help':
                status.set('"help" "pack" "unpack"\n"zip" "unzip" "ie" "fd"')

            elif temp == 'pack':
                status.set('묶을 파일을 선택하십시오.')
                win.update()
                time.sleep(0.2)
                out = filedialog.askopenfile(title='파일 선택')
                out = out.name.replace('/','\\')
                ntool = nox2.toolbox()
                ntool.set(4,'bp.png')
                ntool.pack(out,False,'png')
                ntool.clear(False)
                os.remove('temp270\\source.dat')
                os.remove('temp270\\status.txt')
                status.set('temp270 폴더에 묶였습니다.')
                win.update()

            elif temp == 'unpack':
                status.set('풀 파일이 든 폴더를 선택하십시오.')
                win.update()
                time.sleep(0.2)
                out = filedialog.askdirectory(title='폴더 선택')
                out = out.replace('/','\\')
                ntool = nox2.toolbox()
                ntool.set(4,'bp.png')
                ntool.unpack( [out] + ntool.detect(out) )
                ntool.clear(False)
                os.remove('temp270\\status.txt')
                status.set('temp270 폴더에 풀렸습니다.')
                win.update()

            elif temp == 'zip':
                status.set('묶을 폴더를 선택하십시오.')
                win.update()
                time.sleep(0.2)
                out = filedialog.askdirectory(title='폴더 선택')
                out = out.replace('/','\\')
                mtool = mung2.toolbox()
                mtool.pack(out,'mpacked',False)
                status.set('mpacked 파일로 묶였습니다.')
                win.update()

            elif temp == 'unzip':
                status.set('풀 파일을 선택하십시오.')
                win.update()
                time.sleep(0.2)
                out = filedialog.askopenfile(title='파일 선택')
                out = out.name.replace('/','\\')
                mtool = mung2.toolbox()
                mtool.unpack(out)
                status.set('temp261 폴더에 풀렸습니다.')
                win.update()

            else:
                status.set('알 수 없는 명령어입니다.\n사용 가능한 명령어 목록을 보려면\n"help"를 입력하십시오.')
            win.update()
            
        but0 = tkinter.Button(win, font = ('Consolas', 14), text='GO', command=inf)
        but0.place(x=10,y=150)

        win.mainloop()

class userclass:

    def manualfunc(self):
        win = tkinter.Tk()
        win.title('자동세팅')
        win.geometry("500x200+100+50")
        win.resizable(False, False)

        status = tkinter.StringVar()
        status.set('수동 사진 추출 모드입니다.\nkds 파일을 선택하십시오.')
        label0 = tkinter.Label(win, font = ('Consolas', 14), textvariable = status)
        label0.place(x=10,y=10)

        def inf():
            nonlocal win
            nonlocal status
            time.sleep(0.1)
            out = filedialog.askopenfile(title='파일 선택')
            out = out.name.replace('/','\\') #kds file
            with open(out,'rb') as f:
                head = f.read(4) #매직넘버
                tp = f.read(2) #타입
                size = f.read(1)[0] + f.read(1)[0] * 256 #헤더크기
                f.read(8)
                txt = str( f.read(size),'utf-8' ) #헤더 str
            if head != b'KDS1':
                status.set('올바른 kds 파일이 아닙니다.')
                win.update()
                time.sleep(0.2)
            elif tp != b'IE':
                status.set('인터넷 다운로드 파일이 아닙니다.')
                win.update()
                time.sleep(0.2)
            else:
                otool = oreo.toolbox()
                txt = otool.readstr(txt) #딕셔너리 데이터
                info = txt['header#info']
                status.set(info + '\ntemp353.txt 파일의 모든 URL에 접속해\n모든 사진을 하나의 폴더에 다운로드 받으십시오.\n이후 다운받은 사진이 있는 폴더를 선택하십시오.')
                win.update()
                time.sleep(0.2)
                num = txt['header#num'] #url num
                urls = [ ]
                for i in range(0,num):
                    urls.append( txt['header#'+str(i)] )
                with open('temp353.txt','w',encoding='utf-8') as f:
                    for i in urls:
                        f.write(i+'\n')
                time.sleep(0.5)
                out = filedialog.askdirectory(title='폴더 선택')
                out = out.replace('/','\\')
                status.set('풀기 작업 진행중...')
                win.update()
                time.sleep(0.2)
                ntool = nox2.toolbox()
                ntool.set(4,'bp.png')
                ntool.unpack( [out] + ntool.detect(out) )
                ntool.clear(False)
                os.remove('temp270\\status.txt')
                os.rename('temp270\\result.dat','temp270\\manual_unzip.kds')
                status.set('temp270 폴더에 풀렸습니다.')
                win.update()
            
        but0 = tkinter.Button(win, font = ('Consolas', 14), text='GO', command=inf)
        but0.place(x=10,y=150)

        win.mainloop()

    def extfunc(self,name,tp,head):
        if tp == b'IE':
            otool = oreo.toolbox()
            txt = otool.readstr( str(head,'utf-8') ) #dict
            num = txt['header#num']
            urls = [ ]
            for i in range(0,num):
                urls.append( txt['header#'+str(i)] )
            ktool = kdcm3.toolbox()
            try:
                try:
                    shutil.rmtree('temp353')
                except:
                    pass
                os.mkdir('temp353') #초기화
                for i in urls: #사진 모으기
                    ktool.getpic(i)
                    temp = os.listdir('temp306a')
                    for j in temp: #옮기기
                        os.rename('temp306a\\'+j,'temp353\\'+j)
                    time.sleep(3)
                ntool = nox2.toolbox()
                ntool.set(4,'bp.png')
                ntool.unpack( ['temp353'] + ntool.detect('temp353') )
                ntool.clear(False)
                os.remove('temp270\\status.txt')
                os.rename('temp270\\result.dat','install_file.kds')
                shutil.rmtree('temp270')
                shutil.rmtree('temp306a')
                shutil.rmtree('temp306b')
                shutil.rmtree('temp353')
            except:
                tkinter.messagebox.showinfo('추출중 오류',' 데이터 추출 중 오류가 발생했습니다. 인터넷 연결을 확인한 후 다시 시도하거나 문제가 계속된다면 수동 모드로 추출하십시오. ')

        else:
            otool = oreo.toolbox()
            txt = otool.readstr( str(head,'utf-8') ) #dict
            num = txt['header#num'] #order num
            try:
                shutil.rmtree('temp353')
            except:
                pass
            os.mkdir('temp353') #초기화
            with open('temp353\\temp','wb') as f:
                with open(name,'rb') as t:
                    t.read( 16 + len(head) )
                    temp = ''
                    while temp != b'':
                        temp = t.read(100000000)
                        f.write(temp)
            mtool = mung2.toolbox()
            mtool.unpack('temp353\\temp') #풀기

            start = os.path.expanduser('~') + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\' #startup
            bck = os.path.expanduser('~') + '\\Desktop\\' #바탕화면
            user = os.path.expanduser('~') + '\\' #user folder
            this = '' #current folder
            dwn = 'temp261\\' #downloaf folder temp261
            for i in range(0,num):
                try:
                    time.sleep(0.5)
                    order = txt['header#'+str(i)+'#order'] #order str
                    if order == 'start':
                        loc1 = txt['header#'+str(i)+'#loc1']
                        name1 = txt['header#'+str(i)+'#name1']
                        if loc1 == 'start':
                            loc1 = start
                        elif loc1 == 'bck':
                            loc1 = bck
                        elif loc1 == 'user':
                            loc1 = user
                        elif loc1 == 'dwn':
                            loc1 = dwn
                        elif loc1 == 'this':
                            loc1 = this
                        os.startfile(loc1 + name1)
                    elif order == 'del':
                        loc1 = txt['header#'+str(i)+'#loc1']
                        name1 = txt['header#'+str(i)+'#name1']
                        if loc1 == 'start':
                            loc1 = start
                        elif loc1 == 'bck':
                            loc1 = bck
                        elif loc1 == 'user':
                            loc1 = user
                        elif loc1 == 'dwn':
                            loc1 = dwn
                        elif loc1 == 'this':
                            loc1 = this
                        if os.path.isfile(loc1 + name1):
                            os.remove(loc1 + name1)
                        else:
                            shutil.rmtree(loc1 + name1)
                    elif order == 'move':
                        loc1 = txt['header#'+str(i)+'#loc1']
                        name1 = txt['header#'+str(i)+'#name1']
                        if loc1 == 'start':
                            loc1 = start
                        elif loc1 == 'bck':
                            loc1 = bck
                        elif loc1 == 'user':
                            loc1 = user
                        elif loc1 == 'dwn':
                            loc1 = dwn
                        elif loc1 == 'this':
                            loc1 = this
                        loc2 = txt['header#'+str(i)+'#loc2']
                        name2 = txt['header#'+str(i)+'#name2']
                        if loc2 == 'start':
                            loc2 = start
                        elif loc2 == 'bck':
                            loc2 = bck
                        elif loc2 == 'user':
                            loc2 = user
                        elif loc2 == 'dwn':
                            loc2 = dwn
                        elif loc2 == 'this':
                            loc2 = this
                        shutil.move(loc1 + name1, loc2 + name2)
                    elif order == 'lnk':
                        loc1 = txt['header#'+str(i)+'#loc1']
                        name1 = txt['header#'+str(i)+'#name1']
                        if loc1 == 'start':
                            loc1 = start
                        elif loc1 == 'bck':
                            loc1 = bck
                        elif loc1 == 'user':
                            loc1 = user
                        elif loc1 == 'dwn':
                            loc1 = dwn
                        elif loc1 == 'this':
                            loc1 = this
                        loc2 = txt['header#'+str(i)+'#loc2']
                        name2 = txt['header#'+str(i)+'#name2']
                        if loc2 == 'start':
                            loc2 = start
                        elif loc2 == 'bck':
                            loc2 = bck
                        elif loc2 == 'user':
                            loc2 = user
                        elif loc2 == 'dwn':
                            loc2 = dwn
                        elif loc2 == 'this':
                            loc2 = this
                        shell = Dispatch('WScript.Shell')
                        shortcut = shell.CreateShortCut(loc2 + name2)
                        shortcut.Targetpath = loc1 + name1
                        temp = loc1 + name1
                        temp = temp.replace('/','\\')
                        if '\\' in temp:
                            temp = temp[ 0:temp.rfind('\\') ]
                        else:
                            temp = ''
                        shortcut.WorkingDirectory = temp
                        shortcut.save()
                except Exception as e:
                    time.sleep(0.5)
                    temp = otool.wrcom(txt['header#'+str(i)].data,True,False)
                    tkinter.messagebox.showinfo('설치 중 명령어 오류',' 일부 구성 요소가 불완전하게 설치될 수 있습니다.\n' + str(e)[0:20] + '\n' + temp + ' ')
            
            shutil.rmtree('temp261')
            shutil.rmtree('temp353')

if __name__ == '__main__':
    mp.freeze_support()
    k = mainclass()
    k.mainfunc()
    time.sleep(0.5)

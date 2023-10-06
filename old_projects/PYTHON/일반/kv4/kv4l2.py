# KVault4 Layer 2

import tkinter
import tkinter.ttk
import tkinter.font
import tkinter.messagebox
from tkinter import filedialog

import os
import shutil
import time
import random
import multiprocessing as mp

import kv4l1 as fcore

class console:

    def __init__(self):
        self.co = 0 # layer 1 tool
        self.open = False # opened const
        self.pnum = -1 # folder path int
        self.comp = [ ] # lower component [int]
        self.rand = random.randrange(0, 10000)

    def set(self, path): # cluster folder path
        self.co = fcore.toolbox(path) # layer 1 tool
        if self.co.settings['settings#layer2#atominfo'] == 0:
            self.atominfo = True
        else:
            self.atominfo = False
        if self.co.settings['settings#layer2#structinfo'] == 0:
            self.structinfo = True
        else:
            self.structinfo = False
        if self.co.settings['settings#layer2#actualsize'] == 0:
            self.actualsize = True
        else:
            self.actualsize = False
        if self.co.settings['settings#layer2#export'] == '':
            self.export = os.path.join(os.path.expanduser('~'), 'Desktop')
        else:
            self.export = self.co.settings['settings#layer2#export']

    def sizeconv(self, num): # num int -> converted size str
        a = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        b = 0
        c = float(num)
        while c >= 1000:
            if b < len(a) - 1:
                c = c / 1024
                b = b + 1
            else:
                break
        if c < 10:
            c = int(c * 100) / 100
        elif c < 100:
            c = int(c * 10) / 10
        else:
            c = int(c)
        return f'({c}{a[b]})'

    def imfull(self, dirname, strname, status, win): # str, str, class, class
        status.set(f'imfull : {dirname}')
        win.update()
        flist = os.listdir(dirname)
        file = [ ] # tgt file fullpath
        folder = [ ] # tgt folder full path
        for i in flist:
            temp = f'{dirname}/{i}'
            if os.path.isdir(temp):
                folder.append(temp)
            else:
                file.append(temp)
        num = self.co.getnum(strname) # current struct num
        if file != [ ]:
            self.co.imfiles(num, file, self.rand)
        for i in folder:
            temp = i[i.rfind('/') + 1:]
            self.co.newfolder(num, temp)
            self.imfull(i, f'{strname}{temp}/', status, win)

    def exfull(self, strnum, dirname, status, win): # int, str, class, class
        status.set(f'exfull : {dirname}')
        win.update()
        os.mkdir(dirname)
        atom = [ ] # num [int]
        struct = [ ] # num [int]
        name = [ ] # dir name full [str]
        for i in self.co.getlower(strnum):
            temp = self.co.tool.fsinfow(i)
            if temp[1] == 0:
                struct.append(i)
                name.append(f'{dirname}/{temp[2]}')
            else:
                atom.append(i)
        if atom != [ ]:
            self.co.exatoms(atom, dirname, self.rand)
        for i in range( 0, len(struct) ):
            self.exfull(struct[i], name[i], status, win)

    def main(self): # main window
        win = tkinter.Tk()
        win.title('KVault4')
        win.geometry("800x600+100+50")
        win.resizable(False, False)

        def mf1(): # im files
            time.sleep(0.1)
            nonlocal status
            files = [ ] # tgt files
            if self.pnum != -1:
                out = filedialog.askopenfiles(title='파일들 선택')
                for i in out:
                    files.append(i.name)
                try:
                    if files != [ ]:
                        self.co.imfiles(self.pnum, files, self.rand)
                        status.set('파일들 가져오기 성공')
                        self.comp = self.co.getlower(self.pnum)
                        func3()
                except Exception as e:
                    if str(e) == 'fpusherror':
                        status.set('파일 업로드 과정 오류')
                    elif str(e) == 'hpusherror':
                        status.set('헤더 업로드 과정 오류')
                    else:
                        status.set(f'critical error : {e}')
                try:
                    shutil.rmtree(f'temp474_{self.rand}')
                except:
                    pass

        def mf2(): # im folder
            time.sleep(0.1)
            nonlocal status
            if self.pnum != -1:
                try:
                    files = filedialog.askdirectory(title='폴더 선택')
                except:
                    files = ''
                try:
                    if files != '':
                        self.co.imfolder(self.pnum, files, self.rand)
                        status.set('폴더 가져오기 성공')
                        self.comp = self.co.getlower(self.pnum)
                        func3()
                except Exception as e:
                    if str(e) == 'fpusherror':
                        status.set('파일 업로드 과정 오류')
                    elif str(e) == 'hpusherror':
                        status.set('헤더 업데이트 과정 오류')
                    else:
                        status.set(f'critical error : {e}')
                try:
                    shutil.rmtree(f'temp474_{self.rand}')
                except:
                    pass

        def mf3(): # im full
            time.sleep(0.1)
            nonlocal status
            nonlocal win
            nonlocal current
            if self.pnum != -1:
                try:
                    files = filedialog.askdirectory(title='폴더 선택')
                    files = files.replace('\\', '/')
                except:
                    files = ''
                if files != '':
                    try:
                        temp = files[files.rfind('/') + 1:]
                        self.co.newfolder(self.pnum, temp)
                        self.imfull(files, f'{current.get()}{temp}/', status, win)
                        status.set('전체 폴더 가져오기 성공')
                        self.comp = self.co.getlower(self.pnum)
                        func3()
                    except Exception as e:
                        if str(e) == 'fpusherror':
                            status.set('파일 업로드 과정 오류')
                        elif str(e) == 'hpusherror':
                            status.set('헤더 업데이트 과정 오류')
                        else:
                            status.set(f'critical error : {e}')
                    try:
                        shutil.rmtree(f'temp474_{self.rand}')
                    except:
                        pass

        def mf4(): # ex atoms
            time.sleep(0.1)
            nonlocal listbox
            nonlocal status
            temp = listbox.curselection()
            if temp != [ ]:
                nums = [ ]
                for i in temp:
                    if self.co.tool.fsinfof( self.comp[i] )[1] != 0:
                        nums.append( self.comp[i] )
                try:
                    if self.pnum != -1:
                        self.co.exatoms(nums, self.export, self.rand)
                        status.set('atoms 내보내기 성공')
                except Exception as e:
                    if str(e) == 'notvalidFPTR':
                        status.set('잘못된 파일 포인터')
                    elif str(e) == 'fpoperr':
                        status.set('파일 다운로드 과정 오류')
                    elif str(e) == 'decrypterr':
                        status.set('잘못된 키 데이터')
                    elif str(e) == 'unziperr':
                        status.set('KZIP 언패킹 과정 오류')
                    else:
                        status.set(f'critical error : {e}')
                try:
                    shutil.rmtree(f'temp474_{self.rand}')
                except:
                    pass

        def mf5(): # ex struct
            time.sleep(0.1)
            nonlocal status
            nonlocal win
            nonlocal listbox
            tgt = self.comp[ listbox.curselection()[0] ]
            temp = self.co.tool.fsinfow(tgt)
            if temp[1] == 0:
                try:
                    self.exfull(tgt, self.export.replace('\\', '/') + f'/{temp[2]}', status, win)
                    status.set('전체 struct 내보내기 성공')
                except Exception as e:
                    if str(e) == 'notvalidFPTR':
                        status.set('잘못된 파일 포인터')
                    elif str(e) == 'fpoperr':
                        status.set('파일 다운로드 과정 오류')
                    elif str(e) == 'decrypterr':
                        status.set('잘못된 키 데이터')
                    elif str(e) == 'unziperr':
                        status.set('KZIP 언패킹 과정 오류')
                    else:
                        status.set(f'critical error : {e}')
                try:
                    shutil.rmtree(f'temp474_{self.rand}')
                except:
                    pass

        def mf6(): # new struct
            time.sleep(0.1)
            nonlocal listbox
            nonlocal status
            num = -1
            fin = True
            while fin:
                fin = False
                num = num + 1
                for i in self.comp:
                    if f'NewStruct{num}' in self.co.tool.fsinfow(i)[2]:
                        fin = True
            if self.pnum != -1:
                try:
                    self.co.newfolder(self.pnum, f'NewStruct{num}')
                    status.set('새로운 struct 만들기 성공')
                    self.comp = self.co.getlower(self.pnum)
                    func3()
                except Exception as e:
                    if str(e) == 'hpusherror':
                        status.set('헤더 업데이트 과정 오류')
                    else:
                        status.set(f'critical error : {e}')

        def mf7(): # move
            time.sleep(0.1)
            nonlocal listbox
            nonlocal current
            nonlocal status
            nonlocal win
            movpnum = -1 # move tgt num (-1 주의)
            movcomp = [ ] # move component [int]
            tgt = listbox.curselection()[0] # move 대상
            
            if self.pnum != -1:
                
                movwin = tkinter.Toplevel(win)
                movwin.title('Move')
                movwin.geometry("300x300+100+50")
                movwin.resizable(False, False)

                def movshow(): # listbox show
                    nonlocal movlistbox
                    nonlocal movlast
                    nonlocal movcomp
                    movlast = -1
                    movlistbox.delete( 0, movlistbox.size() )
                    tname = [ ]
                    tcomp = [ ]
                    for i in movcomp:
                        info = self.co.tool.fsinfow(i) # 깊이, 종류, 이름, 포인터
                        if info[1] == 0:
                            tname.append( info[2] + '/' )
                            tcomp.append(i)
                    movcomp = tcomp
                    for i in range( 0, len(movcomp) ):
                        temp = tname[i]
                        if self.structinfo:
                            info = self.co.info( movcomp[i] )
                            if self.actualsize:
                                temp = temp + f'    /크기 {info[2]}{self.sizeconv(info[2])}'
                            else:
                                temp = temp + f'    /크기 {self.sizeconv(info[2])}'
                        movlistbox.insert(movlistbox.size(), temp)

                def movf():
                    time.sleep(0.1)
                    nonlocal movpnum
                    nonlocal movcomp
                    nonlocal movcurrent
                    if movcurrent.get() != 'root':
                        info = self.co.tool.fsinfof(movpnum)
                        if info[0] == 0:
                            movpnum = -1
                            movcomp = [ self.co.getnum('bin/'), self.co.getnum('main/') ]
                            movcurrent.set('root')
                        else:
                            movpnum = self.co.getupper(movpnum)
                            movcomp = self.co.getlower(movpnum)
                            temp = movcurrent.get()[0:-1]
                            movcurrent.set( temp[0:temp.rfind('/') + 1] )
                        movshow()
                
                movbut = tkinter.Button(movwin, text = ' < ', font = ("Consolas", 14), command = movf)
                movbut.place(x = 5, y = 5)
                movcurrent = tkinter.StringVar() # 현재 스트럭트 문자열 표시
                movcurrent.set('root')
                movcurshow = tkinter.Entry(movwin, font = ("맑은 고딕", 18), width=14, textvariable = movcurrent, state = 'readonly')
                movcurshow.place(x = 57, y = 7)

                def gof():
                    time.sleep(0.1)
                    nonlocal movpnum
                    nonlocal movwin
                    if movpnum != -1:
                        
                        temp = tgt
                        name = self.co.tool.fsinfow( self.comp[temp] )[2] # 대상 이름
                        flag = True # 중복 통과 여부
                        for i in self.co.getlower(movpnum):
                            if name == self.co.tool.fsinfow(i)[2]:
                                flag = False
                        if flag:
                            try:
                                self.co.move(self.comp[temp], movpnum)
                                self.pnum = self.co.getnum( current.get() )
                                self.comp = self.co.getlower(self.pnum)
                                status.set('단일 대상 이동 성공')
                                func3()
                            except Exception as e:
                                if str(e) == 'notvalidDST':
                                    status.set('목적 경로와 이동 대상 겹침')
                                elif str(e) == 'hpusherr':
                                    status.set('헤더 업데이트 과정 오류')
                                else:
                                    status.set(f'critical error : {e}')
                        else:
                            status.set(f'movpnum : {movpnum}, 이름 중복 존재 : {name}')
                    
                        movwin.destroy()
                gobut = tkinter.Button(movwin, text = ' * ', font = ("Consolas", 14), command = gof)
                gobut.place(x = 250, y = 5)

                movframe = tkinter.Frame(movwin)
                movframe.place(x=5,y=55)
                movlistbox = tkinter.Listbox( movframe, width=27,  height=10, font = ("Consolas", 14) )
                movlistbox.pack(side="left", fill="y") # listbox
                movscrollbar0 = tkinter.Scrollbar(movframe, orient="vertical")
                movscrollbar0.config(command = movlistbox.yview)
                movscrollbar0.pack(side="right", fill="y")
                movlistbox.config(yscrollcommand = movscrollbar0.set)

                movlast = -1 # last click
                movcomp.append( self.co.getnum('bin/') )
                movcomp.append( self.co.getnum('main/') )
                movshow()
                def movclick(event):
                    time.sleep(0.1)
                    nonlocal movlistbox
                    nonlocal movpnum
                    nonlocal movcomp
                    nonlocal movlast
                    nonlocal movcurrent
                    temp = movlistbox.curselection()
                    if len(temp) == 1:
                        if movlast == temp[0]:
                            info = self.co.tool.fsinfow( movcomp[movlast] )
                            movpnum = movcomp[movlast]
                            movcomp = self.co.getlower(movpnum)
                            if movcurrent.get() == 'root':
                                movcurrent.set(info[2] + '/')
                            else:
                                movcurrent.set(movcurrent.get() + info[2] + '/')
                            movshow()
                        else:
                            movlast = temp[0]
                movlistbox.bind('<ButtonRelease-1>', movclick)
                
                movbut.mainloop()

        def mf8(): # move to bin
            time.sleep(0.1)
            nonlocal status
            nonlocal listbox
            nonlocal current
            if self.pnum != -1:
                tgt = self.comp[ listbox.curselection()[0] ] # 삭제 대상
                name = self.co.tool.fsinfow(tgt)[2]
                flag = True
                binnum = self.co.getnum('bin/')
                for i in self.co.getlower(binnum):
                    if name in self.co.tool.fsinfow(i)[2]:
                        flag = False
                if flag:
                    try:
                        self.co.move(tgt, binnum)
                        self.pnum = self.co.getnum( current.get() )
                        self.comp = self.co.getlower(self.pnum)
                        status.set('단일 대상 휴지통으로 이동됨')
                        func3()
                    except Exception as e:
                        if str(e) == 'notvalidDST':
                            status.set('목적 경로와 이동 대상 겹침')
                        elif str(e) == 'hpusherr':
                            status.set('헤더 업데이트 과정 오류')
                        else:
                            status.set(f'critical error : {e}')
                else:
                    status.set(f'bin/ pnum : {binnum}, 이름 중복 존재 : {name}')

        def mf9(): # rename
            time.sleep(0.1)
            nonlocal status
            nonlocal listbox
            nonlocal win
            tgt = listbox.curselection()[0] # move 대상
            
            if self.pnum != -1:
                nmwin = tkinter.Toplevel(win)
                nmwin.title('Rename')
                nmwin.geometry("300x300+100+50")
                nmwin.resizable(False, False)

                temp = '이름 생성 제한 경고 :\n윈도우에서는 다음 특수문자를 사용할\n수 없습니다. \\ / : * ? " < > |\n'
                temp = temp + '리눅스에서는 다음 특수문자 사용\n시 문제를 일으킬 수 있습니다. \\ / -\n'
                temp = temp + 'KVault4에서는 / 을 제외한 특수문자를\n사용할 수 있으나, 외부 입출력 시\n호환성을 고려해야 합니다.'
                nmlabel = tkinter.Label(nmwin, font = ("맑은 고딕", 12), text = temp)
                nmlabel.place(x = 5, y = 120)

                oldname = tkinter.StringVar()
                oldname.set( self.co.tool.fsinfow( self.comp[tgt] )[2] )
                nmshow = tkinter.Entry(nmwin, font = ("맑은 고딕", 18), width=22, textvariable = oldname, state = 'readonly')
                nmshow.place(x = 5, y = 5)

                def nmf():
                    time.sleep(0.1)
                    nonlocal status
                    nonlocal nmin
                    nonlocal nmwin
                    newname = nmin.get()
                    reflag = True
                    for i in self.comp:
                        if newname == self.co.tool.fsinfow(i)[2]:
                            reflag = False
                    if reflag:
                        if ('/' not in newname) and (newname != ''):
                            forbid = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
                            flag = False
                            for i in forbid:
                                if i in newname:
                                    flag = True
                            if flag:
                                nmflag = tkinter.messagebox.askokcancel(title="위험한 이름 경고", message=" 윈도우와 호환되지 않는 특수문자가 포함된 이름입니다. 정말 이대로 진행하시겠습니까? ")
                            else:
                                nmflag = True
                            if nmflag:
                                nmwin.destroy()
                                try:
                                    self.co.rename(self.comp[tgt], newname)
                                    self.comp = self.co.getlower(self.pnum)
                                    status.set('새 이름으로 변경됨')
                                    func3()
                                except Exception as e:
                                    if str(e) == 'hpusherr':
                                        status.set('헤더 업데이트 과정 오류')
                                    else:
                                        status.set(f'critical error : {e}')
                nmbut = tkinter.Button(nmwin, text = ' * ', font = ("Consolas", 14), command = nmf)
                nmbut.place(x = 5, y = 45)
                nmin = tkinter.Entry(nmwin, font = ("맑은 고딕", 18), width=18)
                nmin.place(x = 55, y = 47)

                nmwin.mainloop()

        def mf10(): # name sort
            time.sleep(0.1)
            nonlocal status
            try:
                if self.pnum != -1:
                    self.co.namesort(self.pnum)
                    self.comp = self.co.getlower(self.pnum)
                    status.set('현재 struct의 항목이 이름순 정렬됨')
                    func3()
            except Exception as e:
                if str(e) == 'nosort':
                    status.set('정렬될 필요 없는 struct')
                elif str(e) == 'hpusherr':
                    status.set('헤더 업데이트 과정 오류')
                else:
                    status.set(f'critical error : {e}')

        def mf11(): # bin delete
            time.sleep(0.1)
            nonlocal current
            nonlocal status
            nonlocal listbox
            tgt = self.comp[ listbox.curselection()[0] ]
            if current.get() == 'bin/':
                try:
                    self.co.delete(tgt)
                    self.comp = self.co.getlower(self.pnum)
                    status.set('선택한 단일 항목이 영구 삭제됨')
                    func3()
                except Exception as e:
                    if str(e) == 'hpusherr':
                        status.set('헤더 업데이트 과정 오류')
                    else:
                        status.set(f'critical error : {e}')

        def mf12(): # info
            time.sleep(0.1)
            nonlocal status
            nonlocal listbox
            nonlocal current
            temp = self.comp[ listbox.curselection()[0] ]
            try:
                info0 = self.co.tool.fsinfow(temp)
                info1 = self.co.info(temp)
                if info0[1] == 0:
                    if current.get() == 'root':
                        a = f'{info0[2]}/'
                    else:
                        a = f'{current.get()}{info0[2]}/'
                    b = f' 깊이 : {info0[0]}, 종류 : struct(#) \n'
                    b = b + f' offset num : {temp}, fs offset : {self.co.tool.offset[temp]} \n'
                    b = b + f' 하위 폴더 : {info1[0]}, 하위 파일 : {info1[1]} \n'
                    if self.actualsize:
                        b = b + f' 크기 : {info1[2]}{self.sizeconv(info1[2])} '
                    else:
                        b = b + f' 크기 : {self.sizeconv(info1[2])} '
                else:
                    a = f'{current.get()}{info0[2]}'
                    if info0[1] == 1:
                        b = f' 깊이 : {info0[0]}, 종류 : atom.sol($) \n'
                    else:
                        b = f' 깊이 : {info0[0]}, 종류 : atom.zip(&), offset num : {temp}, fs offset : {self.co.tool.offset[temp]} \n'
                    if self.actualsize:
                        b = b + f' 크기 : {info1[2]}{self.sizeconv(info1[2])}, 생성 : {info1[3]} \n 수정 : {info1[4]}, 엑세스 : {info1[5]} \n'
                    else:
                        b = b + f' 크기 : {self.sizeconv(info1[2])}, 생성 : {info1[3]}, 수정 : {info1[4]}, 엑세스 : {info1[5]} \n'
                    b = b + f' 물리 주소 : {info1[0]} \n fptr : {bytes.hex(info1[1])} \n file key : {bytes.hex(info1[6])} '
                status.set(f'정보 엑세스 성공')
                tkinter.messagebox.showinfo(title=a, message=b)
            except Exception as e:
                status.set(f'critical error : {e}')

        def mf13(): # pw reset
            time.sleep(0.1)
            nonlocal win
            nonlocal status
            pwwin = tkinter.Toplevel(win)
            pwwin.title('PWset')
            pwwin.geometry("300x300+100+50")
            pwwin.resizable(False, False)

            def pwselkey():
                time.sleep(0.1)
                nonlocal pwkey
                try:
                    temp = filedialog.askopenfile(title='파일 선택').name
                    pwkey.set(temp)
                except:
                    pwkey.set('기본키파일')
            pwkey = tkinter.StringVar() # keyfile path
            pwkey.set('기본키파일')
            pwkeybut = tkinter.Button(pwwin, text = '...', font = ("Consolas", 14), command = pwselkey)
            pwkeybut.place(x = 5, y = 5)
            pwkeyshow = tkinter.Entry(pwwin, font = ("맑은 고딕", 18), width=14, textvariable = pwkey, state = 'readonly')
            pwkeyshow.place(x = 57, y = 7)

            pwhintin = tkinter.Text(pwwin, font = ("맑은 고딕", 14), width=28,  height=6)
            pwhintin.place(x = 5, y = 55)
            pwin0 = tkinter.Entry(pwwin, font = ("맑은 고딕", 17), width=22, show = '●')
            pwin0.place(x = 5, y = 215)
            pwin1 = tkinter.Entry(pwwin, font = ("맑은 고딕", 17), width=22, show = '●')
            pwin1.place(x = 5, y = 255)

            def gof():
                time.sleep(0.1)
                nonlocal status
                nonlocal pwkey
                nonlocal pwhintin
                nonlocal pwin0
                nonlocal pwin1
                nonlocal pwwin
                pw0 = bytes(pwin0.get(), 'utf-8')
                pw1 = bytes(pwin1.get(), 'utf-8')
                hint = bytes(pwhintin.get('1.0', tkinter.END)[0:-1], 'utf-8')
                kfp = pwkey.get()
                if pw0 == pw1:
                    pwwin.destroy()
                    try:
                        self.co.pwset(pw0, kfp, hint)
                        if ('pwset' in self.co.debug) and ('success' in self.co.debug):
                            status.set('비밀번호 변경 성공')
                        else:
                            raise Exception('PWset Error Occurred')
                    except Exception as e:
                        status.set(f'critical error : {e}')
                else:
                    tkinter.messagebox.showinfo(title='비밀번호 불일치', message=' 비밀번호와 비밀번호 확인이 \n 불일치합니다. 다시 입력하세요. ')
            gobut = tkinter.Button(pwwin, text = ' * ', font = ("Consolas", 14), command = gof)
            gobut.place(x = 250, y = 5)

            pwwin.mainloop()

        def mf14(): # debug
            time.sleep(0.1)
            b = f' order : {self.co.order} \n debug : {self.co.debug} '
            if self.actualsize:
                b = b + f'\n fsl : {len(self.co.tool.fs)}{self.sizeconv(len(self.co.tool.fs))} '
                b = b + f'\n fkl : {len(self.co.tool.fk)}{self.sizeconv(len(self.co.tool.fk))} '
                b = b + f'\n offl : {len(self.co.tool.offset)}{self.sizeconv(len(self.co.tool.offset))} '
            else:
                b = b + f'\n fsl : {self.sizeconv(len(self.co.tool.fs))} \n fkl : {self.sizeconv(len(self.co.tool.fk))} \n offl : {self.sizeconv(len(self.co.tool.offset))} '
            tkinter.messagebox.showinfo(title='비밀번호 불일치', message=b)

        def mf15(): # clean
            time.sleep(0.1)
            nonlocal status
            try:
                temp = self.co.clean()
                status.set(f'del fk : {temp[0]}, del fptr : {temp[1]}, del fs : {temp[2]}')
            except Exception as e:
                if str(e) == 'hpusherr':
                    status.set('헤더 업데이트 과정 오류')
                else:
                    status.set(f'critical error : {e}')

        def mf16(): # settings
            time.sleep(0.1)
            nonlocal status
            try:
                os.startfile('settings.txt')
                status.set('디렉토리 내 세팅 파일 열림')
            except Exception as e:
                status.set(f'critical error : {e}')

        def mf17(): # help
            time.sleep(0.1)
            nonlocal status
            try:
                os.startfile('readme.txt')
                status.set('디렉토리 내 설명서 파일 열림')
            except Exception as e:
                status.set(f'critical error : {e}')

        mbar = tkinter.Menu(win) # 메뉴 바
        
        menu0 = tkinter.Menu(mbar, tearoff=0) # import
        menu0.add_command(label="Files", font = ("맑은 고딕", 14), command=mf1)
        menu0.add_command(label="Folder", font = ("맑은 고딕", 14), command=mf2)
        menu0.add_separator()
        menu0.add_command(label="Full Folder", font = ("맑은 고딕", 14), command=mf3)
        mbar.add_cascade(label="  Import  ", menu=menu0)
        
        menu1 = tkinter.Menu(mbar, tearoff=0) # export
        menu1.add_command(label="Atoms", font = ("맑은 고딕", 14), command=mf4)
        menu1.add_separator()
        menu1.add_command(label="Struct", font = ("맑은 고딕", 14), command=mf5)
        mbar.add_cascade(label="  Export  ", menu=menu1)

        menu2 = tkinter.Menu(mbar, tearoff=0) # file
        menu2.add_command(label="New Struct", font = ("맑은 고딕", 14), command=mf6)
        menu2.add_command(label="Move", font = ("맑은 고딕", 14), command=mf7)
        menu2.add_command(label="Recycle", font = ("맑은 고딕", 14), command=mf8)
        mbar.add_cascade(label="  Files  ", menu=menu2)

        menu3 = tkinter.Menu(mbar, tearoff=0) # action
        menu3.add_command(label="Rename", font = ("맑은 고딕", 14), command=mf9)
        menu3.add_command(label="Sort Name", font = ("맑은 고딕", 14), command=mf10)
        menu3.add_separator()
        menu3.add_command(label="Terminate", font = ("맑은 고딕", 14), command=mf11)
        mbar.add_cascade(label="  Action  ", menu=menu3)

        menu4 = tkinter.Menu(mbar, tearoff=0) # manage
        menu4.add_command(label="Info", font = ("맑은 고딕", 14), command=mf12)
        menu4.add_command(label="Reset PW", font = ("맑은 고딕", 14), command=mf13)
        menu4.add_command(label="Debug", font = ("맑은 고딕", 14), command=mf14)
        menu4.add_separator()
        menu4.add_command(label="Clean", font = ("맑은 고딕", 14), command=mf15)
        mbar.add_cascade(label="  Manage  ", menu=menu4)

        menu5 = tkinter.Menu(mbar, tearoff=0) # others
        menu5.add_command(label="Settings", font = ("맑은 고딕", 14), command=mf16)
        menu5.add_command(label="Help", font = ("맑은 고딕", 14), command=mf17)
        mbar.add_cascade(label="  Others  ", menu=menu5)
        
        win.config(menu=mbar)

        def func1(): # 상위 폴더로 이동
            time.sleep(0.1)
            nonlocal current
            nonlocal status
            if current.get() != 'root':
                info = self.co.tool.fsinfof(self.pnum)
                if info[0] == 0:
                    self.pnum = -1
                    self.comp = [ self.co.getnum('bin/'), self.co.getnum('main/') ]
                    current.set('root')
                    func3()
                    status.set('pnum : -1, depth : -1')
                else:
                    self.pnum = self.co.getupper(self.pnum)
                    self.comp = self.co.getlower(self.pnum)
                    temp = current.get()[0:-1]
                    current.set( temp[0:temp.rfind('/') + 1] )
                    func3()
                    status.set(f'pnum : {self.pnum}, depth : {info[0] - 1}')
        but1 = tkinter.Button(win, text = ' < ', font = ("Consolas", 14), command = func1)
        but1.place(x = 5, y = 5)
        current = tkinter.StringVar() # 현재 스트럭트 문자열 표시
        current.set('root')
        show1 = tkinter.Entry(win, font = ("맑은 고딕", 18), width=56, textvariable = current, state = 'readonly')
        show1.place(x = 63, y = 6)

        def func2(): # 검색
            time.sleep(0.1)
            nonlocal win
            nonlocal current
            schwin = tkinter.Toplevel(win)
            schwin.title('Search')
            schwin.geometry("300x300+100+50")
            schwin.resizable(False, False)
            schshow = tkinter.Entry(schwin, font = ("맑은 고딕", 18), width=22, textvariable = current, state = 'readonly')
            schshow.place(x = 5, y = 5) # 현재 검색 범위
            schin = tkinter.Entry(schwin, font = ("맑은 고딕", 18), width=18)
            schin.place(x = 55, y = 53) # 검색어 입력창
            def schfunc():
                time.sleep(0.1)
                nonlocal schlistbox
                nonlocal schin
                schlistbox.delete( 0, listbox.size() )
                if self.pnum == -1:
                    for i in self.co.search( self.comp[0], schin.get() ):
                        schlistbox.insert(listbox.size(), i)
                    for i in self.co.search( self.comp[1], schin.get() ):
                        schlistbox.insert(listbox.size(), i)
                else:
                    for i in self.co.search( self.pnum, schin.get() ):
                        schlistbox.insert(listbox.size(), i)
            schbut = tkinter.Button(schwin, text = ' ? ', font = ("Consolas", 14), command = schfunc)
            schbut.place(x = 5, y = 50)
            schframe = tkinter.Frame(schwin)
            schframe.place(x=5,y=100)
            schlistbox = tkinter.Listbox( schframe, width=27,  height=8, font = ("Consolas", 14) )
            schlistbox.pack(side="left", fill="y") # listbox
            schscrollbar0 = tkinter.Scrollbar(schframe, orient="vertical")
            schscrollbar0.config(command=schlistbox.yview)
            schscrollbar0.pack(side="right", fill="y")
            schlistbox.config(yscrollcommand=schscrollbar0.set)
            schwin.mainloop()
        but2 = tkinter.Button(win, text = ' ? ', font = ("Consolas", 14), command = func2)
        but2.place(x = 5, y = 555)

        def func3(): # listbox show
            nonlocal listbox
            nonlocal last
            last = -1
            listbox.delete( 0, listbox.size() )
            for i in range( 0, len(self.comp) ):
                info = self.co.tool.fsinfow( self.comp[i] ) # 깊이, 종류, 이름, 포인터
                if info[1] == 0:
                    temp = info[2] + '/'
                    info = self.co.info( self.comp[i] )
                    if self.structinfo:
                        if self.actualsize:
                            temp = temp + f'    /크기 {info[2]}{self.sizeconv(info[2])}'
                        else:
                            temp = temp + f'    /크기 {self.sizeconv(info[2])}'
                else:
                    temp = info[2]
                    info = self.co.info( self.comp[i] )
                    if self.atominfo:
                        if self.actualsize:
                            temp = temp + f'    /크기 {info[2]}{self.sizeconv(info[2])}'
                        else:
                            temp = temp + f'    /크기 {self.sizeconv(info[2])}'
                listbox.insert(listbox.size(), temp)
        
        status = tkinter.StringVar() # 상태 표시
        status.set('booting working')
        show3 = tkinter.Entry(win, font = ("맑은 고딕", 18), width=56, textvariable = status, state = 'readonly')
        show3.place(x = 63, y = 556)

        frame = tkinter.Frame(win)
        frame.place(x=5,y=55)
        listbox = tkinter.Listbox(frame, width=59,  height=15, font = ("맑은 고딕", 17), selectmode = 'extended')
        listbox.pack(side="left", fill="y") # listbox
        scrollbar0 = tkinter.Scrollbar(frame, orient="vertical")
        scrollbar0.config(command=listbox.yview)
        scrollbar0.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar0.set)

        self.comp.append( self.co.getnum('bin/') )
        self.comp.append( self.co.getnum('main/') )
        func3()
        status.set('booting complete')

        last = -1 # listbox 마지막 단일 선택
        def click(event):
            time.sleep(0.1)
            nonlocal listbox
            nonlocal last
            nonlocal current
            nonlocal status
            temp = listbox.curselection()
            if len(temp) == 1:
                if last == temp[0]:
                    info = self.co.tool.fsinfow( self.comp[last] )
                    if info[1] == 0:
                        self.pnum = self.comp[last]
                        self.comp = self.co.getlower(self.pnum)
                        if current.get() == 'root':
                            current.set(info[2] + '/')
                        else:
                            current.set(current.get() + info[2] + '/')
                        func3()
                        status.set(f'pnum : {self.pnum}, depth : {info[0]}')
                else:
                    last = temp[0]
        listbox.bind('<ButtonRelease-1>',click)

        win.mainloop()

def login():
    global k
    win = tkinter.Tk()
    win.title('KVault4')
    win.geometry("300x300+100+50")
    win.resizable(False, False)

    def selclu():
        time.sleep(0.1)
        nonlocal clu
        nonlocal hstr
        nonlocal flag
        try:
            temp = filedialog.askdirectory(title='폴더 선택')
            if temp != '':
                clu.set(temp)
                try:
                    k.set(temp)
                    hstr.set( str(k.co.view(), 'utf-8') )
                    flag = True
                except Exception as e:
                    flag = False
                    if str(e) == 'newCLU':
                        hstr.set('빈 폴더 선택\n새 클러스터 생성됨')
                    elif str(e) == 'notvalidCLU':
                        hstr.set('올바르지 않은\n클러스터 폴더\n다시 선택하세요')
                    elif str(e) == 'notvalidHEAD':
                        hstr.set('올바르지 않은\n클러스터 헤더\n다시 선택하세요')
                    else:
                        hstr.set(f'critical error\n{e}')
        except:
            flag = False
            clu.set('클러스터 선택되지 않음')
    clu = tkinter.StringVar() # cluster path
    clu.set('클러스터 선택되지 않음')
    clubut = tkinter.Button(win, text = 'CLU', font = ("맑은 고딕", 14), command = selclu)
    clubut.place(x = 10, y = 10)
    clushow = tkinter.Entry(win, font = ("맑은 고딕", 17), width=16, textvariable = clu, state = 'readonly')
    clushow.place(x = 70, y = 15)

    def selkey():
        time.sleep(0.1)
        nonlocal key
        try:
            temp = filedialog.askopenfile(title='파일 선택').name
            key.set(temp)
        except:
            key.set('기본키파일')
    key = tkinter.StringVar() # keyfile path
    key.set('기본키파일')
    keybut = tkinter.Button(win, text = 'KEY', font = ("맑은 고딕", 14), command = selkey)
    keybut.place(x = 10, y = 60)
    keyshow = tkinter.Entry(win, font = ("맑은 고딕", 17), width=16, textvariable = key, state = 'readonly')
    keyshow.place(x = 70, y = 65)

    def go():
        time.sleep(0.1)
        nonlocal goin
        nonlocal key
        nonlocal flag
        if flag:
            pw = bytes(goin.get(), 'utf-8')
            try:
                k.co.read( pw, key.get() )
                k.open = True
                nonlocal win
                win.destroy()
            except Exception as e:
                if str(e) == 'notvalidKEY':
                    tkinter.messagebox.showinfo('비밀번호 불일치', ' 비밀번호 또는 키 파일이 \n 올바르지 않습니다. \n 다시 시도하세요. ')
                else:
                    tkinter.messagebox.showinfo('critical error', f' {e} ')
    gobut = tkinter.Button(win, text = 'GO', font = ("맑은 고딕", 14), command = go)
    gobut.place(x = 245, y = 245)
    goin = tkinter.Entry(win, font = ("맑은 고딕", 17), width=17, show = '●')
    goin.place(x = 10, y = 250)
    flag = False # pw in flag

    hstr = tkinter.StringVar()
    hstr.set('-')
    hshow = tkinter.Label( win, font = ("맑은 고딕", 14), textvariable = hstr )
    hshow.place(x=10, y=110)

    win.mainloop()

if __name__ == '__main__':
    mp.freeze_support()
    k = console()
    login()
    if k.open:
        k.main()
    time.sleep(0.5)

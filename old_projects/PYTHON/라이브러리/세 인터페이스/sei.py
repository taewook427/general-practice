import time
import tkinter
import tkinter.font
import tkinter.messagebox
from tkinter import filedialog
import tkinter.ttk

class lite:
    def init(self,title): #창 제목, 리스트 생성
        win = tkinter.Tk()
        win.title(title)
        win.geometry("310x265+100+50")
        win.resizable(False, False)
        win.configure(bg='dim gray')
        font = tkinter.font.Font(family="맑은 고딕", size=10)
        win.update()

        frame = tkinter.Frame(win)
        frame.place(x=5,y=5)

        listbox = tkinter.Listbox(
            frame, width=40,  height=10, font = font,
            bg='gray20', fg='lawn green', selectbackground='gray20', selectforeground='lawn green')
        listbox.pack(side="left", fill="y")

        scrollbar0 = tkinter.Scrollbar(frame, orient="vertical")
        scrollbar0.config(command=listbox.yview)
        scrollbar0.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar0.set)
        
        win.update()
        #self.num = 0
        
        return [win,listbox] #창, 리스트 반환

    def end(self,win): #창 닫기
        win.destroy()

    def hide(self,win): #창 숨기기
        win.withdraw()

    def show(self,win): #창 보이기
        win.deiconify()

    def msg(self,title,content,mode): # ask / info 알림창
        time.sleep(0.1)
        i = True
        if mode == 'ask':
            i = tkinter.messagebox.askokcancel(title,' '+content+' ')
        elif mode == 'info':
            tkinter.messagebox.showinfo(title,' '+content+' ')
            i = True
        return i #T/F

    def select(self,mode): #파일/폴더 선택
        out = [ ]
        ftype = (
            ('all files', '*.*'),('k files', '*.k'),('png files', '*.png'),('jpg files', '*.jpg'),
            ('webp files', '*.webp'),('txt files', '*.txt'),('mp4 files', '*.mp4'),('html files', '*.html')
            )
        if mode == 'file':
            file = filedialog.askopenfile(title='파일 선택',filetypes=ftype)
            out = file.name #파일명 문자열 하나
        elif mode == 'files':
            file = filedialog.askopenfiles(title='파일들 선택',filetypes=ftype)
            out = [ ]
            for i in file:
                out.append(i.name) #파일명 리스트
        elif mode == 'folder':
            file = filedialog.askdirectory(title='폴더 선택')
            out = file #폴더명 문자열 하나
        return out

    def print(self,win,listbox,data): #한 줄 출력 - \n 주의!
        temp = data.split('\n')
        for i in temp:
            listbox.insert( listbox.size(),i )
        listbox.see( listbox.size() )
        win.update()
        #self.num = self.num + 1

    def erase(self,win,listbox): #마지막 한 줄 지우기 - \n 주의!
        listbox.delete( listbox.size()-1,listbox.size() )
        win.update()
        #self.num = self.num - 1

    def input0(self,win): #한줄 일반 입력, 입력은 >>> 등으로 따로 출력
        def getdt():
            time.sleep(0.1)
            nonlocal in0
            nonlocal but0
            nonlocal temp
            temp.set( in0.get() )
            in0.destroy()
            but0.destroy()
            win.quit()
        
        font = tkinter.font.Font(family="맑은 고딕", size=10)
        in0 = tkinter.Entry(width=35, font = font, bg='gray20', fg='lawn green')
        in0.grid(column = 0 , row = 0)
        in0.place(x=5,y=195)
        win.update()

        temp = tkinter.StringVar()
        but0 = tkinter.Button(win, text = '입력', font = font, command = getdt, bg='gray50')
        but0.place(x = 265,y = 195)
        win.update()

        win.mainloop()
        return temp.get()

    def input1(self,win): #한줄 특수 입력
        def getdt():
            time.sleep(0.1)
            nonlocal in0
            nonlocal but0
            nonlocal temp
            temp.set( in0.get() )
            in0.destroy()
            but0.destroy()
            win.quit()
        
        font = tkinter.font.Font(family="맑은 고딕", size=10)
        in0 = tkinter.Entry(width=35, font = font, bg='gray20', fg='lawn green', show = '●')
        in0.grid(column = 0 , row = 0)
        in0.place(x=5,y=195)
        win.update()

        temp = tkinter.StringVar()
        but0 = tkinter.Button(win, text = '입력', font = font, command = getdt, bg='gray50')
        but0.place(x = 265,y = 195)
        win.update()

        win.mainloop()
        return temp.get()

    def input2(self,win): #여러줄 입력
        def getdt():
            time.sleep(0.1)
            nonlocal in0
            nonlocal but0
            nonlocal temp
            temp.set( in0.get('1.0','end') )
            in0.destroy()
            but0.destroy()
            win.quit()
        
        font = tkinter.font.Font(family="맑은 고딕", size=10)
        in0 = tkinter.Text(width=35, height=2, font = font, bg='gray20', fg='lawn green')
        in0.grid(column = 0 , row = 0)
        in0.place(x=5,y=195)
        win.update()

        temp = tkinter.StringVar()
        but0 = tkinter.Button(win, text = '입력', font = font, command = getdt, bg='gray50')
        but0.place(x = 265,y = 200)
        win.update()

        win.mainloop()
        return temp.get()[0:-1]

    def ask2(self,win): # 예 : '0' / 아니오 : '1'
        font = tkinter.font.Font(family="맑은 고딕", size=10)
        temp = tkinter.StringVar()

        def get0():
            time.sleep(0.1)
            nonlocal temp
            temp.set('0')
            win.quit()

        def get1():
            time.sleep(0.1)
            nonlocal temp
            temp.set('1')
            win.quit()

        but0 = tkinter.Button(win, text = '  예  ', font = font, command = get0, bg='gray50')
        but0.place(x = 5,y = 195)
        but1 = tkinter.Button(win, text = '아니오', font = font, command = get1, bg='gray50')
        but1.place(x = 65,y = 195)

        win.update()
        win.mainloop()
        but0.destroy()
        but1.destroy()
        return temp.get()

    def ask4(self,win): # A 0, B 1, C 2, D 3
        font = tkinter.font.Font(family="맑은 고딕", size=10)
        temp = tkinter.StringVar()

        def get0():
            time.sleep(0.1)
            nonlocal temp
            temp.set('0')
            win.quit()

        def get1():
            time.sleep(0.1)
            nonlocal temp
            temp.set('1')
            win.quit()

        def get2():
            time.sleep(0.1)
            nonlocal temp
            temp.set('2')
            win.quit()

        def get3():
            time.sleep(0.1)
            nonlocal temp
            temp.set('3')
            win.quit()

        but0 = tkinter.Button(win, text = '  A  ', font = font, command = get0, bg='gray50')
        but0.place(x = 5,y = 195)
        but1 = tkinter.Button(win, text = '  B  ', font = font, command = get1, bg='gray50')
        but1.place(x = 65,y = 195)
        but2 = tkinter.Button(win, text = '  C  ', font = font, command = get2, bg='gray50')
        but2.place(x = 125,y = 195)
        but3 = tkinter.Button(win, text = '  D  ', font = font, command = get3, bg='gray50')
        but3.place(x = 185,y = 195)

        win.update()
        win.mainloop()
        but0.destroy()
        but1.destroy()
        but2.destroy()
        but3.destroy()
        return temp.get()

    def ask5(self,win): # 1 : 0, 2 : 1, 3 : 2, 4 : 3, 5 : 4
        font = tkinter.font.Font(family="맑은 고딕", size=10)
        temp = tkinter.StringVar()

        def get0():
            time.sleep(0.1)
            nonlocal temp
            temp.set('0')
            win.quit()

        def get1():
            time.sleep(0.1)
            nonlocal temp
            temp.set('1')
            win.quit()

        def get2():
            time.sleep(0.1)
            nonlocal temp
            temp.set('2')
            win.quit()

        def get3():
            time.sleep(0.1)
            nonlocal temp
            temp.set('3')
            win.quit()

        def get4():
            time.sleep(0.1)
            nonlocal temp
            temp.set('4')
            win.quit()

        but0 = tkinter.Button(win, text = '  1  ', font = font, command = get0, bg='gray50')
        but0.place(x = 5,y = 195)
        but1 = tkinter.Button(win, text = '  2  ', font = font, command = get1, bg='gray50')
        but1.place(x = 65,y = 195)
        but2 = tkinter.Button(win, text = '  3  ', font = font, command = get2, bg='gray50')
        but2.place(x = 125,y = 195)
        but3 = tkinter.Button(win, text = '  4  ', font = font, command = get3, bg='gray50')
        but3.place(x = 185,y = 195)
        but4 = tkinter.Button(win, text = '  5  ', font = font, command = get4, bg='gray50')
        but4.place(x = 245,y = 195)

        win.update()
        win.mainloop()
        but0.destroy()
        but1.destroy()
        but2.destroy()
        but3.destroy()
        but4.destroy()
        return temp.get()

    def getnum(self,win): # 최대 30자리 숫자, 출력은 문자열 형태
        font = tkinter.font.Font(family="맑은 고딕", size=10)
        temp = tkinter.StringVar()

        def get0():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '0' )

        def get1():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '1' )

        def get2():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '2' )

        def get3():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '3' )

        def get4():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '4' )

        def get5():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '5' )

        def get6():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '6' )

        def get7():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '7' )

        def get8():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '8' )

        def get9():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '9' )

        def gete():
            time.sleep(0.03)
            nonlocal temp
            t = temp.get()
            if t != '':
                temp.set( t[0:-1] )

        def getp():
            time.sleep(0.1)
            win.quit()

        def getc():
            time.sleep(0.1)
            temp.set('')

        but0 = tkinter.Button(win, text = '0', font = font, command = get0, bg='gray50')
        but0.place(x = 5,y = 225)

        but1 = tkinter.Button(win, text = '1', font = font, command = get1, bg='gray50')
        but1.place(x = 25,y = 225)

        but2 = tkinter.Button(win, text = '2', font = font, command = get2, bg='gray50')
        but2.place(x = 45,y = 225)

        but3 = tkinter.Button(win, text = '3', font = font, command = get3, bg='gray50')
        but3.place(x = 65,y = 225)

        but4 = tkinter.Button(win, text = '4', font = font, command = get4, bg='gray50')
        but4.place(x = 85,y = 225)

        but5 = tkinter.Button(win, text = '5', font = font, command = get5, bg='gray50')
        but5.place(x = 105,y = 225)

        but6 = tkinter.Button(win, text = '6', font = font, command = get6, bg='gray50')
        but6.place(x = 125,y = 225)

        but7 = tkinter.Button(win, text = '7', font = font, command = get7, bg='gray50')
        but7.place(x = 145,y = 225)

        but8 = tkinter.Button(win, text = '8', font = font, command = get8, bg='gray50')
        but8.place(x = 165,y = 225)

        but9 = tkinter.Button(win, text = '9', font = font, command = get9, bg='gray50')
        but9.place(x = 185,y = 225)

        bute = tkinter.Button(win, text = '←', font = font, command = gete, bg='gray50')
        bute.place(x = 220,y = 225)

        butp = tkinter.Button(win, text = '✔', font = font, command = getp, bg='gray50')
        butp.place(x = 250,y = 225)

        butc = tkinter.Button(win, text = 'C', font = font, command = getc, bg='gray50')
        butc.place(x = 280,y = 225)

        label0 = tkinter.Label(win, textvariable=temp, font = tkinter.font.Font(family="맑은 고딕", size=14), bg='dim gray', fg='yellow green')
        label0.place(x = 3,y = 190)

        win.update()
        win.mainloop()
        but0.destroy()
        but1.destroy()
        but2.destroy()
        but3.destroy()
        but4.destroy()
        but5.destroy()
        but6.destroy()
        but7.destroy()
        but8.destroy()
        but9.destroy()
        bute.destroy()
        butp.destroy()
        butc.destroy()
        label0.destroy()
        return temp.get()

class standard: #표준 크기

    def init(self,title): #창 제목, 리스트 생성
        win = tkinter.Tk()
        win.title(title)
        win.geometry("805x655+150+100")
        win.resizable(False, False)
        win.configure(bg='gray20')
        font = tkinter.font.Font(family="맑은 고딕", size=14)
        win.update()

        frame = tkinter.Frame(win)
        frame.place(x=15,y=10)

        listbox = tkinter.Listbox(frame, width=75,  height=20, font = font,
                                  bg='midnight blue', fg='gold', selectbackground='midnight blue', selectforeground='gold')
        listbox.pack(side="left", fill="y")

        scrollbar0 = tkinter.Scrollbar(frame, orient="vertical")
        scrollbar0.config(command=listbox.yview)
        scrollbar0.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar0.set)
        
        win.update()
        #self.num = 0
        
        return [win,listbox] #창, 리스트 반환

    def end(self,win): #창 닫기
        win.destroy()

    def hide(self,win): #창 숨기기
        win.withdraw()

    def show(self,win): #창 보이기
        win.deiconify()

    def msg(self,title,content,mode): # ask / info 알림창
        time.sleep(0.1)
        i = True
        if mode == 'ask':
            i = tkinter.messagebox.askokcancel(title,' '+content+' ')
        elif mode == 'info':
            tkinter.messagebox.showinfo(title,' '+content+' ')
            i = True
        return i #T/F

    def select(self,mode): #파일/폴더 선택
        out = [ ]
        ftype = (
            ('all files', '*.*'),('k files', '*.k'),('png files', '*.png'),('jpg files', '*.jpg'),
            ('webp files', '*.webp'),('txt files', '*.txt'),('mp4 files', '*.mp4'),('html files', '*.html')
            )
        if mode == 'file':
            file = filedialog.askopenfile(title='파일 선택',filetypes=ftype)
            out = file.name #파일명 문자열 하나
        elif mode == 'files':
            file = filedialog.askopenfiles(title='파일들 선택',filetypes=ftype)
            out = [ ]
            for i in file:
                out.append(i.name) #파일명 리스트
        elif mode == 'folder':
            file = filedialog.askdirectory(title='폴더 선택')
            out = file #폴더명 문자열 하나
        return out

    def print(self,win,listbox,data): #한 줄 출력 - \n 주의!
        temp = data.split('\n')
        for i in temp:
            listbox.insert( listbox.size(),i )
        listbox.see( listbox.size() )
        win.update()
        #self.num = self.num + 1

    def erase(self,win,listbox): #마지막 한 줄 지우기 - \n 주의!
        listbox.delete( listbox.size()-1,listbox.size() )
        win.update()
        #self.num = self.num - 1

    def input0(self,win): #한줄 일반 입력, 입력은 >>> 등으로 따로 출력
        def getdt():
            time.sleep(0.1)
            nonlocal in0
            nonlocal but0
            nonlocal temp
            temp.set( in0.get() )
            in0.destroy()
            but0.destroy()
            win.quit()
        
        font = tkinter.font.Font(family="맑은 고딕", size=14)
        in0 = tkinter.Entry(width=70, font = font, bg='midnight blue', fg='gold')
        in0.grid(column = 0 , row = 0)
        in0.place(x=15,y=550)
        win.update()

        temp = tkinter.StringVar()
        but0 = tkinter.Button(win, text = '입력', font = font, command = getdt, bg='gray50')
        but0.place(x = 729,y = 544)
        win.update()

        win.mainloop()
        return temp.get()

    def input1(self,win): #한줄 특수 입력
        def getdt():
            time.sleep(0.1)
            nonlocal in0
            nonlocal but0
            nonlocal temp
            temp.set( in0.get() )
            in0.destroy()
            but0.destroy()
            win.quit()
        
        font = tkinter.font.Font(family="맑은 고딕", size=14)
        in0 = tkinter.Entry(width=70, font = font, bg='midnight blue', fg='gold', show = '●')
        in0.grid(column = 0 , row = 0)
        in0.place(x=15,y=550)
        win.update()

        temp = tkinter.StringVar()
        but0 = tkinter.Button(win, text = '입력', font = font, command = getdt, bg='gray50')
        but0.place(x = 729,y = 544)
        win.update()

        win.mainloop()
        return temp.get()

    def input2(self,win): #여러줄 입력
        def getdt():
            time.sleep(0.1)
            nonlocal in0
            nonlocal but0
            nonlocal temp
            temp.set( in0.get('1.0','end') )
            in0.destroy()
            but0.destroy()
            win.quit()
        
        font = tkinter.font.Font(family="맑은 고딕", size=14)
        in0 = tkinter.Text(width=70, height=3, font = font, bg='midnight blue', fg='gold')
        in0.grid(column = 0 , row = 0)
        in0.place(x=15,y=550)
        win.update()

        temp = tkinter.StringVar()
        but0 = tkinter.Button(win, text = '입력', font = font, command = getdt, bg='gray50')
        but0.place(x = 729,y = 544)
        win.update()

        win.mainloop()
        return temp.get()[0:-1]

    def ask2(self,win): # 예 : '0' / 아니오 : '1'
        font = tkinter.font.Font(family="맑은 고딕", size=14)
        temp = tkinter.StringVar()

        def get0():
            time.sleep(0.1)
            nonlocal temp
            temp.set('0')
            win.quit()

        def get1():
            time.sleep(0.1)
            nonlocal temp
            temp.set('1')
            win.quit()

        but0 = tkinter.Button(win, text = '  예  ', font = font, command = get0, bg='gray50')
        but0.place(x = 20,y = 560)
        but1 = tkinter.Button(win, text = '아니오', font = font, command = get1, bg='gray50')
        but1.place(x = 120,y = 560)

        win.update()
        win.mainloop()
        but0.destroy()
        but1.destroy()
        return temp.get()

    def ask4(self,win): # A 0, B 1, C 2, D 3
        font = tkinter.font.Font(family="맑은 고딕", size=14)
        temp = tkinter.StringVar()

        def get0():
            time.sleep(0.1)
            nonlocal temp
            temp.set('0')
            win.quit()

        def get1():
            time.sleep(0.1)
            nonlocal temp
            temp.set('1')
            win.quit()

        def get2():
            time.sleep(0.1)
            nonlocal temp
            temp.set('2')
            win.quit()

        def get3():
            time.sleep(0.1)
            nonlocal temp
            temp.set('3')
            win.quit()

        but0 = tkinter.Button(win, text = '  A  ', font = font, command = get0, bg='gray50')
        but0.place(x = 20,y = 560)
        but1 = tkinter.Button(win, text = '  B  ', font = font, command = get1, bg='gray50')
        but1.place(x = 120,y = 560)
        but2 = tkinter.Button(win, text = '  C  ', font = font, command = get2, bg='gray50')
        but2.place(x = 220,y = 560)
        but3 = tkinter.Button(win, text = '  D  ', font = font, command = get3, bg='gray50')
        but3.place(x = 320,y = 560)

        win.update()
        win.mainloop()
        but0.destroy()
        but1.destroy()
        but2.destroy()
        but3.destroy()
        return temp.get()

    def ask5(self,win): # 1 : 0, 2 : 1, 3 : 2, 4 : 3, 5 : 4
        font = tkinter.font.Font(family="맑은 고딕", size=14)
        temp = tkinter.StringVar()

        def get0():
            time.sleep(0.1)
            nonlocal temp
            temp.set('0')
            win.quit()

        def get1():
            time.sleep(0.1)
            nonlocal temp
            temp.set('1')
            win.quit()

        def get2():
            time.sleep(0.1)
            nonlocal temp
            temp.set('2')
            win.quit()

        def get3():
            time.sleep(0.1)
            nonlocal temp
            temp.set('3')
            win.quit()

        def get4():
            time.sleep(0.1)
            nonlocal temp
            temp.set('4')
            win.quit()

        but0 = tkinter.Button(win, text = '  1  ', font = font, command = get0, bg='gray50')
        but0.place(x = 20,y = 560)
        but1 = tkinter.Button(win, text = '  2  ', font = font, command = get1, bg='gray50')
        but1.place(x = 120,y = 560)
        but2 = tkinter.Button(win, text = '  3  ', font = font, command = get2, bg='gray50')
        but2.place(x = 220,y = 560)
        but3 = tkinter.Button(win, text = '  4  ', font = font, command = get3, bg='gray50')
        but3.place(x = 320,y = 560)
        but4 = tkinter.Button(win, text = '  5  ', font = font, command = get4, bg='gray50')
        but4.place(x = 420,y = 560)

        win.update()
        win.mainloop()
        but0.destroy()
        but1.destroy()
        but2.destroy()
        but3.destroy()
        but4.destroy()
        return temp.get()

    def getnum(self,win): # 최대 58자리 숫자, 출력은 문자열 형태
        font = tkinter.font.Font(family="맑은 고딕", size=14)
        temp = tkinter.StringVar()

        def get0():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '0' )

        def get1():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '1' )

        def get2():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '2' )

        def get3():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '3' )

        def get4():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '4' )

        def get5():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '5' )

        def get6():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '6' )

        def get7():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '7' )

        def get8():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '8' )

        def get9():
            time.sleep(0.03)
            nonlocal temp
            temp.set( temp.get() + '9' )

        def gete():
            time.sleep(0.03)
            nonlocal temp
            t = temp.get()
            if t != '':
                temp.set( t[0:-1] )

        def getp():
            time.sleep(0.1)
            win.quit()

        def getc():
            time.sleep(0.1)
            temp.set('')

        but0 = tkinter.Button(win, text = ' 0 ', font = font, command = get0, bg='gray50')
        but0.place(x = 20,y = 595)

        but1 = tkinter.Button(win, text = ' 1 ', font = font, command = get1, bg='gray50')
        but1.place(x = 80,y = 595)

        but2 = tkinter.Button(win, text = ' 2 ', font = font, command = get2, bg='gray50')
        but2.place(x = 140,y = 595)

        but3 = tkinter.Button(win, text = ' 3 ', font = font, command = get3, bg='gray50')
        but3.place(x = 200,y = 595)

        but4 = tkinter.Button(win, text = ' 4 ', font = font, command = get4, bg='gray50')
        but4.place(x = 260,y = 595)

        but5 = tkinter.Button(win, text = ' 5 ', font = font, command = get5, bg='gray50')
        but5.place(x = 320,y = 595)

        but6 = tkinter.Button(win, text = ' 6 ', font = font, command = get6, bg='gray50')
        but6.place(x = 380,y = 595)

        but7 = tkinter.Button(win, text = ' 7 ', font = font, command = get7, bg='gray50')
        but7.place(x = 440,y = 595)

        but8 = tkinter.Button(win, text = ' 8 ', font = font, command = get8, bg='gray50')
        but8.place(x = 500,y = 595)

        but9 = tkinter.Button(win, text = ' 9 ', font = font, command = get9, bg='gray50')
        but9.place(x = 560,y = 595)

        bute = tkinter.Button(win, text = ' ← ', font = font, command = gete, bg='gray50')
        bute.place(x = 620,y = 595)

        butp = tkinter.Button(win, text = '입력', font = font, command = getp, bg='gray50')
        butp.place(x = 683,y = 595)

        butc = tkinter.Button(win, text = ' C ', font = font, command = getc, bg='gray50')
        butc.place(x = 750,y = 595)

        label0 = tkinter.Label(win, textvariable=temp, font = tkinter.font.Font(family="맑은 고딕", size=18), bg='gray20', fg='yellow green')
        label0.place(x = 20,y = 540)

        win.update()
        win.mainloop()
        but0.destroy()
        but1.destroy()
        but2.destroy()
        but3.destroy()
        but4.destroy()
        but5.destroy()
        but6.destroy()
        but7.destroy()
        but8.destroy()
        but9.destroy()
        bute.destroy()
        butp.destroy()
        butc.destroy()
        label0.destroy()
        return temp.get()

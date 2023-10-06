import time
import tkinter
import tkinter.messagebox
import winsound

def gettime():
    cal = ['월요일','화요일','수요일','목요일','금요일','토요일','일요일']
    temp = time.time()
    now = time.localtime( temp )
    hour = int( time.strftime( '%H' , now ) )
    if hour >= 12:
        ap = '오후 '
    else:
        ap = '오전 '
    hour = hour % 12
    if hour == 0:
        hour = 12
    temp = str( temp - int(temp) )[2] #소숫점 첫째자리
    sec = ap + str(hour) + ':' + time.strftime( '%M:%S' , now ) + '.' + temp
    m = str( int( time.strftime( '%m' , now ) ) ) + '월 '
    d = str( int( time.strftime( '%d' , now ) ) ) + '일 '
    y = str( int( time.strftime( '%Y' , now ) ) ) + '년 '
    day = y + m + d + cal[now.tm_wday]
    return [sec,day] #시분초 / 날짜

def clock():
    win = tkinter.Tk()
    win.title("Argon")
    win.geometry("360x150+300+200")
    win.resizable(0,0)

    txt0 = tkinter.StringVar()
    txt0.set('오전 12:00:00.0')
    label0 = tkinter.Label(win, textvariable = txt0, font=("Consolas", 30))
    label0.place(x=5,y=5)

    txt1 = tkinter.StringVar()
    txt1.set('2022년 12월 31일 일요일')
    label1 = tkinter.Label(win, textvariable = txt1, font=("맑은 고딕", 15))
    label1.place(x=5,y=55)

    off = True
    def shutdown():
        nonlocal off
        off = False
        nonlocal win
        win.destroy()
    win.protocol('WM_DELETE_WINDOW', shutdown)
    win.update()

    def lock():
        time.sleep(0.05)
        nonlocal locked
        nonlocal but0
        nonlocal win
        if locked:
            locked = False
            but0.configure(bg='gray50')
            win.wm_attributes("-topmost", 0)
        else:
            locked = True
            but0.configure(bg='lawn green')
            win.wm_attributes("-topmost", 1)
    but0 = tkinter.Button(win, text = 'LOCK', font = ("맑은 고딕", 15), command = lock, bg = 'gray50')
    but0.place(x=5,y=95)
    locked = False

    def timerf():
        time.sleep(0.05)
        nonlocal off
        off = False
        nonlocal win
        win.destroy()
        timer()
    but1 = tkinter.Button(win, text = 'TIMER', font = ("맑은 고딕", 15), command = timerf, bg = 'gray50')
    but1.place(x=110,y=95)

    def stopf():
        time.sleep(0.05)
        nonlocal off
        off = False
        nonlocal win
        win.destroy()
        stop()
    but2 = tkinter.Button(win, text = 'STOPWATCH', font = ("맑은 고딕", 15), command = stopf, bg = 'gray50')
    but2.place(x=220,y=95)

    while off:
        time.sleep(0.03)
        temp = gettime()
        txt0.set(temp[0])
        txt1.set(temp[1])
        win.update()
    time.sleep(0.5)

###############

def count(txt0,win,but2): #카운트다운
    global off
    global started
    global timeleft
    temp = time.time() #작업 시작 시간
    while off and started:
        time.sleep(0.03)
        timepass = time.time() - temp #지나간 시간
        gone = timeleft - timepass #실질남은시간
        txt0.set( tpcom(gone) )
        win.update()
        if gone <= 0:
            started = False
            txt0.set( tpcom(0.0) )
            win.update()
            but2.configure(bg='deep sky blue', text = ' ♪ ')
            win.configure(bg='red')
            win.update()
            global sound
            if sound:
                winsound.Beep(500, 1500)
            else:
                time.sleep(1.5)
            win.configure(bg='gray95')
            but2.configure(bg='hot pink', text = ' ▶ ')
            win.update()
    temp = timeleft - timepass
    if temp < 0:
        temp = 0.0
    return temp #남은시간 0.0 #####소리 추가할것

def timer():
    win = tkinter.Tk()
    win.title("Argon")
    win.geometry("360x150+300+200")
    win.resizable(0,0)

    txt0 = tkinter.StringVar() #시간 출력
    txt0.set('00:10:00.0')
    label0 = tkinter.Label(win, textvariable = txt0, font=("Consolas", 30))
    label0.place(x=5,y=5)

    global off #창닫기 매소드
    off = True
    def shutdown():
        global off
        off = False
        nonlocal win
        win.destroy()
    win.protocol('WM_DELETE_WINDOW', shutdown)

    def lock(): #고정 매소드
        time.sleep(0.05)
        nonlocal locked
        nonlocal but0
        nonlocal win
        if locked:
            locked = False
            but0.configure(bg='gray50')
            win.wm_attributes("-topmost", 0)
        else:
            locked = True
            but0.configure(bg='lawn green')
            win.wm_attributes("-topmost", 1)
    but0 = tkinter.Button(win, text = 'LOCK', font = ("맑은 고딕", 15), command = lock, bg = 'gray50')
    but0.place(x=290,y=5)
    locked = False

    def soundf(): #소리 조절
        time.sleep(0.05)
        global sound
        nonlocal but1
        if sound:
            sound = False
            but1.configure(bg='gray50')
        else:
            sound = True
            but1.configure(bg='lawn green')
    but1 = tkinter.Button(win, text = ' ♪ ', font = ("맑은 고딕", 15), command = soundf, bg = 'lawn green')
    but1.place(x=180,y=75)
    global sound
    sound = True

    global started
    started = False
    def start(): #시작 버튼
        time.sleep(0.05)
        global started
        nonlocal but2
        nonlocal txt0
        nonlocal win
        if started: #동작 여부
            started = False
            but2.configure(bg='hot pink', text = ' ▶ ')
        else:
            started = True
            but2.configure(bg='gray50', text = ' | | ')
            global timeleft
            timeleft = count(txt0,win,but2)
            if timeleft == 0.0:
                setting()
    but2 = tkinter.Button(win, text = ' ▶ ', font = ("맑은 고딕", 15), command = start, bg = 'hot pink')
    but2.place(x=240,y=75)

    initvar = 0 #두번누르기 보조
    def init(): #초기화 버튼
        time.sleep(0.05)
        global started
        started = False
        nonlocal but2
        but2.configure(bg='hot pink', text = ' ▶ ')
        global timeleft
        setting()
        nonlocal txt0
        txt0.set( tpcom(timeleft) )
        win.update()
        nonlocal initvar
        nonlocal but3
        if initvar == 0: #처음 눌렀음
            but3.configure(bg='deep sky blue')
            initvar = 1
        else:
            but3.configure(bg='gray50')
            initvar = 0
    but3 = tkinter.Button(win, text = ' ■ ', font = ("맑은 고딕", 15), command = init, bg = 'gray50')
    but3.place(x=300,y=75)
    win.update()

    #시간 입력창
    label1 = tkinter.Label(win, text = '시 : ', font=("맑은 고딕", 15))
    label1.place(x=5,y=55)
    in1 = tkinter.Entry(width=5, font=("맑은 고딕", 14))
    in1.grid(column = 0 , row = 0)
    in1.place(x=55,y=55)
    label2= tkinter.Label(win, text = '분 : ', font=("맑은 고딕", 15))
    label2.place(x=5,y=85)
    in2 = tkinter.Entry(width=5, font=("맑은 고딕", 14))
    in2.grid(column = 0 , row = 0)
    in2.place(x=55,y=85)
    label3 = tkinter.Label(win, text = '초 : ', font=("맑은 고딕", 15))
    label3.place(x=5,y=115)
    in3 = tkinter.Entry(width=5, font=("맑은 고딕", 14))
    in3.grid(column = 0 , row = 0)
    in3.place(x=55,y=115)

    def setting(): #시간세팅 버튼
        time.sleep(0.05)
        nonlocal txt0
        global timeleft
        global started
        nonlocal in1
        nonlocal in2
        nonlocal in3
        if not started:
            try:
                if in1.get() == '':
                    h = 0
                else:
                    h = int( in1.get() )
                if in2.get() == '':
                    m = 0
                else:
                    m = int( in2.get() )
                if in3.get() == '':
                    s = 0
                else:
                    s = int( in3.get() )
                if (m >= 60) or (s >= 60):
                    tkinter.messagebox.askokcancel('잘못된 시간 설정',' 분과 초 설정은 60 미만의 정수만 가능합니다 ')
                else:
                    timeleft = float( 3600 * h + 60 * m + s )
                    txt0.set( tpcom(timeleft) )
                    win.update()
            except:
                tkinter.messagebox.askokcancel('잘못된 시간 설정',' 시, 분, 초 설정칸에는 정수만 입력해 주세요 ')
    but4 = tkinter.Button(win, text = ' ✔ ', font = ("맑은 고딕", 15), command = setting, bg = 'deep sky blue')
    but4.place(x=120,y=75)
    win.update()

    global timeleft #남은시간
    timeleft = 600.0 #기본 10분
    win.mainloop()
    time.sleep(0.5)

###############

def tpcom(timepass): # 0.1s 단위
    ti = int(timepass) #int
    tf = timepass - ti #float
    h = str(ti // 3600) #hour
    ti = ti % 3600
    m = str(ti // 60) #minute
    ti = ti % 60
    s = str(ti) #second
    ms = str( tf )[2] #소숫점 첫째자리
    if len(h) == 1:
        h = '0' + h
    if len(m) == 1:
        m = '0' + m
    if len(s) == 1:
        s = '0' + s
    return h + ':' + m + ':' + s + '.' + ms #공용 #####

def tpf(txt0,win,timetemp):
    global timepass
    global started
    temp = time.time()
    while off and started:
        time.sleep(0.03)
        timepass = time.time() - temp + timetemp #지나간 시간
        txt0.set( tpcom(timepass) )
        win.update()
    return timepass #센 시간 반환

def stop():
    win = tkinter.Tk()
    win.title("Argon")
    win.geometry("360x150+300+200")
    win.resizable(0,0)

    txt0 = tkinter.StringVar() #시간 출력
    txt0.set('00:00:00.0')
    label0 = tkinter.Label(win, textvariable = txt0, font=("Consolas", 30))
    label0.place(x=5,y=5)

    global off #창닫기 매소드
    off = True
    def shutdown():
        global off
        off = False
        nonlocal win
        win.destroy()
    win.protocol('WM_DELETE_WINDOW', shutdown)

    def lock(): #고정 매소드
        time.sleep(0.05)
        nonlocal locked
        nonlocal but0
        nonlocal win
        if locked:
            locked = False
            but0.configure(bg='gray50')
            win.wm_attributes("-topmost", 0)
        else:
            locked = True
            but0.configure(bg='lawn green')
            win.wm_attributes("-topmost", 1)
    but0 = tkinter.Button(win, text = 'LOCK', font = ("맑은 고딕", 15), command = lock, bg = 'gray50')
    but0.place(x=290,y=5)
    locked = False

    list0 = tkinter.Listbox(width=17,  height=3, font = ("맑은 고딕", 14))
    list0.place(x=5,y=60)
    list0.insert(1,'< 기록 >')

    def start(): #시작 버튼
        time.sleep(0.05)
        global started
        nonlocal but1
        nonlocal txt0
        nonlocal win
        global st2
        nonlocal timetemp
        if started:
            started = False
            but1.configure(bg='hot pink', text = ' ▶ ')
        else:
            started = True
            but1.configure(bg='gray50', text = ' | | ')
            timetemp = tpf(txt0,win,timetemp)
    but1 = tkinter.Button(win, text = ' ▶ ', font = ("맑은 고딕", 15), command = start, bg = 'hot pink')
    but1.place(x=190,y=75)
    global started
    started = False
    timetemp = 0.0 #지나간 시간 추가

    def log(): #기록 버튼
        time.sleep(0.005)
        nonlocal list0
        global timepass
        temp = list0.size()
        wr = '기록' + str(temp) + ' : ' + tpcom(timepass)
        list0.insert( temp,wr )
        list0.see( temp + 1 )
    but2 = tkinter.Button(win, text = ' ≡ ', font = ("맑은 고딕", 15), command = log, bg = 'gray50')
    but2.place(x=250,y=75)

    global timepass
    timepass = 0.0
    def init(): #초기화 버튼
        time.sleep(0.05)
        global timepass
        timepass = 0.0
        global started
        started = False
        nonlocal but1
        but1.configure(bg='hot pink', text = ' ▶ ')
        nonlocal list0
        nonlocal txt0
        nonlocal win
        list0.delete( 1,list0.size() )
        txt0.set( tpcom(0.0) )
        nonlocal timetemp
        timetemp = 0.0
        win.update()
    but3 = tkinter.Button(win, text = ' ■ ', font = ("맑은 고딕", 15), command = init, bg = 'gray50')
    but3.place(x=300,y=75)
    win.update()

    win.mainloop()
    time.sleep(0.5)

clock()

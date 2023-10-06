import tkinter
import tkinter.ttk
import time
import os

try:
    with open('temp400.txt','r',encoding='utf-8') as f:
        temp = f.readlines()
    os.remove('temp400.txt')
    mode = temp[0][0:-1]
    core = temp[1][0:-1]
    t = temp[2][0:-1]
    msg = temp[3][0:-1]

    if mode == 'kpng':
        path = 'temp270\\status.txt'
    elif mode == 'kaes':
        path = 'temp271\\status.txt'
    else:
        path = 'status.txt'

    win = tkinter.Tk()
    win.title('Event Viewer')
    win.geometry('300x200+500+400')
    win.resizable(0,0)

    label0 = tkinter.Label(win, text = 'Type : ' + mode, font = ('Consolas',14) )
    label0.place(x=10,y=10)
    label1 = tkinter.Label(win, text = 'Process Using : ' + core, font = ('Consolas',14) )
    label1.place(x=10,y=40)
    label2 = tkinter.Label(win, text = 'Start Time : ' + t, font = ('Consolas',14) )
    label2.place(x=10,y=70)
    label3 = tkinter.Label(win, text = 'Msg : ' + msg, font = ('Consolas',14) )
    label3.place(x=10,y=100)
    err = tkinter.StringVar()
    err.set('No Error Found')
    label4 = tkinter.Label(win, textvariable = err, font = ('Consolas',14) )
    label4.place(x=10,y=130)

    status = tkinter.DoubleVar() # 0 ~ 1000
    progress = tkinter.ttk.Progressbar(win,maximum=1000,variable = status,length=250)
    progress.place(x=25,y=165)

    end = True
    while end:
        time.sleep(0.127)
        try:
            with open(path,'r',encoding='utf-8') as f:
                a = int( f.readline()[0:-1] )
                b = int( f.readline()[0:-1] )
            if a == b:
                end = False
                status.set(1000)
                err.set('No Error Found')
            else:
                status.set( int(a/b*1000) )
        except Exception as e:
            err.set( str(e) )
        win.update()

    time.sleep(0.5)
    win.destroy()
    
except:
    time.sleep(0.1)

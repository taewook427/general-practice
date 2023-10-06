import time
import os

import tkinter
import tkinter.messagebox
import tkinter.ttk

import oreo

def main():
    with open('data350.txt','r',encoding='utf-8') as f:
        data = f.read()

    otool = oreo.toolbox()
    data = otool.readstr(data)
    num = data['data#num'] #항목 개수

    names = [ ]
    infos = [ ]
    orders = [ ]
    for i in range(0,num):
        names.append( data['data#'+str(i)+'#name'] )
        infos.append( data['data#'+str(i)+'#info'] )
        orders.append( data['data#'+str(i)+'#order'] )

    win = tkinter.Tk()
    win.title('KOS 2023')
    win.geometry("270x330+200+100")
    win.resizable(False, False)
    win.configure(bg='turquoise1')

    frame = tkinter.Frame(win)
    frame.place(x=10,y=10)
    listbox = tkinter.Listbox(
        frame, width=20,  height=10, font = ('Consolas', 15),
        bg='turquoise1', fg='RoyalBlue1', selectbackground='RoyalBlue1', selectforeground='turquoise1')
    listbox.pack(side="left", fill="y")
    scrollbar0 = tkinter.Scrollbar(frame, orient="vertical")
    scrollbar0.config(command=listbox.yview)
    scrollbar0.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar0.set)
    win.update()

    time.sleep(0.2)
    for i in names:
        listbox.insert( listbox.size(),i )
        time.sleep(0.05)
        win.update()

    status = tkinter.StringVar()
    status.set('====================\n쉽고 빠른 명령어 실행\n====================')
    label0 = tkinter.Label(win, textvariable = status, font = ('Consolas', 15), bg='turquoise1', fg='RoyalBlue1')
    label0.place(x=10,y=255)

    last = -1
    def click(event):
        time.sleep(0.1)
        nonlocal last
        nonlocal listbox
        temp = listbox.curselection()[0]
        if last == temp:
            time.sleep(0.1)
            nonlocal orders
            out = exe( orders[temp] )
            if '1' in out:
                tkinter.messagebox.showinfo('ERR 1',' '+out+' ')
        else:
            nonlocal infos
            last = temp
            nonlocal status
            status.set( infos[temp] )
        nonlocal win
        win.update()
    listbox.bind('<ButtonRelease-1>',click)

    win.mainloop()

def exe(orders):
    out = ''
    for i in orders:
        time.sleep(0.1)
        try:
            temp = os.system(i)
        except:
            temp = 1
        out = out + str(temp) + ' '
    return out

main()

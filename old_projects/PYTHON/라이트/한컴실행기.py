import time
import os

import tkinter
import tkinter.messagebox
import tkinter.ttk

with open('data346.txt','r',encoding='utf-8') as f:
    data = f.readlines()
data = [ i[0:-1] for i in data ]
name = [ ]
path = [ ]
for i in range( 0,len(data)//2 ):
    name.append( data[2*i] )
    path.append( data[2*i+1] )

win = tkinter.Tk()
win.title('한컴오피스 통합실행')
win.geometry("370x270+100+50")
win.resizable(False, False)
win.configure(bg='aquamarine')

frame = tkinter.Frame(win)
frame.place(x=10,y=10)
listbox = tkinter.Listbox(
    frame, width=30,  height=10, font = ('Consolas', 15),
    bg='aquamarine', fg='green4', selectbackground='green4', selectforeground='aquamarine')
listbox.pack(side="left", fill="y")
scrollbar0 = tkinter.Scrollbar(frame, orient="vertical")
scrollbar0.config(command=listbox.yview)
scrollbar0.pack(side="right", fill="y")
listbox.config(yscrollcommand=scrollbar0.set)
win.update()

time.sleep(0.5)
for i in name:
    listbox.insert( listbox.size(),i )
    win.update()
    time.sleep(0.1)

last = -1
def click(event):
    time.sleep(0.1)
    global name
    global path
    global listbox
    global last
    temp = listbox.curselection()[0]
    if last == temp:
        time.sleep(0.1)
        os.startfile( path[last] )
    else:
        last = temp
listbox.bind('<ButtonRelease-1>',click)

win.mainloop()
time.sleep(0.5)

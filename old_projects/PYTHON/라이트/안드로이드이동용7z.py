import py7zr
import zipfile
import os
import shutil
import random
import time
import tkinter
import tkinter.font
from tkinter import filedialog

def zip7z(pw, path): # new file : path
    with py7zr.SevenZipFile(path, 'w', password=pw) as archive:
        archive.writeall('temp446')

def unzip7z(name, pw):
    with py7zr.SevenZipFile(name, mode='r', password=pw) as archive:
        archive.extractall("temp446")

def unzip7z2(name, pw, path):
    with py7zr.SevenZipFile(name, mode='r', password=pw) as archive:
        archive.extractall(path)

def zipzip(name): # zip file name
    temp = zipfile.ZipFile('temp446/' + name, "w")
    names = os.listdir('./')
    res = ['andcom1realexe.exe', 'temp446', 'test446realexe.py']
    for i in res:
        if i in names:
            names.remove(i)
    for i in names:
        temp.write(i, compress_type=zipfile.ZIP_DEFLATED)
    temp.close() # 임시 압축파일 생성
    for i in names:
        os.remove(i)

def unzipzip(name, path): # path : unzip folder
    with zipfile.ZipFile(name, 'r') as zip_ref:
        zip_ref.extractall(path)

def init(names):
    try:
        shutil.rmtree('temp446')
    except:
        pass
    os.mkdir('temp446')
    for i in names:
        temp = i.replace('\\','/')
        new = temp[temp.rfind('/')+1:]
        shutil.copyfile(i, new) # 파일 복사

def init2(names):
    try:
        shutil.rmtree('temp446')
    except:
        pass
    os.mkdir('temp446')
    for i in names:
        temp = i.replace('\\','/')
        new = 'temp446/' + temp[temp.rfind('/')+1:]
        shutil.copyfile(i, new) # 파일 복사

def end(names): # 삭제 안할경우 names 빈 리스트
    try:
        shutil.rmtree('temp446')
    except:
        pass
    for i in names:
        os.remove(i)

def engine0(enfiles, defile, pw0, pw1, mode): # ERR 가능성
    out = "complete : "
    
    if enfiles != [ ]:
        if pw0 == pw1:
            init(enfiles)
            zipzip(str( random.randrange(1000,10000) ) + '.zip')
            temp = os.path.join(os.path.expanduser('~'),'Desktop') + '/' + str( random.randrange(1000,10000) ) + '.7z'
            zip7z(pw0, temp)
            if mode:
                end(enfiles)
            else:
                end( [ ] )
            out = out + temp
            
        else:
            out = out + "PW Not Match"
        
    elif defile != "":
        init( [ ] )
        unzip7z(defile, pw0)
        ft = os.listdir('temp446')
        if ft == ['temp446']:
            ft = os.listdir('temp446/temp446')
            zipname = ft[0]
            shutil.move('temp446/temp446/' + zipname, zipname)
        else:
            zipname = ft[0]
            shutil.move('temp446/' + zipname, zipname)

        temp = os.path.join(os.path.expanduser('~'),'Desktop') + '/' + str( random.randrange(1000,10000) )
        os.mkdir(temp)
        unzipzip(zipname, temp)
        os.remove(zipname)

        if mode:
            end( [defile] )
        else:
            end( [ ] )
        out = out + temp
        
    else:
        out = out + "Nothing"

    return out

def engine1(enfiles, defile, pw0, pw1, mode): # ERR 가능성
    out = "complete : "
    
    if enfiles != [ ]:
        if pw0 == pw1:
            init2(enfiles)
            temp = os.path.join(os.path.expanduser('~'),'Desktop') + '/' + str( random.randrange(1000,10000) ) + '.7z'
            zip7z(pw0, temp)
            if mode:
                end(enfiles)
            else:
                end( [ ] )
            out = out + temp
            
        else:
            out = out + "PW Not Match"
        
    elif defile != "":
        init2( [ ] )
        temp = os.path.join(os.path.expanduser('~'),'Desktop') + '/' + str( random.randrange(1000,10000) )
        os.mkdir(temp)
        unzip7z2(defile, pw0, temp)

        if mode:
            end( [defile] )
        else:
            end( [ ] )
        out = out + temp
        
    else:
        out = out + "Nothing"

    return out

def main():
    win = tkinter.Tk()
    win.title('test446')
    win.geometry("450x350+100+50")
    win.resizable(False, False)

    enfiles = [ ]
    defile = ""
    del0 = False
    del1 = False
    status = tkinter.StringVar()

    def func0():
        time.sleep(0.1)
        file = filedialog.askopenfiles(title='파일들 선택')
        nonlocal enfiles
        enfiles = [ ]
        for i in file:
            enfiles.append(i.name) #파일명 리스트
        nonlocal defile
        defile = ""
        nonlocal ens
        if enfiles != [ ]:
            ens.set(f'({len(enfiles)}) {enfiles[0]}')
        else:
            ens.set("(0) - ")
        nonlocal des
        des.set("(0) - ")
        nonlocal win
        win.update()
        
    but0 = tkinter.Button(win, text = 'EN', font = ("Consolas", 20), command = func0)
    but0.place(x = 5,y = 5)
    ens = tkinter.StringVar()
    ens.set("(0) - ")
    lbl0 = tkinter.Label( win, textvariable = ens, font = ("Consolas", 16) )
    lbl0.place(x = 60, y = 15)

    def func1():
        time.sleep(0.1)
        file = filedialog.askopenfile( title='파일 선택', filetypes = ( ('7z files', '*.7z'), ('all files', '*.*') ) )
        nonlocal defile
        try:
            defile = file.name
        except:
            defile = ""
        nonlocal enfiles
        enfiles = [ ]
        nonlocal ens
        ens.set("(0) - ")
        nonlocal des
        if defile != "":
            des.set(f"(1) {defile}")
        else:
            des.set("(0) - ")
        nonlocal win
        win.update()
        
    but1 = tkinter.Button(win, text = 'DE', font = ("Consolas", 20), command = func1)
    but1.place(x = 5,y = 65)
    des = tkinter.StringVar()
    des.set("(0) - ")
    lbl1 = tkinter.Label( win, textvariable = des, font = ("Consolas", 16) )
    lbl1.place(x = 60, y = 75)

    lbl5 = tkinter.Label( win, text = "pw", font = ("Consolas", 16) )
    lbl5.place(x = 5, y = 140)
    in1 = tkinter.Entry( width=28, font = ("Consolas", 16), show = '●' )
    in1.grid(column = 0 , row = 0)
    in1.place(x=80, y=140)
    lbl6 = tkinter.Label( win, text = "pw", font = ("Consolas", 16) )
    lbl6.place(x = 5, y = 175)
    in2 = tkinter.Entry( width=28, font = ("Consolas", 16), show = '●' )
    in2.grid(column = 0 , row = 0)
    in2.place(x=80, y=175)

    def chk0():
        time.sleep(0.1)
        nonlocal del0
        nonlocal chkv0
        if chkv0.get() == 0:
            del0 = False
        else:
            del0 = True
        nonlocal win
        win.update()
    chkv0 = tkinter.IntVar()
    chkb0 = tkinter.Checkbutton(win, text = "원본 삭제", font = ("Consolas", 16), variable = chkv0, command = chk0)
    chkb0.place(x = 5, y = 230)

    def chk1():
        time.sleep(0.1)
        nonlocal del1
        nonlocal chkv1
        if chkv1.get() == 1:
            del1 = True
        else:
            del1 = False
        nonlocal win
        win.update()
    chkv1 = tkinter.IntVar()
    chkb1 = tkinter.Checkbutton(win, text = "7z 형식만", font = ("Consolas", 16), variable = chkv1, command = chk1)
    chkb1.place(x = 140, y = 230)

    def gogo():
        nonlocal win
        nonlocal enfiles
        nonlocal defile
        nonlocal in1
        nonlocal in2
        nonlocal del0
        nonlocal del1
        nonlocal status
        global mydll
        if del1:
            try:
                out = engine1(enfiles, defile, in1.get(), in2.get(), del0)
            except Exception as e:
                out = str(e)
        else:
            try:
                out = engine0(enfiles, defile, in1.get(), in2.get(), del0)
            except Exception as e:
                out = str(e)
        temp = os.path.join(os.path.expanduser('~'),'Desktop')
        if temp in out:
            loc = out.find(temp)
            out = out[0:loc] + out[loc + len(temp):]
        status.set(out)
        win.update()
        time.sleep(0.1)
    but2 = tkinter.Button(win, text = '  G O  ', font = ("Consolas", 20), command = gogo)
    but2.place(x = 290,y = 220)

    status.set('program stand-by')
    lbl7 = tkinter.Label( win, textvariable = status, font = ("Consolas", 16) )
    lbl7.place(x = 5, y = 300)
    
    win.mainloop()

main()
end( [ ] )
time.sleep(0.5)

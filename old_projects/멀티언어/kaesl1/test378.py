import ctypes
import hashlib
import time
import os
import tkinter
import tkinter.font
from tkinter import filedialog

def init():
    global mydll
    temp = dohash('mydll.dll')
    keys = [4280751,
            b'[\x08j\xf3\xe8m.l\xc0Hx\r"\xe3\xff3\x0en8\xd0\xdf\x1b\xc46ws\x7f\xd6<m\x01\xb3',
            b'\xb9\t\xb6\xe5^b\xf5\xa7\xf1\xc9E\xc7gTL(\xebc\xee\xce\xca\x8dL\x96\xbeP\xf7\xa6X\xdcog']
    
    if temp == keys:
        # Go DLL 로드
        mydll = ctypes.CDLL('./mydll.dll')

        # Go 함수 시그니처 정의
        mydll.engine.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.c_int)
        mydll.engine.restype = ctypes.POINTER(ctypes.c_char)
        mydll.seehint.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.c_int)
        mydll.seehint.restype = ctypes.POINTER(ctypes.c_char)
        mydll.freeptr.argtypes = (ctypes.POINTER(ctypes.c_char),)

        return True
    
    else:
        mydll = 0
        return False

def convert(enfiles, defile, hint, pw0, pw1, del0, del1):
    mode = 0
    if not(del0): # 일반 삭제
        mode = mode + 1
    if del1: # 안전 삭제
        mode = mode + 5

    out = ""
    out = out + f'{len(enfiles):0>3}'
    for i in enfiles:
        out = out + f'{len(bytes(i,"utf-8")):0>3}' + i
    out = out + f'{len(bytes(defile,"utf-8")):0>3}' + defile
    out = out + f'{len(bytes(hint,"utf-8")):0>3}' + hint
    out = out + f'{len(bytes(pw0,"utf-8")):0>3}' + pw0
    out = out + f'{len(bytes(pw1,"utf-8")):0>3}' + pw1
    out = out + str(mode)

    return out

def engine(instr):
    # 입력 바이트 길이 제한 : int, 출력 바이트 길이 제란 : char
    temp = instr
    length = len( temp.encode('utf-8') )

    # 문자열을 C 스타일의 정수 배열로 변환
    arr = ctypes.c_char_p(temp.encode('utf-8'))

    # Go 함수 호출
    ptr = mydll.engine(arr, length)

    # 출력 문자열 바이트 생성
    out = [0] * ptr[0][0]
    for i in range(1, len(out) + 1):
        out[i - 1] = ptr[i][0]
    out = bytes(out)

    # 출력 배열 메모리 해제
    mydll.freeptr(ptr)
    
    return str(out, encoding='utf-8')

def seehint(name):
    temp = f'{len(bytes(name,"utf-8")):0>3}' + name
    length = len( temp.encode('utf-8') )

    # 문자열을 C 스타일의 정수 배열로 변환
    arr = ctypes.c_char_p(temp.encode('utf-8'))

    # Go 함수 호출
    ptr = mydll.seehint(arr, length)

    # 출력 문자열 바이트 생성
    out = [0] * ptr[0][0]
    for i in range(1, len(out) + 1):
        out[i - 1] = ptr[i][0]
    out = bytes(out)

    # 출력 배열 메모리 해제
    mydll.freeptr(ptr)
    
    return str(out, encoding='utf-8')

def dohash(name):
    with open(name, 'rb') as f:
        dllbyte = f.read()
        rev = bytes( reversed(dllbyte) )

    keys = [ ]
    keys.append( len(dllbyte) )
    keys.append( hashlib.sha3_256(dllbyte).digest() )
    keys.append( hashlib.sha3_256(rev).digest() )

    return keys

def main(load):
    win = tkinter.Tk()
    win.title('test378')
    win.geometry("450x550+100+50")
    win.resizable(False, False)

    enfiles = [ ]
    defile = ""
    hint = tkinter.StringVar()
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
        file = filedialog.askopenfile( title='파일 선택', filetypes = ( ('ote files', '*.ote'), ('all files', '*.*') ) )
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
        global mydll
        nonlocal hint
        if mydll != 0:
            hint.set(f'hint  {seehint(defile)}')
        nonlocal win
        win.update()
        
    but1 = tkinter.Button(win, text = 'DE', font = ("Consolas", 20), command = func1)
    but1.place(x = 5,y = 65)
    des = tkinter.StringVar()
    des.set("(0) - ")
    lbl1 = tkinter.Label( win, textvariable = des, font = ("Consolas", 16) )
    lbl1.place(x = 60, y = 75)

    lbl2 = tkinter.Label( win, text = "core  32 스레드 고정", font = ("Consolas", 16) )
    lbl2.place(x = 5, y = 150)

    hint.set("hint  - ",)
    lbl3 = tkinter.Label( win, textvariable = hint, font = ("Consolas", 16) )
    lbl3.place(x = 5, y = 210)
    lbl4 = tkinter.Label( win, text = "hint", font = ("Consolas", 16) )
    lbl4.place(x = 5, y = 250)
    in0 = tkinter.Entry( width=28, font = ("Consolas", 16) )
    in0.grid(column = 0 , row = 0)
    in0.place(x=80, y=250)

    lbl5 = tkinter.Label( win, text = "pw", font = ("Consolas", 16) )
    lbl5.place(x = 5, y = 295)
    in1 = tkinter.Entry( width=28, font = ("Consolas", 16), show = '●' )
    in1.grid(column = 0 , row = 0)
    in1.place(x=80, y=295)
    lbl6 = tkinter.Label( win, text = "pw", font = ("Consolas", 16) )
    lbl6.place(x = 5, y = 330)
    in2 = tkinter.Entry( width=28, font = ("Consolas", 16), show = '●' )
    in2.grid(column = 0 , row = 0)
    in2.place(x=80, y=330)

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
    def chk1():
        time.sleep(0.1)
        nonlocal del1
        nonlocal chkv1
        if chkv1.get() == 0:
            del1 = False
        else:
            del1 = True
        nonlocal win
        win.update()
    chkv0 = tkinter.IntVar()
    chkv1 = tkinter.IntVar()
    chkb0 = tkinter.Checkbutton(win, text = "원본 삭제", font = ("Consolas", 16), variable = chkv0, command = chk0)
    chkb1 = tkinter.Checkbutton(win, text = "고급 삭제", font = ("Consolas", 16), variable = chkv1, command = chk1)
    chkb0.place(x = 5, y = 400)
    chkb1.place(x = 140, y = 400)

    def gogo():
        nonlocal win
        nonlocal enfiles
        nonlocal defile
        nonlocal in0
        nonlocal in1
        nonlocal in2
        nonlocal del0
        nonlocal del1
        nonlocal status
        global mydll
        if mydll != 0:
            status.set('working. . .')
            win.update()
            k = convert(enfiles, defile, in0.get(), in1.get(), in2.get(), del0, del1)
            k = engine(k)
            status.set(k)
        else:
            status.set('stop by dll loading fail')
        win.update()
        time.sleep(0.1)
    but2 = tkinter.Button(win, text = '  G O  ', font = ("Consolas", 20), command = gogo)
    but2.place(x = 290,y = 390)

    if load:
        status.set('dll load success')
    else:
        status.set('dll load fail')
    lbl7 = tkinter.Label( win, textvariable = status, font = ("Consolas", 16) )
    lbl7.place(x = 5, y = 470)
    
    win.mainloop()

if os.path.exists('tempkaesl'):
    os.remove('tempkaesl')
load = init() # dll 로드 여부
main(load)
if os.path.exists('tempkaesl'):
    os.remove('tempkaesl')
time.sleep(0.5)

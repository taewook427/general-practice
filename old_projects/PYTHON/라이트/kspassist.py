# --hidden-import "pynput.keyboard._win32" --hidden-import "pynput.mouse._win32" //win

import os
import time

import pyautogui
import keyboard

keys = ['!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'add', 'alt', 'apps', 'backspace',
'capslock', 'clear',
'ctrl', 'decimal', 'del', 'delete',
'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'help', 'home', 'insert',
'left', 'numlock', 'pagedown', 'pageup', 'pause',
'print', 'return', 'right', 'select', 'separator',
'shift', 'sleep', 'space', 'subtract', 'tab',
'up', 'win',
'command', 'option']

def main():
    files = [x for x in os.listdir('./') if x[-4:] == '.txt']
    menu = ['0000 recording']
    for i in range( 0, len(files) ):
        menu.append(f'{i+1:0>4} {files[i]}')
    mode = input('\n'.join(menu) + '\n')
    try:
        mode = int(mode)

        if mode == 0:
            name = input('title of work record (without txt) : ')
            print('press a key to signal exit')
            time.sleep(0.1)
            ex = keyboard.read_key()
            print(f'<{ex}>')
            input('press enter to start... ')
            time.sleep(0.1)
            try:
                record(name, ex)
                print('procedure end successfully')
            except Exception as e:
                print(f'error : {e}')

        else:
            input('press enter to start... ')
            print(3)
            time.sleep(1)
            print(2)
            time.sleep(1)
            print(1)
            time.sleep(1)
            try:
                decord( files[mode - 1] )
                print('procedure end successfully')
            except Exception as e:
                print(f'error : {e}')
        
        return True
    except:
        return False

def record(name, ex):
    mem = [ ] # 명령어 모음
    current = '' # 지난번 눌린 키
    last = float( time.time() ) # 마지막 변화 시간
    const = True
    while const:
        time.sleep(0.01)
        var = False # 이번 회차에 키가 눌렸는지
        for i in keys:
            if keyboard.is_pressed(i): # 키가 눌림
                if i == ex:
                    const = False
                if current != i: # 키 누름 시작
                    t = float( time.time() ) - last
                    mem.append(f'sleep {t:.2f}')
                    last = float( time.time() )
                    current = i
                var = True
                break
        if not var:
            if current != '': # 키 눌림 끝
                t = float( time.time() ) - last
                mem.append(f'press {current} {t:.2f}')
                last = float( time.time() )
                current = ''
    with open(f'{name}.txt', 'w', encoding='utf-8') as f:
        f.write( '\n'.join(mem) + '\n' )

def decord(name):
    pyautogui.PAUSE = 0.0001
    with open(name, 'r', encoding='utf-8') as f:
        temp = [ x.replace('\n', '').split(' ') for x in f.readlines() ]
    for i in temp:
        if i[0] == 'sleep':
            time.sleep( float( i[1] ) )
        elif i[0] == 'press':
            pyautogui.keyDown( i[1] )
            time.sleep( float( i[2] ) )
            pyautogui.keyUp( i[1] )

print('KOS KSP Flight Assist 1\nenter number to work, others to exit\n')
k = True
while k:
    k = main()
    if k:
        print('\nnew work...')
    else:
        print('\nexiting...')
time.sleep(0.5)

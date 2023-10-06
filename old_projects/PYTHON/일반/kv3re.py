import time
import os
import hashlib

import sei

import psutil

def dohash(name):
    with open(name, 'rb') as f:
        dllbyte = f.read()
        rev = bytes( reversed(dllbyte) )

    keys = [ ]
    keys.append( len(dllbyte) )
    keys.append( hashlib.sha3_256(dllbyte).digest() )
    keys.append( hashlib.sha3_256(rev).digest() )

    return keys

def main(check, result, path):
    val = True
    for i in range( 0, len(check) ):
        if dohash(check[i]) != result[i]:
            val = False
    if val:
        os.startfile(path)

def vera():
    a = ['veracrypt\\VeraCrypt Format-x64.exe', 'veracrypt\\VeraCrypt-x64.exe', 'veracrypt\\VeraCryptExpander-x64.exe', 'veracrypt\\veracrypt-x64.sys']
    b = [ [6011176, b'\xe9\xba\x8c\xc9\xbf\xe2\xd5\x11\xac\xd8m\xe0\xfa\xf9_:\xa9X\tO\x90^-,g\x0f\xc6bg\x06\xee\xf4', b'\xfb\x82 qn6\xdc\xa9:\xfa\xb0P#\x16\xe5\x88\xd5n\\gK!Af\xfe-\x82\xc0\xcf@A~'],
    [5990184, b'\x126x\xf5\x8d~Iz\xfe\xad\x863\xc0\xe3\xcf\x0b\x84\x7f\xc1qZ\xe84\x0f\xfbY\xde*\x0cD\xad[', b'HO?\xabd\xd0*.i\xd2\x9d*\x82Z\xe9ZWn|\x8f\xab\x8a\xbbJ#Y>\xd2\xe7>\xda\xf1'],
    [5483816, b'\x9b\xc1\xae\x97\xf3\x85W\xaej\xac\x83\xed\x04\xdf\xb9\xb5V\x1f\xf9\x19\x95^DQc\xfc%\xc3f\xd6\xc4\xf8', b"\x84\xbd\xb9Vyl\x0e\xd2\x9cD[\x8e\xc0\xe4\x9d\xe4\x9d\xbdE'\xec%\xe7\x06\x0c$\xf8)\xae\xeaa9"],
    [817672, b'\x90\x1b\xde\xfb\xd8\x8f=;\xc5DW\xe4\x1a\xabb\x93\xde{V\x1a\x9cg\x1cHb\xe0&ZW\x8fs\x02', b'\xdfP\xf29\xc7\x01\x1b\xf1X;\x1f\xb4\xa8\xe2\x90\xbah\x16\x1eH\x86\x8e8\xfe\xfc*!\xe2\xf6\xf3\x89C'] ]
    p = 'veracrypt\\VeraCrypt-x64.exe'
    main(a, b, p)

def ffconv():
    a = ['ffconv\\ffconv.exe', 'ffconv\\ffmpeg.exe', 'ffconv\\ffplay.exe', 'ffconv\\ffprobe.exe']
    b = [ [10838504, b'\x0eY9#FcW\xe5\xd8:\xa3\xbaF\x08/CJ\x95:U\xc51\xcfe\x06\xa9\xfc\xca\x87wDu', b'\x8c\x18\x8eG\xf2CU\xd6\xe2\xcb\x1c\nX\xe0\x13\xb1\x01\xf7\xa6\x1cX\x91\xc2\x92\xeb\xce\xdc\x9f\r\xee\x14\xb1'],
[396288, b'\x9a\x95\x8a\x18\x17K\x0f\xb5\xa8*\x86\xb3>\x07,b\x08t\xfe\xe4\xa1\xfe\xb0W\t\xd5}\x87\xd5M<:', b'm\xb8i\xb3\xe5\xba\x01\xad\xe1\xe4\xd1\x17\x1b\xe7\x81\xb3\x0f\x82\xee\xd4qI\xe4\xad\xf7\xa3\twa\xa3\xd4\xdc'],
[2363392, b'_Bc\x9e\xf6\x1d\xf5=\xa6\x1c\xe3Ke:\x93\x0f\xaeU\x15\x9a\x06\xd4\xe2\xde\x85\xa2\xd9\x16\xd7\xe8B\xce', b'3\xcdx\xd2\xca_\\\xa53pC\xa8\xfe>\x85\x9eQ\xd1E?\x95\x95m\xe5\x15\xf6\xf3\xf4\x91\x95\x91h'],
[197632, b'\x05Mq!\xe3q\xca\xa4\x9d\xcb\xb0\xec\xbdRv\x03+\xa6\xbf}\xba\xbbVU\x8a\xf7uP[\xe2\xe7\xa5', b'\x0eK\x9f6;\x92\xfe\xbb\xbf~\xc2#\xb9\xcd\xee\x02d\xab\x8f\x1a\x9bs\x7fw\n\xe4\x94\x89\x0c\x90\xc2\x94'] ]
    p = 'ffconv\\ffconv.exe'
    main(a, b, p)

def verawork():
    working = False
    for proc in psutil.process_iter():
        if 'VeraCrypt-x64.exe' == proc.name():
            working = True
    return working

def ram(size):
    vera()
    count = 0.0
    validity = True
    while (count < 60.0) and validity:
        if verawork():
            validity = False
        count = count + 0.3
        time.sleep(0.3)

    if not validity:
        while verawork():
            time.sleep(0.3)
        key = [ ]
        for i in range(0, size // 1000):
            key.append(b'\x00' * 1048576000)
        for i in range(0, size % 1000):
            key.append(b'\x00' * 1048576)
        time.sleep(0.3)

def kill(size):
    vera()
    count = 0.0
    validity = True
    while (count < 60.0) and validity:
        if verawork():
            validity = False
        count = count + 0.3
        time.sleep(0.3)

    if not validity:
        while verawork():
            time.sleep(0.3)
        key = [ ]
        for i in range(0, size // 1000):
            key.append(b'\x00' * 1048576000)
        for i in range(0, size % 1000):
            key.append(b'\x00' * 1048576)
        time.sleep(0.3)

        os.system('shutdown -s -f -t 0')

try:
    tool = sei.lite()
    p = tool.init('KV3re')
    win = p[0]
    listbox = p[1]
    tool.print(win, listbox, 'KOS 2023 KV3 re\n\nA : ffconv (normal)\nB : veracrypt (normal)\nC : veracrypt (ram fill)\nD : veracrypt (kill switch)')
    p = tool.ask4(win)
    if p == '0':
        time.sleep(0.1)
        ffconv()
        tool.end(win)
    elif p == '1':
        time.sleep(0.1)
        vera()
        tool.end(win)
    elif p == '2':
        tool.hide(win)
        time.sleep(0.1)
        ram( int(psutil.virtual_memory().total * 0.9) // 1048576 )
    elif p == '3':
        tool.hide(win)
        time.sleep(0.1)
        kill( int(psutil.virtual_memory().total * 0.9) // 1048576 )
except:
    pass
time.sleep(0.5)

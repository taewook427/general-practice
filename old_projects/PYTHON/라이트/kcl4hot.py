# KCloud 4 hot (482)

import time
import os
import shutil

import oreo
import sei
import mung2

def gt():
    return time.strftime( '%Y,%m,%d_%H,%M,%S' , time.localtime( time.time() ) )

def clear(path):
    path = path.replace('\\', '/')
    temp = os.listdir(path)
    for i in temp:
        try:
            shutil.rmtree(f'{path}/{i}')
        except:
            try:
                os.remove(f'{path}/{i}')
            except:
                pass

def gs():
    t = oreo.toolbox()
    f = t.readfile('settings.txt')
    return [ f['settings#size'], f['settings#local'], f['settings#server'] ]

k = sei.lite()
obj = k.init('KCloud4hot')
k.print(obj[0], obj[1], f'현재 시각 : {gt()}')
k.print(obj[0], obj[1], 'A : 조각 내보내기 B : 조각 가져오기\nC : 동기화 폴더 열기 D : 결과물 폴더 열기')
mode = k.ask4( obj[0] )
clear('enin')
clear('enout')
clear('dein')
clear('deout')
con = gs() # 설정 데이터
if not os.path.exists( con[1] ):
    os.mkdir( con[1] ) # 동기화 폴더
if not os.path.exists( con[2] ):
    os.mkdir( con[2] ) # 결과물 폴더
mtool = mung2.toolbox()

if mode == '0':
    temp = f'enin/temp482'
    mtool.pack(con[1], temp, False)
    k.print(obj[0], obj[1], '패키징 완료')
    os.startfile('test480.exe')
    time.sleep(0.5)
    while os.path.exists(temp):
        time.sleep(0.5)
    k.print(obj[0], obj[1], '암호화 완료')

    temp = 'enout/temp482'
    name = f'{con[2]}/{gt()}'
    size = os.path.getsize(temp)
    clear( con[2] )

    with open(temp, 'rb') as f:
        for i in range( 0, size // con[0] ):
            with open(f'{name}.{i}.kcl4', 'wb') as t:
                data = f.read( con[0] )
                t.write(data)
                data = 0
        if size % con[0] != 0:
            data = f.read( size % con[0] )
            with open(f'{name}.{size//con[0]}.kcl4', 'wb') as t:
                t.write(data)
                data = 0

    os.remove(temp)
    k.print(obj[0], obj[1], '조각화 완료')
    temp = os.listdir( con[2] )
    temp = '\n'.join(temp)
    k.print(obj[0], obj[1], temp)
    k.print(obj[0], obj[1], '전체 완료')

elif mode == '1':
    temp = [x for x in os.listdir( con[2] ) if x[-5:] == '.kcl4']
    name = temp[0][ 0:temp[0].find('.') ]
    num = 0
    while os.path.exists(f'{con[2]}/{name}.{num}.kcl4'):
        num = num + 1
    clear( con[1] )

    with open('dein/temp482', 'wb') as f:
        for i in range(0, num):
            with open(f'{con[2]}/{name}.{i}.kcl4', 'rb') as t:
                data = t.read()
                f.write(data)
                data = 0
    k.print(obj[0], obj[1], '조각모음 완료')

    os.startfile('test480.exe')
    time.sleep(0.5)
    while os.path.exists('dein/temp482'):
        time.sleep(0.5)
    k.print(obj[0], obj[1], '복호화 완료')

    mtool.unpack('deout/temp482')
    os.remove('deout/temp482')
    name = 'temp261/' + os.listdir('temp261')[0] # mtool 출력 폴더 결과
    temp = os.listdir(name)
    for i in temp:
        shutil.move(f'{name}/{i}', f'{con[1]}/{i}')
    shutil.rmtree('temp261')
    k.print(obj[0], obj[1], '언패킹 완료')
    temp = '\n'.join(temp)
    k.print(obj[0], obj[1], temp)
    k.print(obj[0], obj[1], '전체 완료')

elif mode == '2':
    os.startfile( con[1] )

else:
    os.startfile( con[2] )

k.ask2( obj[0] )
k.end( obj[0] )

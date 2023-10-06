# installer

import os
import shutil
import time

typeb = '\\test137.py'
typeb = '\\WindowsAPI.exe'

typea = '\\test136.py'
typea = '\\ChromeDriver.exe'

desk = os.path.join(os.path.expanduser('~'),'Desktop')
start = os.path.join(os.path.expanduser('~'),'AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
drive = os.path.expanduser('~')
setup = os.path.join(os.path.expanduser('~'),'.setup')
restart = os.path.join(os.path.expanduser('~'),'.restart')

time.sleep(0.5)

print('설치기 작동 시작')

try:
    shutil.copy2(typea[1:], desk + typea)
    time.sleep(1.5)
    print(typea , 'desk 에 복사')
except:
    print(typeb , 'desk 에 이미 존재')

time.sleep(0.3)

try:
    shutil.copy2(typea[1:], start + typea)
    time.sleep(1.5)
    print(typea , 'start 에 복사')
except:
    print(typeb , 'start 에 이미 존재')

time.sleep(0.3)

try:
    shutil.copy2(typea[1:], drive + typea)
    time.sleep(1.5)
    print(typea , 'drive 에 복사')
except:
    print(typeb , 'drive 에 이미 존재')

time.sleep(0.3)

try:
    os.makedirs(setup)
    time.sleep(0.5)
    print('setup 폴더 생성')
except:
    print('setup 폴더 이미 존재')

time.sleep(0.3)

try:
    os.makedirs(restart)
    time.sleep(0.5)
    print('restart 폴더 생성')
except:
    print('restart 폴더 이미 존재')

time.sleep(0.3)

try:
    shutil.copy2(typea[1:], restart + typea)
    time.sleep(1.5)
    print(typea , 'restart 에 복사')
except:
    print(typea , 'restart 에 이미 존재')

time.sleep(0.3)

try:
    shutil.copy2(typeb[1:], restart + typeb)
    time.sleep(1.5)
    print(typeb , 'restart 에 복사')
except:
    print(typeb , 'restart 에 이미 존재')

time.sleep(0.3)

os.startfile(start)
time.sleep(0.3)
os.startfile(drive)
time.sleep(0.3)
os.startfile(setup)
time.sleep(0.3)
os.startfile(restart)
time.sleep(0.3)

print('모든 작업 완료')
k = input('press enter to exit... ')

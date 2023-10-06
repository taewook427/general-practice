# KCloud 4 relay (483)

import time
import os
import shutil

import oreo

def log(con):
    path = os.path.join(os.path.expanduser('~'),'Desktop')
    path = os.path.join(path,'log483.txt')
    realtime = int( time.time() ) #정수 유닉스 시간
    nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) ) #시간 구조
    logstring = nowtime + '/' + str(realtime) + '#' + f'{con}\n'
    logfile = open(path,'a')
    logfile.write(logstring)
    logfile.close()
    logfile = open(path,'r')
    firsttime = logfile.readline()
    logfile.close()
    loc1 = firsttime.find('/')
    loc2 = firsttime.find('#')
    firsttime = int( firsttime[loc1 + 1 : loc2] )
    if realtime - firsttime > 31536000 * 3: #3년까지 기록
        logfile = open(path,'w')
        logfile.write(logstring)
        logfile.close()

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

def gt(folder):
    folder = folder.replace('\\', '/')
    out = 0.0
    temp = os.listdir(folder)
    for i in temp:
        try:
            tt = os.path.getmtime(f'{folder}/{i}')
        except:
            tt = os.path.getctime(f'{folder}/{i}')
        if tt > out:
            out = tt
    return out

def cp(src, dst):
    src = src.replace('\\', '/')
    dst = dst.replace('\\', '/')
    temp = os.listdir(src)
    clear(dst)
    for i in temp:
        if os.path.isdir(f'{src}/{i}'):
            shutil.copytree(f'{src}/{i}' ,f'{dst}/{i}')
        else:
            shutil.copy(f'{src}/{i}' ,f'{dst}/{i}')

otool = oreo.toolbox()
setdt = otool.readfile('settings.txt') # settings dict
num = setdt['settings#num'] # path num
path = [0] * num
for i in range(0, num):
    path[i] = setdt[f'settings#{i}'] # path [str]
last = [gt(x) for x in path] # last update of each path [int]
maxt = 0 # 최대 시간 번호
for i in range(0, num):
    if last[maxt] < last[i]:
        maxt = i
log('kcl4relayStart')
for i in range(0, num):
    if i != maxt:
        cp( path[maxt], path[i] )
        log(f'{maxt}to{i}')

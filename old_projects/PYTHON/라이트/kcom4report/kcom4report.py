# kcom 4 report (487)

import os
import shutil
import time

import oreo

def log(con):
    path = os.path.join(os.path.expanduser('~'),'Desktop')
    path = os.path.join(path,'log487.txt')
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

otool = oreo.toolbox()
sdt = otool.readfile('settings.txt')
cpath = [ ]
for i in range( 0, sdt['settings#channel#num'] ):
    cpath.append( sdt[f'settings#channel#{i}#path'] )
fpath = [ ]
for i in range( 0, sdt['settings#report#num'] ):
    fpath.append( sdt[f'settings#report#{i}'] )
clear('enin')
clear('enout')
clear('dein')
clear('deout')
chn = ''
for i in cpath:
    i = i.replace('\\', '/')
    temp = os.listdir(i)
    if 'server.txt' in temp:
        chn = i
        os.remove(f'{chn}/server.txt')
if chn == '':
    log('NoChnDetected')
else:
    for i in fpath:
        i = i.replace('\\', '/')
        temp = i[i.rfind('/') + 1:]
        shutil.copy(i, f'enin/{temp}')
    os.startfile('test480')
    time.sleep(0.5)
    count = 0
    while os.listdir('enin') != [ ]:
        time.sleep(0.5)
        count = count + 1
        if count > 200:
            log('EnTimeover')
            raise Exception('to')
    for i in os.listdir('enout'):
        shutil.move(f'enout/{i}', f'{chn}/{i}')
        log(f'Upload{i}')

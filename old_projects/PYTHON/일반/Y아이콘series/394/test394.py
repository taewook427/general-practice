# DC 자동 뷰어
import requests
from bs4 import BeautifulSoup

import oreo
import kdcm3

import time
import os

def wrlog(content):
    realtime = int( time.time() ) #정수 유닉스 시간
    nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) ) #시간 구조
    path = os.path.join(os.path.expanduser('~'),'Desktop')
    path = os.path.join(path,'log394.txt')
    logstring = nowtime + '/' + str(realtime) + '#' + content + '\n'
    with open(path,'a',encoding='utf-8') as f:
        f.write(logstring)
    with open(path,'r',encoding='utf-8') as f:
        temp = f.readline()
    loc1 = temp.find('/')
    loc2 = temp.find('#')
    firsttime = int( temp[loc1 + 1 : loc2] )
    if realtime - firsttime > 31536000 * 3: #3년까지 기록
        with open(path,'w',encoding='utf-8') as f:
            f.write(logstring)

def getlast():
    realtime = int( time.time() ) #정수 유닉스 시간
    firsttime = settings['settings#last']
    return realtime - firsttime > settings['settings#viewtime']

def update():
    path = os.path.join(os.path.expanduser('~'),'Desktop')
    path = os.path.join(path,'msedgedriver.exe')
    if os.path.isfile(path):
        try:
            os.remove('msedgedriver.exe')
        except:
            pass
        shutil.copy(path, 'msedgedriver.exe')
        return True
    else:
        return False

def check(): #바탕화면 alert305.txt 유뮤 체크
    path = os.path.join(os.path.expanduser('~'),'Desktop')
    path = os.path.join(path,'alert305.txt')
    return os.path.isfile(path)

def mkorder():
    wrlog('mkorder')
    temp = kdcm3.toolbox()
    num = 0
    while f'settings#{num}m' in settings.keys():
        num = num + 1
    with open('order394.txt', 'w', encoding='utf-8') as f:
        for i in range(0,num):
            time.sleep(2)
            gallmax = temp.getnum( settings[f'settings#{i}m'] ) + 1
            t0 = gallmax // 100
            t1 = gallmax % 100
            for j in range(0,t0):
                f.write(f'{i},{100 * j},{100 * j + 100}\n')
            f.write(f'{i},{100 * t0},{100 * t0 + t1}\n')

def doorder():
    keep = True
    while keep:
        with open('order394.txt', 'r', encoding='utf-8') as f:
            nextorder = f.readline().strip()
        if nextorder == '':
            keep = False
            wrlog('orderend')
            os.remove('order394.txt')
            temp = settings['settings']
            k.revice( temp, 'settings#last', int( time.time() ) )
            temp = k.wrcom(temp.data, True, False)
            with open('data394.txt', 'w', encoding='utf-8') as f:
                f.write(temp)
        else:
            temp = nextorder.split(',')
            num = temp[0]
            st = int( temp[1] )
            ed = int( temp[2] )
            link = settings[f'settings#{num}v']
            name = link[ link.find('=') + 1:link.find('&') ]
            count = 0
            
            temp = kdcm3.toolbox()
            for i in range(st, ed):
                
                if check():
                    wrlog(f'autoshutdown')
                    keep = False
                    break
                
                time.sleep(2)
                try:
                    pics = temp.getpic( link + str(i) )
                    for j in pics:
                        count = count + os.path.getsize(j)
                except:
                    time.sleep(10)
            
            with open('order394.txt', 'r', encoding='utf-8') as f:
                temp = ''.join( f.readlines()[1:] )
            if keep:
                with open('order394.txt', 'w', encoding='utf-8') as f:
                    f.write(temp)
            if keep:
                wrlog(f'{name} {st} {ed} {count}')
            
        if check() and keep:
            wrlog(f'autoshutdown')
            keep = False
        else:
            time.sleep(30)

def main():
    if not( check() ):
        if os.path.isfile('order394.txt'):
            doorder()
        else:
            if getlast():
                mkorder()
                time.sleep(2)
                doorder()

k = oreo.toolbox()
settings = k.readfile('data394.txt')
main()

# kcom4 manager (479)

import os
import shutil
import time

import oreo

class toolbox:

    def __init__(self):
        self.otool = oreo.toolbox() # oreo tool
        self.settings = self.otool.readfile('settings.txt') # settings dict
        self.wait = self.settings['settings#coldwait'] # current waiting time
        self.last = float( time.time() ) - 10000 # last ordered time

        self.cname = [ ] # channel name
        self.cpath = [ ] # channel path
        self.sname = [ ] # server name
        self.spath = [ ] # server path
        for i in range( 0, self.settings['settings#channel#num'] ):
            self.cname.append( self.settings[f'settings#channel#{i}#name'] )
            self.cpath.append( self.settings[f'settings#channel#{i}#path'] )
        for i in range( 0, self.settings['settings#server#num'] ):
            self.sname.append( self.settings[f'settings#server#{i}#name'] )
            self.spath.append( self.settings[f'settings#server#{i}#path'] )

        # 채널 초기화
        for i in self.cpath:
            self.clear(i)

        self.log('kcom4manStart')
        self.log('modeColdWait')

    def log(self, con):
        path = os.path.join(os.path.expanduser('~'),'Desktop')
        path = os.path.join(path,'log479.txt')
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

    def clear(self, path):
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

    def cycle(self): # check whole cycle x1
        st = float( time.time() )
        flag = 0 # 처리 수
        for i in self.cpath:
            try:
                flag = flag + self.chn(i)
            except Exception as e:
                self.log( str(e).replace('\n',' ') )
            self.clear('enin')
            self.clear('enout')
            self.clear('dein')
            self.clear('deout')
        ed = float( time.time() )

        # 처리 수 기반 대기시간 조정
        if flag != 0:
            self.last = float( time.time() )
        if ed - self.last > self.settings['settings#convtime']:
            temp = self.wait
            self.wait = self.settings['settings#coldwait']
            if temp != self.wait:
                self.log('modeColdWait')
        else:
            temp = self.wait
            self.wait = self.settings['settings#hotwait']
            if temp != self.wait:
                self.log('modeHotWait')
            
        if ed - st > self.wait:
            time.sleep(0.5)
        else:
            time.sleep( self.wait - (ed - st) + 0.5 )

    def chn(self, channel):
        channel = channel.replace('\\', '/')
        temp = os.listdir(channel) # channel 폴더 하위 리스트
        if 'manager.txt' in temp:
            shutil.move(f'{channel}/manager.txt', 'dein/manager.txt')
            os.startfile('test480.exe')
            time.sleep(0.5)
            st = float( time.time() )
            while os.path.exists('dein/manager.txt'):
                time.sleep(0.5)
                if float( time.time() ) - st > 180:
                    raise Exception('de180sOver')
            order = self.otool.readfile('deout/manager.txt')
            os.startfile( self.spath[ self.sname.index( order['order#name'] ) ] ) # tgt exe start
            self.log(f'{order["order#name"]}Start')
            return 1
        else:
            return 0

time.sleep(300)
k = toolbox()
apath = os.path.join(os.path.expanduser('~'),'Desktop')
apath = os.path.join(apath,'alert305.txt')
fin = True
while fin:
    k.cycle()
    if os.path.exists(apath):
        k.log('AutoShutdown')
        fin = False
time.sleep(0.5)

import time
import os
import sei

time.sleep(0.5)
path = os.path.join(os.path.expanduser('~'),'Desktop')
path = os.path.join(path,'alert305.txt') #종료 예고 삭제
try:
    os.remove(path)
except:
    pass

realtime = int( time.time() ) #정수 유닉스 시간
nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) ) #시간 구조

k = sei.lite()
p = k.init('Titanium')
win = p[0]
listbox = p[1]

k.print(win,listbox,nowtime+'\npower on')
logstring = nowtime + '/' + str(realtime) + '#' + 'POWERED\n'
path = os.path.join(os.path.expanduser('~'),'Desktop')
path = os.path.join(path,'log305.txt')

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

k.print(win,listbox,'log has been written')
time.sleep(3)
k.end(win)

time.sleep(900) #15분 대기 ###############

shutdown = False #방금 켜진 상태
while not shutdown:
    time.sleep(600) #10분 대기 ###############
    local = time.localtime( time.time() )
    date = local.tm_mday #정수 날짜
    hour = local.tm_hour #정수 시간
    minute = local.tm_min #정수 분

    if date % 3 == 0: #3의 배수 날
        if hour == 3: #오전 3시
            if 5 <= minute <= 25: #15분 +- 10분
                shutdown = True

path = os.path.join(os.path.expanduser('~'),'Desktop')
path = os.path.join(path,'alert305.txt') #종료 예고 생성
f = open(path,'w')
f.close()

time.sleep(900) # 15분 대기 ###############
path = os.path.join(os.path.expanduser('~'),'Desktop')
path = os.path.join(path,'alert305.txt') #종료 예고 삭제
try:
    os.remove(path)
except:
    pass
os.system('shutdown -f -r -t 5') #다시 시작

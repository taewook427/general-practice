import os
import time
print('power on')
realtime = int( time.time() )
nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) )
print(nowtime)
logstring = nowtime + '/' + str(realtime) + '#' + 'POWERED\n'
path = os.path.join(os.path.expanduser('~'),'Desktop')
path = os.path.join(path,'powerlog.txt')
logfile = open(path,'a')
logfile.write(logstring)
logfile.close()
logfile = open(path,'r')
firsttime = logfile.readline()
logfile.close()
loc1 = firsttime.find('/')
loc2 = firsttime.find('#')
firsttime = int( firsttime[loc1 + 1 : loc2] )
if realtime - firsttime > 31536000:
    logfile = open(path,'w')
    logfile.write(logstring)
    logfile.close()
print('log has been written')
time.sleep(1.5)

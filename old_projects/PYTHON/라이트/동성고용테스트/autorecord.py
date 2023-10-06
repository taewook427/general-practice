import time

f = open('data.txt','w')
f.close()
while True:
    f = open('data.txt','a')
    now = time.localtime( time.time() )
    t = time.strftime( '%H:%M:%S' , now )
    f.write( t + '\n' )
    f.close()
    time.sleep(10)


# kcom4on2 (488)

import time
import os
import shutil

import sei
import oreo

otool = oreo.toolbox()
sdt = otool.readfile('settings.txt')
stool = sei.standard()
sobj = stool.init('kcom4on2')

cname = [ ]
cpath = [ ]
for i in range( 0, sdt['settings#channel#num'] ):
    cname.append( sdt[f'settings#channel#{i}#name'] )
    cpath.append( sdt[f'settings#channel#{i}#path'] )
order = [ ]
for i in range( 0, sdt['settings#order#num'] ):
    order.append( sdt[f'settings#order#{i}'] )

stool.print(sobj[0], sobj[1], '채널 선택')
for i in range( 0, len(cname) ):
    stool.print(sobj[0], sobj[1], f'{i} : {cname[i]}')
chn = cpath[ int( stool.getnum( sobj[0] ) ) ]
chn = chn.replace('\\', '/')
stool.print(sobj[0], sobj[1], '명령어 선택')
for i in range( 0, len(order) ):
    stool.print(sobj[0], sobj[1], f'{i} : {order[i]}')
ordin = order[ int( stool.getnum( sobj[0] ) ) ]

temp = otool.mkobj('order')
otool.putdt(temp, 'name', ordin)
temp = otool.wrcom(temp.data, True, False)
with open('enin/manager.txt', 'w', encoding = 'utf-8') as f:
    f.write(temp)
os.startfile('test480')
time.sleep(0.5)
while os.path.exists('enin/manager.txt'):
    time.sleep(0.5)
shutil.move('enout/manager.txt', f'{chn}/manager.txt')

stool.print(sobj[0], sobj[1], '전송 완료. 채널을 열까요?')
temp = stool.ask2( sobj[0] )
if temp == '0':
    os.startfile( chn.replace('/', '\\') )
time.sleep(0.5)
stool.end( sobj[0] )
time.sleep(0.5)

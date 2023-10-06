import sei

def setup(tgt):
    f = open(tgt,'rb')
    data = f.read()
    f.close()

    out = ['class xenon:\n','    data0 = b""\n']
    num = len(data)//80
    for i in range(0,num):
        p = str( data[ i*80 : i*80+80 ] )
        out.append('    data0 = data0 + ' +p+'\n')
    if not( len(data) % 80 == 0 ):
        p = str( data[num*80:] )
    else:
        p = str( b'' )
    out.append('    data0 = data0 + ' +p+'\n')

    f = open('data.txt','w')
    f.writelines(out)
    f.close()

def add(tgt,num):
    f = open(tgt,'rb')
    data = f.read()
    f.close()

    kk = 'data'+num
    out = ['\n','    '+kk+' = b""\n']
    num = len(data)//80
    for i in range(0,num):
        p = str( data[ i*80 : i*80+80 ] )
        out.append('    '+kk+' = '+kk+' + ' +p+'\n')
    if not( len(data) % 80 == 0 ):
        p = str( data[num*80:] )
    else:
        p = str( b'' )
    out.append('    '+kk+' = '+kk+' + ' +p+'\n')

    f = open('data.txt','a')
    f.writelines(out)
    f.close()

k = sei.lite()
p = k.init('xenon2')
win = p[0]
listbox = p[1]

k.print(win,listbox,'수kb 이하 파일 내장장치\ndata.txt에 출력\n내장할 파일을 선택하십시오.')
p = k.select('file')
k.print(win,listbox,'경로선택 : '+p)
setup(p)
pp = 0
k.print(win,listbox,'파일을 더 내장하시겠습니까?')
while k.ask2(win) == '0':
    tgt = k.select('file')
    k.print(win,listbox,'경로선택 : '+tgt)
    pp = pp + 1
    add(tgt,str(pp))
    k.print(win,listbox,'파일을 더 내장하시겠습니까?')
k.print(win,listbox,'종료합니다.')
k.ask2(win)
k.end(win)

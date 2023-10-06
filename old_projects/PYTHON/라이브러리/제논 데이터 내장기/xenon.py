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

print('수kb 이하 파일 내장장치 /end 로 종료')
p = input('내장할 파일 경로 : ')
setup(p)
pp = 0
while not (p == '/end'):
    tgt = input('내장할 파일 경로 : ')
    pp = pp + 1
    add(tgt,str(pp))
print('종료')

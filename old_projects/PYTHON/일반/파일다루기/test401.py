import os
import shutil

import hashlib
from Cryptodome.Cipher import AES

from PIL import Image

def check(path,num):
    path = path.replace('/','\\')
    try:
        shutil.rmtree('temp401')
    except:
        pass
    os.mkdir('temp401')
    for i in range(0,num):
        f = Image.open(path+'\\'+str(i)+'.png')
        f.save('temp401\\'+str(i)+'.bmp')
    out = b'' # out bytes
    for i in range(0,num):
        f = open('temp401\\'+str(i)+'.bmp','rb')
        bmphead = f.read(10)
        bmphead = f.read(1)[0] + 256 * f.read(1)[0] + 65536 * f.read(1)[0] + 16777216 * f.read(1)[0]
        f.close()
        f = open('temp401\\'+str(i)+'.bmp','rb')
        temp = f.read(bmphead)
        temp = f.read() # temp bmp bytes
        chunk = [0] * (len(temp) // 2)
        for i in range( 0,len(chunk) ):
            chunk[i] = 16 * (temp[2*i] % 16) + (temp[2*i+1] % 16)
        out = out + bytes(chunk)
        
    with open('temp401\\temp401.dat','wb') as f:
        f.write(out)
    salt = str( out[0:64] , 'utf-8' ) #str
    pwhash = out[64:128] #bytes
    hint = str( out[128:188] , 'utf-8' ) #str
    filename = str( out[188:252] , 'utf-8' ) #str
    filesize = out[252] + 256 * out[253] + 65536 * out[254] + 16777216 * out[255] #int
    return [salt, pwhash, hint, filename, filesize]

def pw(salt,pw,pwhash): # h = 3512( pw + salt ), k = 2256( salt + pw ), i = md5( salt )
    temp0 = ( pw + salt ).encode('utf-8')
    for i in range(0,1000001):
        temp0 = hashlib.sha3_512( temp0 ).digest() #bytes
    temp1 = ( salt + pw ).encode('utf-8')
    for i in range(0,1000001):
        temp1 = hashlib.sha256( temp1 ).digest() #bytes
    temp2 = hashlib.md5( ( salt ).encode( 'utf-8' ) ).digest() #bytes
    if temp0 == pwhash:
        return ['P',temp1,temp2]
    else:
        return ['N',b'',b'']

def unpack(filename,filesize,key,iv):
    with open('temp401\\temp401.dat','rb') as tgt:
        with open(os.path.join(os.path.expanduser('~'),'Desktop') + '\\re_' + filename,'wb') as tow:
            tool = AES.new(key,AES.MODE_CBC,iv)
            temp = tgt.read(256)
            
            for i in range(0,int( filesize/16 ) - 1 ):
                temp = tgt.read(16)
                tow.write( tool.decrypt(temp) )
            temp = tgt.read(16)
            unpad = lambda x : x[:-x[-1]]
            temp = unpad( tool.decrypt(temp) )
            tow.write(temp)
    shutil.rmtree('temp401')

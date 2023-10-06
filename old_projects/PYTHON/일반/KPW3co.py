import os
import time

from Cryptodome.Cipher import AES
import hashlib
from zlib import crc32
import base64

from PIL import Image

import oreo

class infunc:

    def de(self,binary): #리틀 엔디안 디코딩
        value = 0
        for i in range( 0,len(binary) ):
            k = 256 ** i
            k = k * binary[i]
            value = value + k
        return value

    def getpwhash(self,salt,kf,pw): #salt 바이트 keyfile 바이트 pw str
        pw = bytes(pw,encoding='utf-8') #pw 바이트
        tool = infunc()
        func = tool.gethash
        init = pw #init byte
        for i in range(0,100):
            init = func(init + kf,'sha3512')
            for j in range(0,5000):
                init = func(salt + init,'sha3512')
                init = func(init + salt,'sha3512')
        return init #64 바이트

    def getmasterkey(self,salt,kf,pw): #salt 바이트 keyfile 바이트 pw str
        pw = bytes(pw,encoding='utf-8') #pw 바이트
        tool = infunc()
        func = tool.gethash
        pw = bytes( reversed(pw) )
        salt = bytes( reversed(salt) )
        kf = bytes( reversed(kf) )
        init = pw #init byte
        for i in range(0,10):
            init = func(init + kf,'sha3512')
            for j in range(0,5000):
                init = func(salt + init,'sha3512')
                init = func(init + salt,'sha3512')
        return init #64 바이트

    def deshort(self,key,iv,data): #짧은 데이터 복호화, 입력은 바이트, 패딩 있음
        num = ( len(data)//16 ) - 1 #non pad chunk + pad chunk 1
        out = [0] * num * 16
        func = AES.new(key,AES.MODE_CBC,iv)
        func = func.decrypt
        for i in range(0,num):
            ii = 16 * i
            iii = ii + 16
            out[ii:iii] = func( data[ii:iii] )
        unpad = lambda x : x[:-x[-1]]
        ii = 16 * num
        iii = ii + 16
        temp = unpad( func( data[ii:iii] ) )
        out = bytes(out) + temp
        return out #10MB당 1.4s 정도

    def gethash(self,data,mode): #해시구하기
        tp = type(data) #바이트, 문자열, 정수 등 받음
        if tp == str: #모드는 문자열
            data = bytes(data,encoding='utf-8')
        elif tp != bytes:
            data = bytes(str(data),encoding='utf-8')
        if mode == 'crc32':
            temp = crc32(data)
            out = [0,0,0,0]
            out[3] = temp % 256
            temp = temp // 256
            out[2] = temp % 256
            temp = temp // 256
            out[1] = temp % 256
            temp = temp // 256
            out[0] = temp % 256
            temp = temp // 256
            return bytes(out) #4바이트
        elif mode == 'sha3512':
            temp = hashlib.sha3_512(data).hexdigest()
            return bytes.fromhex(temp) #64바이트
        elif mode == 'sha2256':
            temp = hashlib.sha256(data).hexdigest()
            return bytes.fromhex(temp) #32바이트
        elif mode == 'sha2512':
            temp = hashlib.sha512(data).hexdigest()
            return bytes.fromhex(temp) #64바이트
        elif mode == 'md5':
            temp = hashlib.md5(data).hexdigest()
            return bytes.fromhex(temp) #16바이트
        else:
            return b'' #목록에 없음

    def b64de(self,data): #base64 디코딩, 입력은 문자열
        data = data.replace('$','+') # +:$ /:% =:&
        data = data.replace('%','/')
        data = data.replace('&','=')
        data = base64.b64decode(data)
        return data #출력은 바이트

    def getkeyfile(self,path):
        try:
            with open(path,'rb') as f:
                temp = f.read()
        except:
            temp = b'580sd8gfgjf92fc3857fjj2309478572382390vjfjwifdjf8v3785249057vwdfj904689324n89k90fdkc73458k823475686890vmtjdfvg9k87b683489013458k90jgfdfiosjkv9f3498u23yubt98458'
        return temp

    def readpng(self,path): # png to data byte
        temp = Image.open(path)
        temp.save('bp.bmp')
        with open('bp.bmp','rb') as f:
            bmp = f.read() # bmp data
        os.remove('bp.bmp')
        size = bmp[10] + bmp[11] * 256 + bmp[12] * 65536 + bmp[13] * 16777216
        bmpmain = bmp[size:]
        size = len(bmpmain) // 4 #output size
        out = [0] * size
        for i in range(0,size):
            temp = i * 4
            out[i] = (bmpmain[temp] % 4) * 64 + (bmpmain[temp+1] % 4) * 16 + (bmpmain[temp+2] % 4) * 4 + (bmpmain[temp+3] % 4)
        return bytes(out)
    
tool = infunc()
print('비밀번호 저장 파일 출력기')
print('같은 폴더 상에 k.png 파일을 위치시키십시오.')
print('파일의 비밀번호를 0000, 기본키파일로 맞추십시오.')
input('press enter to continue... ')
try:
    data = tool.readpng('k.png')
    if data[0:3] != b'KP3':
        raise Exception('Magic Num Err') # 매직넘버 불일치
    else:
        hs = tool.de( data[3:5] ) #헤더크기
        ds = tool.de( data[5:8] ) #데이터크기
        crc = data[8:12] #crc byte
        head = data[16:16+hs] #head byte
        data = data[16+hs:16+hs+ds] #data byte
        if tool.gethash(head + data,'crc32') != crc:
            raise Exception('Hash Err') # 해시값 불일치
        else:
            otool = oreo.toolbox()
            head = otool.readstr( otool.etor( str(head,'utf-8'),'BKLOVE' ) )
            pwhash = tool.b64de( head['header#pwhash'] ) #pwhash byte
            salt = tool.b64de( head['header#salt'] ) #salt byte
            ckeydt = tool.b64de( head['header#ckeydt'] ) #ckeydt byte
            if pwhash == tool.getpwhash(salt,tool.getkeyfile('기본키파일'),'0000'):
                mkey = tool.getmasterkey(salt,tool.getkeyfile('기본키파일'),'0000')
                ckey = tool.deshort(mkey[0:32],mkey[32:48],ckeydt)
                data = tool.deshort(ckey,mkey[48:64],data)
                content = str(data,'utf-8')
                content = otool.readstr(content)
                temp = [0] * content['data#num']
                for i in range( 0,len(temp) ):
                    temp[i] = content['data#'+str(i)]
                print('===============')
                for i in temp:
                    print(i + '\n===============')
except Exception as e:
    print(e)
input('press enter to exit... ')
time.sleep(0.5)

import getpass
import time
import os
import random
import hashlib
from Cryptodome.Cipher import AES
from PIL import Image
import shutil

class getsalt:
    def __init__(self):
        output = ''
        for i in range(0,1024):
            output = output + chr(random.randrange(32,126))
        self.salt = output

class gethash:
    def sha3512(self,letter):
        out = letter.encode('utf-8')
        for i in range(0,1000000):
            out = hashlib.sha3_512( out ).hexdigest()
            out = bytes.fromhex(out)
        return hashlib.sha3_512( out ).hexdigest()
    def sha2256(self,letter):
        out = letter.encode('utf-8')
        for i in range(0,1000000):
            out = hashlib.sha256( out ).hexdigest()
            out = bytes.fromhex(out)
        return hashlib.sha256( out ).hexdigest()
    def md5(self,letter):
        return hashlib.md5( ( letter ).encode( 'utf-8' ) ).hexdigest()

class aesfunc:
    def set_cbc(self,key,iv):
        self.key = key
        self.iv = iv
        self.e_cipher = AES.new(self.key,AES.MODE_CBC,self.iv)
        self.d_cipher = AES.new(self.key,AES.MODE_CBC,self.iv)
    def en_cbc(self,data):
        return self.e_cipher.encrypt(data)
    def de_cbc(self,data):
        return self.d_cipher.decrypt(data)

class start:
    def __init__(self):
        print("KOS PW MANAGER V2\n")
        print("모드 선택 : 내용 보기(1) 내보내기(2) 가져오기(3)")
        mode = input("==================== ")
        if mode == '1':
            kos = mode1()
            k = 0
            while k == 0:
                k = kos.view()
                
        elif mode == '2':
            kos = mode2()
        elif mode == '3':
            f = input('불러올 파일 입력\n>>> ')
            if f[0] == '"' or f[0] == "'":
                f = f[1:-1]
            k = 0
            try:
                k = open(f,'rb')
                k.close()
                k = 1
            except:
                print('오류 : 불러올 파일 찾을 수 없음 !')
            if k == 1:
                i1 = Image.open(f)
                i1.save('test48.bmp')
                do = mode3()
                print('가져오기 성공 !')
            k = input('아무 키나 입력하여 종료... ')
        else:
            print('\n알수없는 모드')

class mode1:
    def __init__(self):
        f = open('pre.txt','r')
        self.lastread = f.readline()[0:-1]
        self.lastpw = f.readline()[0:-1]
        self.lastcon = f.readline()[0:-1]
        f.close()
        f = open('salt.txt','r')
        self.salt = f.readline()
        f.close()
        f = open('hint.txt','r',encoding='utf-8')
        self.hint = f.readline()
        f.close()
        f = open('pwhash.txt','r')
        self.pwhash = f.readline()
        f.close()
        f = open('data','rb')
        self.data = f.read()
        f.close()
        salt = self.salt
        print('비밀번호 힌트 : ' + self.hint)
        income = getpass.getpass('비밀번호 : ')
        hset = gethash()
        pwhashp = hset.sha3512(income + salt)
        self.iv = hset.md5(salt)
        self.iv = bytes.fromhex(self.iv)
        if pwhashp == self.pwhash:
            self.pw = income
            self.key = hset.sha2256(salt + income)
            self.key = bytes.fromhex(self.key)
            do = aesinout()
            self.content = do.dode(self.data,self.key,self.iv)
            self.content = str(self.content,encoding='utf-8')
        else:
            print('비밀번호가 올바르지 않습니다.')
            income = getpass.getpass('비밀번호 : ')
            hset = gethash()
            pwhashp = hset.sha3512(income + salt)
            if pwhashp == self.pwhash:
                self.pw = income
                self.key = hset.sha2256(salt + income)
                self.key = bytes.fromhex(self.key)
                do = aesinout()
                self.content = do.dode(self.data,self.key,self.iv)
                self.content = str(self.content,encoding='utf-8')
            else:
                print('비밀번호가 올바르지 않습니다.')
                income = getpass.getpass('비밀번호 : ')
                hset = gethash()
                pwhashp = hset.sha3512(income + salt)
                if pwhashp == self.pwhash:
                    self.pw = income
                    self.key = hset.sha2256(salt + income)
                    self.key = bytes.fromhex(self.key)
                    do = aesinout()
                    self.content = do.dode(self.data,self.key,self.iv)
                    self.content = str(self.content,encoding='utf-8')
                else:
                    print('비밀번호가 올바르지 않습니다.')
                    print('종료합니다.')
                    time.sleep(1)
                    os.exit()
        
    def view(self):
        print(' ')
        print('마지막 내용 접근 : '+self.lastread)
        print('마지막 비밀번호 변경 : '+self.lastpw)
        print('마지막 내용 수정 : '+self.lastcon)
        print('현재 비밀번호 : '+self.pw[0]+' *'*(len(self.pw)-2)+' '+self.pw[-1])
        nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) )
        f = open('pre.txt','w')
        f.write(nowtime + '\n')
        f.write(self.lastpw + '\n')
        f.write(self.lastcon + '\n')
        f.close()
        self.lastread = nowtime
        print('\n' + self.content + '\n')
        print('도구 : 내용수정(1) 비밀번호변경(2) 끝내기(3)')
        mode = input('>>> ')
        if mode == '1':
            new = open('txt.txt','w',encoding='utf-8')
            new.write(self.content)
            new.close()
            os.startfile('txt.txt')
            mode = input('내용 수정이 끝나면 아무 키나 입력하십시오 ')
            print('저장 중...\n==================== ')
            new = open('txt.txt','r',encoding='utf-8')
            newcon = new.readlines()
            new.close()
            rword = ''
            for i in range(0,1024 * 5):
                rget = getsalt()
                rword = rword + rget.salt + '\n'
            new = open('txt.txt','w')
            new.write(rword)
            new.close()
            os.remove('txt.txt')
            self.content = ''
            for i in newcon:
                self.content = self.content + i
            self.data = self.content.encode('utf-8')
            do = aesinout()
            towrite = do.doen(self.data,self.key,self.iv)
            f = open('data','wb')
            f.write(towrite)
            f.close()
            nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) )
            f = open('pre.txt','w')
            f.write(self.lastread + '\n')
            f.write(self.lastpw + '\n')
            f.write(nowtime + '\n')
            f.close()
            self.lastcon = nowtime
            return 0
        elif mode == '2':
            newpw1 = getpass.getpass('새 비밀번호 입력 : ')
            newpw2 = getpass.getpass('새 비밀번호 확인 : ')
            if newpw1 == newpw2:
                newpw = newpw1
                if len(newpw) > 4:
                    self.pw = newpw
                    self.hint = input('비밀번호 힌트 설정\n>>> ')
                    nowtime = time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( time.time() ) )
                    f = open('pre.txt','w')
                    f.write(self.lastread + '\n')
                    f.write(nowtime + '\n')
                    f.write(self.lastcon + '\n')
                    f.close()
                    self.lastpw = nowtime
                    t = getsalt()
                    salt = t.salt
                    f = open('hint.txt','w',encoding = 'utf-8')
                    f.write(self.hint)
                    f.close()
                    f = open('salt.txt','w')
                    f.write(salt)
                    f.close()
                    hset = gethash()
                    self.key = hset.sha2256(salt + self.pw)
                    self.key = bytes.fromhex(self.key)
                    pwhash = hset.sha3512(self.pw + salt)
                    f = open('pwhash.txt','w')
                    f.write(pwhash)
                    f.close()
                    self.iv = hset.md5(salt)
                    self.iv = bytes.fromhex(self.iv)
                    do = aesinout()
                    data = self.content.encode('utf-8')
                    newdata = do.doen(data,self.key,self.iv)
                    f = open('data','wb')
                    f.write(newdata)
                    f.close()
                    print('비밀번호 변경 완료!')
                    print('==================== ')
                else:
                    print('변경 불가 : 비밀번호는 5자리 이상이여야 합니다\n')
                    print('==================== ')
            else:
                print('변경 불가 : 새 비밀번호 불일치!\n')
                print('==================== ')
            return 0
        elif mode == '3':
            print('\n프로그램을 종료합니다.')
            return 1
        else:
            print('\n알수없는 모드')
            return 0
        
class mode2:
    def __init__(self):
        temp = open('temp','wb')
        sset = endecode()
        
        f = open('data','rb')
        tow = f.read()
        size = sset.encode(len(tow))
        f.close()
        temp.write(size)
        temp.write(tow)
        
        f = open('hint.txt','rb')
        tow = f.read()
        size = sset.encode(len(tow))
        f.close()
        temp.write(size)
        temp.write(tow)

        f = open('pre.txt','rb')
        tow = f.read()
        size = sset.encode(len(tow))
        f.close()
        temp.write(size)
        temp.write(tow)

        f = open('pwhash.txt','rb')
        tow = f.read()
        size = sset.encode(len(tow))
        f.close()
        temp.write(size)
        temp.write(tow)

        f = open('salt.txt','rb')
        tow = f.read()
        size = sset.encode(len(tow))
        f.close()
        temp.write(size)
        temp.write(tow)
        
        temp.close()
        print('임시 파일 생성 완료')
        i1 = Image.open('test45.png')
        i1.save('test46.bmp','bmp')
        
        source = open('test46.bmp','rb')
        new = open('test44.bmp','wb')

        k = source.read(10)
        stpoint = sset.decode( source.read(4) )
        source.close()
        source = open('test46.bmp','rb')

        head = source.read(stpoint)
        smain = source.read()
        f = open('temp','rb')
        tow = f.read() + b'\x7f'*120000
        tow = tow[0:120000]
        f.close()

        wmain = b''
        for i in range(0,160000):
            if i%4 == 0:
                i = int(i/4)
                wmain = wmain + tow[3*i:3*i+3]
            else:
                wmain = wmain + smain[3*i:3*i+3]
        new.write(head)
        new.write(wmain)

        source.close()
        new.close()
        os.remove('temp')
        print('사진 생성 완료')

        i1 = Image.open('test44.bmp')
        i1.save('test47.png','png')
        os.remove('test44.bmp')
        os.remove('test46.bmp')
        path = os.path.join(os.path.expanduser('~'),'Desktop')
        path = path + '\\\\pw.png'
        shutil.copy('test47.png',path)
        os.remove('test47.png')
        print('바탕화면에 결과물 표시됨')
        k = input('아무 키나 입력하여 종료... ')

class mode3:
    def __init__(self):
        source = open('test48.bmp','rb')
        k = source.read(10)
        nset = endecode()
        stpoint = nset.decode( source.read(4) )
        source.close()

        source = open('test48.bmp','rb')
        k = source.read(stpoint)
        mdata = source.read()

        raw = b''
        for i in range(0,160000):
            if i%4 == 0:
                raw = raw + mdata[3*i:3*i+3]

        size = nset.decode(raw[0:4])
        raw = raw[4:]
        tow = raw[0:size]
        f = open('data','wb')
        f.write(tow)
        f.close()
        raw = raw[size:]

        size = nset.decode(raw[0:4])
        raw = raw[4:]
        tow = raw[0:size]
        f = open('hint.txt','wb')
        f.write(tow)
        f.close()
        raw = raw[size:]

        size = nset.decode(raw[0:4])
        raw = raw[4:]
        tow = raw[0:size]
        f = open('pre.txt','wb')
        f.write(tow)
        f.close()
        raw = raw[size:]

        size = nset.decode(raw[0:4])
        raw = raw[4:]
        tow = raw[0:size]
        f = open('pwhash.txt','wb')
        f.write(tow)
        f.close()
        raw = raw[size:]

        size = nset.decode(raw[0:4])
        raw = raw[4:]
        tow = raw[0:size]
        f = open('salt.txt','wb')
        f.write(tow)
        f.close()
        raw = raw[size:]
        
        source.close()
        os.remove('test48.bmp')

def preset():
    f = open('pre.txt','w')
    f.write('-\n-\n-\n')
    f.close()
    f = open('hint.txt','w',encoding='utf-8')
    f.write('기본 비밀번호는 0000 입니다.')
    f.close()
    f = getsalt()
    salt = f.salt
    f = open('salt.txt','w')
    f.write(salt)
    f.close()
    pw = '0000'
    hset = gethash()
    pwhash = hset.sha3512(pw + salt)
    f = open('pwhash.txt','w')
    f.write(pwhash)
    f.close()
    data = '환영합니다!'
    data = data.encode( 'utf-8' )
    key = hset.sha2256(salt + pw)
    key = bytes.fromhex(key)
    iv = hset.md5(salt)
    iv = bytes.fromhex(iv)
    aesset = aesfunc()
    aesset.set_cbc(key,iv)
    data = aesset.en_cbc(data)
    data = data + aesset.en_cbc(b'\x10'*16)
    f = open('data','wb')
    f.write(data)
    f.close()
    print('초기 설정 완료!')

class aesinout:
    def doen(self,data,key,iv):
        result = b''
        aesset = aesfunc()
        aesset.set_cbc(key,iv)
        while len(data) >= 16:
            temp = data[0:16]
            result = result + aesset.en_cbc(temp)
            data = data[16:]
        pad = lambda x : x + bytes(chr( 16 - len(x) ),'utf-8') * (16 - len(x))
        temp = pad(data)
        result = result + aesset.en_cbc(temp)
        return result
        
    def dode(self,data,key,iv):
        result = b''
        aesset = aesfunc()
        aesset.set_cbc(key,iv)
        while len(data) >= 16:
            temp = data[0:16]
            result = result + aesset.de_cbc(temp)
            data = data[16:]
        unpad = lambda x : x[:-x[-1]]
        result = unpad(result)
        return result

class endecode():
    def encode(self,num):
        k = [ ]
        for i in range( 0,4 ):
            k.append( num % 256 )
            num = num // 256
        j = bytes( { k[0] } )
        for i in range( 1,len(k) ):
            j = j + bytes( { k[i] } )
        return j
    def decode(self,binary):
        value = 0
        for i in range( 0,len(binary) ):
            k = 256 ** i
            k = k * binary[i]
            value = value + k
        return value

try:
    f = open('pre.txt','r')
    f.close()
except:
    preset()
kos = start()
time.sleep(1.5)

# KVault4 Layer 0

import os
import shutil
import time
import base64
import multiprocessing as mp

class infunc:
    
    def b64en(self, data): #base64 인코딩, 입력은 바이트
        data = base64.b64encode(data) # +:$ /:% =:&
        data = str(data,encoding='utf-8')
        data = data.replace('+','$')
        data = data.replace('/','%')
        data = data.replace('=','&')
        return data #출려은 문자열

    def b64de(self, data): #base64 디코딩, 입력은 문자열
        data = data.replace('$','+') # +:$ /:% =:&
        data = data.replace('%','/')
        data = data.replace('&','=')
        data = base64.b64decode(data)
        return data #출력은 바이트

    def getfptr(self, path): # path 폴더 안 fptr 구하기
        temp = os.listdir(path)
        out = [ ]
        for i in temp:
            if len(i) == 20:
                if i[-4:] == '.kv4':
                    out.append( self.b64de( i[0:16] ) )
                else:
                    os.remove(path + '/' + i)
            else:
                os.remove(path + '/' + i)
        out.sort()
        return b''.join(out)

    def en8b(self, number): #리틀 엔디안 인코딩 (8B)
        temp = [ ]
        for i in range(0, 8):
            temp.append( number % 256 )
            number = number // 256
        return bytes(temp)

    def de8b(self,binary): #리틀 엔디안 디코딩 (8B)
        value = 0
        for i in range(0, 8):
            if binary[i] != 0:
                temp = 256 ** i
                temp = temp * binary[i]
                value = value + temp
        return value

    def find(self, chunk, fptr): # 정렬된 12B * n chunk 에서 fptr 인덱스 반환, 없으면 -1 반환
        st = 0
        ed = len(chunk) // 12 - 1
        temp = -1 # 검색 결과
        while st <= ed:
            mid = (st + ed) // 2
            piv = chunk[mid * 12:mid * 12 + 12]
            if piv > fptr:
                ed = mid - 1
            elif piv < fptr:
                st = mid + 1
            else:
                temp = mid
                st = 0
                ed = -1
        return temp

    def insert(self, chunk, fptr): # 정렬된 12B * n chunk 에 fptr 삽입, 청크 반환
        st = 0
        ed = len(chunk) // 12 - 1
        mid = 0 # 삽입 위치
        while st < ed:
            mid = (st + ed) // 2
            piv = chunk[mid * 12:mid * 12 + 12]
            if piv > fptr:
                ed = mid - 1
            elif piv < fptr:
                st = mid + 1
            else:
                raise Exception('fptrexist')
        if st == ed:
            piv = chunk[st * 12:st * 12 + 12]
            if piv > fptr:
                mid = st
            elif piv < fptr:
                mid = st + 1
            else:
                raise Exception('fptrexist')
        if mid == 0:
            return fptr + chunk
        elif mid == len(chunk) // 12:
            return chunk + fptr
        else:
            return chunk[0:12 * mid] + fptr + chunk[12 * mid:]

class toolbox:
    
    def __init__(self, path): # cluster path
        self.channel = os.path.abspath(path).replace('\\', '/') # 클러스터 경로
        self.fptr = [ ] # 포인터 리스트
        self.valid = False # 올바른 클러스터 여부
        self.empty = False # 빈 폴더 여부
        self.t = infunc() # infunc
        self.num = 5000 # 컨테이너당 파일 수
        temp = os.listdir(path)
        if 'header.kv4' in temp and '0' in temp:
            self.valid = True
        elif temp == [ ]:
            self.empty = True
        if self.valid:
            num = 0 # 존재하는 컨테이너 본호 + 1
            while str(num) in temp:
                num = num + 1
            p = mp.Pool(8)
            self.fptr = [0] * num
            for i in range(0, num // 8):
                for j in range(0, 8):
                    self.fptr[8 * i + j] = p.apply_async( self.t.getfptr, ( self.channel + '/' + str(8 * i + j), ) )
                for j in range(0, 8):
                    self.fptr[8 * i + j] = self.fptr[8 * i + j].get()
            count = num - num % 8
            for i in range(0, num % 8):
                self.fptr[count + i] = p.apply_async( self.t.getfptr, ( self.channel + '/' + str(count + i), ) )
            for i in range(0, num % 8):
                self.fptr[count + i] = self.fptr[count + i].get()
            p.close()
            p.join()

    def hpush(self, mhead, fsb, fkb): # mheader B, file sys enB, fptr key enB
        if not os.path.exists(self.channel + '/0'):
            os.mkdir(self.channel + '/0')
        if os.path.exists(self.channel + '/' + 'header.kv4.bck'):
            os.remove(self.channel + '/' + 'header.kv4.bck')
        if os.path.exists(self.channel + '/' + 'header.kv4'):
            os.rename(self.channel + '/' + 'header.kv4', self.channel + '/' + 'header.kv4.bck')
        with open(self.channel + '/' + 'header.kv4', 'wb') as f:
            f.write(b'KV4H')
            f.write( self.t.en8b( len(mhead) ) )
            f.write(mhead)
            f.write( self.t.en8b( len(fsb) ) )
            f.write(fsb)
            f.write( self.t.en8b( len(fkb) ) )
            f.write(fkb)

    def hpop(self): # vaild 여부 확인 필요
        if os.path.exists(self.channel + '/' + 'header.kv4'):
            with open(self.channel + '/' + 'header.kv4', 'rb') as f:
                if f.read(4) == b'KV4H':
                    temp = True
                    mhead = f.read( self.t.de8b( f.read(8) ) )
                    fsb = f.read( self.t.de8b( f.read(8) ) )
                    fkb = f.read( self.t.de8b( f.read(8) ) )
                else:
                    temp = False
        else:
            raise Exception('noheader') # err
        if temp:
            return [mhead, fsb, fkb]
        else:
            raise Exception('wrongheader') # err

    def fpush(self, path, fptr): # en file path, fptr 12B / fptr 사전 체크 필요
        temp = 0
        fin = True
        while fin:
            if len( self.fptr[temp] ) // 12 < self.num:
                fin = False
            else:
                temp = temp + 1
                if not os.path.exists( self.channel + '/' + str(temp) ):
                    os.mkdir( self.channel + '/' + str(temp) )
                    self.fptr.append(b'')
                    fin = False
        shutil.move(path, f'{self.channel}/{str(temp)}/{self.t.b64en(fptr)}.kv4')
        self.fptr[temp] = self.t.insert(self.fptr[temp], fptr)

    def fpop(self, path, fptr): # file path, en file fptr 12B
        temp = 0
        fin = True
        while fin:
            if self.t.find(self.fptr[temp], fptr) != -1:
                fin = False
            else:
                temp = temp + 1
                if temp == len(self.fptr):
                    fin = False
                    raise Exception('nofptr')
        shutil.copy(f'{self.channel}/{str(temp)}/{self.t.b64en(fptr)}.kv4', path)

    def fchk(self, fptr): # fptr 12B
        temp = 0
        out = True
        fin = True
        size = len(self.fptr)
        while fin:
            if self.t.find(self.fptr[temp], fptr) != -1:
                fin = False
            else:
                temp = temp + 1
                if temp == size:
                    out = False
                    fin = False
        return out

    def finfo(self, fptr): # fptr 12B
        # 반환 : [물리 위치, 포인터 바이트, 크기, 생성 날자, 수정 날자, 엑세스 날자]
        temp = 0
        out = True
        fin = True
        size = len(self.fptr)
        while fin:
            if self.t.find(self.fptr[temp], fptr) != -1:
                fin = False
            else:
                temp = temp + 1
                if temp == size:
                    out = False
                    fin = False
        if out:
            path = f'{self.channel}/{str(temp)}/{self.t.b64en(fptr)}.kv4'
            data = [ path, fptr, os.path.getsize(path) ]
            data.append( time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( os.path.getctime(path) ) ) )
            data.append( time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( os.path.getmtime(path) ) ) )
            data.append( time.strftime( '%Y-%m-%d_%H:%M:%S' , time.localtime( os.path.getatime(path) ) ) )
            return data
        else:
            raise Exception('nofptr')

    def fdel(self, fptr): # fptr 12B
        temp = 0
        out = True
        fin = True
        size = len(self.fptr)
        while fin:
            if self.t.find(self.fptr[temp], fptr) != -1:
                fin = False
            else:
                temp = temp + 1
                if temp == size:
                    out = False
                    fin = False
        if out:
            path = f'{self.channel}/{str(temp)}/{self.t.b64en(fptr)}.kv4'
            os.remove(path)
            chunk = self.fptr[temp]
            num = self.t.find(chunk, fptr)
            if num == len(chunk) // 12 - 1:
                self.fptr[temp] = chunk[0:12 * num]
            else:
                self.fptr[temp] = chunk[0:12 * num] + chunk[12 * num + 12:]
        else:
            raise Exception('nofptr') # err

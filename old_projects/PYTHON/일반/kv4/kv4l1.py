# KVault4 Layer 1

import os
import shutil
import multiprocessing as mp

import oreo
import mung2
import kaes4hy as en4hy
import kv4l0 as fio

class infunc:

    def __init__(self):
        self.otool = oreo.toolbox() # oreo tool
        self.mtool = mung2.toolbox() # mung2 tool
        self.en4 = en4hy.toolbox() # kaes4 tool
        if not self.en4.valid:
            raise Exception('notvalidKAES4') # err
        
        self.fk = b'' # fptr - key
        self.fs = b'' # file structure
        self.offset = [ ] # fs offset

    def getkey(self, fptr): # 키 반환 fptr 12B -> key 48B
        st = 0
        ed = len(self.fk) // 60 - 1
        temp = -1 # 검색 결과
        while st <= ed:
            mid = (st + ed) // 2
            piv = self.fk[mid * 60 : mid * 60 + 12]
            if piv > fptr:
                ed = mid - 1
            elif piv < fptr:
                st = mid + 1
            else:
                temp = mid
                st = 0
                ed = -1
        if temp == -1:
            raise Exception('nofptr') # err
        else:
            return self.fk[temp * 60 + 12 : temp * 60 + 60]

    def insertkey(self, fptr, key): # 키 삽입 fptr 12B, key 48B
        st = 0
        ed = len(self.fk) // 60 - 1
        mid = 0 # 삽입 위치
        while st < ed:
            mid = (st + ed) // 2
            piv = self.fk[mid * 60 : mid * 60 + 12]
            if piv > fptr:
                ed = mid - 1
            elif piv < fptr:
                st = mid + 1
            else:
                raise Exception('fptrexist') # err
        if st == ed:
            piv = self.fk[st * 60 : st * 60 + 12]
            if piv > fptr:
                mid = st
            elif piv < fptr:
                mid = st + 1
            else:
                raise Exception('fptrexist') # err
        if mid == 0:
            self.fk = fptr + key + self.fk
        elif mid == len(self.fk) // 60:
            self.fk = self.fk + fptr + key
        else:
            self.fk = self.fk[0:60 * mid] + fptr + key + self.fk[60 * mid:]

    def delkey(self, fptr): # 키 삭제 fptr 12B
        st = 0
        ed = len(self.fk) // 60 - 1
        temp = -1 # 검색 결과
        while st <= ed:
            mid = (st + ed) // 2
            piv = self.fk[mid * 60 : mid * 60 + 12]
            if piv > fptr:
                ed = mid - 1
            elif piv < fptr:
                st = mid + 1
            else:
                temp = mid
                st = 0
                ed = -1
        if temp == -1:
            raise Exception('nofptr') # err
        elif temp == len(self.fk) // 60:
            self.fk = self.fk[0:60 * temp]
        else:
            self.fk = self.fk[0:60 * temp] + self.fk[60 * temp + 60:]

    def offsetin(self, start, end): # offset calc inline, [st, ed), 각 항목의 시작 지점 기준
        out = [ ]
        for i in range(start, end):
            if self.fs[i] == 10: # b'\n' detect
                out.append(i + 1)
        return out

    def getoffset(self): # offset calc, 각 항목의 시작 지점 기준
        self.en4 = 0 # kaes4 mp
        temp = [0] * 16
        p = mp.Pool(16)
        size = len(self.fs)
        count = 0
        for i in range(0, 15):
            temp[i] = p.apply_async( self.offsetin, (count, count + size // 16) )
            count = count + size // 16
        temp[15] = p.apply_async( self.offsetin, (count, size) )
        out = [0]
        for i in range(0, 16):
            out.extend( temp[i].get() )
        p.close()
        p.join()
        out.pop(-1)
        self.offset = out
        self.en4 = en4hy.toolbox() # kaes4 mp

    def mkhead(self, pw, kf, hint, akey, tkey): # pw B, kf B, hint B, akey 48B, tkey 48B -> header B
        salt = self.en4.genrandom(32) # salt 32B
        pwh = self.en4.svkey(salt, pw, kf) # pwhash 256B
        mkey = self.en4.mkkey(salt, pw, kf) # master key 48B
        pw = b'0' * 64
        kf = b'0' * 64
        akeydt = self.en4.enshort(mkey[0:32], mkey[32:48], akey) # akey data 48B
        tkeydt = self.en4.enshort(mkey[0:32], mkey[32:48], tkey) # tkey data 48B
        akey = b'0' * 64
        tkey = b'0' * 64
        header = {'mode' : 'KV4', 'salt' : salt, 'pwh' : pwh, 'akdt' : akeydt, 'tkdt' : tkeydt, 'hint' : hint}
        header = bytes(self.en4.mkhead(header), 'utf-8')
        return header

    def rdhead(self, pw, kf, header): # pw B, kf B, header B -> akey 48B, tkey 48B
        header = self.en4.rdhead( str(header, 'utf-8') )
        if header['MODE'] == 'KV4':
            salt = header['SALT'] # salt 32B
            pwh = header['PWH'] # pwhash 256B
            akeydt = header['AKDT'] # akey data 48B
            tkeydt = header['TKDT'] # tkey data 48B
        else:
            raise Exception('notvalidHEAD') # err
        if self.en4.svkey(salt, pw, kf) == pwh:
            mkey = self.en4.mkkey(salt, pw, kf) # master key 48B
            pw = b'0' * 64
            kf = b'0' * 64
            akey = self.en4.deshort(mkey[0:32], mkey[32:48], akeydt) # akey 48B
            tkey = self.en4.deshort(mkey[0:32], mkey[32:48], tkeydt) # tkey 48B
            return [akey, tkey]
        else:
            raise Exception('notvalidKEY') # err

    def mknew(self): # [mh B, fs B, fk B]
        pw = b'0000'
        hint = bytes('빈 폴더를 선택해\n새 클러스터가 생성되었습니다.\n초기 비밀번호는\n0000 입니다.', 'utf-8')
        kf = en4hy.getkf('기본키파일')
        fptrkey = b''
        filesys = bytes('0#bin\n0#main\n', 'utf-8')
        akey = b'0' * 48
        tkey = b'1' * 48
        mhead = self.mkhead(pw, kf, hint, akey, tkey)
        fsb = self.en4.enfunc(tkey, filesys)
        fkb = self.en4.enfunc(akey, fptrkey)
        return [mhead, fsb, fkb]

    def fsinfof(self, offset): # offset int -> [depth int, type int]
        # 0 : struct, 1 : atom.sol, 2 : atom.zip
        size = len(self.offset) - 1
        if offset == size:
            temp = self.fs[self.offset[offset]:-1]
        else:
            temp = self.fs[self.offset[offset]:self.offset[offset + 1] - 1]
        cur = 0
        reg = [ ]
        while (temp[cur] != 36) and (temp[cur] != 35) and (temp[cur] != 38):
            reg.append( temp[cur] )
            cur = cur + 1
        depth = int( str(bytes(reg), 'utf-8') )
        reg = temp[cur]
        if reg == 36:
            tp = 1
        elif reg == 35:
            tp = 0
        else:
            tp = 2
        return [depth, tp]

    def fsinfow(self, offset): # offset int -> [depth int, type int, name str, fptr 12B]
        # 0 : struct, 1 : atom.sol, 2 : atom.zip
        size = len(self.offset) - 1
        if offset == size:
            temp = self.fs[self.offset[offset]:-1]
        else:
            temp = self.fs[self.offset[offset]:self.offset[offset + 1] - 1]
        cur = 0
        reg = [ ]
        while (temp[cur] != 36) and (temp[cur] != 35) and (temp[cur] != 38):
            reg.append( temp[cur] )
            cur = cur + 1
        depth = int( str(bytes(reg), 'utf-8') )
        reg = temp[cur]
        if reg == 36:
            tp = 1
            reg = [ ]
            cur = cur + 1
            while temp[cur] != 47:
                reg.append( temp[cur] )
                cur = cur + 1
            cur = cur + 1
            name = str(bytes(reg), 'utf-8')
            fptr = temp[cur:]
        elif reg == 35:
            tp = 0
            name = str(temp[cur + 1:], 'utf-8')
            fptr = b''
        else:
            tp = 2
            reg = [ ]
            cur = cur + 1
            while temp[cur] != 47:
                reg.append( temp[cur] )
                cur = cur + 1
            cur = cur + 1
            name = str(bytes(reg), 'utf-8')
            fptr = temp[cur:]
        return [depth, tp, name, fptr]

class toolbox:

    def __init__(self, path): # 클러스터 폴더 경로
        self.io = fio.toolbox(path) # io Layer 0
        self.tool = infunc() # infunc
        self.settings = self.tool.otool.readfile('settings.txt') # settings dict
        self.debug = 'init : -' # debug data -> more info str
        self.order = f'init : {path}' # debug data -> order info str

        self.mhead = b'' # current main header B
        self.akey = b'' # current akey 48B
        self.tkey = b'' # current tkey 48B
        self.fsb = b'' # temp filesys B
        self.fkb = b'' # temp filekey B

        if not self.io.valid:
            if self.io.empty:
                temp = self.tool.mknew()
                self.io.hpush( temp[0], temp[1], temp[2] )
                self.debug = 'init : made new cluster' # debug data
                raise Exception('newCLU') # 새 클러스터 생성 err
            else:
                self.debug = 'init : not valid cluster header' # debug data
                raise Exception('notvalidCLU') # 잘못된 클러스터 err

    def view(self): # -> hint B
        self.order = f'view : -' # debug data
        temp = self.io.hpop()
        self.mhead = temp[0]
        self.fsb = temp[1]
        self.fkb = temp[2]
        self.debug = f'view : mhl {len(self.mhead)}\nfsbl {len(self.fsb)}\nfkbl {len(self.fkb)}' # debug data
        temp = self.tool.en4.rdhead( str(self.mhead, 'utf-8') )
        if temp['MODE'] == 'KV4':
            return temp['HINT']
        else:
            self.debug = f'view : mode {temp["MODE"]}' # debug data
            raise Exception('notvalidHEAD') # err

    def read(self, pw, kfpath): # pw B, kfpath str
        self.order = f'read : {len(pw)} {len(kfpath)}' # debug data
        # 헤더 복호화
        kf = en4hy.getkf(kfpath)
        temp = self.tool.rdhead(pw, kf, self.mhead)
        self.akey = temp[0]
        self.tkey = temp[1]
        self.tool.fs = self.tool.en4.defunc(self.tkey, self.fsb)
        self.tool.fk = self.tool.en4.defunc(self.akey, self.fkb)
        self.fsb = b''
        self.fkb = b''
        self.debug = 'read : header decrypted' # debug data
        # 라운드 키 업데이트
        self.akey = self.tool.en4.genrandom(48)
        self.tkey = self.tool.en4.genrandom(48)
        hint = self.tool.en4.rdhead( str(self.mhead, 'utf-8') )['HINT']
        self.mhead = self.tool.mkhead(pw, kf, hint, self.akey, self.tkey)
        fsb = self.tool.en4.enfunc(self.tkey, self.tool.fs)
        fkb = self.tool.en4.enfunc(self.akey, self.tool.fk)
        pw = b'0' * 64
        kf = b'0' * 64
        kfpath = b'0' * 64
        self.io.hpush(self.mhead, fsb, fkb)
        self.debug = 'read : round key updated' # debug data
        # 오프셋 계산
        self.tool.getoffset()

    def getscope(self, num): # num int -> [st int, ed int], num 폴더의 범위 구하기, st 포함 시작 ed 포함 끝
        self.order = f'getscope : {num}' # debug data
        depth = self.tool.fsinfof(num)[0]
        start = num
        temp = num + 1 # 현재 탐색 지점
        size = len(self.tool.offset)
        fin = True
        while fin:
            if temp == size:
                fin = False
                self.debug = 'getscope : endby sizeover' # debug data
            elif self.tool.fsinfof(temp)[0] <= depth:
                fin = False
                self.debug = 'getscope : endby depthover' # debug data
            else:
                temp = temp + 1
        end = temp - 1
        return [start, end]

    def getlower(self, num): # num int -> [int], num 폴더의 직접 하위 항목 반환
        self.order = f'getlower : {num}' # debug data
        depth = self.tool.fsinfof(num)[0]
        out = [ ]
        temp = num + 1 # 현재 탐색 지점
        size = len(self.tool.offset)
        fin = True
        while fin:
            if temp == size:
                fin = False
                self.debug = 'getlower : endby sizeover' # debug data
            else:
                piv = self.tool.fsinfof(temp)[0]
                if piv <= depth:
                    fin = False
                    self.debug = 'getlower : endby depthover' # debug data
                elif piv == depth + 1:
                    out.append(temp)
                    temp = temp + 1
                else:
                    temp = temp + 1
        return out

    def getupper(self, num): # num int -> int, num 폴더의 직접 상위 항목 반환
        self.order = f'getupper : {num}' # debug data
        depth = self.tool.fsinfof(num)[0]
        if depth == 0:
            self.debug = f'getupper : depth {depth}\nnot exist' # debug data
            return -1 # num 최상단 폴더
        else:
            temp = num # 현재 탐색 대상
            while self.tool.fsinfof(temp)[0] != depth - 1:
                temp = temp - 1
                if temp < 0:
                    self.debug = f'getupper : depth {depth}\nnot exist' # debug data
                    return -1 # err/not exist
            self.debug = f'getupper : depth {depth}\nexist {temp}' # debug data
            return temp

    def getnum(self, path): # path str -> int, /로 구분된 폴더파일 경로로 번호 찾기
        self.order = f'getnum : {path}' # debug data
        path = [x for x in path.split('/') if x != '']
        size = len(self.tool.offset)
        temp = 0 # 현재 탐색 대상
        fin = True
        i = 0 # path name index
        while fin:
            if temp == size and i != len(path):
                self.debug = f'getnum : endby sizeover\ntemp {temp}\ni {i}' # debug data
                fin = False
                temp = -1
            elif i == len(path):
                self.debug = f'getnum : endby pathfind\ntemp {temp}\ni {i}' # debug data
                fin = False
                temp = temp - 1
            else:
                name = path[i]
            if fin:
                if name == self.tool.fsinfow(temp)[2]:
                    temp = temp + 1
                    i = i + 1
                else:
                    temp = self.getscope(temp)[1] + 1
        return temp

    def imfiles(self, fonum, paths, tempnum): # folder num int, paths list [str], temp folder num int
        # err/오류 발생시 임시 폴더 초기화, 함수 완료 후 임시 폴더 초기화, 폴더 여부 확인 필요
        self.order = f'imfiles : {fonum} {len(paths)} {tempnum}' # debug data
        paths = [os.path.abspath(x).replace('\\', '/') for x in paths]
        names = [x[x.rfind('/') + 1:] for x in paths]
        fptrs = [ ] # [12 B]
        for i in names:
            fin = True
            while fin:
                temp = self.tool.en4.genrandom(12)
                try:
                    self.tool.getkey(temp)
                    flag = False
                except:
                    flag = True
                if (flag) and (temp not in fptrs) and (b'\n' not in temp):
                    fptrs.append(temp)
                    fin = False
        keys = [self.tool.en4.genrandom(48) for x in names] # [48 B]
        try:
            shutil.rmtree(f'temp474_{tempnum}')
        except:
            pass
        os.mkdir(f'temp474_{tempnum}')
        self.debug = f'imfiles : mkfolder temp474_{tempnum}' # debug data
        for i in range( 0, len(names) ):
            self.tool.en4.enfunc(keys[i], paths[i], f'temp474_{tempnum}/{i}')
            
        # fio fpush
        result = [ ]
        for i in range( 0, len(names) ):
            try:
                self.io.fpush( f'temp474_{tempnum}/{i}', fptrs[i] )
                result.append('success')
            except Exception as e:
                result.append( str(e) )
        flag = True # 헤더 업데이트 flag
        for i in range( 0, len(names) ):
            if result[i] != 'success':
                flag = False
                self.debug = f'imfiles : i {i}\nfpush fail {result[i]}' # debug data
                try:
                    self.io.fdel( fptrs[i] )
                except:
                    pass

        # fs, fk update
        if flag:
            for i in range( 0, len(names) ): # fk update
                self.tool.insertkey( fptrs[i], keys[i] )
            depth = self.tool.fsinfof(fonum)[0] # 삽입 위치 폴더의 깊이
            fsin = b'' # 삽입될 파일 시스템 바이트
            if fonum == len(self.tool.offset) - 1:
                addt = len(self.tool.fs) # offset addition const
            else:
                addt = self.tool.offset[fonum + 1]
            offin = [ ] # 삽입될 offset
            for i in range( 0, len(names) ):
                offin.append(len(fsin) + addt)
                fsin = fsin + bytes(f'{depth + 1}${names[i]}/', 'utf-8') + fptrs[i] + b'\n'
            addfs = len(fsin) # 오프셋에 더해질 값
            if fonum == len(self.tool.offset) - 1: # fs update
                self.tool.fs = self.tool.fs + fsin
            else:
                self.tool.fs = self.tool.fs[0:addt] + fsin + self.tool.fs[addt:]
            self.debug = f'imfiles : fonum {fonum}\nfsinl {addfs}' # debug data
        else:
            self.debug = self.debug + f'\nflag {flag}' # debug data
            raise Exception('fpusherror') # err

        # fio hpush
        try:
            fsb = self.tool.en4.enfunc(self.tkey, self.tool.fs)
            fkb = self.tool.en4.enfunc(self.akey, self.tool.fk)
            self.io.hpush(self.mhead, fsb, fkb)
            self.debug = f'imfiles : hpush success\nfsl {len(self.tool.fs)}\nfkl {len(self.tool.fk)}' # debug data
            flag = True # offset update flag
        except Exception as e:
            self.debug = f'imfiles : hpush fail {e}\nfsl {len(self.tool.fs)}\nfkl {len(self.tool.fk)}' # debug data
            flag = False

        # offset update
        if flag:
            for i in range( fonum + 1, len(self.tool.offset) ):
                self.tool.offset[i] = self.tool.offset[i] + addfs
            if fonum == len(self.tool.offset) - 1:
                self.tool.offset = self.tool.offset + offin
            else:
                self.tool.offset = self.tool.offset[0:fonum + 1] + offin + self.tool.offset[fonum + 1:]
            self.debug = f'imfiles : offset updated\noffl {len(self.tool.offset)}' # debug data
        else:
            for i in range( 0, len(names) ): # fptr update
                try:
                    self.io.fdel( fptrs[i] )
                except:
                    pass
            for i in range( 0, len(names) ): # fk update
                self.tool.delkey( fptrs[i] )
            if fonum == len(self.tool.offset) - 1: # fs update
                self.tool.fs = self.tool.fs[0:addt]
            else:
                self.tool.fs = self.tool.fs[0:addt] + self.tool.fs[addt + addfs:]
            self.debug = f'imfiles : recovered\nfsl {len(self.tool.fs)}\nfkl {len(self.tool.fk)}' # debug data
            try:
                fsb = self.tool.en4.enfunc(self.tkey, self.tool.fs)
                fkb = self.tool.en4.enfunc(self.akey, self.tool.fk)
                self.io.hpush(self.mhead, fsb, fkb)
                self.debug = self.debug + '\nrecover hpush success' # debug data
            except Exception as e:
                self.debug = self.debug + f'\nrecover hpush fail {e}' # debug data
            raise Exception('hpusherror') # err

    def imfolder(self, fonum, path, tempnum): # folder num int, folder path str, temp folder num int
        # err/오류 발생시 임시 폴더 초기화, 함수 완료 후 임시 폴더 초기화, 폴더 여부 확인 필요
        self.order = f'imfolder : {fonum} {path} {tempnum}' # debug data
        path = os.path.abspath(path).replace('\\', '/')
        name = path[path.rfind('/') + 1:]
        fin = True
        while fin:
            fptr = self.tool.en4.genrandom(12) # fptr 12B
            try:
                self.tool.getkey(fptr)
            except:
                if b'\n' not in fptr:
                    fin = False
        key = self.tool.en4.genrandom(48) # key 48B
        try:
            shutil.rmtree(f'temp474_{tempnum}')
        except:
            pass
        os.mkdir(f'temp474_{tempnum}')
        self.debug = f'imfolder : mkfolder temp474_{tempnum}' # debug data
        self.tool.mtool.pack(path.replace('/', '\\'), f'temp474_{tempnum}/pack', False) 
        self.tool.en4.enfunc(key, f'temp474_{tempnum}/pack', f'temp474_{tempnum}/0')
        try:
            shutil.rmtree('temp261')
        except:
            pass

        # fio fpush
        try:
            self.io.fpush(f'temp474_{tempnum}/0', fptr)
            flag = True # 헤더 업데이트 flag
        except Exception as e:
            flag = False
            self.debug = f'imfolder : fpush fail {e}' # debug data

        # fs, fk update
        if flag:
            self.tool.insertkey(fptr, key) # fk update
            depth = self.tool.fsinfof(fonum)[0] # 삽입 위치 폴더의 깊이
            fsin = b'' # 삽입될 파일 시스템 바이트
            if fonum == len(self.tool.offset) - 1:
                addt = len(self.tool.fs) # offset addition const
            else:
                addt = self.tool.offset[fonum + 1]
            offin = addt # 삽입될 offset
            fsin = bytes(f'{depth + 1}&{name}/', 'utf-8') + fptr + b'\n'
            addfs = len(fsin) # 오프셋에 더해질 값
            if fonum == len(self.tool.offset) - 1: # fs update
                self.tool.fs = self.tool.fs + fsin
            else:
                self.tool.fs = self.tool.fs[0:addt] + fsin + self.tool.fs[addt:]
            self.debug = f'imfolder : fonum {fonum}\nfsinl {addfs}' # debug data
        else:
            self.debug = self.debug + f'\nflag {flag}' # debug data
            raise Exception('fpusherror') # err

        # fio hpush
        try:
            fsb = self.tool.en4.enfunc(self.tkey, self.tool.fs)
            fkb = self.tool.en4.enfunc(self.akey, self.tool.fk)
            self.io.hpush(self.mhead, fsb, fkb)
            self.debug = f'imfolder : hpush success\nfsl {len(self.tool.fs)}\nfkl {len(self.tool.fk)}' # debug data
            flag = True # offset update flag
        except Exception as e:
            self.debug = f'imfolder : hpush fail {e}\nfsl {len(self.tool.fs)}\nfkl {len(self.tool.fk)}' # debug data
            flag = False

        # offset update
        if flag:
            for i in range( fonum + 1, len(self.tool.offset) ):
                self.tool.offset[i] = self.tool.offset[i] + addfs
            if fonum == len(self.tool.offset) - 1:
                self.tool.offset.append(offin)
            else:
                self.tool.offset.insert(fonum + 1, offin)
            self.debug = f'imfolder : offset updated\noffl {len(self.tool.offset)}' # debug data
        else:
            try:
                self.io.fdel(fptr) # fptr update
            except:
                pass
            self.tool.delkey(fptr) # fk update
            if fonum == len(self.tool.offset) - 1: # fs update
                self.tool.fs = self.tool.fs[0:addt]
            else:
                self.tool.fs = self.tool.fs[0:addt] + self.tool.fs[addt + addfs:]
            self.debug = f'imfolder: recovered\nfsl {len(self.tool.fs)}\nfkl {len(self.tool.fk)}' # debug data
            try:
                fsb = self.tool.en4.enfunc(self.tkey, self.tool.fs)
                fkb = self.tool.en4.enfunc(self.akey, self.tool.fk)
                self.io.hpush(self.mhead, fsb, fkb)
                self.debug = self.debug + '\nrecover hpush success' # debug data
            except Exception as e:
                self.debug = self.debug + f'\nrecover hpush fail {e}' # debug data
            raise Exception('hpusherror') # err

    def newfolder(self, fonum, name): # folder num int, folder name str
        self.order = f'newfolder : {fonum} {name}' # debug data

        # fs update
        depth = self.tool.fsinfof(fonum)[0] # 삽입 위치 폴더의 깊이
        fsin = b'' # 삽입될 파일 시스템 바이트
        if fonum == len(self.tool.offset) - 1:
            addt = len(self.tool.fs) # offset addition const
        else:
            addt = self.tool.offset[fonum + 1]
        offin = addt # 삽입될 offset
        fsin = bytes(f'{depth + 1}#{name}\n', 'utf-8')
        addfs = len(fsin) # 오프셋에 더해질 값
        if fonum == len(self.tool.offset) - 1: # fs update
            self.tool.fs = self.tool.fs + fsin
        else:
            self.tool.fs = self.tool.fs[0:addt] + fsin + self.tool.fs[addt:]
        self.debug = f'newfolder : fonum {fonum}\nfsinl {addfs}' # debug data

        # fio hpush
        try:
            fsb = self.tool.en4.enfunc(self.tkey, self.tool.fs)
            fkb = self.tool.en4.enfunc(self.akey, self.tool.fk)
            self.io.hpush(self.mhead, fsb, fkb)
            self.debug = f'newfolder : hpush success\nfsl {len(self.tool.fs)}\nfkl {len(self.tool.fk)}' # debug data
            flag = True # offset update flag
        except Exception as e:
            self.debug = f'newfolder : hpush fail {e}\nfsl {len(self.tool.fs)}\nfkl {len(self.tool.fk)}' # debug data
            flag = False

        # offset update
        if flag:
            for i in range( fonum + 1, len(self.tool.offset) ):
                self.tool.offset[i] = self.tool.offset[i] + addfs
            if fonum == len(self.tool.offset) - 1:
                self.tool.offset.append(offin)
            else:
                self.tool.offset.insert(fonum + 1, offin)
            self.debug = f'newfolder : offset updated\noffl {len(self.tool.offset)}' # debug data
        else:
            if fonum == len(self.tool.offset) - 1: # fs update
                self.tool.fs = self.tool.fs[0:addt]
            else:
                self.tool.fs = self.tool.fs[0:addt] + self.tool.fs[addt + addfs:]
            self.debug = f'newfolder : recovered\nfsl {len(self.tool.fs)}\nfkl {len(self.tool.fk)}' # debug data
            try:
                fsb = self.tool.en4.enfunc(self.tkey, self.tool.fs)
                fkb = self.tool.en4.enfunc(self.akey, self.tool.fk)
                self.io.hpush(self.mhead, fsb, fkb)
                self.debug = self.debug + '\nrecover hpush success' # debug data
            except Exception as e:
                self.debug = self.debug + f'\nrecover hpush fail {e}' # debug data
            raise Exception('hpusherror') # err

    def exatoms(self, nums, path, tempnum): # atoms num [int], tgt path str, temp folder num int
        # err/오류 발생시 임시 폴더 초기화, 함수 완료 후 임시 폴더 초기화, 파일 여부 확인 필요
        self.order = f'exatoms : {len(nums)} {path}' # debug data
        path = os.path.abspath(path).replace('\\', '/')
        try:
            shutil.rmtree(f'temp474_{tempnum}')
        except:
            pass
        os.mkdir(f'temp474_{tempnum}')

        for i in range( 0, len(nums) ):
            info = self.tool.fsinfow( nums[i] )
            if info[1] == 1: # atom.sol
                try:
                    key = self.tool.getkey( info[3] ) # key 48B
                    name = info[2] # name str
                except:
                    self.debug = f'exatoms : nokeyerr\nfptr {info[3]}' # debug data
                    raise Exception('notvalidFPTR') # err
                try:
                    self.io.fpop( f'temp474_{tempnum}/{i}', info[3] )
                except Exception as e:
                    self.debug = f'exatoms : fpoperr {e}' # debug data
                    raise Exception('fpoperr') # err
                try:
                    self.tool.en4.defunc(key, f'temp474_{tempnum}/{i}', f'{path}/{name}')
                except Exception as e:
                    self.debug = f'exatoms : decrypterr {e}' # debug data
                    raise Exception('decrypterr') # err
                    
            elif info[1] == 2: # atom.zip
                try:
                    key = self.tool.getkey( info[3] ) # key 48B
                    name = info[2] # name str
                except:
                    self.debug = f'exatoms : nokeyerr\nfptr {info[3]}' # debug data
                    raise Exception('notvalidFPTR') # err
                try:
                    self.io.fpop( f'temp474_{tempnum}/{i}', info[3] )
                except Exception as e:
                    self.debug = f'exatoms : fpoperr {e}' # debug data
                    raise Exception('fpoperr') # err
                try:
                    self.tool.en4.defunc(key, f'temp474_{tempnum}/{i}', f'temp474_{tempnum}/{i}.pack')
                except Exception as e:
                    self.debug = f'exatoms : decrypterr {e}' # debug data
                    raise Exception('decrypterr') # err
                try:
                    self.tool.mtool.unpack(f'temp474_{tempnum}/{i}.pack')
                    shutil.move(f'temp261/{os.listdir("temp261")[0]}', f'{path}/{name}')
                    shutil.rmtree('temp261')
                except Exception as e:
                    self.debug = f'exatoms : unziperr {e}' # debug data
                    raise Exception('unziperr') # err

    def delete(self, num): # atom/struct num int
        self.order = f'delete : {num}' # debug data

        scope = self.getscope(num) # [st, ed], 포함 오프셋 정수
        fsst = self.tool.offset[ scope[0] ] # fs 포함 위치
        if scope[1] == len(self.tool.offset) - 1:
            fslen = len(self.tool.fs) - fsst # fs 구간 길이
        else:
            fslen = self.tool.offset[scope[1] + 1] - fsst
        fptrs = [ ] # 포함된 fptr 주소들
        for i in range(scope[0], scope[1] + 1):
            temp = self.tool.fsinfow(i)
            if temp[1] != 0:
                fptrs.append( temp[3] )
        keys = [ ] # fptr - keys
        for i in fptrs:
            keys.append( self.tool.getkey(i) )
        self.debug = f'delete : scope {scope}\nfsst {fsst} fslen {fslen}\nfptrsl {len(fptrs)} keysl {len(keys)}' # debug data

        # fs, fk update
        if fsst + fslen == len(self.tool.fs):
            frag = self.tool.fs[fsst:]
        else:
            frag = self.tool.fs[fsst:fsst + fslen] # delete fragment
        if fsst + fslen == len(self.tool.fs):
            self.tool.fs = self.tool.fs[0:fsst]
        else:
            self.tool.fs = self.tool.fs[0:fsst] + self.tool.fs[fsst + fslen:]
        for i in fptrs:
            self.tool.delkey(i)

        # fio hpush
        try:
            fsb = self.tool.en4.enfunc(self.tkey, self.tool.fs)
            fkb = self.tool.en4.enfunc(self.akey, self.tool.fk)
            self.io.hpush(self.mhead, fsb, fkb)
            self.debug = f'delete : hpush success\nfsl {len(self.tool.fs)}\nfkl {len(self.tool.fk)}' # debug data
            flag = True # offset update flag
        except Exception as e:
            self.debug = f'delete : hpush fail {e}\nfsl {len(self.tool.fs)}\nfkl {len(self.tool.fk)}' # debug data
            flag = False

        # fio fdel
        if flag:
            for i in fptrs:
                try:
                    self.io.fdel(i)
                except:
                    pass
        else:
            if fsst == len(self.tool.fs): # fs recover
                self.tool.fs = self.tool.fs + frag
            else:
                self.tool.fs = self.tool.fs[0:fsst] + frag + self.tool.fs[fsst:]
            for i in range( 0, len(fptrs) ): # fk recover
                self.tool.insertkey( fptrs[i], keys[i] )
            try:
                fsb = self.tool.en4.enfunc(self.tkey, self.tool.fs)
                fkb = self.tool.en4.enfunc(self.akey, self.tool.fk)
                self.io.hpush(self.mhead, fsb, fkb)
                self.debug = f'delete : recover success\nfsl {len(self.tool.fs)}\nfkl {len(self.tool.fk)}' # debug data
            except Exception as e:
                self.debug = f'delete : recover fail {e}\nfsl {len(self.tool.fs)}\nfkl {len(self.tool.fk)}' # debug data
            raise Exception('hpusherr') # err

        # offset update
        if flag:
            if scope[1] == len(self.tool.offset) - 1:
                self.tool.offset = self.tool.offset[ 0:scope[0] ]
            else:
                self.tool.offset = self.tool.offset[ 0:scope[0] ] + self.tool.offset[scope[1] + 1:]
            for i in range( scope[0], len(self.tool.offset) ):
                self.tool.offset[i] = self.tool.offset[i] - fslen
            self.debug = f'delete : offset updated\noffl {len(self.tool.offset)}' # debug data

    def rename(self, num, name): # tgt num int, newname str
        self.order = f'rename : {num} {name}' # debug data

        st = self.tool.offset[num] # fs chunk 포함 시작점
        if num == len(self.tool.offset) - 1:
            ed = len(self.tool.fs) - 1 # fs chunk 포함 종점
            oldfrag = self.tool.fs[st:] # old fragment
        else:
            ed = self.tool.offset[num + 1] - 1
            oldfrag = self.tool.fs[st:ed + 1] # old fragment
        info = self.tool.fsinfow(num) # fs info
        if info[1] == 0:
            newfrag = bytes(f'{info[0]}#{name}\n', 'utf-8') # new fragment
        elif info[1] == 1:
            newfrag = bytes(f'{info[0]}${name}/', 'utf-8') + info[3] + b'\n'
        else:
            newfrag = bytes(f'{info[0]}&{name}/', 'utf-8') + info[3] + b'\n'
        offadd = len(newfrag) - len(oldfrag) # 더할 오프셋 상수
        self.debug = f'rename : oldfrag {oldfrag}\nnewfrag{newfrag}\nst {st} ed {ed}' # debug data

        # fs update
        if num == len(self.tool.offset) - 1:
            self.tool.fs = self.tool.fs[0:st] + newfrag
        else:
            self.tool.fs = self.tool.fs[0:st] + newfrag + self.tool.fs[ed + 1:]

        # fio hpush
        try:
            fsb = self.tool.en4.enfunc(self.tkey, self.tool.fs)
            fkb = self.tool.en4.enfunc(self.akey, self.tool.fk)
            self.io.hpush(self.mhead, fsb, fkb)
            self.debug = f'rename : hpush success\nfsl {len(self.tool.fs)}\nfkl {len(self.tool.fk)}' # debug data
            flag = True # offset update flag
        except Exception as e:
            self.debug = f'rename : hpush fail {e}\nfsl {len(self.tool.fs)}\nfkl {len(self.tool.fk)}' # debug data
            flag = False

        # offset update
        if flag:
            for i in range( num + 1, len(self.tool.offset) ): # offset update
                self.tool.offset[i] = self.tool.offset[i] + offadd
            self.debug = f'rename : offset updated\noffl {len(self.tool.offset)}' # debug data
        else:
            if num == len(self.tool.offset) - 1: # fs update
                self.tool.fs = self.tool.fs[0:st] + oldfrag
            else:
                self.tool.fs = self.tool.fs[0:st] + oldfrag + self.tool.fs[ed + 1 + offadd:]
            try:
                fsb = self.tool.en4.enfunc(self.tkey, self.tool.fs)
                fkb = self.tool.en4.enfunc(self.akey, self.tool.fk)
                self.io.hpush(self.mhead, fsb, fkb)
                self.debug = f'rename : recover success\nfsl {len(self.tool.fs)}\nfkl {len(self.tool.fk)}' # debug data
            except Exception as e:
                self.debug = f'rename : recover fail {e}\nfsl {len(self.tool.fs)}\nfkl {len(self.tool.fk)}' # debug data
            raise Exception('hpusherr') # err

    def move(self, srcnum, dstnum): # scr num int, dst num int, src struct/atom -> move to under dst struct
        self.order = f'move : {srcnum} {dstnum}' # debug data

        depths = [ ] # [int]
        types = [ ] # [int]
        names = [ ] # [str]
        fptrs = [ ] # [bytes]
        temp = self.getscope(srcnum)
        stnum = temp[0] # 포함 시작 num
        ednum = temp[1] # 포함 종료 num

        for i in range(stnum, ednum + 1):
            temp = self.tool.fsinfow(i)
            depths.append( temp[0] )
            types.append( temp[1] )
            names.append( temp[2] )
            if temp[1] == 0:
                fptrs.append(b'')
            else:
                fptrs.append( temp[3] )

        olddepth = self.tool.fsinfof(srcnum)[0] - 1 # src 항목이 위치하는 스트럭트의 깊이
        newdepth = self.tool.fsinfow(dstnum)[0] # dst 스트럭트의 깊이
        depthcon = newdepth - olddepth # depth 보정 const
        self.debug = f'move : stnum {stnum} ednum {ednum}\nolddepth {olddepth} newdepth {newdepth}' # debug data

        if ednum == len(self.tool.offset) - 1:
            oldfrag = self.tool.fs[self.tool.offset[stnum]:] # old fs fragment
        else:
            oldfrag = self.tool.fs[ self.tool.offset[stnum]:self.tool.offset[ednum + 1] ]
        newfrag = [ ]
        for i in range( 0, len(depths) ):
            if types[i] == 0:
                newfrag.append( bytes(f'{depths[i] + depthcon}#{names[i]}\n', 'utf-8') )
            elif types[i] == 1:
                newfrag.append( bytes(f'{depths[i] + depthcon}${names[i]}/', 'utf-8') + fptrs[i] + b'\n' )
            else:
                newfrag.append( bytes(f'{depths[i] + depthcon}&{names[i]}/', 'utf-8') + fptrs[i] + b'\n' )
        newfrag = b''.join(newfrag)

        # fs update
        # partA (partB / tgt) partC
        if dstnum < stnum:
            parta = self.tool.fs[ 0:self.tool.offset[dstnum + 1] ]
            partb = self.tool.fs[ self.tool.offset[dstnum + 1]:self.tool.offset[stnum] ]
            if ednum == len(self.tool.offset) - 1:
                partc = b''
            else:
                partc = self.tool.fs[self.tool.offset[ednum + 1]:]
            self.tool.fs = parta + newfrag + partb + partc
        elif dstnum > ednum:
            parta = self.tool.fs[ 0:self.tool.offset[stnum] ]
            if dstnum == len(self.tool.offset) - 1:
                partb = self.tool.fs[self.tool.offset[ednum + 1]:]
                partc = b''
            else:
                partb = self.tool.fs[ self.tool.offset[ednum + 1]:self.tool.offset[dstnum + 1] ]
                partc = self.tool.fs[self.tool.offset[dstnum + 1]:]
            self.tool.fs = parta + partb + newfrag + partc
        else:
            self.debug = f'move : stnum {stnum} ednum {ednum} dstnum {dstnum}' # debug data
            raise Exception('notvalidDST') # err

        # fio hpush
        try:
            fsb = self.tool.en4.enfunc(self.tkey, self.tool.fs)
            fkb = self.tool.en4.enfunc(self.akey, self.tool.fk)
            self.io.hpush(self.mhead, fsb, fkb)
            self.debug = f'move : hpush success\nfsl {len(self.tool.fs)}' # debug data
            flag = True # offset update flag
        except Exception as e:
            self.debug = f'move : hpush fail {e}\nfsl {len(self.tool.fs)}' # debug data
            flag = False

        # offset update
        if flag:
            parta = b''
            partb = b''
            partc = b''
            oldfrag = b''
            newfrag = b''
            self.tool.getoffset()
            self.debug = f'move : offset updated\noffl {len(self.tool.offset)}' # debug data
        else:
            if dstnum < stnum:
                self.tool.fs = parta + partb + oldfrag + partc
            elif dstnum > ednum:
                self.tool.fs = parta + oldfrag + partb + partc
            parta = b''
            partb = b''
            partc = b''
            oldfrag = b''
            newfrag = b''
            try:
                fsb = self.tool.en4.enfunc(self.tkey, self.tool.fs)
                fkb = self.tool.en4.enfunc(self.akey, self.tool.fk)
                self.io.hpush(self.mhead, fsb, fkb)
                self.debug = f'move : recover success\nfsl {len(self.tool.fs)}' # debug data
            except Exception as e:
                self.debug = f'move : recover fail {e}\nfsl {len(self.tool.fs)}' # debug data
            raise Exception('hpusherr') # err

    def info(self, num): # struct/atom num int -> [ ]
        # 반환 : [물리 위치, 포인터 바이트, 크기, 생성 날자, 수정 날자, 엑세스 날자, 파일 키]
        # 반환 : [하위 폴더 수, 하위 파일 수, 하위 파일들 크기]
        self.order = f'info : {num}' # debug data

        if self.tool.fsinfof(num)[1] == 0:
            num0 = 0 # 하위 폴더수
            num1 = 0 # 하위 파일 수
            num2 = 0 # 하위 파일 크기
            for i in range(num + 1, self.getscope(num)[1] + 1):
                if self.tool.fsinfof(i)[1] == 0:
                    num0 = num0 + 1
                else:
                    num1 = num1 + 1
                    num2 = num2 + self.io.finfo( self.tool.fsinfow(i)[3] )[2]
            temp = [num0, num1, num2]
        else:
            fptr = self.tool.fsinfow(num)[3]
            temp = self.io.finfo(fptr)
            temp.append( self.tool.getkey(fptr) )
        self.debug = f'info : {temp}' # debug data
        return temp

    def pwset(self, pw, kfpath, hint): # pw B, kfpath str, hint B
        self.order = f'pwset : pwl {len(pw)} kfpl {len(kfpath)} hl {len(hint)}' # debug data
        
        kf = en4hy.getkf(kfpath)
        self.akey = self.tool.en4.genrandom(48)
        self.tkey = self.tool.en4.genrandom(48)
        self.mhead = self.tool.mkhead(pw, kf, hint, self.akey, self.tkey)
        pw = b'0' * 64
        kfpath = b'0' * 64
        kf = b'0' * 64
        fsb = self.tool.en4.enfunc(self.tkey, self.tool.fs)
        fkb = self.tool.en4.enfunc(self.akey, self.tool.fk)
        try:
            self.io.hpush(self.mhead, fsb, fkb)
            self.io.hpush(self.mhead, fsb, fkb)
            self.io.hpush(self.mhead, fsb, fkb)
            self.debug = f'pwset : hpush success\nmhl {len(self.mhead)}\nfsl {len(self.tool.fs)}\nfkl {len(self.tool.fk)}' # debug data
        except Exception as e:
            self.debug = f'pwset : hpush fail {e}\nmhl {len(self.mhead)}\nfsl {len(self.tool.fs)}\nfkl {len(self.tool.fk)}' # debug data

    def schin(self, st, ed, word): # st 포함, ed 미포함 검색, search inline
        out = [ ]
        for i in range(st, ed):
            info = self.tool.fsinfow(i)
            if word in info[2]:
                num = i
                if info[1] == 0:
                    temp = f'{info[2]}/'
                else:
                    temp = f'{info[2]}'
                while info[0] != 0:
                    num = self.getupper(num)
                    info = self.tool.fsinfow(num)
                    temp = f'{info[2]}/{temp}'
                out.append(temp)
        return out

    def search(self, fonum, word): # fonum folder num int, tgt word str -> [str]
        self.order = f'search : {fonum} {word}' # debug data
        
        self.tool.en4 = 0 # kaes4 mp
        temp = self.getscope(fonum)
        stnum = temp[0]
        ednum = temp[1] + 1
        out = [ ]
        temp = [0] * 16
        p = mp.Pool(16)
        count = (ednum - stnum) // 16
        for i in range(0, 15):
            temp[i] = p.apply_async( self.schin, (stnum + count * i, stnum + count * (i + 1), word) )
        temp[15] = p.apply_async( self.schin, (stnum + count * 15, ednum, word) )
        for i in range(0, 16):
            out.extend( temp[i].get() )
        p.close()
        p.join()
        self.tool.en4 = en4hy.toolbox() # kaes4 mp
        self.debug = f'search : stnum {stnum}\nednum {ednum - 1}\nresultl {len(out)}' # debug data
        return out

    def namesort(self, fonum): # fonum folder num int
        self.order = f'namesort : {fonum}' # debug data

        if fonum != len(self.tool.offset) - 1: # 가장 마지막이 아님
            lowers = self.getlower(fonum)
            if lowers != [ ]: # 하위 항목 존재
                temp = self.getscope(fonum)
                stnum = temp[0] + 1
                ednum = temp[1]
                oldnames = [ ]
                oldwords = [ ]
                for i in range(0, len(lowers) - 1):
                    oldnames.append( self.tool.fsinfow( lowers[i] )[2] )
                    oldwords.append( self.tool.fs[ self.tool.offset[ lowers[i] ]:self.tool.offset[ lowers[i + 1] ] ] )
                if lowers[-1] == len(self.tool.offset) - 1:
                    oldnames.append( self.tool.fsinfow( lowers[-1] )[2] )
                    oldwords.append( self.tool.fs[self.tool.offset[ lowers[-1] ]:] )
                else:
                    if ednum == len(self.tool.offset) - 1:
                        oldnames.append( self.tool.fsinfow( lowers[-1] )[2] )
                        oldwords.append( self.tool.fs[self.tool.offset[ lowers[-1] ]:] )
                    else:
                        oldnames.append( self.tool.fsinfow( lowers[-1] )[2] )
                        oldwords.append( self.tool.fs[ self.tool.offset[ lowers[-1] ]:self.tool.offset[ednum + 1] ] )
                
            else:
                self.debug = f'namesort : no lower struct/atom' # debug data
                raise Exception('nosort') # err
        else:
            self.debug = f'namesort : last struct' # debug data
            raise Exception('nosort') # err

        oldfrag = b''.join(oldwords)
        newnames = [ ]
        newwords = [ ]
        while oldnames != [ ]:
            name = oldnames[-1]
            word = oldwords[-1]
            oldnames.pop(-1)
            oldwords.pop(-1)
            temp = 0
            if newnames == [ ]:
                newnames.append(name)
                newwords.append(word)
            else:
                while ( temp < len(newnames) ) and (newnames[temp] < name):
                    temp = temp + 1
                newnames.insert(temp, name)
                newwords.insert(temp, word)
        self.debug = f'namesort : stnum {stnum - 1}\nednum {ednum}\nnamel {len(newnames)}' # debug data

        # partA (names) partB
        newfrag = b''.join(newwords)
        oldnames = [ ]
        newnames = [ ]
        oldwords = [ ]
        newwords = [ ]
        parta = self.tool.fs[ 0:self.tool.offset[stnum] ]
        if ednum == len(self.tool.offset) - 1:
            partb = b''
        else:
            partb = self.tool.fs[self.tool.offset[ednum + 1]:]

        # fs update
        self.tool.fs = parta + newfrag + partb

        # fio hpush
        try:
            fsb = self.tool.en4.enfunc(self.tkey, self.tool.fs)
            fkb = self.tool.en4.enfunc(self.akey, self.tool.fk)
            self.io.hpush(self.mhead, fsb, fkb)
            self.debug = f'namesort : hpush success\nfsl {len(self.tool.fs)}' # debug data
            flag = True # offset update flag
        except Exception as e:
            self.debug = f'namesort : hpush fail {e}\nfsl {len(self.tool.fs)}' # debug data
            flag = False

        # offset update
        if flag:
            parta = b''
            partb = b''
            oldfrag = b''
            newfrag = b''
            self.tool.getoffset()
            self.debug = f'namesort : offset updated\noffl {len(self.tool.offset)}' # debug data
        else:
            self.tool.fs = parta + oldfrag + partb
            parta = b''
            partb = b''
            oldfrag = b''
            newfrag = b''
            try:
                fsb = self.tool.en4.enfunc(self.tkey, self.tool.fs)
                fkb = self.tool.en4.enfunc(self.akey, self.tool.fk)
                self.io.hpush(self.mhead, fsb, fkb)
                self.debug = f'namesort : recover success\nfsl {len(self.tool.fs)}' # debug data
            except Exception as e:
                self.debug = f'namesort : recover fail {e}\nfsl {len(self.tool.fs)}' # debug data
            raise Exception('hpusherr') # err

    def clean(self): # fptr - key 정리
        self.order = f'clean : -' # debug data
        
        # fk -> fptr
        list0 = [ ] # exist at fk, not exist at fptrs L0
        for i in range(0, len(self.tool.fk) // 60):
            temp = self.tool.fk[60 * i:60 * i + 12]
            if not self.io.fchk(temp):
                list0.append(temp)
        self.debug = f'clean : list0 {list0}' # debug data

        # fptr -> fk
        list1 = [ ] # exist at fptrs L0, not exist at fk
        for i in self.io.fptr:
            for j in range(0, len(i) // 12):
                temp = i[12 * j:12 * j + 12]
                try:
                    self.tool.getkey(temp)
                except:
                    list1.append(temp)
        self.debug = self.debug + f'\nlist1 {list1}' # debug data

        # fk 정리
        for i in list0:
            self.tool.delkey(i)

        # fptr 정리
        for i in list1:
            try:
                self.io.fdel(i)
            except:
                pass

        # fs -> fk
        list2 = [ ] # exist at fs, not exist at fk
        for i in range( 0, len(self.tool.offset) ):
            temp = self.tool.fsinfow(i)
            if temp[1] != 0:
                try:
                    self.tool.getkey( temp[3] )
                except:
                    list2.append(i)
        self.debug = self.debug + f'\nlist2 {list2}' # debug data

        # fs 정리
        temp = len(list2) - 1 # current tgt
        while temp >= 0:
            num = list2[temp]
            start = self.tool.offset[num]
            length = 0
            while self.tool.fs[start + length] != 10:
                length = length + 1
            self.tool.fs = self.tool.fs[0:start] + self.tool.fs[start + length + 1:]
            temp = temp - 1

        # offset update
        self.tool.getoffset()

        # fio hpush
        try:
            fsb = self.tool.en4.enfunc(self.tkey, self.tool.fs)
            fkb = self.tool.en4.enfunc(self.akey, self.tool.fk)
            self.io.hpush(self.mhead, fsb, fkb)
            self.debug = f'clean : hpush success' # debug data
        except Exception as e:
            self.debug = f'clean : hpush fail {e}' # debug data
            raise Exception('hpusherr') # err

        self.debug = f'clean : {list0}\n{list1}\n{list2}' # debug data
        return [list0, list1, list2]

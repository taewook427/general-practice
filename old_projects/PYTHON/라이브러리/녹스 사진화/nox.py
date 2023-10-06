import random
import os
import shutil
from PIL import Image
import multiprocessing as mp
import oreo # oreo.py 파일 필요

#settings.txt 파일 예시
#[settings]
#{
#    [nox]
#    {
#        [source] {"p0.png"}
#        [process] {0d8}
#    }
#}

class infunc:

    def en(self,number,length): #리틀 엔디안 인코딩
        k = [ ]
        for i in range( 0,length ):
            k.append( number % 256 )
            number = number // 256
        j = bytes( { k[0] } )
        for i in range( 1,len(k) ):
            j = j + bytes( { k[i] } )
        return j

    def de(self,binary): #리틀 엔디안 디코딩
        value = 0
        for i in range( 0,len(binary) ):
            k = 256 ** i
            k = k * binary[i]
            value = value + k
        return value
    
    def getsource(self): #소스 경로 구하기
        try:
            f = open('settings.txt','r',encoding='utf-8')
            t = f.read()
            f.close()
            tool = oreo.toolbox()
            t = tool.readstr(t)
            return t['settings#nox#source']
        except:
            return 'source.png'

    def getcore(self): #프로세스 개수 구하기
        try:
            f = open('settings.txt','r',encoding='utf-8')
            t = f.read()
            f.close()
            tool = oreo.toolbox()
            t = tool.readstr(t)
            return t['settings#nox#process']
        except:
            return 16

    def getsize(self,path,mode):
        i = Image.open(path) #이미지 객체
        bs = ( i.size[0] * i.size[1] ) * 3 #사진 바이트 수
        if mode:
            return bs #mode True면 풀 모드
        else:
            if bs % 2 == 0:
                return int(bs/2) #mode False면 위장모드
            else:
                raise Exception('위장 모드의 바이트 수는 짝수여야 합니다.')

    def imagecom(self,path,mode):
        nm = path[0:path.rfind('.')]
        tp = path[path.rfind('.')+1:]
        if not (tp == mode):
            i = Image.open(path)
            i.save(nm+'.'+mode)

    def imagecom2(self,path,res):
        i = Image.open(path)
        i.save(res)

    def getname(self,mode):
        data0 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        data1 = ['A','E','I','O','U']
        data2 = ['B','C','D','F','G','H','J','K','L','M','N','P','Q','R','S','T','V','W','X','Y','Z']
        name = data0[ random.randrange(0,26) ] + data0[ random.randrange(0,26) ] + data0[ random.randrange(0,26) ]
        if mode: #mode True 전체 모드
            name = name + data1[ random.randrange(0,5) ]
        else: #mode False 위장 모드
            name = name + data2[ random.randrange(0,21) ]
        return name

    def init(self): #초기화
        try:
            shutil.rmtree('temp270')
        except:
            pass
        tool = infunc()
        spath = tool.getsource()
        os.mkdir('temp270')
        shutil.copy(spath,'temp270\\source.dat')
        tool.imagecom('temp270\\source.dat','bmp')
        f = open('temp270\\source.bmp','rb')
        bmphead = f.read(10)
        bmphead = tool.de( f.read(4) )
        f.close()
        f = open('temp270\\source.bmp','rb')
        bmphead = f.read(bmphead) #bmp header
        bmpmain = f.read() #bmp data
        f.close()
        return [bmphead,bmpmain]

    def filecom(self,data,para): #bmp 파일 하나 변환
        bmphead = data[0] #bmp header
        bmpmain = data[1] #bmp data
        filedata = data[2] #file data
        mode = para[0] #T/F T가 전체 F가 위장
        name = para[1] #넘버링 정수

        if mode:
            f = open('temp270\\'+str(name)+'.bmp','wb') #bmp file
            f.write(bmphead)
            f.write(filedata)
            f.close()

        else:
            f = open('temp270\\'+str(name)+'.bmp','wb') #bmp file
            f.write(bmphead)
            num = len(filedata)
            tow = [0,0] * num
            for i in range(0,num):
                p = filedata[i]
                loc1 = p // 16
                loc2 = p % 16
                ii = i * 2
                iii = ii + 1
                tgt1 = bmpmain[ii]
                tgt2 = bmpmain[iii]
                tow[ii] = 16*(tgt1 // 16) + loc1
                tow[iii] = 16*(tgt2 // 16) + loc2
            f.write(bytes(tow))
            f.close()

    def filetopicall(self,path,style): #파일 변환 전체
        tool = infunc()
        bmp = tool.init() #bmphead bmpmain
        isize = tool.getsize('temp270\\source.bmp',True) #사진당 바이트수
        fsize = os.path.getsize(path) #파일사이즈
        num = fsize // isize
        add = fsize % isize

        f = open(path,'rb')
        core = tool.getcore() #프로세스 수
        p = mp.Pool(core)

        for i in range(0,num):
            data = f.read(isize)
            if (i + 1) % (core * 2) == 0:
                p.apply_async(tool.filecom,(bmp+[data],[True,i])).get()
            else:
                p.apply_async(tool.filecom,(bmp+[data],[True,i]))

        if add != 0:
            data = f.read(isize)
            t = isize - len(data)
            data = data + (b'\x00' * t)
            p.apply_async(tool.filecom,(bmp+[data],[True,num]))
            num = num + 1

        p.close()
        f.close()
        p.join()

        name = tool.getname(True)

        p = mp.Pool(core)

        for i in range(0,num): #style은 png/webp 등
            res = 'temp270\\' + name + str(i) + '.' + style
            if (i + 1) % (core * 2) == 0:
                p.apply_async(tool.imagecom2,('temp270\\'+str(i)+'.bmp',res)).get()
            else:
                p.apply_async(tool.imagecom2,('temp270\\'+str(i)+'.bmp',res))

        p.close()
        p.join()

        return [num,name] # num은 사진 파일 개수 name는 일련번호

    def filetopiccamo(self,path,style): #파일 변환 위장
        tool = infunc()
        bmp = tool.init() #bmphead bmpmain
        isize = tool.getsize('temp270\\source.bmp',False) #사진당 바이트수
        fsize = os.path.getsize(path) #파일사이즈
        num = fsize // isize
        add = fsize % isize

        f = open(path,'rb')
        core = tool.getcore() #프로세스 수
        p = mp.Pool(core)

        for i in range(0,num):
            data = f.read(isize)
            if (i + 1) % (core * 2) == 0:
                p.apply_async(tool.filecom,(bmp+[data],[False,i])).get()
            else:
                p.apply_async(tool.filecom,(bmp+[data],[False,i]))

        if add != 0:
            data = f.read(isize)
            t = isize - len(data)
            data = data + (b'\x00' * t)
            p.apply_async(tool.filecom,(bmp+[data],[False,num]))
            num = num + 1

        p.close()
        f.close()
        p.join()

        name = tool.getname(False)

        p = mp.Pool(core)

        for i in range(0,num): #style은 png/webp 등
            res = 'temp270\\' + name + str(i) + '.' + style
            if (i + 1) % (core * 2) == 0:
                p.apply_async(tool.imagecom2,('temp270\\'+str(i)+'.bmp',res)).get()
            else:
                p.apply_async(tool.imagecom2,('temp270\\'+str(i)+'.bmp',res))

        p.close()
        p.join()

        return [num,name] # num은 사진 파일 개수 name는 일련번호

    def unpackpic(self,path,num,mode): #사진 1개 풀기, 경로 문자열, 사진 번호 정수
        i = Image.open(path) #사진 객체
        i.save( 'temp270\\' + str(num) + '.bmp' )
        tool = infunc()
        if mode: #mode True 전체
            f = open('temp270\\' + str(num) + '.bmp','rb')
            bmphead = f.read(10)
            bmphead = tool.de( f.read(4) )
            f.close()
            f = open('temp270\\' + str(num) + '.bmp','rb')
            bmphead = f.read(bmphead) #bmp header
            bmpmain = f.read() #bmp data
            f.close()
            return bmpmain
        else: #mode False 위장
            f = open('temp270\\' + str(num) + '.bmp','rb')
            bmphead = f.read(10)
            bmphead = tool.de( f.read(4) )
            f.close()
            f = open('temp270\\' + str(num) + '.bmp','rb')
            bmphead = f.read(bmphead) #bmp header
            bmpmain = f.read() #bmp data
            f.close()
            t = len(bmpmain) // 2
            out = [0] * t
            for i in range(0,t):
                ii = 2*i
                out[i] = ( 16 * (bmpmain[ii] % 16) ) + ( bmpmain[ii+1] % 16 )
            return bytes(out)

class toolbox:

    def clear(self,mode): #temp 청소
        if mode: #mode True 전체삭제
            try:
                shutil.rmtree('temp270')
            except:
                pass
        else: #mode False bmp만 삭제
            try:
                flist = os.listdir('temp270') #경로의 파일 리스트
                for i in flist:
                    if '.bmp' in i:
                        os.remove('temp270\\'+i)
            except:
                pass

    def detect(self,path): #폴더 경로에서 일련번호, 개수 탐지
        flist = os.listdir(path) #경로의 파일 리스트
        piclist = [ ]
        for i in flist:
            if '.' in i:
                if (i[i.rfind('.')+1:] in ['bmp','png','webp']) and (len(i) > 6):
                    piclist.append(i) #piclist 무손실 사진 목록
        if piclist == [ ]:
            return [0,'',''] # 사진 개수 일련번호 확장자 , 감지된 것 없음

        else:
            temp = 0
            head = -1
            while temp == 0:
                head = head + 1
                d = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
                a0 = piclist[head][0]
                a1 = piclist[head][1]
                a2 = piclist[head][2]
                a3 = piclist[head][3]
                a4 = piclist[head][4]
                a5 = piclist[head][5]
                if (a0 in d) and (a1 in d) and (a2 in d) and (a3 in d) and (a4 == '0') and (a5 == '.'):
                    temp = 1
                elif len(piclist)-1 == head:
                    temp = 2

            if temp == 2:
                return [0,'',''] #감지된 것 없음

            else:
                name = piclist[head]
                char = name[0:4] #일련번호
                ext = name[name.rfind('.')+1:] #확장자
                num = 0
                while os.path.isfile(path+'\\'+char+str(num)+'.'+ext):
                    num = num + 1 #파일 개수
                return [num,char,ext]
        

    def pack(self,path,mode,style): #사진화
        if mode: #mode True 전체
            tool = infunc()
            return tool.filetopicall(path,style) #[파일개수,일련번호]
        else: #mode False 위장
            tool = infunc()
            return tool.filetopiccamo(path,style) #[파일개수,일련번호]

    def unpack(self,para):
        path = para[0] #폴더경로
        num = para[1] #파일 개수
        char = para[2] #일련번호
        ext = para[3] #확장자

        d = ['A','E','I','O','U']
        if char[3] in d:
            mode = True #전체
        else:
            mode = False #위장

        try:
            shutil.rmtree('temp270')
        except:
            pass
        os.mkdir('temp270')

        tool = infunc()
        core = tool.getcore() #프로세스 수
        f = open('temp270\\result.dat','wb')
        p = mp.Pool(core)

        i = num // core
        j = num % core
        for k in range(0,i):
            out = [0] * core
            for m in range(0,core):
                n = (k * core) + m
                fp = path + '\\' + char + str(n) + '.' + ext
                out[m] = p.apply_async(tool.unpackpic,(fp,n,mode))
            for m in range(0,core):
                f.write( out[m].get() )
        out = [0] * j
        for m in range(0,j):
            n = (i * core) + m
            fp = path + '\\' + char + str(n) + '.' + ext
            out[m] = p.apply_async(tool.unpackpic,(fp,n,mode))
        for m in range(0,j):
            f.write( out[m].get() )
        
        p.close()
        p.join()
        f.close()

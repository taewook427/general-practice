import os

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

class stream:

    def __init__(self):
        self.path = '' #파일 위치
        self.header = '' #파일 헤더
        self.data = [ ] #청크 시작위치
        self.size = [ ] #청크 크기

    def read(self,path): #read path file
        with open(path,'rb') as f:
            st = f.read(4)
        if st == b'KSD1':
            tool = infunc()
            self.path = os.path.abspath(path)
            f = open(self.path,'rb')
            f.read(4)
            hs = tool.de( f.read(4) ) #header size
            self.header = str( f.read(hs), 'utf-8' )

            temp = ''
            while temp != b'':
                temp = f.read(4)
                if temp != b'':
                    size = tool.de( temp ) #data size
                    current = f.tell() #data point
                    self.size.append(size)
                    self.data.append(current)
                    f.seek(current + size)

            f.close()

    def get(self,num): #num 번째 청크 바이너리 가져오기
        with open(self.path,'rb') as f:
            f.seek( self.data[num] )
            data = f.read( self.size[num] )
        return data

    def write(self,path,header): #스트림 데이터 쓰기
        self.path = os.path.abspath(path) #파일 위치
        self.header = header #파일 헤더
        tool = infunc()
        with open(self.path,'wb') as f:
            f.write(b'KSD1')
            f.write( tool.en( len(bytes( self.header, encoding='utf-8') ), 4 ) )
            f.write( bytes(self.header, encoding='utf-8') )

    def append(self,binary): #스트림에 이진 데이터 추가
        tool = infunc()
        self.data.append( os.path.getsize(self.path) + 4 )
        self.size.append( len(binary) )
        with open(self.path,'ab') as f:
            f.write( tool.en( len(binary), 4 ) )
            f.write(binary)

class infunc:
    #전처리
    def pre(self,code):
        temp = len(code)
        raw = [''] * temp
        for i in range(0,temp):
            raw[i] = code[i] #1글자로 쪼개기
            
        out = [ ]
        temp = ''
        isstr = False
        isgra = True
        isesc = False
        isname = False
        for i in raw:
            if (isstr) and (not isgra): #문자열 부위
                
                if isesc: # #다음

                    isesc = False
                    if i == '#':
                        temp = temp + '#'
                        
                    elif i == '"':
                        temp = temp + '"'
                        
                    elif i == 'n':
                        temp = temp + '\n'

                    elif i == 's':
                        temp = temp + ' '
                        
                    else:
                        raise Exception("전처리 중 문법 오류 : 잘못된 이스케이프")
                
                else: #일반 문자열

                    if i == '#':
                        isesc = True
                        
                    elif i == '"':
                        isesc = False
                        isstr = False
                        isgra = True
                        isname = False
                        out.append(temp)
                        temp = ''
                        
                    else:
                        temp = temp + i
            
            elif (not isstr) and (isgra): #문법 부위

                if isname:
                    if i == ']':
                        out.append(temp)
                        temp = ''
                        isname = False
                        out.append('G'+i)
                    else:
                        temp = temp + i
                    
                else:
                    if i == '[':
                        if not (temp == ''):
                            out.append(temp)
                        out.append('G'+i)
                        isname = True
                        temp = 'V'
                    
                    elif i in {']', '{', '}', ',', ' ', '\n', '\t'}:
                        if not (temp == ''):
                            out.append(temp)
                        out.append('G'+i)
                        temp = ''
                        
                    elif i == '"':
                        temp = 'S'
                        isstr = True
                        isgra = False
                        isesc = False
                        isname = False
                        
                    elif i in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', '.', 'b', 'o', 'd', 'x'}:
                        if temp == '':
                            temp = 'N' + i
                        else:
                            temp = temp + i
                            
                    else:
                        out.append('U'+i)
                
            
            else:
                raise Exception("전처리 중 문법 오류 : 알 수 없음")

        return out
    
    def single(self,code,domain): # 단일 항목 해석
        # [] {...}
        names = ''
        value = [ ]

        var = code[ code.index('G[') + 1 ]
        if var[0] == 'V':
            var = var[1:]
            if not ('#' in var):

                names = domain + '#' + var
                txt = code[ code.index('G{') + 1:code.index('G}') ]
                txt = list( filter( lambda x: (x[0] == 'N') or (x[0] == 'S'), txt ) )
                for i in txt:
                    if i[0] == 'N':
                        num = i[1:]
                        if 'b' in num:
                            num = int(num,base=2)
                        elif 'o' in num:
                            num = int(num,base=8)
                        elif 'd' in num:
                            num = int(num[2:])
                        elif 'x' in num:
                            num = int(num,base=16)
                        elif '.' in num:
                            num = float(num)
                        else:
                            num = int(num)
                        value.append(num)
                        
                    elif i[0] == 'S':
                        value.append(i[1:])

                    else:
                        raise Exception("단일 항목 해석 중 오류 : 잘못된 항목 값")

                if len(txt) == 1:
                    value = value[0]

                return [names,value] #값은 숫자, 문자열, 리스트, 빈 리스트는 빈 객체

            else:
                return [ ] #주석이면 빈 리스트
        
        else:
            raise Exception("단일 항목 해석 중 오류 : 잘못된 변수 이름")

    def double(self,code,domain): #단일 객체 해석
        # [] { [] {} [] {} }
        var = code[ code.index('G[') + 1 ]
        var = var[1:]
        name = domain + '#' + var

        code.reverse()
        temppp = code.index('G}')
        temppp = len(code) - temppp - 1
        code.reverse()

        raw = code[code.index('G{') + 1: temppp]
        counta = raw.count('G{')
        countb = raw.count('G}')
        if counta == countb:
            out0 = [ ]
            out1 = [ ]
            
            tool = infunc()
            for i in range(0,counta):
                tempppp = raw.index('G}') + 1
                tempp = raw[raw.index('G[') : tempppp]
                temp = tool.single(tempp,name)
                if temp == [ ]: #주석이면 패스
                    pass
                
                elif temp[1] == [ ]: #빈 객체면 kobj 삽입
                    a = kobj()
                    a.put(tempp)
                    out0.append( temp[0] )
                    out1.append( a )

                else: # 다 아니면 일반 삽입
                    out0.append( temp[0] )
                    out1.append( temp[1] )

                raw = raw[tempppp:]

            return [out0, out1]
            # 빈 객체면 [ [],[] ]
            # [ [이름들], [값들] ]

        else:
            raise Exception("단일 객체 해석 중 오류 : 중괄호 개수 불일치")

    def complete(self,code,domain): #복합 객체 해석
        # [] { [] { [] {} } }
        tool = infunc()
        names = [ ]
        values = [ ]

        var = code[ code.index('G[') + 1 ]
        var = var[1:]
        name = domain + '#' + var

        code.reverse()
        temppp = code.index('G}')
        temppp = len(code) - temppp - 1
        code.reverse()

        raw = code[code.index('G{') + 1: temppp]
        counta = raw.count('G{')
        countb = raw.count('G}')

        if counta == countb:
            
            while 'G[' in raw:
                
                temp0 = raw.index('G{') # { 위치
                temp1 = 1 # {} 찾기 보조변수
                temp2 = temp0 # } 위치
                temp3 = 1 # { 깊이
                temp4 = False # { 깊이 보조변수
                while temp1 > 0:
                    temp2 = temp2 + 1
                    if raw[temp2] == 'G{':
                        temp1 = temp1 + 1
                        if temp3 == 1:
                            temp3 = 2
                        elif temp4:
                            temp3 = 3
                        temp4 = True
                    elif raw[temp2] == 'G}':
                        temp1 = temp1 - 1
                        temp4 = False

                togo = raw[0:temp2 + 1]
                raw = raw[temp2 + 1:]

                if temp3 == 1: # 단일 항목
                    re = tool.single(togo,name)
                    if re == [ ]: #주석인 경우
                        pass
                    elif re[1] == [ ]: # 빈 객체인 경우
                        temp = kobj()
                        temp.put(togo)
                        names.append( re[0] )
                        values.append( temp )
                    else: # 주석이 아니면 항목 추가
                        names.append( re[0] )
                        values.append( re[1] )

                elif temp3 == 2: # 단일 객체
                    re = tool.double(togo,name)
                    temp = kobj()
                    temp.put(togo)
                    var = togo[ togo.index('G[') + 1 ]
                    var = var[1:]
                    names.append( name + '#' + var )
                    values.append( temp )
                    if not(re == [ [],[] ]):
                        tempn = re[0]
                        tempv = re[1]
                        for i in range( 0,len( tempn ) ):
                            names.append( tempn[i] )
                            values.append( tempv[i] )

                else: # 복합 객체
                    re = tool.complete(togo,name)
                    temp = kobj()
                    temp.put(togo)
                    var = togo[ togo.index('G[') + 1 ]
                    var = var[1:]
                    names.append( name + '#' + var )
                    values.append( temp )
                    tempn = re[0]
                    tempv = re[1]
                    for i in range( 0,len( tempn ) ):
                        names.append( tempn[i] )
                        values.append( tempv[i] )

            return [names,values]

        else:
            raise Exception("복합 객체 해석 중 오류 : 중괄호 개수 불일치")

    def strcom(self,raw,mode): #실제로 쓰여질 문자열
        num = len(raw) # 모드가 참이면 단축형
        out = [0] * num
        for i in range(0,num):
            temp = raw[i]
            if temp == '#':
                out[i] = '##'
            elif temp == '"':
                out[i] = '#"'
            elif mode and (temp == ' '):
                out[i] = '#s'
            elif mode and (temp == '\n'):
                out[i] = '#n'
            else:
                out[i] = temp
        out = ['"'] + out + ['"']
        return ''.join(out)
        
class kobj: #객체용 타입
    def put(self,data):
        self.data = data
    def tostring(self):
        out = [ x[1:] for x in self.data ]
        return ''.join(out)

class toolbox:
    def readstr(self,code): #문자열 파싱
        temp = infunc()
        tempp = temp.pre(code)
        re = temp.complete(tempp,'')
        out0 = [ x[1:] for x in re[0] ]
        out1 = re[1]
        num = len(out0)
        output = { }
        k = kobj()
        k.put(tempp)
        output[ out0[0].split('#')[0] ] = k
        for i in range(0,num):
            output[ out0[i] ] = out1[i]
        return output

    def readfile(self,path): #파일 파싱
        f = open(path,'r',encoding = 'utf-8')
        code = f.readlines()
        f.close()
        code = ''.join(code)
        temp = infunc()
        tempp = temp.pre(code)
        re = temp.complete(tempp,'')
        out0 = [ x[1:] for x in re[0] ]
        out1 = re[1]
        num = len(out0)
        output = { }
        k = kobj()
        k.put(tempp)
        output[ out0[0].split('#')[0] ] = k
        for i in range(0,num):
            output[ out0[i] ] = out1[i]
        return output

    def rtoe(self,code,key): # R모드에서 E모드로
        temp = code.encode('utf-8')
        p = len(temp)
        raw = [0] * p
        for i in range( 0,p ):
            raw[i] = temp[i]
            
        keylist = [ ] #key는 영문 문자열
        for i in range( 0,len(key) ):
            keylist.append( ord(key[i]) )
        keylist = keylist * ( int( p/len(key) ) + 2 )
        table = list( range(0,256) ) * 2
        
        output = [0] * p
        for i in range(0,p):
            output[i] = table[ keylist[i] + raw[i] ]

        pp = p//16 # 숫자 16개씩 줄바꿈으로 끊어적기
        temp = [0] * pp # 각 숫자는 띄어쓰기
        for i in range(0,pp):
            tempp = [0] * 16
            k = 16 * i
            for j in range(0,16):
                tempp[j] = str( output[k + j] )
            temp[i] = ' '.join(tempp) + '\n'
        ppp = pp * 16
        for i in range(0,p-ppp):
            temp.append( str( output[ppp + i] ) + ' ' )
        temp = ''.join(temp)
        return temp

    def etor(self,code,key): # E모드에서 R모드로
        code = code.replace('\n',' ')
        code = code.split(' ')
        code = list( filter( lambda a : a != '',code ) )
        code = [ int(x) for x in code ] # 리스트 형식으로 변환
        p = len(code)
        
        keylist = [ ] #key는 영문 문자열
        for i in range( 0,len(key) ):
            keylist.append( ord(key[i])-256 )
        keylist = keylist * ( int( p/len(key) ) + 2 )
        table = list( range(0,256) ) * 2

        out = [0] * p # 디코딩
        for i in range(0,p):
            out[i] = table[ code[i] - keylist[i] ]
        out = bytes(out)
        out = out.decode('utf-8')
        return out

    def dotcom(self,code): # 띄어쓰기 줄바꿈 불안정할 때 상호변환
        if ' ' in code:
            code = code.replace(' ','.')
            return code.replace('\n','.\n')
        
        elif '.' in code:
            return code.replace('.',' ')
        
        else:
            raise Exception('알 수 없는 E모드 문자열')

    def rore(self,code): #E/R모드 판별
        if '[' in code:
            return 'R'
        else:
            return 'E'

    def mkobj(self,name): # 새 객체 생성
        if ('#' in name) or ('[' in name) or (']' in name):
            raise Exception('객체 생성 오류 : 이름에 사용할 수 없는 문자')
        else:
            temp = kobj()
            temp.put( [ 'G[', 'V'+name, 'G]', 'G\n', 'G{', 'G\n', 'G}' ] )
            return temp

    def putdt(self,obj,name,value): #최상위 객체에 값 삽입
        if ('#' in name) or ('[' in name) or (']' in name):
            raise Exception('값 삽입 오류 : 이름에 사용할 수 없는 문자')
        
        else:
            temp = obj.data
            temp.reverse()
            toin = temp.index('G}')
            toin = len(temp) - toin - 1
            temp.reverse()

            p = type(value)
            if p == int:
                out = temp[0:toin] + ['G '] * 4
                out = out + [ 'G[', 'V'+name, 'G]', 'G ', 'G{', 'N'+str(value), 'G}', 'G\n' ]
                out = out + temp[toin:]
                
            elif p == float:
                out = temp[0:toin] + ['G '] * 4
                out = out + [ 'G[', 'V'+name, 'G]', 'G ', 'G{', 'N'+str(value), 'G}', 'G\n' ]
                out = out + temp[toin:]
                
            elif p == str:
                out = temp[0:toin] + ['G '] * 4
                out = out + [ 'G[', 'V'+name, 'G]', 'G ', 'G{', 'S'+str(value), 'G}', 'G\n' ]
                out = out + temp[toin:]
                
            elif p == list:
                num = len(value)
                table = [0] * num
                for i in range(0,num):
                    pp = value[i]
                    p = type( pp )
                    if p == int:
                        table[i] = 'N' + str(pp)
                    elif p == float:
                        table[i] = 'N' + str(pp)
                    elif p == str:
                        table[i] = 'S' + pp
                    else:
                        table[i] = 'S' + str(pp)
                        
                out = temp[0:toin] + (['G '] * 4) + [ 'G[', 'V'+name, 'G]', 'G ', 'G{' ]
                if num > 5:
                    long = True
                else:
                    long = False
                    
                for i in table:
                    if long:
                        out = out + [ 'G\n', 'G ', 'G ', 'G ', 'G ' ]
                    out = out + [i] + [ 'G,', 'G ' ]
                out = out[0:-2] + [ 'G}', 'G\n' ] + temp[toin:]
            
            else:
                out = temp[0:toin] + ['G '] * 4
                out = out + [ 'G[', 'V'+name, 'G]', 'G ', 'G{', 'S'+str(value), 'G}', 'G\n' ]
                out = out + temp[toin:]
                
            obj.put(out)

    def putobj(self,obj,tgt): # 최상위 객체에 객체 삽입
        temp = obj.data
        temp.reverse()
        toin = temp.index('G}')
        toin = len(temp) - toin - 1
        temp.reverse()

        tgt = tgt.data
        out = temp[0:toin] + [ 'G ', 'G ', 'G ', 'G ' ]
        for i in tgt:
            if i == 'G\n':
                out = out + [ 'G\n', 'G ', 'G ', 'G ', 'G ' ]
            else:
                out.append(i)
        out = out + [ 'G\n' ] + temp[toin:]
        obj.data = out

    def wrcom(self,code,mode,dry): #쓰기 리스트를 문자열화
        if dry:
            code = list( filter( lambda a : a != 'G\n',code ) )
            code = list( filter( lambda a : a != 'G ',code ) )
        num = len(code) #mode True면 단축 문자열
        out = [0] * num #리스트를 받음
        temp = infunc() #dry True면 단축저장형
        for i in range(0,num):
            if code[i][0] == 'S':
                out[i] = temp.strcom( code[i][1:],mode )
            else:
                out[i] = code[i][1:]
        return ''.join(out)

    def revice(self,obj,name,value): #객체의 특정 값을 수정
        names = name.split('#')
        toin = 0 #특정 데이터 위치
        temp = obj.data #객체 리스트 데이터

        while not (names == [ ]):
            t = temp.index('V'+names[0])
            toin = toin + t + 1
            temp = temp[t+1:]
            del names[0]
        p = toin + temp.index('G{') # 값 시작 위치
        q = toin + temp.index('G}') # 값 종료 위치

        temp = toolbox()
        t = temp.mkobj('') #객체 생성
        temp.putdt(t,'',value) #객체에 값 삽입
        t = t.data #객체의 리스트 데이터
        t = t[5:]
        pp = t.index('G{')
        qq = t.index('G}')
        toin = t[pp:qq+1] # 값 { ... }
        add = ([ 'G ' ] * 4) * ( name.count('#') - 1 )
        togo = [ ]
        for i in toin:
            if i == 'G\n':
                togo = togo + [i] + add
            else:
                togo = togo + [i]

        k = obj.data
        obj.data = k[0:p] + togo + k[q+1:]

    def wrfile(self,path,string):
        f = open(path,'w',encoding = 'utf-8')
        f.write(string)
        f.close()
        

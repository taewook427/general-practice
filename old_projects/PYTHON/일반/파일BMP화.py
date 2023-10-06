import hashlib
import random
import os
from math import ceil
def work():
    showmain()
    endthis()
def endthis():
    a = input('\nENTER ANY KEY TO EXIT... ')
def getsize(name):
    filesize = 0
    file = open(name,'rb')
    byte = file.read(1)
    while not byte == b'':
        byte = file.read(1)
        filesize = filesize + 1
    file.close()
    return filesize
def gethash(string,salt):
    myhash = hashlib.sha256( ( string+salt ).encode( 'utf-8' ) ).hexdigest()
    return myhash
def getbmp(name):
    print('Seperating file header')
    file = open(name,'rb')
    bmpstruct = [ ]
    startpoint = 0
    keyhash = 0
    salt = 0
    hint = 0
    length = 0
    k = file.read(10)
    startpoint = decoding( file.read(4) )
    file.close()
    file = open(name,'rb')
    k = file.read(startpoint)
    keyhash = file.read(32).hex()
    salt = str( file.read(4),'utf-8' )
    hint = str( file.read(256),'utf-8' )
    length = decoding( file.read(4) )
    file.close()
    bmpstruct.append(startpoint)
    bmpstruct.append(keyhash)
    bmpstruct.append(salt)
    bmpstruct.append(hint)
    bmpstruct.append(length)
    return bmpstruct
def decoding(binary):
    value = 0
    for i in range( 0,len(binary) ):
        k = 256 ** i
        k = k * binary[i]
        value = value + k
    return value
def encoding(number,length):
    k = [ ]
    for i in range( 0,length ):
        k.append( number % 256 )
        number = number // 256
    j = bytes( { k[0] } )
    for i in range( 1,len(k) ):
        j = j + bytes( { k[i] } )
    return j
def showmain():
    alpha = 'KOs Crypto Program V2\n\n'
    alpha = alpha + 'This program encrypts/decrypts yout file.\nThere are two modes, simple BMP mode and hided BMP mode.\n\n'
    alpha = alpha + 'Do not convert BMP result file to other style.\n'
    alpha = alpha + 'Your file size should be \nunder 4294915000 Bytes ( ~ 3.9 GB ).\n'
    alpha = alpha + 'Passowrd hint should be under 256 Bytes ( ~ 85 words ).\n'
    alpha = alpha + 'If you are using Hide mode, your file size \nshould be under 49766000 Bytes ( ~ 47 MB ).\n'
    print(alpha)
    reading = 0
    while reading == 0:
        i = input('Encrypt/Decrypt - Select Mode (e/d) : ')
        if i == 'e':
            reading = 1
        elif i == 'd':
            reading = -1
    convert = 0
    while convert == 0:
        i = input('Simple/Hide - Select Mode (s/h) : ')
        if i == 's':
            convert = 1
        elif i == 'h':
            convert = -1
    if reading == 1:
        if convert == 1:
            ensi()
        else:
            enhi()
    else:
        if convert == 1:
            desi()
        else:
            dehi()
def ensi():
    name = input('\nEnter file name to convert : ')
    print('Checking file size ; 10 MB / s')
    if getfilename(name) == 0:
        size = getsize(name)
        if size <= 4294915000:
            psword = input('Set password of BMP file : ')
            hint = input('Set password hint\n>>> ')
            hint = bytes(hint,'utf-8')
            if len(hint) > 256:
                print('ERROR : HINT LENGTH TOO LONG ; ',str(len(hint)),' BYTES')
            else:
                hint = hint + bytes(b' ') * ( 256 - len(hint) )
                salt =chr(random.randrange(32,126)) + chr(random.randrange(32,126)) + chr(random.randrange(32,126)) + chr(random.randrange(32,126))
                key = gethash(psword,salt)
                salt = bytes(salt,'utf-8')
                key = bytes.fromhex(key)
                size = encoding(size,4)
                startensi(name,key,salt,hint,size)
        else:
            print('\nERROR : FILE SIZE TOO BIG ; ', str(size), ' BYTES')
def enhi():
    try:
        source = open('8Ksource.bmp','rb')
        source.close()
        name = input('Enter file name to convert : ')
        if getfilename(name) == 0:
            print('Checking file size ; 10 MB / s')
            size = getsize(name)
            if size <= 49766000:
                psword = input('Set password of BMP file : ')
                hint = input('Set password hint\n>>> ')
                hint = bytes(hint,'utf-8')
                if len(hint) > 256:
                    print('ERROR : HINT LENGTH TOO LONG ; ',str(len(hint)),' BYTES')
                else:
                    hint = hint + bytes(b' ') * ( 256 - len(hint) )
                    salt =chr(random.randrange(32,126)) + chr(random.randrange(32,126)) + chr(random.randrange(32,126)) + chr(random.randrange(32,126))
                    key = gethash(psword,salt)
                    salt = bytes(salt,'utf-8')
                    key = bytes.fromhex(key)
                    size = encoding(size,4)
                    print('\nMaking temp file ; 2 MB / s')
                    temp = open('temp','wb')
                    temp.write(key)
                    temp.write(salt)
                    temp.write(hint)
                    temp.write(size)
                    target = open(name,'rb')
                    k = target.read(1)
                    while not k == b'':
                        temp.write(k)
                        k = target.read(1)
                    target.close()
                    temp.close()
                    print('Temp file was written successfully.')
                    startenhi(name)
    except:
        print('ERROR : CANNOT FIND SOURCE FILE')
def desi():
    name = input('\nEnter file name to convert : ')
    if getfilename(name) == 0:
        bmpstruct = getbmp(name)
        startpoint = bmpstruct[0]
        keyhash = bmpstruct[1]
        salt = bmpstruct[2]
        hint = bmpstruct[3]
        length = bmpstruct[4]
        print('Psaaword hint\n>>> ',hint)
        password = input('\nEnter your password : ')
        while not gethash(password,salt) == keyhash:
            print('ERROR : INCORRECT PASSWORD')
            password = input('\nEnter your password : ')
        print('Writing main file ; 2 MB / s')
        target = open(name,'rb')
        file = open(name[:-4],'wb')
        k = target.read(startpoint)
        k = target.read(296)
        for i in range(0,length):
            k = target.read(1)
            file.write(k)
        target.close()
        file.close()
        print('File converted sucessfully')
def dehi():
    name = input('Enter file name to convert : ')
    if getfilename(name) == 0:
        source = open(name,'rb')
        k = source.read(10)
        startpoint = decoding( source.read(4) )
        source.close()
        source = open(name,'rb')
        k = source.read(startpoint)
        print('Checking file header')
        temp = open('temp','wb')
        for i in range(0,98):
            k = source.read(3)
            j = source.read(3)
            temp.write(k)
        k = source.read(2)
        temp.write(k)
        temp.close()
        source.close()
        temp = open('temp','rb')
        keyhash = temp.read(32).hex()
        salt = str( temp.read(4),'utf-8' )
        hint = str( temp.read(256),'utf-8' )
        length = decoding( temp.read(4) )
        temp.close()
        os.remove('temp')
        print('Psaaword hint\n>>> ',hint)
        password = input('\nEnter your password : ')
        while not gethash(password,salt) == keyhash:
            print('ERROR : INCORRECT PASSWORD')
            password = input('\nEnter your password : ')
        print('Making temp file ; 2 MB / s')
        source = open(name,'rb')
        temp = open('temp','wb')
        k = source.read(startpoint)
        for i in range(0,33177600):
            k = source.read(3)
            if i % 2 == 0:
                temp.write(k)
        source.close()
        temp.close()
        print('Writting main file ; 2 MB / s')
        temp = open('temp','rb')
        file = open(name[:-4],'wb')
        k = temp.read(296)
        for i in range(0,length):
            k = temp.read(1)
            file.write(k)
        file.close()
        temp.close()
        os.remove('temp')
        print('File converted sucessfully')
def startensi(name,key,salt,hint,size):
    numsize = decoding(size)
    bmpsize = ceil( ( ceil( ( numsize + 296 ) / 3) ) ** 0.5 )
    file = open(name + '.bmp', 'wb')
    raw = open(name, 'rb')
    file.write(b'BM')
    file.write( encoding( 54 + 3 * ( bmpsize ** 2 ) , 4) )
    file.write(b'\x00\x00\x00\x00')
    file.write(b'\x36\x00\x00\x00')
    file.write(b'\x28\x00\x00\x00')
    file.write( encoding( bmpsize,4 ) )
    file.write( encoding( bmpsize,4 ) )
    file.write(b'\x01\x00')
    file.write(b'\x18\x00')
    file.write(b'\x00\x00\x00\x00')
    file.write( encoding( 3 * ( bmpsize ** 2 ),4 ) )
    file.write(bytes(16))
    file.write(key)
    file.write(salt)
    file.write(hint)
    file.write(size)
    print('\nHeader was written successfully')
    print('Writing main file ; 2 MB / s')
    for i in range(0,numsize):
        k = raw.read(1)
        file.write(k)
    for i in range( 0,3 * ( bmpsize ** 2 ) - numsize - 296):
        k = random.randrange(0,256)
        k = bytes({k})
        file.write(k)
    file.close()
    raw.close()
    print('BMP file was written successfully.')
def startenhi(name):
    source = open('8Ksource.bmp','rb')
    temp = open('temp','rb')
    file = open(name + '.bmp','wb')
    k = source.read(10)
    startpoint = decoding( source.read(4) )
    source.close()
    source = open('8Ksource.bmp','rb')
    k = source.read(startpoint)
    file.write(k)
    print('Header was written successfully')
    print('Writing main file ; 0.5 MB / s')
    for i in range(0,33177600):
        k = source.read(3)
        if i % 2 == 0:
            k = temp.read(3)
            if len(k) == 3:
                file.write(k)
            elif len(k) == 2:
                file.write(k)
                file.write(bytes({random.randrange(0,256)}))
            elif len(k) == 1:
                file.write(k)
                file.write(bytes({random.randrange(0,256)}))
                file.write(bytes({random.randrange(0,256)}))
            else:
                file.write(bytes({random.randrange(0,256)}))
                file.write(bytes({random.randrange(0,256)}))
                file.write(bytes({random.randrange(0,256)}))
        else:
            file.write(k)
    print('BMP file was written successfully.')
    source.close()
    temp.close()
    file.close()
    os.remove('temp')
def getfilename(name):
    try:
        f = open(name,'rb')
        f.close()
        return 0
    except:
        print('\nERROR : CANNOT FIND FILE')
        return 1
work()

import os
import shutil
import multiprocessing as mp

from Cryptodome.Cipher import AES
import hashlib
import secrets

import zipfile

# delete file
def delete(target, mode): # target : file path, mode : int
    fsize = os.path.getsize(target) # file size
    
    if mode == 0: # normal delete
        num0 = fsize // 1048576
        num1 = fsize % 1048576
        
        with open(target, 'wb') as f:
            for i in range(0,num0):
                f.write(b'\x00' * 1048576)
                if i % 10 == 0:
                    print(f'deleting {i}/{num0}')
            f.write(b'\x00' * num1)
            print(f'deleting {num0}/{num0}')
        os.remove(target)
        
    else: # secure delete
        num0 = fsize // 1024
        num1 = fsize % 1024
        
        with open(target, 'wb') as f:
            for i in range(0,num0 // 100):
                tempbyte = [0] * 1024
                for j in range(0,1024):
                    tempbyte[j] = secrets.randbelow(256)
                tempbyte = bytes(tempbyte)
                for j in range(0,100):
                    f.write(tempbyte)
                if i % 100 == 0:
                    print(f'deleting {i * 100}/{num0}')
                    
            tempbyte = [0] * 1024
            for i in range(0,1024):
                tempbyte[i] = secrets.randbelow(256)
            tempbyte = bytes(tempbyte)
            for i in range(0,num0 % 100):
                f.write(tempbyte)
                
            tempbyte = [0] * num1
            for i in range(0,num1):
                tempbyte[i] = secrets.randbelow(256)
            tempbyte = bytes(tempbyte)
            f.write(tempbyte)
            print(f'deleting {num0}/{num0}')
        os.remove(target)

# files -> tempkaesl
def dozip(targets): # targets : file path list
    num = len(targets)
    with open('tempkaesl','wb') as f:
        f.write( bytes( [num % 256, num // 256] ) )
        count = 0
        
        for i in targets:
            count = count + 1
            
            tempname = i.replace('\\','/')
            tempname = tempname[tempname.rfind('/') + 1:] # file name
            tempnum = len( bytes(tempname,encoding='utf-8') ) # file name size
            f.write( bytes( [tempnum % 256, tempnum // 256] ) )
            f.write( bytes(tempname, encoding='utf-8') )
            
            filesize = os.path.getsize(i) # file size
            tempsize = filesize
            tempbyte = [0] * 8
            for j in range(0,8):
                tempbyte[j] = tempsize % 256
                tempsize = tempsize // 256
            f.write( bytes(tempbyte) )
            
            num0 = filesize // 1048576
            num1 = filesize % 1048576
            with open(i,'rb') as t:
                for j in range(0,num0):
                    f.write( t.read(1048576) )
                f.write( t.read(num1) )
            print(f'zipping {count}/{num}')

# tempkaesl -> path + files
def unzip(path): # path : folder path
    path = path.replace('\\','/')
    if path == '':
        path = ''
    elif path[-1] == '/':
        path = path
    else:
        path = path + '/'
        
    with open('tempkaesl','rb') as f:
        tempbyte = f.read(2)
        num = tempbyte[0] + tempbyte[1] * 256
        
        for i in range(0, num):
            tempbyte = f.read(2)
            namelen = tempbyte[0] + tempbyte[1] * 256
            namestr = str(f.read(namelen), encoding='utf-8')
            
            filesize = 0
            tempbyte = f.read(8)
            for j in range(0,8):
                filesize = filesize + tempbyte[j] * 256 ** j
                
            num0 = filesize // 1048576
            num1 = filesize % 1048576
            with open(path + namestr, 'wb') as t:
                for j in range(0,num0):
                    t.write( f.read(1048576) )
                t.write( f.read(num1) )
            print(f'unzipping {i+1}/{num}')

# key expand inline
def inline0(pre,sub): # pre : byte, sub : byte
    temp = sub
    for i in range(0,10000):
        temp = hashlib.sha3_256(pre + temp).digest()
    return temp # 256bit

# key expand function
def expandkey(ckey): # ckey : byte
    order = [0] * 16
    p = mp.Pool(16)
    for i in range(0,16):
        temp = (7 * i) % 16 # round st point
        if temp > 8:
            pre = ckey[8*temp-64:8*temp]
            sub = ckey[8*temp:] + ckey[0:8*temp-64]
        else:
            pre = ckey[8*temp+64:] + ckey[0:8*temp]
            sub = ckey[8*temp:8*temp+64]
        order[i] = p.apply_async( inline0,(pre,sub) )
    out = [b''] * 32
    for i in range(0,16):
        temp = order[i].get()
        out[i] = temp[0:16]
        out[i + 16] = temp[16:32]
    return out

# short encryption no padding, 16B * n
def inline1(key,iv,data): # key : byte, iv : byte, data : byte
    func = AES.new(key,AES.MODE_CBC,iv).encrypt
    num = len(data)
    out = [0] * num
    for i in range(0,num // 16):
        temp = 16*i
        out[temp:temp+16] = func( data[temp:temp+16] )
    return bytes(out)

# encrypt(tempkaesl) -> move to path, 32 process
def encrypt32(hint, pw, path): # hint : str, pw : str, path : file path
    tempbyte = [0] * 32
    for i in range(0,32):
        tempbyte[i] = secrets.randbelow(256)
    salt = bytes(tempbyte) # salt byte
    
    tempbyte = [0] * 128
    for i in range(0,128):
        tempbyte[i] = secrets.randbelow(256)
    ckey = bytes(tempbyte) # content key byte
    
    tempbyte = [0] * 16
    for i in range(0,16):
        tempbyte[i] = secrets.randbelow(256)
    iv = bytes(tempbyte) # iv byte
    
    pw = bytes(pw, encoding='utf-8') # pw byte
    pwhash = pw # pwh byte
    for i in range(0,100000):
        pwhash = hashlib.sha3_256(salt + pwhash).digest()
    mkey = pw # master key byte
    for i in range(0,10000):
        mkey = hashlib.sha3_256(mkey + salt).digest()
        
    hint = bytes(hint, encoding='utf-8') # hint byte
    hintsize = len(hint)

    func = AES.new( mkey[16:32], AES.MODE_CBC, mkey[0:16] ).encrypt
    ckeydata = [0] * 128 # content key encryption
    for i in range(0,8):
        ckeydata[16*i:16*i+16] = func( ckey[16*i:16*i+16] )
    ckeydata = bytes(ckeydata)
    
    header = b'OTE1' + bytes( [hintsize % 256, hintsize // 256] ) + hint + salt + pwhash + ckeydata + iv # header byte

    keys = expandkey(ckey) # 16B * 32 keys
    ivs = [iv] * 32 # 16B * 32 ivs
    filesize = os.path.getsize('tempkaesl') # target size
    chunknum0 = filesize // 131072 # chunk num
    chunknum1 = filesize % 131072 # left size
    
    with open(path,'wb') as f:
        with open('tempkaesl','rb') as t:
            f.write(header)
            print('encrypting header')
            p = mp.Pool(32)
            order = [0] * 32 # order buffer
            write = [b''] * 32 # write buffer
            count = 0 # iv, key position

            for i in range(0,chunknum0):
                tempdata = t.read(131072) # 128kb
                if (i + 1) % 100 == 0:
                    print(f'encrypting {i + 1}/{chunknum0 + 1}')
                order[count] = p.apply_async( inline1,(keys[count], ivs[count], tempdata) )

                if count == 31:
                    for j in range(0,32):
                        write[j] = order[j].get()
                        ivs[j] = write[j][-16:]
                    f.write( b''.join(write) )
                    count = -1 # reset
                    order = [0] * 32 # reset
                    write = [b''] * 32 # reset

                count = count + 1

            for i in range(0,chunknum0 % 32):
                write[i] = order[i].get()
                ivs[i] = write[i][-16:]
            f.write( b''.join(write) )
            
            pad = lambda x : x + bytes(chr(16 - len(x)),'utf-8') * (16 - len(x))
            tempdata = t.read(chunknum1)
            tempdata = tempdata[0:chunknum1 - (chunknum1 % 16)] + pad( tempdata[chunknum1 - (chunknum1 % 16):] )
            f.write( inline1(keys[count], ivs[count], tempdata) )
            print(f'encrypting {chunknum0 + 1}/{chunknum0 + 1}')

# encrypt(tempkaesl) -> move to path, 8 process
def encrypt8(hint, pw, path): # hint : str, pw : str, path : file path
    tempbyte = [0] * 32
    for i in range(0,32):
        tempbyte[i] = secrets.randbelow(256)
    salt = bytes(tempbyte) # salt byte
    
    tempbyte = [0] * 128
    for i in range(0,128):
        tempbyte[i] = secrets.randbelow(256)
    ckey = bytes(tempbyte) # content key byte
    
    tempbyte = [0] * 16
    for i in range(0,16):
        tempbyte[i] = secrets.randbelow(256)
    iv = bytes(tempbyte) # iv byte
    
    pw = bytes(pw, encoding='utf-8') # pw byte
    pwhash = pw # pwh byte
    for i in range(0,100000):
        pwhash = hashlib.sha3_256(salt + pwhash).digest()
    mkey = pw # master key byte
    for i in range(0,10000):
        mkey = hashlib.sha3_256(mkey + salt).digest()
        
    hint = bytes(hint, encoding='utf-8') # hint byte
    hintsize = len(hint)

    func = AES.new( mkey[16:32], AES.MODE_CBC, mkey[0:16] ).encrypt
    ckeydata = [0] * 128 # content key encryption
    for i in range(0,8):
        ckeydata[16*i:16*i+16] = func( ckey[16*i:16*i+16] )
    ckeydata = bytes(ckeydata)
    
    header = b'OTE1' + bytes( [hintsize % 256, hintsize // 256] ) + hint + salt + pwhash + ckeydata + iv # header byte

    keys = expandkey(ckey) # 16B * 32 keys
    ivs = [iv] * 32 # 16B * 32 ivs
    filesize = os.path.getsize('tempkaesl') # target size
    chunknum0 = filesize // 131072 # chunk num
    chunknum1 = filesize % 131072 # left size

    with open(path,'wb') as f:
        with open('tempkaesl','rb') as t:
            f.write(header)
            print('encrypting header')
            p = mp.Pool(8)
            order = [0] * 8 # order buffer
            write = [b''] * 32 # write buffer
            count = 0 # iv, key position

            for i in range(0,chunknum0):
                tempdata = t.read(131072) # 128kb
                if (i + 1) % 100 == 0:
                    print(f'encrypting {i + 1}/{chunknum0 + 1}')
                order[count % 8] = p.apply_async( inline1,(keys[count], ivs[count], tempdata) )

                if count % 8 == 7:
                    for j in range(0,8):
                        write[count - 7 + j] = order[j].get()
                        ivs[count - 7 + j] = write[count - 7 + j][-16:]
                    order = [0] * 8 # reset

                if count == 31:
                    f.write( b''.join(write) )
                    count = -1 # reset
                    write = [b''] * 32 # reset

                count = count + 1

            for i in range(0,chunknum0 % 8):
                write[count - (chunknum0 % 8) + i] = order[i].get()
                ivs[count - (chunknum0 % 8) + i] = write[count - (chunknum0 % 8) + i][-16:]
            f.write( b''.join(write) )

            pad = lambda x : x + bytes(chr(16 - len(x)),'utf-8') * (16 - len(x))
            tempdata = t.read(chunknum1)
            tempdata = tempdata[0:chunknum1 - (chunknum1 % 16)] + pad( tempdata[chunknum1 - (chunknum1 % 16):] )
            f.write( inline1(keys[count], ivs[count], tempdata) )
            print(f'encrypting {chunknum0 + 1}/{chunknum0 + 1}')

# short decryption no padding, 16B * n
def inline2(key,iv,data): # key : byte, iv : byte, data : byte
    func = AES.new(key,AES.MODE_CBC,iv).decrypt
    num = len(data)
    out = [0] * num
    for i in range(0,num // 16):
        temp = 16*i
        out[temp:temp+16] = func( data[temp:temp+16] )
    return bytes(out)

# decrypt(file) -> tempkaesl, 32 process
def decrypt32(target, pw): # target : file path, pw : str, path : folder path
    with open(target,'rb') as f:
        f.read(4)
        tempbyte = f.read(2)
        hintbyte = f.read(tempbyte[0] + tempbyte[1] * 256)
        saltbyte = f.read(32) # salt byte 32B
        pwhash = f.read(32) # pwhash byte 32B
        ckeydata = f.read(128) # ckeydata byte 128B
        iv = f.read(16) # iv byte 16B

        pw = bytes(pw, encoding='utf-8') # pw byte
        mkey = pw # master key byte
        for i in range(0,10000):
            mkey = hashlib.sha3_256(mkey + saltbyte).digest()

        func = AES.new( mkey[16:32], AES.MODE_CBC, mkey[0:16] ).decrypt
        contentkey = [0] * 128 # content key
        for i in range(0,8):
            contentkey[16*i:16*i+16] = func( ckeydata[16*i:16*i+16] )
        contentkey = bytes(contentkey)

        filesize = os.path.getsize(target) - len(hintbyte) - 214 # actual file size
        chunknum0 = filesize // 131072 # chunk num
        chunknum1 = filesize % 131072 # left size
        if chunknum1 == 0:
            chunknum0 = chunknum0 - 1
            chunknum1 = 131072

        keys = expandkey(contentkey) # 16B * 32 keys
        ivs = [iv] * 32 # 16B * 32 ivs

        with open('tempkaesl','wb') as t:
            print('decrypting header')
            p = mp.Pool(32)
            order = [0] * 32 # order buffer
            write = [b''] * 32 # write buffer
            count = 0 # iv, key position

            for i in range(0,chunknum0):
                tempdata = f.read(131072) # 128kb
                if (i + 1) % 100 == 0:
                    print(f'decrypting {i + 1}/{chunknum0 + 1}')
                order[count] = p.apply_async( inline2,(keys[count], ivs[count], tempdata) )
                ivs[count] = tempdata[-16:]

                if count == 31:
                    for j in range(0,32):
                        write[j] = order[j].get()
                    t.write( b''.join(write) )
                    count = -1 # reset
                    order = [0] * 32 # reset
                    write = [b''] * 32 # reset

                count = count + 1

            for i in range(0,chunknum0 % 32):
                write[i] = order[i].get()
                ivs[i] = write[i][-16:]
            t.write( b''.join(write) )

            unpad = lambda x : x[:-x[-1]]
            tempdata = f.read(chunknum1)
            tempbyte = inline2(keys[count], ivs[count], tempdata)
            tempbyte = tempbyte[0:-16] + unpad( tempbyte[-16:] )
            t.write(tempbyte)
            print(f'decrypting {chunknum0 + 1}/{chunknum0 + 1}')

# decrypt(file) -> tempkaesl, 8 process
def decrypt8(target, pw): # target : file path, pw : str, path : folder path
    with open(target,'rb') as f:
        f.read(4)
        tempbyte = f.read(2)
        hintbyte = f.read(tempbyte[0] + tempbyte[1] * 256)
        saltbyte = f.read(32) # salt byte 32B
        pwhash = f.read(32) # pwhash byte 32B
        ckeydata = f.read(128) # ckeydata byte 128B
        iv = f.read(16) # iv byte 16B

        pw = bytes(pw, encoding='utf-8') # pw byte
        mkey = pw # master key byte
        for i in range(0,10000):
            mkey = hashlib.sha3_256(mkey + saltbyte).digest()

        func = AES.new( mkey[16:32], AES.MODE_CBC, mkey[0:16] ).decrypt
        contentkey = [0] * 128 # content key
        for i in range(0,8):
            contentkey[16*i:16*i+16] = func( ckeydata[16*i:16*i+16] )
        contentkey = bytes(contentkey)

        filesize = os.path.getsize(target) - len(hintbyte) - 214 # actual file size
        chunknum0 = filesize // 131072 # chunk num
        chunknum1 = filesize % 131072 # left size
        if chunknum1 == 0:
            chunknum0 = chunknum0 - 1
            chunknum1 = 131072

        keys = expandkey(contentkey) # 16B * 32 keys
        ivs = [iv] * 32 # 16B * 32 ivs

        with open('tempkaesl','wb') as t:
            print('decrypting header')
            p = mp.Pool(8)
            order = [0] * 8 # order buffer
            write = [b''] * 32 # write buffer
            count = 0 # iv, key position

            for i in range(0,chunknum0):
                tempdata = f.read(131072) # 128kb
                if (i + 1) % 100 == 0:
                    print(f'decrypting {i + 1}/{chunknum0 + 1}')
                order[count % 8] = p.apply_async( inline2,(keys[count], ivs[count], tempdata) )
                ivs[count] = tempdata[-16:]

                if count % 8 == 7:
                    for j in range(0,8):
                        write[count - 7 + j] = order[j].get()
                    order = [0] * 8 # reset

                if count == 31:
                    t.write( b''.join(write) )
                    count = -1 # reset
                    write = [b''] * 32 # reset

                count = count + 1

            for i in range(0,chunknum0 % 8):
                write[count - (chunknum0 % 8) + i] = order[i].get()
                ivs[count - (chunknum0 % 8) + i] = write[count - (chunknum0 % 8) + i][-16:]
            t.write( b''.join(write) )

            unpad = lambda x : x[:-x[-1]]
            tempdata = f.read(chunknum1)
            tempbyte = inline2(keys[count], ivs[count], tempdata)
            tempbyte = tempbyte[0:-16] + unpad( tempbyte[-16:] )
            t.write(tempbyte)
            print(f'decrypting {chunknum0 + 1}/{chunknum0 + 1}')

# valid pw check
def check(salt, pw, pwhash): # salt : bytes, pw : str, pwhash : bytes
    pw = bytes(pw, encoding='utf-8') # pw byte
    pwcheck = pw # pwh byte
    for i in range(0,100000):
        pwcheck = hashlib.sha3_256(salt + pwcheck).digest()
    return pwhash == pwcheck

# valid file check, get pwhs
def view(target): # target : file path
    with open(target,'rb') as f:
        if f.read(4) == b'OTE1':
            tempbyte = f.read(2)
            hintbyte = f.read(tempbyte[0] + tempbyte[1] * 256)
            saltbyte = f.read(32)
            pwhash = f.read(32)
            return [b'\x00', hintbyte, saltbyte, pwhash]
        else:
            return [b'\x01', b'', b'', b'']

# manager
def main(mode):
    re = True
    if mode == '1':
        files = [ ]
        temp = ' '
        while temp != '':
            temp = input('file loc + name (press enter to stop) : ')
            if temp != '':
                files.append(temp)
        hint = input('pw hint : ') # hint str
        pw = input('pw : ') # pw str
        path = os.path.join(os.path.expanduser('~'),'Desktop')
        path = os.path.join(path,f'kaesl{1000 + secrets.randbelow(9000)}.ote') # writing path
        dm = input('advanced delete activate? (0 : Y, others : N) : ')
        dozip(files)
        encrypt32(hint,pw,path)
        if dm == '0':
            delete('tempkaesl',0)
        else:
            delete('tempkaesl',1)
        print('process complete : 1')
        
    elif mode == '2':
        files = [ ]
        temp = ' '
        while temp != '':
            temp = input('file loc + name (press enter to stop) : ')
            if temp != '':
                files.append(temp)
        hint = input('pw hint : ') # hint str
        pw = input('pw : ') # pw str
        path = os.path.join(os.path.expanduser('~'),'Desktop')
        path = os.path.join(path,f'kaesl{1000 + secrets.randbelow(9000)}.ote') # writing path
        dm = input('advanced delete activate? (0 : Y, others : N) : ')
        dozip(files)
        encrypt8(hint,pw,path)
        if dm == '0':
            delete('tempkaesl',0)
        else:
            delete('tempkaesl',1)
        print('process complete : 2')
        
    elif mode == '3':
        file = input('ote file to decrypt : ')
        path = input('extract files to : ')
        temp = view(file)
        if temp[0] == b'\x00':
            print(f'===== hint =====\n{str(temp[1],encoding="utf-8")}')
            pw = '\x00'
            while not( check( temp[2], pw, temp[3] ) ):
                pw = input('password : ')
            dm = input('advanced delete activate? (0 : Y, others : N) : ')
            decrypt32(file, pw)
            unzip(path)
            if dm == '0':
                delete('tempkaesl',0)
            else:
                delete('tempkaesl',1)
        else:
            print('not valid ote1 file')
        print('process complete : 3')
        
    elif mode == '4':
        file = input('ote file to decrypt : ')
        path = input('extract files to : ')
        temp = view(file)
        if temp[0] == b'\x00':
            print(f'===== hint =====\n{str(temp[1],encoding="utf-8")}')
            pw = '\x00'
            while not( check( temp[2], pw, temp[3] ) ):
                pw = input('password : ')
            dm = input('advanced delete activate? (0 : Y, others : N) : ')
            decrypt8(file, pw)
            unzip(path)
            if dm == '0':
                delete('tempkaesl',0)
            else:
                delete('tempkaesl',1)
        else:
            print('not valid ote1 file')
        print('process complete : 4')
        
    elif mode == '5':
        re = False
        
    else:
        print('unknown mode')
        
    return re
    
if __name__ == '__main__':
    mp.freeze_support()
    off = True
    while off:
        mode = input('\n1 : encrypt32, 2 : encrypt8, 3 : decrypt32, 4 : decrypt8, 5 : exit\n>>> ')
        try:
            off = main(mode)
        except Exception as e:
            print(e)

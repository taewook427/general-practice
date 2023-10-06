# KAES4 in

import multiprocessing as mp
from Cryptodome.Cipher import AES

# short encryption no padding 16nB
def enshort(key, iv, data): # bytes, bytes, bytes
    func = AES.new(key,AES.MODE_CBC,iv).encrypt
    num = len(data)
    out = [0] * num
    for i in range(0, num // 16):
        temp = 16*i
        out[temp:temp+16] = func( data[temp:temp+16] )
    return bytes(out) # bytes

# short decryption no padding 16nB
def deshort(key, iv, data): # bytes, bytes, bytes
    func = AES.new(key,AES.MODE_CBC,iv).decrypt
    num = len(data)
    out = [0] * num
    for i in range(0, num // 16):
        temp = 16*i
        out[temp:temp+16] = func( data[temp:temp+16] )
    return bytes(out) # bytes

# ckey + data -> encryption
def enin(ckey, data): # bytes 1536B, bytes
    key = [0] * 32 # key list
    iv = [0] * 32 # iv list
    for i in range(0, 32):
        key[i] = ckey[32 * i : 32 * i + 32]
        iv[i] = ckey[1024 + 16 * i : 1024 + 16 * i + 16]
    size = len(data)
    num0 = size // 131072 # chunk num
    num1 = size % 131072 # left size
    temp = [0] * 32 # encryption buffer
    out = [ ] # output buffer
    p = mp.Pool(32)
    count = 0 # iv, key position

    for i in range(0, num0):
        tempdata = data[131072 * i : 131072 * i + 131072] # 128kb
        temp[count] = p.apply_async( enshort, (key[count], iv[count], tempdata) )
        if count == 31:
            for j in range(0,32):
                temp[j] = temp[j].get()
                iv[j] = temp[j][-16:]
            out = out + temp
            temp = [0] * 32 # reset
            count = -1 # reset
        count = count + 1
    for i in range(0, num0 % 32):
        temp[i] = temp[i].get()
        iv[i] = temp[i][-16:]
    if num0 % 32 != 0:
        out = out + temp[0:num0 % 32]
    pad = lambda x : x + bytes(chr(16 - len(x) % 16),'utf-8') * (16 - len(x) % 16)
    tempdata = data[131072 * num0:]
    tempdata = pad(tempdata)
    out.append( enshort(key[count], iv[count], tempdata) )
    p.close()
    p.join()

    return b''.join(out) # bytes

# ckey + encryption -> data
def dein(ckey, data): # bytes 1536B, bytes
    key = [0] * 32
    iv = [0] * 32
    for i in range(0, 32):
        key[i] = ckey[32 * i : 32 * i + 32]
        iv[i] = ckey[1024 + 16 * i : 1024 + 16 * i + 16]
    size = len(data)
    num0 = size // 131072 # chunk num
    num1 = size % 131072 # left size
    if num1 == 0:
        num0 = num0 - 1
        num1 = 131072
    temp = [0] * 32 # decryption buffer
    out = [ ] # output buffer
    p = mp.Pool(32)
    count = 0 # iv, key position

    for i in range(0,num0):
        tempdata = data[131072 * i : 131072 * i + 131072] # 128kb
        temp[count] = p.apply_async( deshort, (key[count], iv[count], tempdata) )
        iv[count] = tempdata[-16:]
        if count == 31:
            for j in range(0,32):
                temp[j] = temp[j].get()
            out = out + temp
            temp = [0] * 32 # reset
            count = -1 # reset
        count = count + 1
    for i in range(0, num0 % 32):
        temp[i] = temp[i].get()
    if num0 % 32 != 0:
        out = out + temp[0:num0 % 32]
    unpad = lambda x : x[:-x[-1]]
    tempdata = data[131072 * num0:]
    out.append( unpad( deshort(key[count], iv[count], tempdata) ) )
    p.close()
    p.join()

    return b''.join(out) # bytes

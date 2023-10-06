import tkinter
import tkinter.messagebox
import time
import random
import hashlib
import os
from Cryptodome.Cipher import AES

class getsalt:
    def __init__(self):
        output = ''
        for i in range(0,80):
            output = output + chr(random.randrange(32,126))
        self.salt = output

class gethash:
    def type0(self,letter):
        return hashlib.sha3_512( ( letter ).encode( 'utf-8' )).hexdigest()
    def type1(self,letter):
        return hashlib.sha256( ( letter ).encode( 'utf-8' )).hexdigest()
    def type2(self,hexa):
        return hashlib.md5( hexa ).hexdigest()
    def type3(self,hashin,salt):
        output = [ ]
        rawhash = [ ]
        for i in range(0,32):
            rawhash.append( hashin[ 2 * i : 2 * i + 2 ] )
        for i in rawhash:
            temp = hashlib.sha256( ( i + salt ).encode( 'utf-8' )).hexdigest()
            for j in range(0,32):
                output.append( temp[ 2 * j : 2 * j + 2 ] )
        return output

class v1func:
    def minus(self,a,b):
        c = int.from_bytes(a,byteorder = 'big')
        d = int(b,base = 16)
        e = (c - d) % 256
        e = hex(e)[2:]
        if len(e) == 1:
            e = '0' + e
        return bytes.fromhex(e)
    def decrypt_sys(self,filename,key):
        time.sleep(0.5)
        old = open(filename,'rb')
        new = open(filename[:-2],'wb')
        temp = old.read(400)
        converted = 0
        temp = old.read(1)
        f = open('0 MB','wb')
        f.close()
        k = '0'
        med = v1func()
        while not temp == b'':
            tempkey = key[ converted % 1024 ]
            towrite = med.minus(temp,tempkey)
            new.write(towrite)
            converted = converted + 1
            temp = old.read(1)
            if converted % (1048576*5) == 0:
                k = converted // 1048576
                j = k - 5
                k = str(k)
                j = str(j)
                os.remove(j + ' MB')
                f = open(k + ' MB','wb')
                f.close()
        os.remove(k + ' MB')
        old.close()
        new.close()
        global mainconst
        mainconst = 1
    def decrypt(self,filename):
        try:
            f = open(filename)
            f.close()
            raw = open(filename,'rb')
            magicnum_b = raw.read(4)
            salt_b = raw.read(40)
            hash1_b  = raw.read(32)
            hint_b = raw.read(324)
            raw.close()

            if not magicnum_b == b'.kos':
                adwin = tkinter.Tk()
                adwin.geometry('10x10+10+10')
                i = tkinter.messagebox.showinfo('Error : 파일손상','파일을 읽을 수 없습니다.\n파일 헤더가 손상되었는지 확인하십시오.')
                adwin.destroy()
            elif not filename[-2:] == '.k':
                adwin = tkinter.Tk()
                adwin.geometry('10x10+10+10')
                i = tkinter.messagebox.showinfo('Error : 확장자 이상','파일 확장자가 .k 여야 합니다.\nExample.txt.k 와 같이 확장자를 변경해 주십시오.')
                adwin.destroy()
            else:
                salt = str( salt_b , 'utf-8' )
                hash1 = ''
                for i in hash1_b:
                    temp = hex(i)[2:]
                    if len(temp) == 1:
                        temp = '0' + temp
                    hash1 = hash1 + temp
                hint = str( hint_b , 'utf-8' )

                def decrypt():
                    time.sleep(0.2)
                    password = textbox3.get()
                    mob = gethash()
                    if hash1 == mob.type1(salt + password):
                        key = mob.type3( mob.type1( password + salt ) , salt )
                        i = tkinter.messagebox.showinfo('변환 시작','파일 변환이 시작됩니다.\n파일이 위치한 폴더에 진행 사항이 표시됩니다.\n시간이 좀 걸릴 수 있습니다.')
                        dewin.destroy()
                        mav = v1func()
                        mav.decrypt_sys(filename,key)
                        adwin = tkinter.Tk()
                        adwin.geometry('10x10+10+10')
                        time.sleep(0.5)

                        global erase_mode
                        if erase_mode == 1:
                            f = open(filename,'wb')
                            rdata = b''
                            for i in range(0,32):
                                rdata = rdata + bytes.fromhex(mob.type1(filename+str(i)))
                            for i in range(0,5*1024):
                                f.write(rdata)
                            f.close()
                            os.remove(filename)
                        i = tkinter.messagebox.showinfo('변환 완료','파일 변환이 완료되었습니다.')
                        adwin.destroy()
                    else:
                        i = tkinter.messagebox.showinfo('Error : 비밀번호 불일치','비밀번호가 일치하지 않습니다.\n다시 입력해 주십시오.')

                def seehint():
                    time.sleep(0.2)
                    i = tkinter.messagebox.showinfo('비밀번호 힌트보기',hint)

                def txtmodech():
                    global erase_mode
                    if erase_mode == 0:
                        erase_mode = 1
                        txtmode.set('원본 파일 : \n\n삭제됨')
                    else:
                        erase_mode = 0
                        txtmode.set('원본 파일 : \n\n유지됨')

                dewin = tkinter.Tk()
                dewin.title('Cryptography V1')
                dewin.geometry('400x200+500+400')
                dewin.resizable(0,0)
                label1 = tkinter.Label(dewin, text='비밀번호를 정확히 입력하세요')
                label1.place(x = 110,y = 10)
                textbox3 = tkinter.Entry(dewin, width=40)
                textbox3.grid(column = 0 , row = 0)
                textbox3.place(x=55,y=50)
                debut = tkinter.Button(dewin,text = '\n  입력  \n',command = decrypt)
                debut.place(x = 50,y = 110)
                hintbut = tkinter.Button(dewin,text = '\n 힌트보기 \n',command = seehint)
                hintbut.place(x = 270,y = 110)
                global erase_mode
                erase_mode = 0
                txtmode = tkinter.StringVar()
                txtmode.set('원본 파일 : \n\n유지됨')
                delbut = tkinter.Button(dewin,textvariable = txtmode,command = txtmodech)
                delbut.place(x = 150,y = 110)
                dewin.mainloop()

        except:
            i = tkinter.messagebox.showinfo('Error : 파일위치','파일을 찾을 수 없습니다.\n같은 폴더 내의 파일 이름과 확장자를 \n정확히 입력했는지 확인하십시오.')
            
class aes_func:
    def set_ecb(self,key):
        self.key = key
        self.e_cipher = AES.new(self.key,AES.MODE_ECB)
        self.d_cipher = AES.new(self.key,AES.MODE_ECB)
    def set_cbc(self,key,iv):
        self.key = key
        self.iv = iv
        self.e_cipher = AES.new(self.key,AES.MODE_CBC,self.iv)
        self.d_cipher = AES.new(self.key,AES.MODE_CBC,self.iv)
    def en_ecb(self,data):
        return self.e_cipher.encrypt(data)
    def de_ecb(self,data):
        return self.d_cipher.decrypt(data)
    def en_cbc(self,data):
        return self.e_cipher.encrypt(data)
    def de_cbc(self,data):
        return self.d_cipher.decrypt(data)

class main_structure:
    def __init__(self):
        def info():
            infotitle = 'Cryptography V2 INFO'
            infocontent = '''이 프로그램은 파일 암호화로 데이터를 제 3자가
열어볼 수 없게 합니다. 암호화 방식은 현재 국제표준인
SHA3-512, AES-256을 사용합니다.

V1 버전에 비해 편의성과 보안성이 향상되었습니다.
원본파일 삭제 여부와 파일 이름 숨기기 여부의 기본값은
*삭제안함 *숨기지않음 입니다.
암호화 무결성 검사는 기본값이 *진행 입니다.
이는 파일 암호화 창에서 설정할 수 있습니다.
'''
            i = tkinter.messagebox.showinfo(infotitle,infocontent)
        def encrypt():
            self.encrypt()
        def decrypt():
            self.decrypt()
        def endall():
            i = tkinter.messagebox.askokcancel('끝내기','종료하시겠습니까?')
            if not i == 0:
                mainwin.destroy()
                time.sleep(0.5)
                global kos
                kos = 0
                quit()

        global mainwin
        mainwin = tkinter.Tk()
        mainwin.title('Cryptography V2')
        mainwin.geometry('400x200+500+400')
        mainwin.resizable(0,0)
        label1 = tkinter.Label(mainwin, text='파일이름을 확장자까지 정확하게 입력해 주세요')
        label1.place(x = 70,y = 10)
        global textbox0
        textbox0 = tkinter.Entry(mainwin, width=40)
        textbox0.grid(column = 0 , row = 0)
        textbox0.place(x=55,y=50)
        infobut = tkinter.Button(mainwin,text = '\n  INFO  \n',command = info)
        infobut.place(x = 50,y = 110)
        enbut = tkinter.Button(mainwin,text = '\n 암호화 \n',command = encrypt)
        enbut.place(x = 130,y = 110)
        debut = tkinter.Button(mainwin,text = '\n 복호화 \n',command = decrypt)
        debut.place(x = 210,y = 110)
        endbut = tkinter.Button(mainwin,text = '\n 끝내기 \n',command = endall)
        endbut.place(x = 290,y = 110)

        mainwin.mainloop()
    def encrypt(self):
        global textbox0
        global mainwin
        filename = textbox0.get()
        try:
            f = open(filename)
            f.close()
            mainwin.destroy()
            time.sleep(0.5)
            work = v2func()
            work.encrypt(filename)
        except:
            i = tkinter.messagebox.showinfo('Error : 파일위치','파일을 찾을 수 없습니다.\n같은 폴더 내의 파일 이름과 확장자를 \n정확히 입력했는지 확인하십시오.')
        
    def decrypt(self):
        global textbox0
        global mainwin
        filename = textbox0.get()
        try:
            f = open(filename)
            f.close()
            raw = open(filename,'rb')
            magicnum_b = raw.read(4)
            raw.close()
            if magicnum_b == b'.kos':
                time.sleep(0.5)
                mainwin.destroy()
                work = v1func()
                work.decrypt(filename)
            elif magicnum_b == b'kos2':
                time.sleep(0.5)
                mainwin.destroy()
                work = v2func()
                work.decrypt(filename)
            else:
                i = tkinter.messagebox.showinfo('Error : 파일손상','파일을 읽을 수 없습니다.\n파일 헤더가 손상되었는지 확인하십시오.')

        except:
            i = tkinter.messagebox.showinfo('Error : 파일위치','파일을 찾을 수 없습니다.\n같은 폴더 내의 파일 이름과 확장자를 \n정확히 입력했는지 확인하십시오.')

class v2func:
    def encrypt(self,filename):
        def start_en():
            password = textbox1.get()
            hint = textbox2.get()
            hint_b = bytes(hint,'utf-8')
            if len(hint_b) > 600:
                i = tkinter.messagebox.showinfo('Error : 힌트크기','힌트 크기가 너무 큽니다.\n600바이트 이하로 적어 주십시오.\n현재 : '+str(len(hint_b))+' 바이트')
            else:
                length = len(password)
                txt = '비밀번호를 다음과 같이 설정합니다 :\n' + password
                txt = txt + '\n * ( ' + str(length) + ' ) 글자'
                txt = txt + '\n\n암호힌트를 다음과 같이 설정합니다 :\n' + hint
                i = tkinter.messagebox.askokcancel('비밀번호 확인',txt)
                if not i == 0:
                    time.sleep(0.5)
                    i = tkinter.messagebox.showinfo('변환 시작','파일 변환이 시작됩니다.\n파일이 위치한 폴더에 진행 사항이 표시됩니다.\n시간이 좀 걸릴 수 있습니다.')
                    enwin.destroy()
                    work = v2func()
                    work.en_sys(filename,password,hint)

        def erase_ch():
            global erase_mode
            if erase_mode == 0:
                erase_mode = 1
                erase_txt.set('  원본 파일 : \n\n삭제됨  ')
            else:
                erase_mode = 0
                erase_txt.set('  원본 파일 : \n\n유지됨  ')

        def hide_ch():
            global hide_mode
            if hide_mode == 0:
                hide_mode = 1
                hide_txt.set('  원본 이름 : \n\n숨겨짐  ')
            else:
                hide_mode = 0
                hide_txt.set('  원본 이름 : \n\n공개됨  ')

        def check_ch():
            global check_mode
            if check_mode == 0:
                check_mode = 1
                check_txt.set('무결성검사 : \n\n진행됨')
            else:
                check_mode = 0
                check_txt.set('무결성검사 : \n\n취소됨')
        
        enwin = tkinter.Tk()
        enwin.title('Cryptography V2')
        enwin.geometry('400x200+500+400')
        enwin.resizable(0,0)
        label1 = tkinter.Label(enwin, text='파일 : ' + filename)
        label1.place(x = 30,y = 10)

        if len(bytes(filename,'utf-8')) > 255:
            i = tkinter.messagebox.showinfo('파일이름 크기경고','파일 이름이 256바이트 이상입니다.\n이름 숨기기 모드 사용시\n데이터가 소실될 수 있습니다.')
        
        label2 = tkinter.Label(enwin, text='비밀번호 설정 :')
        label2.place(x = 30,y = 40)
        textbox1 = tkinter.Entry(enwin, width=30)
        textbox1.grid(column = 0 , row = 0)
        textbox1.place(x=130,y=42)
        label3 = tkinter.Label(enwin, text='암호힌트 설정 :')
        label3.place(x = 30,y = 65)
        textbox2 = tkinter.Entry(enwin, width=30)
        textbox2.grid(column = 0 , row = 0)
        textbox2.place(x=130,y=67)

        
        putinbut = tkinter.Button(enwin,text = '\n       입력       \n',command = start_en)
        putinbut.place(x = 15,y = 125)
        global erase_mode
        erase_mode = 0
        erase_txt = tkinter.StringVar()
        erase_txt.set('  원본 파일 : \n\n유지됨  ')
        erasebut = tkinter.Button(enwin,textvariable = erase_txt,command = erase_ch)
        erasebut.place(x = 117,y = 125)
        global hide_mode
        hide_mode = 0
        hide_txt = tkinter.StringVar()
        hide_txt.set('  원본 이름 : \n\n공개됨  ')
        hidebut = tkinter.Button(enwin,textvariable = hide_txt,command = hide_ch)
        hidebut.place(x = 210,y = 125)
        global check_mode
        check_mode = 1
        check_txt = tkinter.StringVar()
        check_txt.set('무결성검사 : \n\n진행됨')
        checkbut = tkinter.Button(enwin,textvariable = check_txt,command = check_ch)
        checkbut.place(x = 300,y = 125)
        
        enwin.mainloop()

    def en_sys(self,filename,password,hint):
        salt = getsalt()
        salt_txt = salt.salt
        dohash = gethash()
        pwhash_b = bytes.fromhex(dohash.type0(salt_txt[0:40] + password + salt_txt[40:80]))
        hint = hint + (' ' * 600)
        hint_b = bytes(hint,'utf-8')
        hint_b = hint_b[0:600]
        global erase_mode
        global hide_mode
        global check_mode

        content_key = bytes.fromhex(dohash.type1(salt_txt[0:20] + password + salt_txt[20:80]))
        content_iv = bytes.fromhex(dohash.type2(content_key))
        title_key = bytes.fromhex(dohash.type1(salt_txt[0:60] + password + salt_txt[60:80]))
        title_iv = bytes.fromhex(dohash.type2(title_key))
        
        if hide_mode == 0:
            ori_name_b = b'\x00' * 256
            ori_len_b = b'\x00\x00'
            mode_b = b'op'
        else:
            ori_len_num = len( bytes(filename,'utf-8') )
            ori_name = filename + (' '*256)
            ori_name = bytes(ori_name,'utf-8')[0:256]
            title_en = aes_func()
            title_en.set_cbc(title_key,title_iv)
            ori_name_b = b''
            for i in range(0,16):
                ori_name_b = ori_name_b + title_en.en_cbc( ori_name[16*i:16*i+16] )
            ori_len_num = hex(ori_len_num)[2:]
            if len(ori_len_num) == 1:
                ori_len_num = '0' + ori_len_num
            ori_len_b = bytes.fromhex(ori_len_num)
            ori_len_b = b'\x00' + ori_len_b
            mode_b = b'hi'
        header_b = b'kos2' + bytes(salt_txt,'utf-8') + pwhash_b + hint_b + ori_name_b + ori_len_b + mode_b
        header_b = header_b + bytes.fromhex(dohash.type2(header_b))
        
        if hide_mode == 0:
            new_name = filename + '.k'
        else:
            new_name = ''
            for i in range(0,4):
                new_name = new_name + str(random.randrange(0,9))
            new_name = new_name + '.k'
        tgt = open(new_name,'wb')
        raw = open(filename,'rb')
        content_en = aes_func()
        content_en.set_cbc(content_key,content_iv)
        tgt.write(header_b)
        
        converted = 0
        f = open('0 MB','wb')
        f.close()
        k = 0
        temp = 0
        while not temp == b'':
            temp = raw.read(16)
            converted = converted + 16
            if converted % 20971520 == 0:
                os.remove(str(k)+' MB')
                k = converted // 1048576
                f = open(str(k)+' MB','wb')
                f.close()
            if len(temp) == 16:
                t_data = temp
                tgt.write(content_en.en_cbc(temp))
            elif len(temp) == 0:
                tgt.write(content_en.en_cbc(b'\x00'*16))
            else:
                t_data = temp
                pad = lambda x : x + bytes(chr(16 - len(x)),'utf-8') * (16 - len(x))
                tgt.write(content_en.en_cbc(pad(temp)))
                break
        os.remove(str(k)+' MB')
        tgt.close()
        raw.close()

        if check_mode == 1:
            tgt = open(new_name,'rb')
            raw = tgt.read(1008)
            raw = bytes.fromhex(dohash.type2(raw))
            md5hash = tgt.read(16)
            tgt.close()
            chk_work = v2func()
            chk = chk_work.de_sys('무결성 검사 진행중',new_name,salt_txt,password)

            if not ( (md5hash == raw) and (t_data == chk) ):
                adwin = tkinter.Tk()
                adwin.geometry('10x10+10+10')
                time.sleep(0.5)
                i = tkinter.messagebox.showinfo('무결성 문제','변환된 파일에 이상이 감지되었습니다.\n다시 시도하세요.')
                adwin.destroy()

            f = open('무결성 검사 진행중','wb')
            rdata = b''
            for i in range(0,32):
                rdata = rdata + bytes.fromhex(dohash.type1(filename+str(i)))
            for i in range(0,5*1024):
                f.write(rdata)
            f.close()
            os.remove('무결성 검사 진행중')

        if erase_mode == 1:
            f = open(filename,'wb')
            rdata = b''
            for i in range(0,32):
                rdata = rdata + bytes.fromhex(dohash.type1(filename+str(i)))
            for i in range(0,5*1024):
                f.write(rdata)
            f.close()
            os.remove(filename)

        adwin = tkinter.Tk()
        adwin.geometry('10x10+10+10')
        time.sleep(0.5)
        i = tkinter.messagebox.showinfo('변환 완료','파일 변환이 완료되었습니다.')
        adwin.destroy()

    def decrypt(self,filename):
        dohash = gethash()

        f = open(filename,'rb')
        md5hash = bytes.fromhex( dohash.type2( f.read(1008) ) )
        f.close()
        
        raw = open(filename,'rb')
        magicnum_b = raw.read(4)
        salt = str(raw.read(80),'utf-8')
        pwhash_b = raw.read(64)
        hint = str(raw.read(600),'utf-8')
        title_b = raw.read(256)
        title_len = raw.read(1)
        if not title_len == b'\x00':
            ko = b'\xea\xb3\xa0\xed\x83\x9c\xec\x9a\xb1'
            f = open(str(ko,'utf-8'),'wb')
            f.close()
        title_len = ord( raw.read(1) )
        mode_b = raw.read(2)
        md5_b = raw.read(16)
        raw.close()

        if not magicnum_b == b'kos2':
            adwin = tkinter.Tk()
            adwin.geometry('10x10+10+10')
            i = tkinter.messagebox.showinfo('Error : 파일손상','파일을 읽을 수 없습니다.\n파일 헤더가 손상되었는지 확인하십시오.')
            adwin.destroy()
        elif not filename[-2:] == '.k':
            adwin = tkinter.Tk()
            adwin.geometry('10x10+10+10')
            i = tkinter.messagebox.showinfo('Error : 확장자 이상','파일 확장자가 .k 여야 합니다.\nExample.txt.k 와 같이 확장자를 변경해 주십시오.')
            adwin.destroy()
        elif not md5hash == md5_b:
            adwin = tkinter.Tk()
            adwin.geometry('10x10+10+10')
            i = tkinter.messagebox.showinfo('Error : 파일손상','파일을 읽을 수 없습니다.\n파일 헤더가 손상되었는지 확인하십시오.')
            adwin.destroy()
        else:
            def decrypt():
                time.sleep(0.2)
                password = textbox3.get()
                mob = gethash()
                nonlocal pwhash_b
                nonlocal salt
                nonlocal mode_b
                nonlocal title_len
                nonlocal title_b
                
                if pwhash_b == bytes.fromhex( mob.type0(salt[0:40] + password + salt[40:80]) ):

                    if mode_b == b'hi':
                        title_key = bytes.fromhex(mob.type1(salt[0:60] + password + salt[60:80]))
                        title_iv = bytes.fromhex(mob.type2(title_key))
                        title = b''
                        title_aes = aes_func()
                        title_aes.set_cbc(title_key,title_iv)
                        for i in range(0,16):
                            k = title_aes.de_cbc( title_b[16*i:16*i+16] )
                            title = title + k
                        title = str(title,'utf-8')
                        title = title[0:title_len]
                    else:
                        if not mode_b == b'op':
                            f = open('2021.12.19','wb')
                            f.close()
                            mode_b = b'op'
                        title = filename[0:-2]
                    
                    i = tkinter.messagebox.showinfo('변환 시작','파일 변환이 시작됩니다.\n파일이 위치한 폴더에 진행 사항이 표시됩니다.\n시간이 좀 걸릴 수 있습니다.')
                    dewin.destroy()
                    mav = v2func()
                    k = mav.de_sys(title,filename,salt,password)

                    global erase_mode
                    if erase_mode == 1:
                        f = open(filename,'wb')
                        rdata = b''
                        for i in range(0,32):
                            rdata = rdata + bytes.fromhex(mob.type1(filename+str(i)))
                        for i in range(0,5*1024):
                            f.write(rdata)
                        f.close()
                        os.remove(filename)
                    adwin = tkinter.Tk()
                    adwin.geometry('10x10+10+10')
                    time.sleep(0.5)
                    i = tkinter.messagebox.showinfo('변환 완료','파일 변환이 완료되었습니다.')
                    adwin.destroy()
                else:
                    i = tkinter.messagebox.showinfo('Error : 비밀번호 불일치','비밀번호가 일치하지 않습니다.\n다시 입력해 주십시오.')
            def seehint():
                nonlocal hint
                time.sleep(0.2)
                i = tkinter.messagebox.showinfo('비밀번호 힌트보기',hint)

            def txtmodech():
                global erase_mode
                if erase_mode == 0:
                    erase_mode = 1
                    txtmode.set('원본 파일 : \n\n삭제됨')
                else:
                    erase_mode = 0
                    txtmode.set('원본 파일 : \n\n유지됨')
            
            dewin = tkinter.Tk()
            dewin.title('Cryptography V2')
            dewin.geometry('400x200+500+400')
            dewin.resizable(0,0)
            label1 = tkinter.Label(dewin, text='비밀번호를 정확히 입력하세요')
            label1.place(x = 110,y = 10)
            textbox3 = tkinter.Entry(dewin, width=40)
            textbox3.grid(column = 0 , row = 0)
            textbox3.place(x=55,y=50)
            debut = tkinter.Button(dewin,text = '\n    입력    \n',command = decrypt)
            debut.place(x = 50,y = 110)
            hintbut = tkinter.Button(dewin,text = '\n 힌트보기 \n',command = seehint)
            hintbut.place(x = 270,y = 110)
            global erase_mode
            erase_mode = 0
            txtmode = tkinter.StringVar()
            txtmode.set('원본 파일 : \n\n유지됨')
            delbut = tkinter.Button(dewin,textvariable = txtmode,command = txtmodech)
            delbut.place(x = 150,y = 110)
            dewin.mainloop()

    def de_sys(self,filename,enc,salt,password):
        dohash = gethash()
        global erase_mode
        
        content_key = bytes.fromhex(dohash.type1(salt[0:20] + password + salt[20:80]))
        content_iv = bytes.fromhex(dohash.type2(content_key))
        
        tgt = open(filename,'wb')
        raw = open(enc,'rb')
        content_en = aes_func()
        content_en.set_cbc(content_key,content_iv)
        raw.read(1024)
        
        f = open('0 MB','wb')
        f.close()
        k = 0
        
        converted = 16
        temp = raw.read(16)
        pre = content_en.de_cbc(temp)
        while not temp == b'':
            temp = raw.read(16)
            if temp == b'':
                out = b''
            else:
                converted = converted + 16
                if converted % 20971520 == 0:
                    os.remove(str(k)+' MB')
                    k = converted // 1048576
                    f = open(str(k)+' MB','wb')
                    f.close()
                out = pre
                pre = content_en.de_cbc(temp)
            tgt.write(out)
            if not out == b'':
                t_data = out
        os.remove(str(k)+' MB')
        unpad = lambda x : x[:-x[-1]]
        out = unpad(pre)
        if not out == b'':
            t_data = out
        tgt.write(out)

        tgt.close()
        raw.close()

        return t_data
        
kos = 1
while kos == 1:
    time.sleep(0.5)
    do = main_structure()

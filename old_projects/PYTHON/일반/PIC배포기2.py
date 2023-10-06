from tkinter import filedialog
import tkinter
import time
import random
import os
import shutil
import zipfile

def encode(num):
    k = [ ]
    for i in range( 0,4 ):
        k.append( num % 256 )
        num = num // 256
    j = bytes( { k[0] } )
    for i in range( 1,len(k) ):
        j = j + bytes( { k[i] } )
    return j
def decode(binary):
    value = 0
    for i in range( 0,len(binary) ):
        k = 256 ** i
        k = k * binary[i]
        value = value + k
    return value

try:
    shutil.rmtree('temp')
except:
    time.sleep(0.1)

mainwin = tkinter.Tk()
mainwin.title('FR2')
mainwin.geometry('20x20+10+10')
mainwin.resizable(0,0)

print('File Releaser V2 : Madeby KOS 2022')
k = input('PRESS ENTER TO CONTINUE...\n')
print('겉으로 보여질 사진을 선택하세요.')
time.sleep(0.7)
path = os.path.join(os.path.expanduser('~'),'Desktop')
file = filedialog.askopenfile( initialdir=path, title='위장할 사진 선택', filetypes=( ('png files', '*.png'),('jpg files', '*.jpg'),('all files', '*.*') ) )
photo = file.name
print('사진 선택됨 : '+photo)
psize = os.path.getsize(photo)
k = photo.rfind('/')
ptype = (photo[k+1:])
k = ptype.rfind('.')
ptype = (ptype[k+1:])
time.sleep(0.7)
print('압축되어 숨겨질 파일을 선택하세요.')
time.sleep(0.7)
path = os.path.join(os.path.expanduser('~'),'Desktop')
file = filedialog.askopenfile( initialdir=path, title='압축할 파일 선택', filetypes=( ('all files', '*.*'),('exe files', '*.exe') ) )
tgt = file.name
k = tgt.rfind('/')
filename = (tgt[k+1:])
print('파일 선택됨 : '+tgt)
time.sleep(0.7)

mainwin.destroy()
k = input('PRESS ENTER TO CONTINUE...\n')

os.mkdir('temp')
print('임시 폴더 생성됨')

shutil.copyfile(tgt, filename)
print('목표 파일 복사됨')

zip = zipfile.ZipFile("temp\\temp.zip", "w")
zip.write(filename, compress_type=zipfile.ZIP_DEFLATED)
zip.close()
print('임시 압축 파일 생성됨')

os.remove(filename)
print('목표 임시 파일 삭제됨')

setA = b''
setB = b''
setC = b''

tgt = open('temp//temp.zip','rb')
binary = tgt.read()
tgt.close()
print('압축 파일 가공 시작')

mheadloc = decode( binary[-6:-2] )
setC = binary[-2:]
lheadloc = decode( binary[ mheadloc + 42 : mheadloc + 46 ] )
setA = binary[ 0 : mheadloc + 42 ]
setB = binary[ mheadloc + 46 : -6 ]
print('압축 파일 분할 완료')

mheadloc = encode( mheadloc + psize )
lheadloc = encode( lheadloc + psize )
newb = setA + lheadloc + setB + mheadloc + setC
print('압축 파일 재조립 완료')

f = open(photo,'rb')
pbin = f.read()
f.close()
print('이미지 파일 불러옴')

n = ''
for i in range(0,6):
    n = n + str( random.randrange(0,10) )
newname = n + '.' + ptype
newf = open('temp//'+newname,'wb')
newf.write(pbin)
newf.write(newb)
newf.close()
print('결과 파일 생성함')

path = os.path.join(os.path.expanduser('~'),'Desktop')
try:
    shutil.copyfile('temp//'+newname, path + '\\' + newname)
    print('결과물이 바탕 화면으로 이동됨')
except:
    shutil.copyfile('temp//'+newname, newname)
    print('바탕화면접근불가 : 결과물 프로그램동일폴더에 존재')

shutil.rmtree('temp')
print('\n프로그램 동작이 모두 완료되었습니다.')
k = input('PRESS ENTER TO EXIT...')
time.sleep(0.3)

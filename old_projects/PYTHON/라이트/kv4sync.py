# KVault 4 sync (481)

import os
import shutil

import sei

k = sei.standard()
obj = k.init('KVault4sync')
flag = True

k.print(obj[0], obj[1], '원본 클러스터 선택')
f0 = k.select('folder').replace('\\', '/')
if f0 != '':
    k.print(obj[0], obj[1], f'선택됨 : {f0}')
else:
    k.print(obj[0], obj[1], f'선택되지 않음')
    flag = False

k.print(obj[0], obj[1], '사본 클러스터 선택')
f1 = k.select('folder').replace('\\', '/')
if f1 != '':
    k.print(obj[0], obj[1], f'선택됨 : {f1}')
else:
    k.print(obj[0], obj[1], f'선택되지 않음')
    flag = False

if flag:
    k.print(obj[0], obj[1], '시작합니다')

    if os.path.exists(f'{f1}/header.kv4'):
        os.remove(f'{f1}/header.kv4')
        k.print(obj[0], obj[1], '[사본] 헤더 삭제')
    else:
        k.print(obj[0], obj[1], '[사본] 헤더 없음')

    if os.path.exists(f'{f1}/header.kv4.bck'):
        os.remove(f'{f1}/header.kv4.bck')
        k.print(obj[0], obj[1], '[사본] 백업 헤더 삭제')
    else:
        k.print(obj[0], obj[1], '[사본] 백업 헤더 없음')

    if os.path.exists(f'{f0}/header.kv4'):
        shutil.copy(f'{f0}/header.kv4', f'{f1}/header.kv4')
        k.print(obj[0], obj[1], '[원본] [사본] 헤더 복제')
    else:
        k.print(obj[0], obj[1], '[원본] 헤더 없음')

    num = 0
    while os.path.exists(f'{f0}/{num}'):
        num = num + 1
    for i in range(0, num):
        k.print(obj[0], obj[1], f'[원본] {i} 컨테이너 복제 시작')
        if not os.path.exists(f'{f1}/{i}'):
            os.mkdir(f'{f1}/{i}')
            k.print(obj[0], obj[1], f'[사본] {i} 컨테이너 생성됨')
        temp0 = os.listdir(f'{f0}/{i}')
        temp1 = os.listdir(f'{f1}/{i}')

        for j in temp1:
            if j not in temp0:
                os.remove(f'{f1}/{i}/{j}')
                k.print(obj[0], obj[1], f'[사본] {j} 삭제됨')

        for j in temp0:
            if j not in temp1:
                shutil.copy(f'{f0}/{i}/{j}', f'{f1}/{i}/{j}')
                k.print(obj[0], obj[1], f'[원본] [사본] {j} 복제됨')
            else:
                with open(f'{f0}/{i}/{j}', 'rb') as f:
                    bin0 = f.read(4096)
                with open(f'{f1}/{i}/{j}', 'rb') as f:
                    bin1 = f.read(4096)
                if bin0 != bin1:
                    os.remove(f'{f1}/{i}/{j}')
                    shutil.copy(f'{f0}/{i}/{j}', f'{f1}/{i}/{j}')
                    k.print(obj[0], obj[1], f'[원본] [사본] {j} 복제됨')

    while os.path.exists(f'{f1}/{num}'):
        shutil.rmtree(f'{f1}/{num}')
        k.print(obj[0], obj[1], f'[사본] {num} 컨테이너 삭제됨')
        num = num + 1

    k.print(obj[0], obj[1], '[원본] [사본] 복제 완료')

k.print(obj[0], obj[1], '종료합니다')
k.getnum( obj[0] )
k.end( obj[0] )

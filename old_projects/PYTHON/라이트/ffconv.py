import time
import os
import shutil
import sei

k = sei.standard()
temp = k.init('test448')
win = temp[0]
listbox = temp[1]

k.print(win, listbox, '===== FFmpeg 동영상 화질 변환기 =====\n변환할 동영상들을 선택하세요')
time.sleep(0.5)
target = k.select('files')

if len(target) != 0:
    k.print(win, listbox, f'({len(target)}) {target[0]}')

    k.print(win, listbox, '출력 설정 - 1 : 그대로, 2: 숫자, 3 : 0pad숫자, 4 : 알파벳 숫자, 5 : 알파벳 0pad숫자')
    exmod = k.ask5(win)
    if exmod == '3' or exmod == '4':
        k.print(win, listbox, '앞에 추가할 알파벳 입력')
        alpha = k.input0(win)

    k.print(win, listbox, '화질 설정 - 0 : 수동 입력, 1 : 360p, 2 : 480p, 3 : 720p, 4 : 1080p')
    k.print(win, listbox, '5 : 1440p, 6 : 2160p, 7 : 480p 세로, 8 : 720p 세로, 9 : 1080p 세로')
    convmod = int( k.getnum(win) )
    if convmod == 0 or convmod > 9:
        k.print(win, listbox, 'NxM 형식으로 화질 수동 입력')
        convuser = k.input0(win)
    else:
        p = ['', '640x360', '854x480', '1280x720', '1920x1080', '2560x1440', '3840x2160', '480x854', '720x1280', '1080x1920']
        convuser = p[convmod]

    k.print(win, listbox, '대기 시간 설정 (초)')
    wait = int( k.ask5(win) ) + 1

    isalpha = True
    for i in target:
        for j in i:
            if ord(j) > 128:
                isalpha = False
    if isalpha:
        go = True
    else:
        go = k.msg('아스키코드 문제', '대상 파일 이름에서 아스키코드의\n범위를 벗어나는 문자 (한글 등) 감지\n그래도 진행하시겠습니까?', 'ask')

    if go:
        try:
            shutil.rmtree('temp448')
        except:
            pass
        os.mkdir('temp448')

        num = 0
        for i in target:
            order = f'.\\ffmpeg.exe -i "{i}" -s {convuser} -acodec copy '
            if exmod == '0':
                i = i.replace('\\', '/')
                name = i[i.rfind('/') + 1:]
            elif exmod == '1':
                name = str(num) + '.mp4'
            elif exmod == '2':
                p = len(str(len(target)))
                q = '0' * p + str(num)
                name = f'{q[-p:]}.mp4'
            elif exmod == '3':
                name = f'{alpha}{num}.mp4'
            elif exmod == '4':
                p = len(str(len(target)))
                q = '0' * p + str(num)
                name = f'{alpha}{q[-p:]}.mp4'
            order = order + 'temp448\\' + name

            k.print(win, listbox, f'{num}번 명령 : {order}')
            try:
                temp = os.system(order)
            except:
                temp = 1
            k.print(win, listbox, f'{num}번 결과 : {temp}')

            num = num + 1
            time.sleep(wait)

        os.startfile('temp448')
    
else:
    k.print(win, listbox, '선택된 파일 없음')

k.print(win, listbox, '종료합니다')
k.getnum(win)
k.end(win)
try:
    shutil.rmtree('temp448')
except:
    pass
time.sleep(0.5)

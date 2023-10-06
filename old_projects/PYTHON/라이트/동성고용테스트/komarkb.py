import time

note = '''
Hello, world!

===== K O S   2 0 2 2 =====

지금까지 수많은 프로그램들을 만들어온
OWL SOFT INC.
자유로운 소프트웨어의 사용과 개발을 믿는 사람으로써,
여러분의 프로그래밍을 지원합니다.
디시인사이드 소유즈 갤러리에 자세한 사항이 나와 있습니다.
https://gall.dcinside.com/mini/board/lists/?id=soyuz

동성고 재학생 KO.TW
2022 04 27
'''

time.sleep(0.3)

for i in range( 0,len(note) ):
    if note[i] == '\n':
        print( '\n' , end = '' , flush=True)
        time.sleep(1)
    else:
        print( note[i] , end = '' , flush=True)
        time.sleep(0.15)

time.sleep(3)

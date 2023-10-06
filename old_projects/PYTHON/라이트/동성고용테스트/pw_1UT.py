import time
import random
pw = 'Hello, world!'
a = 0

time.sleep(1.0)
print('이 프로그램은 1% 확률로 비밀번호를 제공합니다.\n')

while a == 0:
    time.sleep(0.3)
    b = input('계속하려면 아무 키나 입력하세요...')
    if random.randrange(0,100) < 1:
        print('비밀번호 : ' , pw , '\n')
        a = 1
    else:
        print('꽝!\n')
b = input('프로그램을 종료합니다.\n')
time.sleep(1)

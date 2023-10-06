import time
import random

k = input('PRESS ENTER TO START ')
k = random.randrange(0,100)

for i in range(0,100000):
    print('')
    time.sleep(0.1)
    for j in range(0,70):
        print( random.randrange(0,2) , end = '' , flush=True)
        time.sleep(0.02)
#0

k = input('PRESS ENTER TO EXIT... ')
time.sleep(1)

'''
print('\n'*150)#1

for i in range(0,100): #2
    s = str(i) + '%'
    print(s , end = '')
    print('\r', end = '')
    time.sleep(0.2)

os.system('cls') #3 os.name == 'nt' / 'dos'

os.system('clear') #4

c = lambda : os. ~ #5
'''

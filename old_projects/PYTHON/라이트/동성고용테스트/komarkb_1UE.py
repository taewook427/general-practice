import time
import random

k = input('PRESS ENTER TO START ')
k = random.randrange(0,100)

if 0 <= k < 20:
    for i in range(0,100000):
        print('')
        time.sleep(0.1)
        for j in range(0,70):
            print( random.randrange(0,2) , end = '' )

elif 20 <= k < 40:
    for i in range(0,100000):
        print('')
        time.sleep(0.1)
        for j in range(0,70):
            print( random.randrange(0,10) , end = '' )

elif 40 <= k < 60:
    m = [ 0,1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f']
    for i in range(0,100000):
        print('')
        time.sleep(0.1)
        for j in range(0,70):
            k = random.randrange(0,16)
            print( m[k] , end = '' )

elif 60 <= k < 80:
    for i in range(0,100000):
        print('')
        time.sleep(0.1)
        for j in range(0,70):
            print( chr( random.randrange(32,126) ) , end = '' )

elif 80 <= k < 100:
    for i in range(0,100000):
        print('')
        time.sleep(0.1)
        for j in range(0,70):
            print( chr( random.randrange(32,55000) ) , end = '' )

k = input('PRESS ENTER TO EXIT... ')
time.sleep(1)

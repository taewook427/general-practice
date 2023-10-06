def main():
    f = open('testlog.txt','r')
    t = f.readline()
    f.close()
    print('마지막 기록 : '+t)
    num = input('재기록(숫자) >>> ')
    try:
        nume = float(num)
        f = open('testlog.txt','w')
        f.write(num)
        f.close()
        print('W : end in 3s')
        time.sleep(3)
    except:
        print('E : end in 3s')
        time.sleep(3)
try:
    f = open('testlog.txt','r')
    t = f.readline()
    f.close()
except:
    f = open('testlog.txt','w')
    f.write('0')
    f.close()
import time
main()

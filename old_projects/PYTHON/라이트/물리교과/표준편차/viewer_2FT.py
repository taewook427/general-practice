print('표준편자 구하기')
filename = input('파일 이름 입력 : ')
data = open(filename,'r')
Rlines = data.readlines()
data.close()
lines = [ ]
for i in Rlines:
    lines.append( i[:-1] )
data_amount = int( lines[0] )
set_amount = int( lines[1] )
for i in range(0,data_amount):
    name = lines[2 + i][0:2]
    data = [ ]
    for j in range(0,set_amount):
        data.append( float( lines[2 + j * data_amount + i][3:] ) )
    data_sum = 0
    sum2 = 0
    for i in data:
        data_sum = data_sum + i
        sum2 = sum2 + i**2
    Ex = data_sum / set_amount
    Ex2 = sum2 / set_amount
    Vx = Ex2 - Ex ** 2
    sigma = Vx ** 0.5
    print('\n항목 : ', name, '\n평균 : ', Ex, '\n표준편차 : ', sigma, '\nsig/E (x1000) : ', sigma/Ex*1000)
print('종료함')
k = input('.')

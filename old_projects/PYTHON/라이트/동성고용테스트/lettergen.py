import random as r
d=['#','$','&','*']
d = d + ['7']* 3
print('')
for i in range(0,16):
    a = '    '
    for j in range(0,48):
        a = a + d[ r.randrange(0,7) ]
    print(a)
print('')

# chr( r.randrange( 32,126 ) )

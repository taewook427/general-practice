print (2)
print (3)
l=[3]
k=1
def prime(q) :
    global c
    c=0
    global b
    b=l[c]
    global d
    d=0
    while b<= q ** 0.5 and d==0 :
        if q%b == 0 :
            d=1
        c = c+1
        b= l[c]
    return d
while k<10000 :
    a=6*k-1
    if prime (a) == 0 :
        print (a)
        l.append(a)
    a=6*k+1
    if prime (a) == 0:
        print (a)
        l.append (a)
    k = k+1

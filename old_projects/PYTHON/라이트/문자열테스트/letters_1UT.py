def trans():
    enter = input('enter string convert mode : ')
    if enter == 'end':
        global transroop
        transroop = 0
    elif enter == 'txt':
        txt()
    elif enter == 'spc':
        code = input('enter string to add/scrub spaces\n')
        output = space(code)
        output = output + '\n'
        print(output)
    elif enter == 'oth':
        other()
    else:
        print('unknown mode\n')
def space(code):
    temp = 0
    for i in range( 0,len(code) ):
        if code[i] == ' ':
            temp = temp + 1
    if temp > 0:
        output = ''
        for temp in range( 0,len(code) ):
            if not code[temp] == ' ':
                output = output + code[temp]
    else:
        n = int( input('inserting space with every N letters\nN : ') )
        output = ''
        num = 0
        for temp in range( 0,len(code) ):
            output = output + code[temp]
            num = num + 1
            if num % n == 0:
                output = output + ' '
    return output
def other():
    print("usable mode : 'cpt' 'sss'")
    print('mode fullname : capital sssss')
    enter = input('enter other mode : ')
    if enter == 'cpt':
        enter = input('enter string to (de)capitalize\n')
        output = capital(enter)
        if not output == '':
            output = output + '\n'
        print(output)
    elif enter == 'sss':
        print('s\n')
    else:
        print('unknown mode\n')
def capital(code):
    alphabetbig = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
    alphabetbig = alphabetbig + ['P','Q','R','S','T','U','V','W','X','Y','Z']
    alphabetsmall = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
    alphabetsmall = alphabetsmall + ['p','q','r','s','t','u','v','w','x','y','z']
    yn = input("(de)capitalize 'up' or 'dn' : ")
    output = ''
    if yn == 'up':
        for i in range( 0,len(code) ):
            if code[i] in alphabetsmall:
                temp = 0
                while not code[i] == alphabetsmall[temp]:
                    temp = temp + 1
                output = output + alphabetbig[temp]
            else:
                output = output + code[i]
    elif yn == 'dn':
        for i in range( 0,len(code) ):
            if code[i] in alphabetbig:
                temp = 0
                while not code[i] == alphabetbig[temp]:
                    temp = temp + 1
                output = output + alphabetsmall[temp]
            else:
                output = output + code[i]
    else:
        print('unknown mode')
    return output
def txt():
    print("reading text in 'input.txt'")
    file = open('input.txt','r')
    codes = file.readlines()
    file.close()
    for i in range( 0,len(codes) - 1 ):
        codes[i] = codes[i][:-1]
    print("usable mode : 'spc'")
    enter = input('enter text file convert mode : ')
    if enter == 'spc':
        outputs = [ ]
        line = input('converts linechange to : ')
        for tempstr in codes:
            tempstr = tempstr + line
            outputs.append(tempstr)
    else:
        outputs = ['unknown mode']
    file = open('output.txt','w')
    for i in outputs:
        file.write(i)
    file.write('\n\n')
    file.close()
    print("text file converted, output at 'output.txt'\n")
print('this program converts string')
print("usable mode : 'txt' 'spc' 'oth' 'end'")
print('mode fullname : text space other end\n')
transroop = 1
while transroop == 1:
    trans()
transroop = input('enter any key to end this program... ')

def trans():
    mode = input('enter cipher mode : ')
    if mode == 'exit':
        global transroop
        transroop = 0
    elif mode == 'caesar':
        caesar()
    elif mode == 'vignere':
        mode = input("'encrypt' or 'decrypt' : ")
        if mode == 'encrypt':
            alphabetbig = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
            alphabetbig = alphabetbig + ['P','Q','R','S','T','U','V','W','X','Y','Z']
            alphabetsmall = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
            alphabetsmall = alphabetsmall + ['p','q','r','s','t','u','v','w','x','y','z']
            key = input('key : ')
            code = input('enter code to encrypt\n')
            valid = 1
            keylist = [ ]
            for i in range( 0,len(key) ):
                if key[i] in alphabetbig:
                    temp = 0
                    while not key[i] == alphabetbig[temp]:
                        temp = temp + 1
                    keylist.append(temp)
                elif key[i] in alphabetsmall:
                    temp = 0
                    while not key[i] == alphabetsmall[temp]:
                        temp = temp + 1
                    keylist.append(temp)
                else:
                    keylist.append(0)
                    valid = 0
            if valid == 0:
                print('invalid key\n')
            else:
                output = vignereencrypt(code,keylist)
                output = output + '\n'
                print(output)
        elif mode == 'decrypt':
            alphabetbig = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
            alphabetbig = alphabetbig + ['P','Q','R','S','T','U','V','W','X','Y','Z']
            alphabetsmall = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
            alphabetsmall = alphabetsmall + ['p','q','r','s','t','u','v','w','x','y','z']
            key = input('key : ')
            code = input('enter code to decrypt\n')
            valid = 1
            keylist = [ ]
            for i in range( 0,len(key) ):
                if key[i] in alphabetbig:
                    temp = 0
                    while not key[i] == alphabetbig[temp]:
                        temp = temp + 1
                    keylist.append(temp)
                elif key[i] in alphabetsmall:
                    temp = 0
                    while not key[i] == alphabetsmall[temp]:
                        temp = temp + 1
                    keylist.append(temp)
                else:
                    keylist.append(0)
                    valid = 0
            if valid == 0:
                print('invalid key\n')
            else:
                output = vigneredecrypt(code,keylist)
                output = output + '\n'
                print(output)
        else:
            print('unknoun mode\n')
    elif mode == 'affine':
        mode = input("'encrypt' or 'decrypt' : ")
        if mode == 'encrypt':
            keys = [1,3,5,7,9,11,15,17,19,21,23,25]
            print('shape : Y = key1 * X + key2 \n=== usable key1 ===')
            print(keys)
            key1 = input('key1 : ')
            key2 = input('key2 : ')
            code = input('enter code to encrypt\n')
            key1 = int(key1)
            key2 = int(key2)
            if key1 in keys:
                output = affineencrypt(key1,key2,code)
            else:
                output = 'invalid key1'
            output = output + '\n'
            print(output)
        elif mode == 'decrypt':
            keys = [1,3,5,7,9,11,15,17,19,21,23,25]
            print('shape : Y = key1 * X + key2 \n=== usable key1 ===')
            print(keys)
            key1 = input('key1 : ')
            key2 = input('key2 : ')
            code = input('enter code to decrypt\n')
            key1 = int(key1)
            key2 = int(key2)
            if key1 in keys:
                output = affinedecrypt(key1,key2,code)
            else:
                output = 'invalid key1'
            output = output + '\n'
            print(output)
        else:
            print('unknoun mode\n')
    elif mode == 'analyze':
        analyze()
    elif mode == 'advanced':
        advanced()
    else:
        print('unknown mode\n')
def caesar():
    alphabetbig = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
    alphabetbig = alphabetbig + ['P','Q','R','S','T','U','V','W','X','Y','Z']
    alphabetsmall = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
    alphabetsmall = alphabetsmall + ['p','q','r','s','t','u','v','w','x','y','z']
    key = input('key : ')
    key = int(key) % 26
    code = input('enter code to convert\n')
    output = ''
    for tempstr in range( 0,len(code) ):
        tempstr = code[tempstr]
        if tempstr in alphabetbig:
            temp = 0
            while not tempstr == alphabetbig[temp]:
                temp = temp + 1
            output = output + alphabetbig[(temp + key) % 26]
        elif tempstr in alphabetsmall:
            temp = 0
            while not tempstr == alphabetsmall[temp]:
                temp = temp + 1
            output = output + alphabetsmall[(temp + key) % 26]
        elif tempstr == ' ':
            output = output + ' '
        elif tempstr == '.':
            output = output + '.'
        elif tempstr == ',':
            output = output + ','
        else:
            output = output + '?'
    output = output + '\n'
    print(output)
def vignereencrypt(code,keylist):
    alphabetbig = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
    alphabetbig = alphabetbig + ['P','Q','R','S','T','U','V','W','X','Y','Z']
    alphabetsmall = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
    alphabetsmall = alphabetsmall + ['p','q','r','s','t','u','v','w','x','y','z']
    output = ''
    keynum = 0
    for tempstr in range( 0,len(code) ):
        tempstr = code[tempstr]
        if tempstr == ' ':
            output = output + ' '
        elif tempstr == '.':
            output = output + '.'
        elif tempstr == ',':
            output = output + ','
        elif tempstr in alphabetbig:
            temp = 0
            while not tempstr == alphabetbig[temp]:
                temp = temp + 1
            temp = ( temp + keylist[ keynum % len(keylist) ] ) % 26
            keynum = keynum + 1
            output = output + alphabetbig[temp]
        elif tempstr in alphabetsmall:
            temp = 0
            while not tempstr == alphabetsmall[temp]:
                temp = temp + 1
            temp = ( temp + keylist[ keynum % len(keylist) ] ) % 26
            keynum = keynum + 1
            output = output + alphabetsmall[temp]
        else:
            output = output + '?'
    return output
def vigneredecrypt(code,keylist):
    alphabetbig = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
    alphabetbig = alphabetbig + ['P','Q','R','S','T','U','V','W','X','Y','Z']
    alphabetsmall = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
    alphabetsmall = alphabetsmall + ['p','q','r','s','t','u','v','w','x','y','z']
    output = ''
    keynum = 0
    for tempstr in range( 0,len(code) ):
        tempstr = code[tempstr]
        if tempstr == ' ':
            output = output + ' '
        elif tempstr == '.':
            output = output + '.'
        elif tempstr == ',':
            output = output + ','
        elif tempstr in alphabetbig:
            temp = 0
            while not tempstr == alphabetbig[temp]:
                temp = temp + 1
            temp = ( temp - keylist[ keynum % len(keylist) ] ) % 26
            keynum = keynum + 1
            output = output + alphabetbig[temp]
        elif tempstr in alphabetsmall:
            temp = 0
            while not tempstr == alphabetsmall[temp]:
                temp = temp + 1
            temp = ( temp - keylist[ keynum % len(keylist) ] ) % 26
            keynum = keynum + 1
            output = output + alphabetsmall[temp]
        else:
            output = output + '?'
    return output
def affineencrypt(key1,key2,code):
    alphabetbig = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
    alphabetbig = alphabetbig + ['P','Q','R','S','T','U','V','W','X','Y','Z']
    alphabetsmall = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
    alphabetsmall = alphabetsmall + ['p','q','r','s','t','u','v','w','x','y','z']
    output = ''
    for tempstr in range( 0,len(code) ):
        tempstr = code[tempstr]
        if tempstr == ' ':
            output = output + ' '
        elif tempstr == '.':
            output = output + '.'
        elif tempstr == ',':
            output = output + ','
        elif tempstr in alphabetbig:
            temp = 0
            while not tempstr == alphabetbig[temp]:
                temp = temp + 1
            temp = (key1 * temp + key2) % 26
            output = output + alphabetbig[temp]
        elif tempstr in alphabetsmall:
            temp = 0
            while not tempstr == alphabetsmall[temp]:
                temp = temp + 1
            temp = (key1 * temp + key2) % 26
            output = output + alphabetsmall[temp]
        else:
            output = output + '?'
    return output
def affinedecrypt(key1,key2,code):
    alphabetbig = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
    alphabetbig = alphabetbig + ['P','Q','R','S','T','U','V','W','X','Y','Z']
    alphabetsmall = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
    alphabetsmall = alphabetsmall + ['p','q','r','s','t','u','v','w','x','y','z']
    output = ''
    for tempstr in range( 0,len(code) ):
        tempstr = code[tempstr]
        if tempstr == ' ':
            output = output + ' '
        elif tempstr == '.':
            output = output + '.'
        elif tempstr == ',':
            output = output + ','
        elif tempstr in alphabetbig:
            temp = 0
            while not tempstr == alphabetbig[temp]:
                temp = temp + 1
            temp = (temp - key2) % 26
            original = -1
            for tempstr in range(0,26):
                if (key1 * tempstr) % 26 == temp:
                    original = tempstr
            output = output + alphabetbig[original]
        elif tempstr in alphabetsmall:
            temp = 0
            while not tempstr == alphabetsmall[temp]:
                temp = temp + 1
            temp = (temp - key2) % 26
            original = -1
            for tempstr in range(0,26):
                if (key1 * tempstr) % 26 == temp:
                    original = tempstr
            output = output + alphabetsmall[original]
        else:
            output = output + '?'
    return output
def analyze():
    alphabetbig = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
    alphabetbig = alphabetbig + ['P','Q','R','S','T','U','V','W','X','Y','Z']
    alphabetsmall = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
    alphabetsmall = alphabetsmall + ['p','q','r','s','t','u','v','w','x','y','z']
    rate = [ ]
    for i in range(0,28):
        rate.append(0)
    code = input('enter code to analyze alphabet rate\n')
    for tempstr in range( 0,len(code) ):
        tempstr = code[tempstr]
        if tempstr == ' ':
            rate[26] = rate[26] + 1
        elif tempstr in alphabetbig:
            temp = 0
            while not tempstr == alphabetbig[temp]:
                temp = temp + 1
            rate[temp] = rate[temp] + 1
        elif tempstr in alphabetsmall:
            temp = 0
            while not tempstr == alphabetsmall[temp]:
                temp = temp + 1
            rate[temp] = rate[temp] + 1
        else:
            rate[27] = rate[27] + 1
    alphabetnum = 0
    for i in range(0,26):
        alphabetnum = alphabetnum + rate[i]
    output = [ ]
    for i in range(0,26):
        tempstr = alphabetbig[i] + ' : ' + str( rate[i] )
        tempstr = tempstr + '/' + str( alphabetnum ) + ' | '
        ratio = rate[i]/alphabetnum
        ratio = str( int(ratio * 10000) / 100 )
        tempstr = tempstr + ratio + '%'
        output.append(tempstr)
    tempstr = 'space : ' + str( rate[26] )
    output.append(tempstr)
    tempstr = 'others : ' + str( rate[27] )
    output.append(tempstr)
    print('===== ANALYSIS RESULT =====')
    for i in output:
        print(i)
    highratio = [ 4 , 19 , 0 , 14 , 8 ]
    high1 = -1
    rate1 = -1
    for i in range( 0,len(rate) ):
        if rate1 < rate[i]:
            high1 = i
            rate1 = rate[i]
    rate[high1] = 0
    high2 = -1
    rate2 = -1
    for i in range( 0,len(rate) ):
        if rate2 < rate[i]:
            high2 = i
            rate2 = rate[i]
    rate[high2] = 0
    high3 = -1
    rate3 = -1
    for i in range( 0,len(rate) ):
        if rate3 < rate[i]:
            high3 = i
            rate3 = rate[i]
    rate[high3] = 0
    high4 = -1
    rate4 = -1
    for i in range( 0,len(rate) ):
        if rate4 < rate[i]:
            high4 = i
            rate4 = rate[i]
    rate[high4] = 0
    high5 = -1
    rate5 = -1
    for i in range( 0,len(rate) ):
        if rate5 < rate[i]:
            high5 = i
            rate5 = rate[i]
    rate[high5] = 0
    high1 = ( high1 - highratio[0] ) % 26
    high2 = ( high2 - highratio[1] ) % 26
    high3 = ( high3 - highratio[2] ) % 26
    high4 = ( high4 - highratio[3] ) % 26
    high5 = ( high5 - highratio[4] ) % 26
    print('===== POSSIBLE KEYS =====')
    print(high1,high2,high3,high4,high5,'\n')
def advanced():
    print(7)
print('this program analyzes/converts classic cipher')
print("usable mode : 'caesar' 'vignere' 'affine' 'analyze' 'advanced'")
print("enter 'exit' to exit this program\n")
transroop = 1
while transroop == 1:
    trans()
transroop = input('\nenter any key to exit... ')

def trans():
    global transroop
    inputmode = input('choose convert input mode : ')
    if inputmode == '\\exit':
        transroop = 0
        inputmode = 1
    elif inputmode == 'asc':
        inputmode = 100
    elif inputmode == 'bin':
        inputmode = 2
    elif inputmode == 'oct':
        inputmode = 8
    elif inputmode == 'dec':
        inputmode = 10
    elif inputmode == 'hex':
        inputmode = 16
    else:
        inputmode = 0
    outputmode = input('choose convert output mode : ')
    if outputmode == '\\exit':
        transroop = 0
        outputmode = 1
    elif outputmode == 'asc':
        outputmode = 100
    elif outputmode == 'bin':
        outputmode = 2
    elif outputmode == 'oct':
        outputmode = 8
    elif outputmode == 'dec':
        outputmode = 10
    elif outputmode == 'hex':
        outputmode = 16
    else:
        outputmode = 0
    if inputmode == 0 or outputmode == 0:
        print('unknown mode\n')
    elif transroop == 0:
        temp = 0
    else:
        incode = input('enter letters to convert\n')
        global codelist
        codelist = [ ]
        inputconvert(incode,inputmode)
        outputconvert(outputmode)
def inputconvert(incode,inputmode):
    if inputmode == 100:
        for i in range( 0,len(incode) ):
            if incode[i] in lettercode:
                temp = 0
                while not incode[i] == lettercode[temp]:
                    temp = temp + 1
                codelist.append(temp + 32)
            else:
                codelist.append(128)
    else:
        templist = [ ]
        tempstr = ''
        temp = 0
        for i in range( 0,len(incode) ):
            if incode[i] == ' ':
                if not tempstr == '':
                    templist.append(tempstr)
                tempstr = ''
            else:
                tempstr = tempstr + incode[i]
        if not tempstr == '':
            templist.append(tempstr)
        for tempstr in templist:
            tempnum = 0
            for i in range( 0,len(tempstr) ):
                if tempstr[i] in numcodebig:
                    temp = 0
                    while not tempstr[i] == numcodebig[temp]:
                        temp = temp + 1
                    tempnum = tempnum + temp * inputmode ** (len(tempstr) - i - 1)
                elif tempstr[i] in numcodesmall:
                    temp = 0
                    while not tempstr[i] == numcodesmall[temp]:
                        temp = temp + 1
                    tempnum = tempnum + temp * inputmode ** (len(tempstr) - i - 1)
                else:
                    tempnum = tempnum + 128
            if tempnum >= 128:
                tempnum = 128
            codelist.append(tempnum)
def outputconvert(outputmode):
    if outputmode == 100:
        output = ''
        for temp in codelist:
            if 31 < temp < 128:
                tempstr = lettercode[temp - 32]
            else:
                tempstr = "¿"
            output = output + tempstr
        output = output + '\n'
        print(output)
    elif outputmode == 2:
        output = ' '
        for temp in codelist:
            tempnum = 128
            tempstr = ''
            while tempnum >= 1:
                if temp / tempnum >= 1:
                    tempstr = tempstr + '1'
                    temp = temp - tempnum
                else:
                    tempstr = tempstr + '0'
                tempnum = tempnum / 2
            output = output + tempstr + ' '
        output = output + '\n'
        print(output)
    elif outputmode == 8:
        output = ' '
        for temp in codelist:
            tempnum = 64
            tempstr = ''
            while tempnum >= 1:
                tempstr = tempstr + str(int(temp // tempnum))
                temp = temp % tempnum
                tempnum = tempnum / 8
            output = output + tempstr + ' '
        output = output + '\n'
        print(output)
    elif outputmode == 10:
        output = ' '
        for temp in codelist:
            output = output + str(temp) + ' '
        output = output + '\n'
        print(output)
    elif outputmode == 16:
        output = ' '
        for temp in codelist:
            tempnum = int(temp // 16)
            output = output + numcodebig[tempnum]
            temp = int(temp % 16)
            output = output + numcodebig[temp] + ' '
        output = output + '\n'
        print(output)
    else:
        print("unknown error\n")
lettercode = [' ','!','"','#','$','%','&',"'",'(',')','*','+',',','-','.','/']
lettercode = lettercode + ['0','1','2','3','4','5','6','7','8','9',':',';','<','=','>','?','@']
lettercode = lettercode + ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
lettercode = lettercode + ['P','Q','R','S','T','U','V','W','X','Y','Z','[','\\',']','^','_','`']
lettercode = lettercode + ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
lettercode = lettercode + ['p','q','r','s','t','u','v','w','x','y','z','{','|','}','~']
numcodebig = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
numcodesmall = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
print(lettercode)
print('\nthis program converts ASCII and letters')
print("available mode : 'asc' 'bin' 'oct' 'dec' 'hex'")
print("enter '\\exit' to end this program")
print('usable area : 32~126\n')
transroop = 1
while transroop == 1:
    trans()
transroop = input('enter any key to exit\n')

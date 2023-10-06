def trans():
    rawinput = input('input letters or code\nenter "\\exit" to stop\n')
    if rawinput == '\\exit':
        global transroop
        transroop = 0
    else:
        temp = 0
        while rawinput[temp] == ' ':
            temp = temp + 1
        if rawinput[temp] == '*' or rawinput[temp] == '-':
            morsetoletter(rawinput[temp:])
        elif rawinput[temp] in engletter or rawinput[temp] in numletter:
            lettertomorse(rawinput[temp:])
        else:
            print('unknown mode\n')
def morsetoletter(inputcode):
    strlist = [ ]
    temp = 0
    strtemp = ''
    while temp < len(inputcode):
        if inputcode[temp] == ' ':
            if not strtemp == '':
                strlist.append(strtemp)
            strtemp = ''
        else:
            strtemp = strtemp + inputcode[temp]
        temp = temp + 1
    if not strtemp == '':
        strlist.append(strtemp)
    output = ''
    for i in range( 0,len(strlist) ):
        if strlist[i] in nummorse:
            temp = 0
            while not strlist[i] == nummorse[temp]:
                temp = temp + 1
            output = output + numletter[temp]
        elif strlist[i] in engmorse:
            temp = 0
            while not strlist[i] == engmorse[temp]:
                temp = temp + 1
            output = output + engletter[temp]
        else:
            output = output + '@'
    output = output + '\n'
    print(output)
def lettertomorse(inputletter):
    strlist = [ ]
    for i in range( 0,len(inputletter) ):
        if inputletter[i] in numletter:
            strlist.append(inputletter[i])
        elif inputletter[i] in engletter:
            strlist.append(inputletter[i])
        elif not inputletter[i] == ' ':
            strlist.append('@')
    output = ' '
    for i in range( 0,len(strlist) ):
        if strlist[i] in numletter:
            temp = 0
            while not strlist[i] == numletter[temp]:
                temp = temp + 1
            output = output + nummorse[temp] + ' '
        elif strlist[i] in engletter:
            temp = 0
            while not strlist[i] == engletter[temp]:
                temp = temp + 1
            output = output + engmorse[temp] + ' '
        else:
            output = output + '@ '
    output = output + '\n'
    print(output)
numletter = ['1','2','3','4','5','6','7','8','9','0','.',',','?','/',':','`','-','(',')']
nummorse = ['*----','**---','***--','****-','*****','-****','--***','---**','----*','-----']
nummorse = nummorse + ['*-*-*-','--**--','**--**','-**-*','---***','*----*','-****-','-*--*','-*--*-']
engletter = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
engletter = engletter + ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
engmorse = ['*-','-***','-*-*','-**','*','**-*','--*','****','**','*---','-*-','*-**','--']
engmorse = engmorse + ['-*','---','*--*','--*-','*-*','***','-','**-','***-','*--','-**-','-*--','--**']
engmorse = engmorse * 2
print('this program converts morse and english\n')
print('you can use both small and big letter\n')
print('space to distinguish each code\n')
print(numletter)
print(nummorse)
print(engletter)
print(engmorse)
transroop = 1
while transroop == 1:
    trans()
transroop = input('enter any key to exit\n')

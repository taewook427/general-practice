def en(key,content):
    table = [ chr(x) for x in range(48,58) ] + [ chr(x) for x in range(65,91) ] + [ chr(x) for x in range(97,123) ]
    content = bytes(content,'utf-8')
    output = ''
    for i in range( 0,len(content) ):
        temp = content[i] + ord( key[ i % len(key) ] ) + ord( key[ (i+2) % len(key) ] ) + ord( key[ (i+3) % len(key) ] )
        temp = temp % 256
        x0 = temp // len(table)
        x1 = temp % len(table)
        output = output + table[x0] + table[x1]
    return output

def de(key,content):
    table = [ chr(x) for x in range(48,58) ] + [ chr(x) for x in range(65,91) ] + [ chr(x) for x in range(97,123) ]
    output = [ ]
    for i in range( 0,len(content)//2 ):
        x0 = table.index( content[2*i] )
        x1 = table.index( content[2*i+1] )
        temp = x0 * len(table) + x1
        temp = temp - ord( key[ i % len(key) ] ) - ord( key[ (i+2) % len(key) ] ) - ord( key[ (i+3) % len(key) ] )
        temp = temp % 256
        output.append(temp)
    return str(bytes(output), 'utf-8')

temp = ''
key = 'abc' # key = 영문 문자열
while temp != 'exit':
    temp = input('\n>>> ')
    if temp == 'setkey':
        key = input('key : ')
    elif temp == 'encode': # content = 문자열
        content = input('content : ')
        print('crypt : ' + en(key, content) )
    elif temp == 'decode': # crypt = 영문 문자열
        crypt = input('crypt : ')
        print('content : ' + de(key, crypt) )
    elif temp == 'viewkey':
        print('key : ' + key)
    elif temp == 'help':
        print('setkey, viewkey, encode, decode, help, exit')
    else:
        print('enter help')
input('press enter to exit... ')

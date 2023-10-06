import pdfkit
import os

def convertF(name):
    config = pdfkit.configuration(wkhtmltopdf="wkhtmltopdf.exe")
    pdfkit.from_file(name, 'output.pdf', configuration=config)
    return 0

def convertU(url):
    config = pdfkit.configuration(wkhtmltopdf="wkhtmltopdf.exe")
    pdfkit.from_url(url, 'output.pdf', configuration=config)
    return 0

def main():
    f = open('input.txt','r')
    order = f.readlines()
    f.close()

    if order[0] == 'html\n':
        os.remove('input.txt')
        try:
            k = convertF( order[1][0:-1] )
        except:
            if os.path.isfile('output.pdf'):
                k = 2
            else:
                k = 1
        
    elif order[0] == 'url\n':
        os.remove('input.txt')
        try:
            k = convertU( order[1][0:-1] )
        except:
            if os.path.isfile('output.pdf'):
                k = 2
            else:
                k = 1
        
    else:
        k = 3

    return k

try:
    output = main()
except:
    output = 1

if output == 0:
    f = open('output.txt','w')
    f.write('0\n')
    f.close()
    
elif output == 1:
    f = open('output.txt','w')
    f.write('1\n')
    f.close()
    
elif output == 2:
    f = open('output.txt','w')
    f.write('2\n')
    f.close()

import sei
import nox2
import multiprocessing as mp

def doit():
    ntool = nox2.toolbox()

    seitool = sei.standard()
    seitoolp = seitool.init('Europium')
    seitoolwin = seitoolp[0]
    seitoollistbox = seitoolp[1]
    seitool.print(seitoolwin,seitoollistbox,'Eu Nox2 CLI Tool\nntool.xxx / exit() / <lastorder>')

    lastorder = ''
    while True:
        tooltemp = seitool.input2(seitoolwin)
        seitool.print(seitoolwin,seitoollistbox,'>>> ' + tooltemp)
        if tooltemp == 'exit()':
            break
        else:
            try:
                exec(tooltemp)
            except Exception as toole:
                seitool.print(seitoolwin,seitoollistbox,str(toole))
        lastorder = tooltemp

    seitool.print(seitoolwin,seitoollistbox,'종료합니다.')
    seitool.ask2(seitoolwin)
    seitool.end(seitoolwin)

if __name__ == '__main__':
    mp.freeze_support()
    doit()

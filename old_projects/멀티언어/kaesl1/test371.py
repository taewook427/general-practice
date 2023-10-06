mode = input('적을 바이트 수 : ')
mode = mode.split()
if mode[-1] == 'kb':
    mode = int(mode[0]) * 1024
elif mode[-1] == 'mb':
    mode = int(mode[0]) * 1024 * 1024
else:
    mode = int(mode[0])
with open('tempkaesl','wb') as f:
    f.write(b'\x00' * mode)

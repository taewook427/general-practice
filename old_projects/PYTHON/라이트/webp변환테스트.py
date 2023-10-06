from PIL import Image
import os

files = os.listdir('jpg')
print(files)

for i in files:
    name = 'jpg\\' + i
    f = Image.open(name)
    new = name[0:name.rfind('.')] + '.webp'
    f.save(new)
    os.remove(name)

print('jpg to webp complete')

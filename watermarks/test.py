import numpy as np
from PIL import Image

img = Image.open('33.png')
img.load()
array = np.array(img)

#array = 255 - array

invimg = Image.fromarray(array, mode='RGB')

invimg.save('test2.png')
invimg.show()

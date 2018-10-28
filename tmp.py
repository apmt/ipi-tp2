from PIL import Image
import numpy as np
img = Image.open("out.bmp")
tmp = Image.new("RGB", (124, 124))
for i in range (0, tmp. height):
	for j in range (0, tmp. width):
		tmp.putpixel((j, i), img.getpixel((j+390, i+490)))
tmp.show()
#tmp.save("tmp.bmp")
import glob
from PIL import Image
import numpy as np
KR=299
KG=587
KB=114
KCB=564
KCR=713
images = glob.glob("Images/*.bmp")
primeira = 1
k=0
for image in images:
	if(primeira == 1):
		img = Image.open(image)
		Y = np.zeros((img.height, img.width), dtype=int)
		CB = np.zeros((img.height, img.width), dtype=int)
		CR = np.zeros((img.height, img.width), dtype=int)
		for i in range (0, img.height):
			for j in range (0, img.width):
				r, g, b = img.getpixel((j, i))
				Y[i, j] = ((KR*r)+(KG*g)+(KB*b))/1000
				CB[i, j] = (KCB*(b-Y[i, j]))/1000
				CR[i, j] = (KCR*(r-Y[i, j]))/1000
		primeira = 0
	else:
		if(k%10==0):
			print "carregando", k, "%"
		k += 1
		img = Image.open(image)
		for i in range (0, img.height):
			for j in range (0, img.width):
				r, g, b = img.getpixel((j, i))
				Y[i, j]+=((KR*r)+(KG*g)+(KB*b))/1000
for i in range (0, img.height):
	for j in range (0, img.width):
		Y[i, j] = Y[i, j]/100
print -1
CB_aux = CB
for i in range (1, img.height-1):
	for j in range (1, img.width-1):
		lista = []
		for k in range (i-1, i+2):
			for l in range (j-1, j+2):
				lista.append(CB_aux[k, l])
		lista.sort()
		CB[i, j]=lista[4]
print -2
############################
###################################################
import pylab
CR_aux = np.fft.fft2(CR)
CR_shift = np.fft.fftshift(CR_aux)
#pylab.imshow(np.abs(ftimage))
#pylab.show()
gmask = np.zeros((img.height, img.width), dtype=int)
gmask[img.height/2, img.width/2]=1
CR = np.fft.ifft2(CR_shift * gmask)

################################
for i in range (0, img.height):
	for j in range (0, img.width):
		r=Y[i, j]+int(1.402*CR[i, j])
		g=Y[i, j]-int(0.344*CB[i, j])-int(0.714*CR[i, j])
		b=Y[i, j]+int(1.772*CB[i, j])
		img.putpixel((j, i), (r, g, b))
img.show()
img.save('out.bmp')
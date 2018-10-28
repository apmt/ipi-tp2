from PIL import Image
import numpy as np
import math
KR=299
KG=587
KB=114
KCB=564
KCR=713
img_aux = Image.open("out.bmp")
img = img_aux
tmp = Image.open("tmp.bmp")
print img.size
print tmp.rotate(45).size
Y = np.zeros((img.height, img.width), dtype=int)
CB = np.zeros((img.height, img.width), dtype=int)
CR = np.zeros((img.height, img.width), dtype=int)
for i in range (0, img.height):
	for j in range (0, img.width):
		r, g, b = img.getpixel((j, i))
		Y[i, j] = ((KR*r)+(KG*g)+(KB*b))/1000
		CB[i, j] = (KCB*(b-Y[i, j]))/1000
		CR[i, j] = (KCR*(r-Y[i, j]))/1000
Temp_Y = np.zeros((tmp.height, tmp.width), dtype=int)
Temp_CB = np.zeros((tmp.height, tmp.width), dtype=int)
Temp_CR = np.zeros((tmp.height, tmp.width), dtype=int)
for i in range (0, tmp.height):
	for j in range (0, tmp.width):
		r, g, b = tmp.getpixel((j, i))
		Temp_Y[i, j] = ((KR*r)+(KG*g)+(KB*b))/1000
		Temp_CB[i, j] = (KCB*(b-Y[i, j]))/1000
		Temp_CR[i, j] = (KCR*(r-Y[i, j]))/1000
Corr=[]
for i in range (0, img.height-tmp.height+1, 3):
	print i
	for j in range (0, img.width-tmp.width+1, 3):
		Correlation = 0
		Soma_quadrados_img = 0.0
		Soma_quadrados_Temp = 0.0
		for p in range (i, i+tmp.height, 3):
			for q in range (j, j+tmp.width, 3):
				Correlation+=Y[p, q]*Temp_Y[p-i, q-j]
				Soma_quadrados_img += Y[p, q]**2
				Soma_quadrados_Temp += Temp_Y[p-i, q-j]**2
		Normalized_Correlation = float(Correlation) 
		Normalized_Correlation /= math.sqrt(Soma_quadrados_img*Soma_quadrados_Temp)
		#print Correlation, Normalized_Correlation
		if(Normalized_Correlation>0.8):
			img_aux.putpixel((j+(tmp.width/2), i+(tmp.height/2)), (0,0,255))
		if(Normalized_Correlation>0.85):
			img_aux.putpixel((j+(tmp.width/2), i+(tmp.height/2)), (0,255,0))
		if(Normalized_Correlation>0.90):
			for m in range (i-5, i+6):
				for n in range (i-5, i+6):
					img_aux.putpixel((n+(tmp.width/2), m+(tmp.height/2)), (255,0,0))


img_aux.show()
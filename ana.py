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
for i in range (0, img.height-tmp.height+1, 5):
	print i
	for j in range (0, img.width-tmp.width+1, 5):
		Correlation = 0
		Soma_img = 0
		Soma_tmp = 0
		Soma_quadrados_img = 0.0
		Soma_quadrados_Temp = 0.0
		Contador = 0
		for p in range (i, i+tmp.height, 5):
			for q in range (j, j+tmp.width, 5):
				Soma_img += CR[p, q]
				Soma_tmp += Temp_CR[p-i, q-j]
				Contador +=1
		Media_img = Soma_img / Contador
		Media_tmp = Soma_tmp / Contador
		for p in range (i, i+tmp.height, 5):
			for q in range (j, j+tmp.width, 5):
				Correlation+=(CR[p, q]-Media_img)*(Temp_CR[p-i, q-j]-Media_tmp)
				Soma_quadrados_img += (CR[p, q]-Media_img)**2
				Soma_quadrados_Temp += (Temp_CR[p-i, q-j]-Media_tmp)**2
		Normalized_Correlation = float(Correlation) 
		Normalized_Correlation /= math.sqrt(Soma_quadrados_img*Soma_quadrados_Temp)
		print Correlation, Normalized_Correlation
		if(Normalized_Correlation>0.2):
			img_aux.putpixel((j+(tmp.width/2), i+(tmp.height/2)), (0,0,255))
		if(Normalized_Correlation>0.85):
			img_aux.putpixel((j+(tmp.width/2), i+(tmp.height/2)), (0,255,0))
		if(Normalized_Correlation>0.3):
			for m in range (i-5, i+6):
				for n in range (i-5, i+6):
					img_aux.putpixel((n+(tmp.width/2), m+(tmp.height/2)), (255,0,0))


img_aux.show()
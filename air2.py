from PIL import Image
import numpy as np
import math
from scipy import ndimage
def template_correlation(tmp, img, img_aux):
	KR=299
	KG=587
	KB=114
	KCB=564
	KCR=713
	red=(255, 0, 0)
	green=(0, 255, 0)
	blue=(0, 0, 255)
	#img_aux = Image.open("out.bmp")
	#img = img_aux
	#tmp = Image.open("tmp.bmp")
	#tmp = tmp.rotate(25)
	#tmp.show()
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
	incremento = 7
	Medias_tmp = (np.mean(Temp_Y), np.mean(Temp_CB), np.mean(Temp_CR))
	for i in range (0, img.height-tmp.height+1, incremento):
		#print i
		for j in range (0, img.width-tmp.width+1, incremento):
			Correlation = np.zeros(3, dtype=float)
			#Soma_img = np.zeros(3, dtype=int)
			#Soma_tmp = np.zeros(3, dtype=int)
			Soma_quadrados_img = np.zeros(3, dtype=float)
			Soma_quadrados_Temp = np.zeros(3, dtype=float)
			#Contador = 0
			labels = np.zeros_like(Y)
			labels[i:i+tmp.height,j:j+tmp.width] = 1
			#for p in range (i, i+tmp.height, incremento):
			#	for q in range (j, j+tmp.width, incremento):
			#		Soma_img += (Y[p, q], CB[p, q], CR[p, q])
			#		Soma_tmp += (Temp_Y[p-i, q-j], Temp_CB[p-i, q-j], Temp_CR[p-i, q-j])
			#		Contador +=1
			#Media_img = Soma_img / Contador
			#Media_tmp = Soma_tmp / Contador
			Medias_img = (ndimage.mean(Y, labels), ndimage.mean(CB, labels), ndimage.mean(CR, labels))
			#for p in range (i, i+tmp.height, incremento):
			#	for q in range (j, j+tmp.width, incremento):
			Correlation=(np.sum((Y[i:i+tmp.height,j:j+tmp.width]-Medias_img[0])*(Temp_Y-Medias_tmp[0])), np.sum((CB[i:i+tmp.height,j:j+tmp.width]-Medias_img[1])*(Temp_CB-Medias_tmp[1])), np.sum((CR[i:i+tmp.height,j:j+tmp.width]-Medias_img[2])*(Temp_CR-Medias_tmp[2])))
			#Correlation[0]+=(Y[p, q]-Media_img[0])*(Temp_Y[p-i, q-j]-Media_tmp[0]
			#Correlation[1]+=(CB[p, q]-Media_img[1])*(Temp_CB[p-i, q-j]-Media_tmp[1])
			#Correlation[2]+=(CR[p, q]-Media_img[2])*(Temp_CR[p-i, q-j]-Media_tmp[2])
			Soma_quadrados_img += (np.sum((Y[i:i+tmp.height,j:j+tmp.width]-Medias_img[0])**2), np.sum((CB[i:i+tmp.height,j:j+tmp.width]-Medias_img[1])**2), np.sum((CR[i:i+tmp.height,j:j+tmp.width]-Medias_img[2])**2))
			Soma_quadrados_Temp += (np.sum((Temp_Y-Medias_tmp[0])**2), np.sum((Temp_CB-Medias_tmp[1])**2), np.sum((Temp_CR-Medias_tmp[2])**2))
			Normalized_Corr = np.zeros(3, dtype=float)
			Normalized_Corr = Correlation/(((Soma_quadrados_img)*(Soma_quadrados_Temp))**(0.5))
			#print Normalized_Corr
			if(Normalized_Corr[0]>0.2 and Normalized_Corr[1]>0.14 and Normalized_Corr[2]>-0.05 and np.mean(Normalized_Corr)>0.136):
				print [i, j], Normalized_Corr, np.mean(Normalized_Corr)
				for m in range (i-1, i+2):
					for n in range (j-1, j+2):
						img_aux.putpixel((n+(tmp.width/2), m+(tmp.height/2)), red)
	img_aux.rotate(0).show()
	return img_aux;

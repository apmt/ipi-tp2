from PIL import Image
import numpy as np
import air2
black = (0, 0, 0)
img = Image.open("out.bmp")
img_aux = Image.new("RGB", img.size)
img_aux = img
tmp = Image.new("RGB", (100, 130))
tmp_aux = Image.new("RGB", (100, 130))
soma = np.zeros(3, dtype=int)
pixel = np.zeros(3, dtype = int)
for i in range (0, tmp.height):
	for j in range (0, tmp.width):
		#pixel = img.getpixel((j+196, i+535))
		#tmp.putpixel((j, i), pixel)
		##############################################3
		pixel1 = img.getpixel((j+96, i+515))
		pixel2 = img.getpixel((j+196, i+535))
		lp1 = list(pixel1)
		lp2 = list(pixel2)
		lp2[0] = (lp2[0]+lp1[0])/2 
		lp2[1] = (lp2[1]+lp1[1])/2 
		lp2[2] = (lp2[2]+lp1[2])/2 
		pixel = tuple(lp2)
		tmp.putpixel((j, i), pixel)
		#################################################
		soma += pixel
tmp.save('tmp.bmp')
media = tuple(soma / (tmp.width*tmp.height))
for i in range (-45, 45, 9):
	tmp_aux = tmp.rotate(i)
	for i in range (0, tmp.height):
		for j in range (0, tmp.width):
			if(tmp_aux.getpixel((j, i))==black):
			#if(matriz_tmp_aux[i, j]==black):
				tmp_aux.putpixel((j, i), media)
	tmp_aux.show()
	img_aux= air2.template_correlation(tmp_aux, img, img_aux)
img_aux.save("final.bmp")
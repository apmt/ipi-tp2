from PIL import Image
img = Image.open("out.bmp")
tmp = Image.new("RGB", (100, 130))
tmp2 = Image.new("RGB", (100, 130))
tmp3 = Image.new("RGB", (100, 130))
#img.show()
for i in range (0, tmp. height):
	for j in range (0, tmp. width):
		pixel1 = img.getpixel((j+96, i+515))
		pixel2 = img.getpixel((j+196, i+535))
		lp1 = list(pixel1)
		lp2 = list(pixel2)
		lp2[0] = (lp2[0]+lp1[0])/2 
		lp2[1] = (lp2[1]+lp1[1])/2 
		lp2[2] = (lp2[2]+lp1[2])/2 
		pixel = tuple(lp2)
		tmp.putpixel((j, i), pixel)
		#tmp2.putpixel((j, i), img.getpixel((j+96, i+515)))
		#tmp3.putpixel((j, i), img.getpixel)
tmp.show()
i, j = (553, 294)
for m in range (i, i+5):
	for n in range (j, j+5):
		img.putpixel((n+(tmp.width/2), m+(tmp.height/2)), (255, 0, 0))
img.show()
#tmp2.show()
#tmp3.show()
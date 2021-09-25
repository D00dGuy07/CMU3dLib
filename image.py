import sys
from PIL import Image

fileName = sys.argv[1]

img = Image.open(fileName)
rgb_img = img.convert('RGB')

sizeX, sizeY = rgb_img.size
if sizeX > 400:
	sizeX = 400
if sizeY > 400:
	sizeY = 400

stepX = 400 / sizeX
stepY = 400 / sizeY
if not ((stepX.is_integer() and stepY.is_integer()) and stepX == stepY):
	stepX = 1
	stepY = 1

file = open(f"{fileName.split('.')[0]}.py", "w")
file.write(f"from cmu_graphics import *\napp.setMaxShapeCount({sizeX * sizeY})\n\n")
for y in range(sizeX):
	for x in range(sizeY):
		r, g, b = rgb_img.getpixel((x, y))
		file.write(f"Rect({x * stepX}, {y * stepY}, {stepX}, {stepY}, fill=rgb({r}, {g}, {b}))\n")

rgb_img.close()
img.close()
file.close()
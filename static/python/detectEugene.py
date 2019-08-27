import math
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
from PIL import Image, ImageDraw
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from functools import reduce

import dlib
import time

import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage import data
from skimage.filters import gaussian
from skimage.segmentation import active_contour

from scriptsEugene import *


# Домиком, Кругом, Линией
def eyebrows(pose, scale):
	scale = 100 / scale

	dir1 = dir_between(pose.part(31).x, pose.part(31).y, pose.part(35).x, pose.part(35).y,
													pose.part(22).x, pose.part(22).y, pose.part(26).x, pose.part(26).y)


	dir2 = dir_between(pose.part(35).x, pose.part(35).y, pose.part(31).x, pose.part(31).y,
													pose.part(21).x, pose.part(21).y, pose.part(17).x, pose.part(17).y)


	eye_line1 = dir_between(pose.part(22).x, pose.part(22).y, pose.part(23).x, pose.part(23).y,
													pose.part(22).x, pose.part(22).y, pose.part(26).x, pose.part(26).y)

	eye_line2 = dir_between(pose.part(21).x, pose.part(21).y, pose.part(20).x, pose.part(20).y,
													pose.part(21).x, pose.part(21).y, pose.part(17).x, pose.part(17).y)
	

	eye_circle = ((eye_line1 + eye_line2) / 2 - 12) * 3.44

	eye_house = mean_square((dir1 + dir2) / 2 * 10, 100 - eye_circle)

	eye_line = mean_square(100 - (dir1 + dir2) / 2 * 10, 100 - eye_circle)

	eye_house, eye_circle, eye_line = clamp(eye_house, 0, 100), clamp(eye_circle, 0, 100), clamp(eye_line, 0, 100)

	return eye_house, eye_circle, eye_line


# Подбородок с ямкой
def fat_chin(pose, image):
    hdist = (pose.part(8).x - pose.part(7).x)
    vdist = (pose.part(8).y - pose.part(57).y)

    pose_max = min(pose.part(7).y, pose.part(9).y)

    min_x = round(pose.part(8).x - hdist / 3)
    max_x = round(pose.part(8).x + hdist / 3)
    min_y = round(pose_max - vdist / 3)
    max_y = round(pose_max)

    r, g, b = get_color(min_x, max_x, min_y, max_y, image, 3)

    if r == -1:
    	return -1

    pit_color = sRGBColor(r / 255, g / 255, b / 255);
    pit_color = convert_color(pit_color, LabColor)

    min_x = round(pose.part(8).x - hdist / 3)
    max_x = round(pose.part(8).x + hdist / 3)
    min_y = round(pose_max - vdist * (2 / 3))
    max_y = round(pose_max - vdist * (1 / 3))

    r, g, b = get_color(min_x, max_x, min_y, max_y, image, 3)

    chin_color = sRGBColor(r / 255, g / 255, b / 255);
    chin_color = convert_color(chin_color, LabColor)

    return clamp((delta_e_cie2000(pit_color, chin_color) - 7) * 5 + 50, 0, 100)


# Брови с подъёмом
def eyebrows_rise(pose, scale):
	scale = 100 / scale

	rise1 = distance(pose.part(36).x, pose.part(36).y, pose.part(17).x, pose.part(17).y )
	near1 = distance(pose.part(39).x, pose.part(39).y, pose.part(21).x, pose.part(21).y )

	rise2 = distance(pose.part(45).x, pose.part(45).y, pose.part(26).x, pose.part(26).y )
	near2 = distance(pose.part(42).x, pose.part(42).y, pose.part(22).x, pose.part(22).y )

	rise = (rise1 + rise2) / 2 * scale / 0.4
	rise += ((rise - (near1 + near2) / 2) * scale - 50) / 4

	return clamp(rise, 0, 100)


# Тёмные густые, Светлые редкие - Брови
def eyebrows_bold(pose, image):
    
    #min_x = min(pose.part(17).x, pose.part(18).x, pose.part(19).x, pose.part(20).x, pose.part(21).x)
    #max_x = max(pose.part(17).x, pose.part(18).x, pose.part(19).x, pose.part(20).x, pose.part(21).x)
    #min_y = min(pose.part(17).y, pose.part(18).y, pose.part(19).y, pose.part(20).y, pose.part(21).y)
    #max_y = max(pose.part(17).y, pose.part(18).y, pose.part(19).y, pose.part(20).y, pose.part(21).y)
    

    min_x = min(pose.part(18).x, pose.part(19).x)
    max_x = max(pose.part(18).x, pose.part(19).x) + 1
    min_y = min(pose.part(18).y, pose.part(19).y)
    max_y = min_y + (pose.part(28).y - pose.part(27).y)

    eyebrows_color1 = get_dominate_color(min_x, max_x, min_y, max_y, image)

    min_x = min(pose.part(24).x, pose.part(25).x)
    max_x = max(pose.part(24).x, pose.part(25).x) + 1
    min_y = min(pose.part(24).y, pose.part(25).y)
    max_y = min_y + (pose.part(28).y - pose.part(27).y)

    eyebrows_color2 = get_dominate_color(min_x, max_x, min_y, max_y, image)

    light_rare = ((eyebrows_color1 + eyebrows_color2) / 2 - 100) / 4
    light_rare = clamp(light_rare, 0, 100)
    bold_often = 100 - light_rare

    return light_rare, bold_often


# Форма волос лба
def forhead_form(pose, image, scale, im):
	
	forhead = [0, 0, 0]
	forhead[0], forhead[1], forhead[2] = add_forehead(pose, image, scale, 1)

	if forhead[1].length == 0:
		return -1,-1,-1

	#distance = lined(forhead[1].x, forhead[1].y, forhead[0].x, forhead[0].y, forhead[2].x, forhead[2].y) * 100/scale

	side_forehead = (forhead[0].length + forhead[2].length) / 2
	min_forehead = min(forhead[0].length, forhead[2].length)
	max_forehead = max(forhead[0].length, forhead[2].length)

	fh_M = clamp((max_forehead - forhead[1].length) * 20, 0, 100)
	fh_circle = clamp((forhead[1].length - min_forehead) * 12, 0, 100)
	fh_square = 100 - clamp(abs(forhead[1].length - side_forehead) * 20, 0, 100)

	return fh_circle, fh_M, fh_square



# Высота лба
def forhead_height(pose, image, scale, im):
	forhead = [0, 0, 0]
	forhead[0], forhead[1], forhead[2] = add_forehead(pose, image, scale, 1)

	if forhead[1].length == 0:
		return -1, -1

	height = forhead[1].length
	wide = clamp((height - 14) * 3, 0, 100)
	narrow = 100 - wide

	return wide, narrow


# Размер бровей
def eyebrows_height(pose, image, scale):

	length1 = eyebrows_height_1(pose, image, scale, 20, 38)
	length2 = eyebrows_height_1(pose, image, scale, 23, 43)

	length = (length1 + length2) / 2
	
	if length in range(10, 17):
		length = clamp(50 * (1 + (length - 13) / 100), 0, 100)
	else:
		length = clamp((length - 5) * 5.8, 0, 100)

	return 100 - length, length


# Форма лица
def face_form(pose, image, scale):
	forhead = [0, 0, 0]
	forhead[0], forhead[1], forhead[2] = add_forehead(pose, image, scale)

	dist1 = distance(pose.part(17).x, pose.part(17).y, pose.part(26).x, pose.part(26).y)
	dist2 = distance(pose.part(1).x, pose.part(1).y, pose.part(15).x, pose.part(15).y)
	dist3 = distance(pose.part(4).x, pose.part(4).y, pose.part(12).x, pose.part(12).y)
	dist4 = distance(pose.part(5).x, pose.part(5).y, forhead[1].x, forhead[1].y)

	dist1, dist2, dist3, dist4 = dist1 * 100/scale, dist2 * 100/scale, dist3 * 100/scale, dist4 * 100/scale
	
	water = mean_square(((dist1 + dist2 + dist3)/3 - 140) * 2.8, ((dist2 + dist3) / 2 - 120) * 1.5)

	wind = mean_square(100 - abs(dist2 - 173.4) * 5, (dist4 - dist2 - 10) * 2.4)

	fire = mean_square(100 - (dist3 - 130) * 2.6, (dist1 - dist3 + 10) * 3.7, 100 - (dist1 + dist2 + dist3 + dist4) / 4 / 3.4)

	max_ = max(water, wind, fire)
	if max_ > 100:
		k = max_ / 100
		water, wind, fire = water / k, wind / k, fire / k

		
	if forhead[1].length == 0:
		return -1, -1, -1

	return clamp(water, 0, 100), clamp(wind, 0, 100), clamp(fire, 0, 100)


# Миры
def worlds(pose, image, scale):
	forhead = [0, 0, 0]
	forhead[0], forhead[1], forhead[2] = add_forehead(pose, image, scale)

	pose_brows_y = (pose.part(24).y + pose.part(19).y) / 2

	material = distance(pose.part(8).x, pose.part(8).y, pose.part(30).x, pose.part(30).y) * 100/scale * 0.75
	family = distance(pose.part(30).x, pose.part(30).y, pose.part(27).x, pose_brows_y) * 100/scale * 0.8

	if forhead[1].length != 0:
		spiritual = clamp(distance(pose.part(27).x, pose_brows_y, forhead[1].x, forhead[1].y) * 100/scale * 0.85, 0, 100)
	else:
		spiritual = -1

	return spiritual, clamp(material, 0, 100), clamp(family, 0, 100)
	

# Размер уха
def ear_size(pose, image, scale, im):
	ear = [0, 0, 0, 0]
	ear[0], ear[1], ear[2], ear[3] = add_ear(pose, image, scale)

	length1 = ear[0].length
	length2 = ear[1].length

	length = max(length1, length2)

	if length == 0:
		#return "Фотография неправильного формата", "Фотография неправильного формата"
		return -1,-1

	
	img = rgb2gray(im)

	dir_ = point_direction(pose.part(0).x, pose.part(0).y, pose.part(3).x, pose.part(3).y) * (np.pi/180)
	dist = distance(pose.part(0).x, pose.part(0).y, pose.part(1).x, pose.part(1).y) 
	s = np.linspace(0, np.pi, 400)
	x = pose.part(1).x + 3 + dist*np.cos(s + dir_)
	y = pose.part(1).y + dist*2*np.sin(s + dir_)
	init1 = np.array([x, y]).T

	snake1 = active_contour(gaussian(img, 3), init1, alpha=0.015, beta=10, gamma=0.001, bc="fixed", w_edge=2)

	########################
	dir_ = point_direction(pose.part(13).x, pose.part(13).y, pose.part(16).x, pose.part(16).y) * (np.pi/180)
	#dist = distance(pose.part(16).x, pose.part(16).y, ear[1].x, ear[1].y) 
	s = np.linspace(0, np.pi, 400)
	x = pose.part(15).x - 3 + dist*np.cos(s + dir_)
	y = pose.part(15).y + dist*2*np.sin(s + dir_)
	init2 = np.array([x, y]).T

	snake2 = active_contour(gaussian(img, 3), init2, alpha=0.015, beta=10, gamma=0.001, bc="fixed", w_edge=2)

	#init = np.vstack((init1, init2))
	#snake = np.vstack((snake1, snake2))
	'''
	fig, ax = plt.subplots(figsize=(7, 7))
	ax.imshow(img, cmap=plt.cm.gray)
	ax.plot(init[:, 0], init[:, 1], '--r', lw=3)
	ax.plot(snake1[:, 0], snake1[:, 1], '-b', lw=3)
	ax.plot(snake2[:, 0], snake2[:, 1], '-b', lw=3)
	ax.set_xticks([]), ax.set_yticks([])
	ax.axis([0, img.shape[1], img.shape[0], 0])
	
	plt.show()
	'''
	dir_ = point_direction(pose.part(28).x, pose.part(28).y, pose.part(1).x, pose.part(1).y)
	lendir_x, lendir_y = lengthDir(scale/100, dir_)

	length1 = 0

	x = pose.part(1).x
	y = pose.part(1).y

	while True:
		
		min_ = 10000
		for i in range(0, 400):
			min_ = min(min_, distance(x, y, snake1[i, 0], snake1[i, 1]))
		
		if min_ < scale/50:
			break
		
		#print(min_)

		x += lendir_x
		y += lendir_y

		length1 += 1
		if length1 == 50:
			length1 = 0
			break

	dir_ = point_direction(pose.part(28).x, pose.part(28).y, pose.part(15).x, pose.part(15).y)
	lendir_x, lendir_y = lengthDir(scale/100, dir_)

	length2 = 0

	x = pose.part(15).x
	y = pose.part(15).y

	while True:
		min_ = 10000
		for i in range(0, 400):
			min_ = min(min_, distance(x, y, snake2[i, 0], snake2[i, 1]))
		
		if min_ < scale/50:
			break
		

		x += lendir_x
		y += lendir_y

		length2 += 1
		if length2 == 50:
			length2 = 0
			break

	if distance(pose.part(0).x, pose.part(0).y, pose.part(17).x, pose.part(17).y) >= distance(pose.part(16).x, pose.part(16).y, pose.part(26).x, pose.part(26).y):
		length = length1
	else:
		length = length2

	length = clamp( length * 3.44, 0, 100)

	return length, 100 - length



def ear_check(pose, image, scale):
	ear = [0, 0, 0, 0]
	ear[0], ear[1], ear[2], ear[3] = add_ear(pose, image, scale)

	if max(ear[0].length, ear[1].length) == 0 and max(ear[2].length, ear[3].length) == 0:
		#return "Неправильный ракурс", "Неправильный ракурс"
		return -1,-1
	result = clamp((max(ear[0].length - ear[2].length, ear[1].length - ear[3].length) - 5) * 3.3, 0, 100)


	return result, 100 - result



def earlobe_size(pose, image, scale):
	ear = [0, 0, 0, 0]
	ear[0], ear[1], ear[2], ear[3] = add_ear(pose, image, scale)
	
	if (ear[0].x != pose.part(1).x) and (ear[0].x != 0):
		x = (ear[0].x + pose.part(1).x + ear[2].x + pose.part(2).x) / 4
		y = (ear[0].y + pose.part(1).y + ear[2].y + pose.part(2).y) / 4
		
		length1 = ear_height(pose, image, scale, x, y) 

	if (ear[2].x != pose.part(15).x) and (ear[2].x != 0):
		x = (ear[1].x + pose.part(15).x + ear[3].x + pose.part(14).x) / 4
		y = (ear[1].y + pose.part(15).y + ear[3].y + pose.part(14).y) / 4
		
		length2 = ear_height(pose, image, scale, x, y) 

	if max(ear[0].length, ear[2].length, ear[1].length, ear[3].length) == 0:
		#return "Неправильный ракурс", "Неправильный ракурс"
		return -1,-1
	result = clamp(max(length1, length2) * 4.8, 0, 100)

	return result, 100 - result



def cheekbones(pose, image, scale):
	eye_x = (pose.part(36).x + pose.part(45).x) / 2
	eye_y = (pose.part(36).y + pose.part(45).y) / 2

	result = lined(eye_x, eye_y, pose.part(0).x, pose.part(0).y, pose.part(16).x, pose.part(16).y)

	result1 = clamp((result + 25) * 2, 0, 100)
	result3 = clamp(100 - abs(result) * 9, 0, 100)
	result2 = 100 - result1 

	return result1, result2, result3



def eye_color(pose, im):

	rs1, gs1, bs1 = get_dominate_color(pose.part(43).x, pose.part(46).x,
																	pose.part(43).y, pose.part(46).y, im, 3)

	rs2, gs2, bs2 = get_dominate_color(pose.part(37).x, pose.part(40).x,
																	pose.part(37).y, pose.part(40).y, im, 3)

	rs, gs, bs = (rs1 + rs2) / 2, (gs1 + gs2) / 2, (bs1 + bs2) / 2

	gol = 50 + (bs-gs)+(bs-rs)

	zel = 50 + (gs-bs)+(gs-rs)

	kar = 50 + (rs-bs)+(rs-gs)

	ser = 100 - (abs(rs - gs)+abs(rs - bs)+abs(gs - bs)) * 1.5

	blck = 100 - (abs(rs - gs)+abs(rs - bs)+abs(gs - bs)) * 2.5 - (rs - 70 + bs - 70 + gs - 70)
	kar = max(blck, kar)

	max_ = max(gol, zel, kar, ser)
	if max_ > 100:
		k = max_ / 100
		gol, zel, kar, ser = gol / k, zel / k, kar / k, ser / k

	gol, zel, kar, ser = clamp(gol, 0, 100), clamp(zel, 0, 100), clamp(kar, 0, 100), clamp(ser, 0, 100)

	return gol, zel, kar, ser


def fat_chin2(predictor_model, file_name, pose, im1):

	im = Image.open(file_name) # Can be many different formats.
	pix = im.load()
	#print('Image Size: '+str(im.size))  # Get the width and hight of the image for iterating over
	x1 = pose.part(7).x
	x2 = pose.part(9).x
	y1 = pose.part(7).y
	y2 = pose.part(9).y
	x = round(x1)
	yn = y1 - (pose.part(8).x-pose.part(7).x) / 4
	y = round((((y2 - y1)*(x - x1)) + yn * (x2 - x1))/(x2 - x1))
	dist = (x2 - x1) / 2
	average_s = 0
	count = 0

	while((x<x2) and (x>0)):
		y = round((((y2 - y1)*(x - x1)) + yn * (x2 - x1))/(x2 - x1))

		second_color=pix[x,y]

		try:
			average_s += (0.299 *	second_color[0] + 0.587 * second_color[1]+ 0.114 * second_color[2]) #* (1 - abs((x - dist/2)/(dist/2)) + 0.5)
		except:
			return -1

		

		im1[y, x] = (255,255,255)
		x += 1
		count += 1

	avrg = average_s / count
	max=0
	min=255
	x1 = pose.part(7).x
	x2 = pose.part(9).x
	y1 = pose.part(7).y
	y2 = pose.part(9).y
	x = round(x1)

	#win = dlib.image_window()

	while((x<x2) and (x>0)):
		y = round((((y2 - y1)*(x - x1)) + yn * (x2 - x1))/(x2 - x1))

		second_color=pix[x,y]

		average_s = (0.299 *	second_color[0] + 0.587 * second_color[1] + 0.114 * second_color[2]) 
		average_s = (average_s - avrg)

		if average_s > 0:
			average_s = average_s * (2 - (abs(x - x1 - dist) / dist) * 2)

		#print(average_s)

		if(average_s<min):
			min=average_s
		if(average_s>max):
			max=average_s

		#im1[y, x] = (255,255,255)
		x+=1

	#win.set_image(im1)
	#time.sleep(7)

	if((max-min)>80):
		result = 100
	else:
		result = 0

	return result


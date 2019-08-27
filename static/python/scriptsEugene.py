import math
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
from PIL import Image, ImageDraw
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

# Угол между линиями
def dir_between(x1, y1, x2, y2, x3, y3, x4, y4):
	if (x2 - x1) == 0:
		x2 += 0.0001
	if (x4 - x3) == 0:
		x4 += 0.0001
	k1 = (y2 - y1) / (x2 - x1)
	k2 = (y4 - y3) / (x4 - x3)

	a = 1
	if (k1 * k2 + a) == 0:
	  return 90
	return math.degrees(math.atan(abs((k1 - k2) / (k1 * k2 + a))))


def mean_square(a, b, c = -404):
	if c == -404:
		return math.sqrt((a**2 + b**2) / 2)
	else:
		return math.sqrt((a**2 + b**2 + c**2) / 3)

# Средняя переменная f. e. (0, 37, 100)
def clamp(val, small, big):
    return max(small, min(val, big))


# Взять цвет прямоугольника
def get_color(min_x, max_x, min_y, max_y, image, value = 1):
	rs = 0
	bs = 0
	gs = 0
	count = 0
	for i in range(min_x, max_x):
		for j in range(min_y, max_y):
			try:
				r, g, b = image.getpixel((i, j))
			except:
				if value == 1:
					return -1
				elif value == 3:
					return -1, -1, -1
			rs += r
			bs += b
			gs += g
			count += 1

	if value == 1:
		return (rs + bs + gs) / count
	elif value == 3:
		return rs / count, bs / count, gs / count


# Взять доминантный цвет
def get_dominate_color(min_x, max_x, min_y, max_y, image, value = 1):
	NUM_CLUSTERS = 1

	area = (min_x, min_y, max_x, max_y)
	cropped_img = image.crop(area)
	try:
		ar = np.asarray(cropped_img)
		shape = ar.shape
		ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)
	except:
		if value == 1:
			return -1
		elif value == 3:
			return -1, -1, -1

	codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
  #print('cluster centres:\n', codes)

	peak = codes[0]
	if value == 1:
		return peak[0] + peak[1] + peak[2]
	elif value == 3:
		return peak[0], peak[1], peak[2]


# Расстояние между точками
def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# Направление линии
def point_direction(x1, y1, x2, y2):
	return math.degrees(math.atan2((y2 - y1), (x2 - x1)))


def lengthDir(length, angle):
  radian_angle = math.radians(angle)
  return (length * math.cos(radian_angle), length * math.sin(radian_angle))


# Насколько точка выше линии (Сначала)
def lined(x, y, x1, y1, x2, y2):
    return y - ((((x - x1) * (y2 - y1)) / (x2 - x1)) + y1)


# Х, У, Радиус круга по трём точкам
def rad_circle(x1, y1, x2, y2, x3, y3, scale):
	ma = (y2 - y1) / (x2 - x1)
	mb = (y3 - y2) / (x3 - x2)

	x = (ma * mb * (y1 - y3) + mb * (x1 + x2) - ma * (x2 + x3)) / (2 * (mb - ma))

	if ma == 0:
		ya = (y2 + y1) / 2
	else: 
		ya = -(1 / (ma)) * (x - (x1 + x2) / 2) + (y1 + y2) / 2

	return x, ya, distance(x, ya, x1, y1)


# Длина высоты
def distance_height(x1, y1, x2, y2, x3, y3):
	a = (y2 - y1) / (x2 - x1)
	b = -1
	c = (y1 * x2 - y2 * x1) / (x2 - x1)

	return abs(a * x3 + b *	y3 + c) / math.sqrt(a*a + b*b)



# Обращает в чёрно-белое
def black_white(image, number_of_black, massive = False):
	gray = image.convert('L')

  # Let numpy do the heavy lifting for converting pixels to pure black or white
	bw = np.asarray(gray).copy()

  # Pixel range is 0...255, 256/2 = 128
	bw[bw < number_of_black] = 0    # Black
	bw[bw >= number_of_black] = 255 # White

  # Now we put it back in Pillow/PIL land
	if (massive):
		return bw
	else:
		return Image.fromarray(bw)


# Объект Лоб
class Forehead(object):
		x = 0
		y = 0
		length = 0

    # The class "constructor" - It actually an initializer 
		def __init__(self, pose, image, scale, pose_number, length_main = 15):

			dir_ = point_direction(pose.part(29).x, pose.part(29).y, pose.part(27).x, pose.part(27).y)
			lendir_x, lendir_y = lengthDir(scale/50, dir_)

			length = length_main
			summ = 0
			average = 0

			sub_scale = 5
			mul_scale = 3

			if pose_number == 1:
				length_main = 9
				length = length_main
				x = (pose.part(19).x + pose.part(24).x) / 2 +  length * lendir_x
				y = (pose.part(19).y + pose.part(24).y) / 2 +  length * lendir_y

			else:
				x = pose.part(pose_number).x +  length * lendir_x
				y = pose.part(pose_number).y +  length * lendir_y

			try:
				r, g, b = image.getpixel((x, y))
				color2_rgb = sRGBColor(r / 255, g / 255, b / 255);
			except:
				x = 0
				y = 0
				length = 0
			else:
				while (length!=0) and (y > 1 + sub_scale):
					r, g, b = get_dominate_color(round(x) - sub_scale, round(x) + sub_scale, round(y) - sub_scale, round(y) + sub_scale, image, 3)

					color1_rgb = sRGBColor(r / 255, g / 255, b / 255);

					# Convert from RGB to Lab Color Space
					color1_lab = convert_color(color1_rgb, LabColor);

					# Convert from RGB to Lab Color Space
					color2_lab = convert_color(color2_rgb, LabColor);

					# Find the color difference
					delta_e = delta_e_cie2000(color1_lab, color2_lab);

					#if pose_number == 27:
					#	print("The difference between the 2 color = ", delta_e)

					if length > length_main + 3:
						if (delta_e > average * 3 + 1) or (delta_e > 7):
							break

					summ += delta_e
					length += 1
					average = summ / length

					color2_rgb = color1_rgb

					x += lendir_x
					y += lendir_y


			self.x = x
			self.y = y
			self.length = length




# Добавляем 3 ебаных блять точки, ведь нейросеть не может блеат
def add_forehead(pose, image, scale, center_pose = 27):
	forh_center = Forehead(pose, image, scale, center_pose)
	forh_0 = Forehead(pose, image, scale, 19)
	forh_2 = Forehead(pose, image, scale, 24)

	return forh_0, forh_center, forh_2



# Скрипт для длины бровей
def eyebrows_height_1(pose, image, scale, pose_number1 = 20, pose_number2 = 38):
	dir_ = point_direction(pose.part(27).x, pose.part(27).y, pose.part(29).x, pose.part(29).y)

	lendir_x, lendir_y = lengthDir(scale/100, dir_)

	length = 2
	summ = 0
	average = 0

	x = pose.part(pose_number1).x +  length * lendir_x
	y = pose.part(pose_number1).y +  length * lendir_y

	try:
		r, g, b = image.getpixel((x, y))
		color2_rgb = sRGBColor(r / 255, g / 255, b / 255);
	except:
		return 0

	for i in range(pose.part(pose_number1).y, pose.part(pose_number2).y):
		r, g, b = image.getpixel((x, y))
		# Red Color
		color1_rgb = sRGBColor(r / 255, g / 255, b / 255);

		# Convert from RGB to Lab Color Space
		color1_lab = convert_color(color1_rgb, LabColor);

		# Convert from RGB to Lab Color Space
		color2_lab = convert_color(color2_rgb, LabColor);

		# Find the color difference
		delta_e = delta_e_cie2000(color1_lab, color2_lab);

		#print ("The difference between the 2 color = ", delta_e)

		if length > 4:
			if (delta_e > average * 5 + 1) or (delta_e > 10):
				break

		summ += delta_e
		length += 1
		average = summ / (length - 2)

		color2_rgb = color1_rgb

		x += lendir_x
		y += lendir_y

	return length



class Ear1(object):
		x = 0
		y = 0
		length = 0

    # The class "constructor" - It actually an initializer 
		def __init__(self, pose, image, scale, pose_number1 = 1, pose_number2 = 28):

			# Создание точкек Ушей
			dir_ = point_direction(pose.part(pose_number2).x, pose.part(pose_number2).y, pose.part(pose_number1).x, pose.part(pose_number1).y)

			lendir_x, lendir_y = lengthDir(scale/100, dir_)

			length = 0
			summ = 0
			average = 0

			x = pose.part(pose_number1).x +  length * lendir_x
			y = pose.part(pose_number1).y +  length * lendir_y

			try:
				r, g, b = image.getpixel((x, y))
				color2_rgb = sRGBColor(r / 255, g / 255, b / 255);
			except:
				print('error')

			for i in range(0, 50):
				try:
					r, g, b = image.getpixel((x, y))
				except:
					x = 0
					y = 0
					length = 0
					break
				# Red Color
				color1_rgb = sRGBColor(r / 255, g / 255, b / 255);

				# Convert from RGB to Lab Color Space
				color1_lab = convert_color(color1_rgb, LabColor);

				# Convert from RGB to Lab Color Space
				color2_lab = convert_color(color2_rgb, LabColor);

				# Find the color difference
				delta_e = delta_e_cie2000(color1_lab, color2_lab);

				#print ("The difference between the 2 color = ", delta_e)

				if length > 2:
					if (delta_e > average * 5 + 1) or (delta_e > 14):
						break

				summ += delta_e
				length += 1
				average = summ / length

				color2_rgb = color1_rgb

				x += lendir_x
				y += lendir_y

			if length == 50:
				length = 0

			self.x = x
			self.y = y
			self.length = length


class Ear(object):
		x = 0
		y = 0
		length = 0

    # The class "constructor" - It actually an initializer 
		def __init__(self, pose, image, scale, pose_number1 = 1, pose_number2 = 28):

			# Создание точкек Ушей
			dir_ = point_direction(pose.part(pose_number2).x, pose.part(pose_number2).y, pose.part(pose_number1).x, pose.part(pose_number1).y)

			lendir_x, lendir_y = lengthDir(scale/200, dir_)

			length = 0
			summ = 0
			average = 0
			sub_scale = 5

			x_ = pose.part(29).y + (pose.part(15).y - pose.part(29).y) / 2
			y_ = pose.part(26).y + (pose.part(12).y - pose.part(26).y) / 2

			x = pose.part(pose_number1).x +  length * lendir_x
			y = pose.part(pose_number1).y +  length * lendir_y

			try:
				r, g, b = get_dominate_color(x_ - 15, x_ + 15, y_ - 15, y + 15, image, 3)
				color2_rgb = sRGBColor(r / 255, g / 255, b / 255);
			except:
				x = 0
				y = 0
				length = 0
			else:
				while (length != 25):
					r, g, b = get_dominate_color(round(x) - sub_scale, round(x) + sub_scale, round(y) - sub_scale, round(y) + sub_scale, image, 3)

					color1_rgb = sRGBColor(r / 255, g / 255, b / 255);

					# Convert from RGB to Lab Color Space
					color1_lab = convert_color(color1_rgb, LabColor);

					# Convert from RGB to Lab Color Space
					color2_lab = convert_color(color2_rgb, LabColor);

					# Find the color difference
					delta_e = delta_e_cie2000(color1_lab, color2_lab);

					#if pose_number == 27:
					#	print("The difference between the 2 color = ", delta_e)

					if length > 10:
						if (delta_e > 20):
							break

					summ += delta_e
					length += 1
					average = summ / length

					#color2_rgb = color1_rgb

					x += lendir_x
					y += lendir_y

			if length == 50:
				length = 0

			self.x = x
			self.y = y
			self.length = length


def add_ear(pose, image, scale):
	ear0 = Ear(pose, image, scale, 1)
	ear1 = Ear(pose, image, scale, 15)
	ear2 = Ear(pose, image, scale, 2, 29)
	ear3 = Ear(pose, image, scale, 14, 29)

	return ear0, ear1, ear2, ear3


def ear_height(pose, image, scale, x, y):
	dir_ = point_direction(pose.part(27).x, pose.part(27).y, pose.part(29).x, pose.part(29).y)

	lendir_x, lendir_y = lengthDir(scale/100, dir_)

	length = 0
	summ = 0
	average = 0

	x = x +  length * lendir_x
	y = y +  length * lendir_y

	try:
		r, g, b = image.getpixel((x, y))
		color2_rgb = sRGBColor(r / 255, g / 255, b / 255);
	except:
		return 0

	for i in range(0, 50):
		r, g, b = image.getpixel((x, y))
		# Red Color
		color1_rgb = sRGBColor(r / 255, g / 255, b / 255);

		# Convert from RGB to Lab Color Space
		color1_lab = convert_color(color1_rgb, LabColor);

		# Convert from RGB to Lab Color Space
		color2_lab = convert_color(color2_rgb, LabColor);

		# Find the color difference
		delta_e = delta_e_cie2000(color1_lab, color2_lab);

		#print ("The difference between the 2 color = ", delta_e)

		if length > 1:
			if (delta_e > average * 5 + 1) or (delta_e > 10):
				break

		summ += delta_e
		length += 1
		average = summ / length

		color2_rgb = color1_rgb

		x += lendir_x
		y += lendir_y

	if length == 50:
		length = 0

	return length


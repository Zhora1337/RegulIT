import sys
import dlib
import detect
#import detectEugene
#import detectVector
import os
#import openface
import imageio
from PIL import Image, ImageDraw
from skimage import io
from skimage.feature import hog
import numpy as np
import math


def script(image1, image):
	ubuntu = True #Эта переменная используется для разработки на Ubuntu. 
	#Чтобы отключить подгон кода под особенности Ubuntu присвойте данной перменной значение False.

	priznak = []
	for i in range(0, 66):
	    priznak.append(0)  # Массив значений признаков

	#if(ubuntu):

	#	print('Ubuntu is used now')

	#	predictor_model = "/home/vector/Documents/shape_predictor_68_face_landmarks.dat" # Модель определения 68 точек на лице
	#	#dir="/home/vector/Documents/Лоб/Прямой лоб"

	#else:

	predictor_model = "C:/shape_predictor_68_face_landmarks.dat" # Модель определения 68 точек на лице

	face_detector = dlib.get_frontal_face_detector()

	hog_list, hog_img = hog(image, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), block_norm='L1',
	                      visualize=True, feature_vector=True) # Генерируем hog изображение

	face_pose_predictor = dlib.shape_predictor(predictor_model) # Модель распознавания лица

	detected_faces = face_detector(image, 1) # Находим лица, что такое "1" - не помню

	if len(detected_faces) == 0:
	  print("Лица на фото не обнаружено")


	if len(detected_faces) > 1:
	  print("Обнаружено более одного лица")

	# Загрузка лица
	#win.set_image(image)
	#draw = ImageDraw.Draw(image1)
	# Loop through each face we found in the image
	if len(detected_faces) == 1: # Если лицо одно, то продолжаем
		for i, face_rect in enumerate(detected_faces):
			pose_landmarks = face_pose_predictor(image, face_rect)


		prop = math.sqrt((pose_landmarks.part(57).x - pose_landmarks.part(27).x) ** 2 +
											(pose_landmarks.part(57).y - pose_landmarks.part(27).y) ** 2)# Измеряем размер лица чтобы получить относительные размеры черт лица

		priznak[21]=detect.lips_gal(pose_landmarks, prop)
		priznak[22]=100-priznak[21]


		priznak = [ '%.1f' % elem for elem in priznak ]
		return priznak

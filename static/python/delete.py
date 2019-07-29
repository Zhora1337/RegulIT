import sys
import dlib
import detect
import detectEugene
#import detectVector
import os
#import openface
import imageio
from PIL import Image, ImageDraw
from skimage import io
from skimage.feature import hog
import numpy as np
import math

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def script(image1, image):
	

	ubuntu = True #Эта переменная используется для разработки на Ubuntu. 
	#Чтобы отключить подгон кода под особенности Ubuntu присвойте данной перменной значение False.

	priznak = []
	for i in range(0, 66):
	    priznak.append(0)  # Массив значений признаков


	predictor_model = os.path.join(BASE_DIR, 'python/shape_predictor_68_face_landmarks.dat') # Модель определения 68 точек на лице

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

		print("Верхняя губа с галочкой: ",priznak[21])
		print("Прямая верхняя губа: ", priznak[22])
		priznak[23]=detect.lips_height(pose_landmarks, face_rect.bottom()-face_rect.top())
		priznak[24] =100-priznak[23]
		print("Толстая верхняя губа: ",priznak[23])
		print("Тонкая верхняя губа: ", priznak[24])
		left =detect.left_lips_ugolki(pose_landmarks, prop)
		right = detect.right_lips_ugolki(pose_landmarks, prop)
		d=(left+right)/2
		if d>0:
			priznak[25]=d
			priznak[26]=0
			if d<20: priznak[27]=100-d*5
		if (d<0):
			priznak[25]=0
			priznak[26] = d
			if d<20: priznak[27]=100-d*5
		print("Уголки губ вверх: ", priznak[25])
		print("Уголки губ вниз: ", priznak[26])
		print("Уголки губ прямо: ", priznak[27])
		priznak[28] =detect.lips_rot(pose_landmarks)
		priznak[29] = 100-priznak[28]
		print("Узкий рот: ", priznak[28])
		print("Широкий рот: ", priznak[29])

		priznak[20]=detect.eye_posadka(pose_landmarks)
		priznak[12] = 100-priznak[20]
		print("Близко-посаженные глаза: ", priznak[12])
		print("Широко-посаженные глаза: ", priznak[20])

		priznak[16],priznak[17],priznak[18],priznak[19]=detect.eye_color(pose_landmarks, image1)
		print("Голубые глаза: ", priznak[16])
		print("Зеленые глаза: ", priznak[17])
		print("Карие и черные глаза: ", priznak[18])
		print("Серые глаза: ", priznak[19])

		priznak[40] =detect.chin_size(pose_landmarks, prop)
		priznak[43] = 100 - priznak[40]
		print("Большой подбородок: ", priznak[40])
		print("Маленький подбородок: ", priznak[43])
		priznak[42] = detect.chin_form(pose_landmarks, prop)
		priznak[41] = 100 - priznak[42]
		print("Квадратный подбородок: ", priznak[41])
		print("Круглый подбородок: ", priznak[42])

		priznak[8] = detect.eyebrows_accreted(pose_landmarks, image1)
		print("Сросшиеся брови: ", priznak[8])

		priznak[3], priznak[4], priznak[5] = detectEugene.eyebrows(pose_landmarks, prop)
		print("Бровин Домиком: ", priznak[3], "Бровин Полукругом: ", priznak[4], "Бровин Линией: ", priznak[5])

		priznak[44] = detectEugene.fat_chin(pose_landmarks, image1)
		print("Раздвоенный подбородок: ", priznak[44])

		priznak[6] = detectEugene.eyebrows_rise(pose_landmarks, prop)
		print("Бровь с подъёмом: ", priznak[6])

		priznak[7], priznak[9] = detectEugene.eyebrows_bold(pose_landmarks, image1)
		print("Брови тёмные, густые:", priznak[9], "Брови светлые, редкие:", priznak[7])

		priznak[32], priznak[34], priznak[55] = detectEugene.forhead_form(pose_landmarks, image1, prop) #круг, М, квадрат
		print("Волосы лба Полукругом: ", priznak[32], " Буквой М: ", priznak[34], "Квадратный: ", priznak[55])

		priznak[35], priznak[56] = detectEugene.forhead_height(pose_landmarks, image1, prop)
		print("Лоб Широкий: ", priznak[35], "Лоб Узкий: ", priznak[56])

		priznak[10], priznak[11] = detectEugene.eyebrows_height(pose_landmarks, image1, prop)
		print("Тонкие брови: ", priznak[10], " Широкие брови: ", priznak[11])

		priznak[51], priznak[52], priznak[53] = detectEugene.face_form(pose_landmarks, image1, prop)
		print("Вода на: ", priznak[51]," Ветер на: ", priznak[52]," Огонь на: ", priznak[53])

		priznak[57], priznak[58], priznak[59] = detectEugene.worlds(pose_landmarks, image1, prop)
		print("Духовный : ", priznak[57]," Материальный: ", priznak[58]," Семейный: ", priznak[59])

		priznak[50], priznak[64] = detectEugene.ear_size(pose_landmarks, image1, prop)
		print("Лопоухий: ", priznak[50], "Прижатые уши: ", priznak[64])

		priznak[47], priznak[49] = detectEugene.ear_check(pose_landmarks, image1, prop)
		print("Прижатые уши: ", priznak[47], "Квадратная мочка уха: ", priznak[49])

		priznak[45], priznak[46], priznak[63] = detectEugene.cheekbones(pose_landmarks, image1, prop)
		print("Скулы выше уровня глаз: ", priznak[45], "Скулы на уровне глаз: ", priznak[46], "Скулы ниже уровня глаз: ", priznak[63])
		
		priznak[1], priznak[2] = detectVector.asymmetry(predictor_model, file_name)
		#print("Ассиметрия в правую сторону: ", priznak[1], "Ассиметрия в левую сторону: ", priznak[2])


		priznak[48], priznak[65] = detectEugene.earlobe_size(pose_landmarks, image1, prop)
		#print("Мочка уха большая: ", priznak[48], "Мочка уха маленькая: ", priznak[65])

		priznak[62], priznak[39] = detectVector.nose(predictor_model, file_name,pose_landmarks)
		#print("Прямой нос: ", priznak[62], "Переносица с впадиной: ", priznak[39])

		priznak[36], priznak[37],priznak[60] = detectVector.nose_size(predictor_model, file_name,pose_landmarks)
		#print("Нос картошкой: ", priznak[36], "Курносый нос: ", priznak[37], "Кончик носа вниз: ", priznak[60])

		priznak[61] = detectVector.nose_wings(predictor_model, file_name,pose_landmarks)
		#print("Крылья носа очерчены: ", priznak[61])

		priznak[39] = detectVector.hump_nose(predictor_model, file_name,pose_landmarks)
		#print("Горбинка на носу: ", priznak[39])

		priznak[33],priznak[31] = detectVector.forehead(predictor_model, file_name,pose_landmarks)
		#print("Прямой лоб : ", priznak[33],"Выпуклый лоб : ", priznak[31])

		priznak[15],priznak[13], priznak[14] = detectVector.eyelids(predictor_model, file_name,pose_landmarks)
		#print("Веки, закрытые внутри : ", priznak[15],"Веки, закрытые посередине  : ", priznak[13],"Веки, закрытые снаружи  : ", priznak[14])'''



		priznak = [ '%.1f' % elem for elem in priznak ]
		return priznak

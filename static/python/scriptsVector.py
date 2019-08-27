#!/usr/bin/python
'''
--------------------------------------------------------------------
graf(x_data=[],y_data=[], save = False, title=None, new_filename='_'): Функция для вывода графиков.
x_data=[] - значения x 
y_data=[] - значения y
title - название графика
save - если True - сохранение в директории
new_filename - если save=True подпись к названию файла для сохранения в директории.

distance(x1,y1,x2,y2): Функция для рассчета расстояния между точками
x1,y1,x2,y2 - координаты точек

face_aligner_func(predictor_path,face_file_path): Функция для выравнивания лица и сохранения полученной фотографии
predictor_path - модель лица из 68 точек
face_file_path - адресс фотографии в дирректории

--------------------------------------------------------------------
'''

import sys 
import dlib 
import cv2
import os
import openface
import random
import imageio
from PIL import Image, ImageDraw
from skimage import io
from skimage.feature import hog
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import scipy
import scipy.misc
import scipy.cluster

def face_aligner_func(predictor_path,face_file_path):

    face_detector=dlib.get_frontal_face_detector()
    face_pose_predictor=dlib.shape_predictor(predictor_path)
    face_aligner=openface.AlignDlib(predictor_path)
    image = cv2.imread(face_file_path)

    detected_faces=face_detector(image,1)
    #print('Found {} faces.'.format(len(detected_faces)))

    for i, face_rect in enumerate(detected_faces):
        #print('-Face# {} found at Left: {} Top:{} Right:{} Bottom: {} '.format(i, face_rect.left(), face_rect.top(), face_rect.right(), face_rect.bottom()))
        pose_landmarks=face_pose_predictor(image,face_rect)
        alignedFace=face_aligner.align(1000,image,face_rect,landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
        cv2.imwrite(face_file_path.replace(".jpg","_aligned.jpg"),alignedFace)
        pose_landmarks = face_pose_predictor(alignedFace, face_rect)

    return pose_landmarks

def distance(x1,y1,x2,y2):
    dist=math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))

    return dist

def range(val1,val2):

    if(val1>100):
        val1=100
        val2=0
    elif(val1<0):
        val1=0
        val2=100

    return val1,val2

def graf(x_data=[],y_data=[], title=None, save = False, file_name='Empty_name', new_filename='_'):
    fig, ax = plt.subplots()
    ax.plot(x_data, y_data)

    if(title!=None):
        ax.set_title(title)

    if((save==1) and (file_name!='Empty_name')):
        fig.savefig(file_name.replace(".jpg", str(new_filename)+".jpg"))

def image_size_printer(im):
    print('Image Size: '+str(im.size))

def test_line(x,y,x1,y1,x2,y2,x11, y11):
    return (y-y11)*(x2-x1)-(x-x11)*(y2-y1)

def radical(a,b):
    if (a>0 and b<0) or (a<0 and b>0):
        return True
    else:
        return False 
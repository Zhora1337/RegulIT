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


"""

import math
import numpy as np
import scipy
import os
import sys
import scipy.misc
import scipy.cluster
from PIL import Image, ImageDraw
import dlib
import cv2
import openface

def face_aligner_func(predictor_path,face_file_path):
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(predictor_path)
    img = dlib.load_rgb_image(face_file_path)
    dets = detector(img, 1)

    num_faces = len(dets)
    if num_faces == 0:
        print("Sorry, there were no faces found in '{}'".format(face_file_path))

    faces = dlib.full_object_detections()
    for detection in dets:
        faces.append(sp(img, detection))

    window = dlib.image_window()

    images = dlib.get_face_chips(img, faces, size=200)
    for image in images:
        window.set_image(image)
        #image22 = cv2.imread(face_file_path)
        cv2.imwrite('aligned_face_{}.jpg'.format(face_file_path),image)
        dlib.hit_enter_to_continue()

    #image = dlib.get_face_chip(img, faces[0])
    #window.set_image(image)
    #dlib.hit_enter_to_continue()
    
"""
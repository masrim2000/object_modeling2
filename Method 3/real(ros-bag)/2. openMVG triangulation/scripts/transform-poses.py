# Reads the poses in images.txt and replaces them 
# with the transformed poses from ROS coordinate
# system to openMVG coordinate system.

import os
import sys
import numpy as np
import mathutils

my_file = open(os.path.join(sys.path[0], "../data/known/images.txt.origin"), "r") # IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME
# reading the file
images_list = my_file.read()
my_file.close()

if os.path.exists(os.path.join(sys.path[0], "../data/known/images.txt")):
    os.remove(os.path.join(sys.path[0], "../data/known/images.txt"))
my_file = open(os.path.join(sys.path[0], "../data/known/images.txt"), "w")

images_list = images_list.split("\n")
images_list = [x for x in images_list if not "#" in x]
images_list = [x for x in images_list if x]

#491 tracks ros_to_openMVG_rotation = np.array([[0,0,1],[0,-1,0],[-1,0,0]]) with trans (good)
#1075 tracks ros_to_openMVG_rotation = np.array([[0,0,-1],[0,1,0],[-1,0,0]]) with trans (better)
#491 tracks ros_to_openMVG_rotation = np.array([[0,0,-1],[0,1,0],[1,0,0]]) with trans (good)
#491 tracks ros_to_openMVG_rotation = np.array([[0,0,1],[0,-1,0],[1,0,0]]) with trans (good)
ros_to_openMVG_rotation = np.array([[0,0,-1],[0,1,0],[-1,0,0]])

for image in images_list:
    image = image.split(" ")
    image = [x if x.__contains__('.jpg') or x.__contains__('.png') else float(x) for x in image]
    image[0] = int(image[0]); image[8] = int(image[8])
    ros_translationW = mathutils.Vector(image[5:8])
    ros_quatW = image[1:5]
    ros_rotationW = mathutils.Matrix(mathutils.Quaternion(ros_quatW).to_matrix())
    ros_translationC = (-1.0 * ros_rotationW.transposed()) @ ros_translationW
    ros_rotationC = ros_rotationW.transposed()
    # openMVG_translation = ros_to_openMVG_rotation @ ros_translationC
    openMVG_translation = ros_translationW
    openMVG_rotation = ros_to_openMVG_rotation @ ros_rotationC
    T = mathutils.Matrix.Translation(openMVG_translation)
    R = mathutils.Matrix(openMVG_rotation).to_4x4()
    new_4x4 = T @ R
    new_translation, new_quat, _ = new_4x4.decompose()
    image[1] = new_quat[0]; image[2] = new_quat[1]; image[3] = new_quat[2]; image[4] = new_quat[3]
    image[5] = new_translation[0]; image[6] = new_translation[1]; image[7] = new_translation[2]
    print(image[0], image[1], image[2], image[3], image[4],
    image[5], image[6], image[7], image[8], image[9], sep=' ', end='\n\n', file=my_file)
my_file.close()
print("Poses transformed!")
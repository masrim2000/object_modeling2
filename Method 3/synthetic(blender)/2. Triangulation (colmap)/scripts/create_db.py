# Reads the information in cameras.txt and images.txt
# and converts them to a .db file for use in colmap.

import os
import sys
import db_utilities

#print(os.path.join(sys.path[0], "../../"))

# opening the file in read mode
my_file = open(os.path.join(sys.path[0], "../data/known/cameras.txt"), "r") #   CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]
camera_list = my_file.read()
my_file.close()

# splitting and coverting to list
camera_list = camera_list.split("\n")
camera_list = [x for x in camera_list if not "#" in x]
for i in range(len(camera_list)):
    camera_list[i] = camera_list[i].split(" ")
    camera_list[i] = [(ele if (ele.__contains__('jpg') or ele.__contains__('png')) else float(ele)) if ele.__contains__('.') else (int(ele) if ele.isdigit() else ele) for ele in camera_list[i]]
    camera_list[i] = [int(1) if ele=='PINHOLE' else ele for ele in camera_list[i]]
camera_list = [x for x in camera_list if len(x)>=2]

my_file = open(os.path.join(sys.path[0], "../data/known/images.txt"), "r")   # images (image_id, name, camera_id, prior_q[0], prior_q[1], prior_q[2],
                                                                    # prior_q[3], prior_t[0], prior_t[1], prior_t[2]))
                                                                    # IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME
# reading the file
images_list = my_file.read()
my_file.close()

# splitting and coverting to list
images_list = images_list.split("\n")
images_list = [x for x in images_list if not "#" in x]
for i in range(len(images_list)):
    images_list[i] = images_list[i].split(" ")
    images_list[i] = [(ele if (ele.__contains__('jpg') or ele.__contains__('png')) else float(ele)) if ele.__contains__('.') else (int(ele) if ele.isdigit() else ele) for ele in images_list[i]]
images_list = [x for x in images_list if len(x)>=2]

db_utilities.create(camera_list, images_list)
print("db created!")

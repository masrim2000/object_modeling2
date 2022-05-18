#!/usr/bin/python

import os
import sys
# import subprocess
import cv2
# import numpy as np
import pyzbar.pyzbar as pyzbar

image_name = os.listdir(os.path.join(sys.path[0],"../images"))

f = open(os.path.join(sys.path[0], "../gcp.txt"), "w")
print("# [img_name, pointX, pointY, xVal, yVal, zVal]", file=f)
for i in image_name:
    image = cv2.imread(os.path.join(sys.path[0], '../images/', i))

    decodedObjects = pyzbar.decode(image)
    for obj in decodedObjects:
        print("Type:", obj.type)
        print("Data: ", obj.data, "\n")
        (x, y, w, h) = obj.rect
        # cv2.rectangle(image, (x,y), (x+w,y+h), (255,0,0), 5)
        print("location: ", obj.rect, "\n")
    if 'y' not in vars():
        print(str(i), ": ERROR: zbar was unable to detect QR code")
        continue

    paddingSize = 10
    image_cropped = image[max(0,y-paddingSize):y+h+paddingSize, max(0,x-paddingSize):x+w+paddingSize]

    # cv2.imshow("QR Scanner", image_cropped)
    # cv2.waitKey(0)
    det=cv2.QRCodeDetector()
    val, pts, st_code=det.detectAndDecode(image_cropped)

    if pts is None:
        print(str(i), "ERROR: OpenCV was unable to detect QR code")
        continue

    corners = [[pts[0][0][0], pts[0][0][1]], [pts[0][1][0], pts[0][1][1]], [pts[0][3][0], pts[0][3][1]], [pts[0][2][0], pts[0][2][1]]]

    c1 = (-paddingSize+x+int(round(corners[0][0])),-paddingSize+y+int(round(corners[0][1])))
    c2 = (-paddingSize+x+int(round(corners[1][0])),-paddingSize+y+int(round(corners[1][1])))
    c3 = (-paddingSize+x+int(round(corners[2][0])),-paddingSize+y+int(round(corners[2][1])))


    cv2.circle(image, c1, 9, (255,255,255), -1)
    cv2.circle(image, c1, 6, (0,0,255), -1)

    cv2.circle(image, c2, 9, (255,255,255), -1)
    cv2.circle(image, c2, 6, (0,255,0), -1)

    cv2.circle(image, c3, 9, (255,255,255), -1)
    cv2.circle(image, c3, 6, (255,0,0), -1)

    write_img_path = ''.join([i[:len(i)-4], '-cornersDetected.jpg'])
    write_img_path = os.path.join(sys.path[0], "../", write_img_path)
    cv2.imwrite(write_img_path, image)

    #           [X, Y, Z]
    # c1_world = [0.0, 0.0, 0.0]
    # c2_world = [0.457, 0.0, 0.0]
    # c3_world = [0.0, 0.0, -0.457]
    # QR string format: 'c1_x,c1_y,c1_z;c2_x,c2_y,c2_z;c3_x,c3_y,c3_z'
    # e.g.: '0,0,0;0,-0.185,0;-0.185,0,0'
    qr_data_rows = val.split(";")
    for row in range(len(qr_data_rows)):
        qr_data_rows[row] = qr_data_rows[row].split(",")
        qr_data_rows[row] = [float(x) for x in qr_data_rows[row]]
    c1_world = qr_data_rows[0]
    c2_world = qr_data_rows[1]
    c3_world = qr_data_rows[2]

    
    # points = [img_name, pointX, pointY, xVal, yVal, zVal]
    print(i, c1[0], c1[1], c1_world[0], c1_world[1], c1_world[2], sep=' ', end='\n', file=f)
    print(i, c2[0], c2[1], c2_world[0], c2_world[1], c2_world[2], sep=' ', end='\n', file=f)
    print(i, c3[0], c3[1], c3_world[0], c3_world[1], c3_world[2], sep=' ', end='\n', file=f)
    

    # cv2.imshow("QR Scanner", image)
    # cv2.waitKey(0)

f.close()

f = open(os.path.join(sys.path[0], "../gcp.txt"), "r")
gcpTxt = f.read()
f.close()

gcpTxt = gcpTxt.split('\n')
gcpTxt = [x for x in gcpTxt if not "#" in x]
gcpTxt = [ele for ele in gcpTxt if not str(ele)==""]
gcpTxt = [x.split(' ') for x in gcpTxt]
for i in range(len(gcpTxt)):
    for j in range(1, len(gcpTxt[0])):
        gcpTxt[i][j] = float(gcpTxt[i][j])

coords = []
myorder = []
for row in gcpTxt:
    coords.append(str(row[3]) + str(row[4]) + str(row[5]))
no_of_unique_coords = len(set(coords))

for i in range(no_of_unique_coords):
    obs_per_point = sum([1 for x in coords if x==list(set(coords))[i]])
    for obs in range(obs_per_point):
        myorder.append(coords.index(coords[i], i+obs*no_of_unique_coords))
gcpTxt = [gcpTxt[i] for i in myorder]


# print(myorder)


f = open(os.path.join(sys.path[0], "../gcp.txt"), "w")
print("# [img_name, pointX, pointY, xVal, yVal, zVal]",
file=f)
for row in gcpTxt:
    print(row[0],row[1],row[2],row[3],row[4],row[5], sep=' ', end='\n', file=f)
f.close()
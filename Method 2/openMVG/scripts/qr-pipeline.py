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
        print("ERROR: zbar was unable to detect QR code")
        continue

    paddingSize = 10
    image_cropped = image[max(0,y-paddingSize):y+h+paddingSize, max(0,x-paddingSize):x+w+paddingSize]

    # cv2.imshow("QR Scanner", image_cropped)
    # cv2.waitKey(0)
    det=cv2.QRCodeDetector()
    val, pts, st_code=det.detectAndDecode(image_cropped)

    if pts is None:
        print("ERROR: OpenCV was unable to detect QR code")
        continue

    corners = [[pts[0][0][0], pts[0][0][1]], [pts[0][1][0], pts[0][1][1]], [pts[0][3][0], pts[0][3][1]], [pts[0][2][0], pts[0][2][1]]]

    c1 = (-paddingSize+x+int(round(corners[0][0])),-paddingSize+y+int(round(corners[0][1])))
    c2 = (-paddingSize+x+int(round(corners[1][0])),-paddingSize+y+int(round(corners[1][1])))
    c3 = (-paddingSize+x+int(round(corners[2][0])),-paddingSize+y+int(round(corners[2][1])))


    cv2.circle(image, c1, 8, (255,255,255), -1)
    cv2.circle(image, c1, 6, (0,0,255), -1)

    cv2.circle(image, c2, 8, (255,255,255), -1)
    cv2.circle(image, c2, 6, (0,255,0), -1)

    cv2.circle(image, c3, 8, (255,255,255), -1)
    cv2.circle(image, c3, 6, (255,0,0), -1)

    write_img_path = ''.join([i[:len(i)-4], '-cornersDetected.jpg'])
    write_img_path = os.path.join(sys.path[0],write_img_path)
    cv2.imwrite(write_img_path, image)

    #           [X, Y, Z]
    c1_world = [0.0, 0.0, 0.0]
    c2_world = [0.457, 0.0, 0.0]
    c3_world = [0.0, 0.0, -0.457]
    #TODO: Make world coordinates encoded in QR code and extracted here

    
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

coords_sum = []
myorder = []
for row in gcpTxt:
    coords_sum.append(sum([float(x) for x in row[3:]]))
no_of_unique_coords = len(set(coords_sum))
for i in range(no_of_unique_coords):
    myorder.append(i)
    myorder.append(coords_sum.index(coords_sum[i], i+2))
gcpTxt = [gcpTxt[i] for i in myorder]

# print(myorder)


f = open(os.path.join(sys.path[0], "../gcp.txt"), "w")

for row in gcpTxt:
    print(row[0],row[1],row[2],row[3],row[4],row[5], sep=' ', end='\n', file=f)
f.close()
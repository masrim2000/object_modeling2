#!/usr/bin/python

import os
import sys

my_file = open(os.path.join(sys.path[0], "../gcp.txt"), "r")
point_list = my_file.read()
my_file.close()
# points = [img_name, pointX, pointY, xVal, yVal, zVal]

point_list = point_list.split("\n")
point_list = [x for x in point_list if not "#" in x]
point_list = [ele for ele in point_list if not str(ele)==""]

for p in range(len(point_list)):
        point_list[p] = point_list[p].split(" ")


if not os.path.exists(os.path.join(sys.path[0], "../sfm_data.json")):
    print("ERROR: json file not found.")

my_file = open(os.path.join(sys.path[0], "../sfm_data.json"), "r")
json = my_file.read()
my_file.close()

views = json
views = views.split("\"intrinsics\": [")[0]
views = views.split("},")
key_name = [[],[]]
for view in views:
    view = view.split("\"key\": ")
    view = view[1].split(",")
    key_name[0].append(view[0])

for view in views:
    view = view.split("\"filename\": \"")
    view = view[1].split("\"")
    key_name[1].append(view[0])


def column(matrix, i):
    return [row[i] for row in matrix]


f = open(os.path.join(sys.path[0], "temp.txt"), "w")

print("""\"control_points\": [\n""", sep='', end='', file=f)
coords_sum = []
for row in point_list:
    coords_sum.append(sum([float(x) for x in row[3:]]))

no_of_unique_coords = len(set(coords_sum))

for i in range(no_of_unique_coords):
    print("""        {
            \"key\": """, i, """,
            \"value\": {
                \"X\": [
                    """, point_list[i*2][3], """,
                    """, point_list[i*2][4], """,
                    """, point_list[i*2][5], """
                ],
                \"observations\": [\n""", sep='', end='', file=f)
    obs_per_point = sum([1 for x in coords_sum if x==list(set(coords_sum))[i]])
    for obs in range(obs_per_point):
        print("""                    {
                        "key": """, int(key_name[0][int(key_name[1].index(point_list[i*2+obs][0]))]), """,
                        "value": {
                            "id_feat": 0,
                            "x": [
                                """, point_list[i*2+obs][1], """,
                                """, point_list[i*2+obs][2], """
                            ]
                        }
                    }""", sep='', end='', file=f)
        if obs<obs_per_point-1:
        # if obs<(column(point_list,0).count(point_list[i][0])-1):
            print(",\n", sep='', end='', file=f)
        else:
            print("\n", sep='', end='', file=f)
    print("""                ]
            }
        }""", sep='', end='', file=f)
    if i<no_of_unique_coords-1:
        print(",\n", sep='', end='', file=f)
    else:
        print("\n    ]", sep='', end='', file=f)

f.close()
my_file = open(os.path.join(sys.path[0], "temp.txt"), "r")
pointsTxt = my_file.read()
my_file.close()
os.remove(os.path.join(sys.path[0], "temp.txt"))

my_file = open(os.path.join(sys.path[0], "../sfm_data_gcpAdded.json"), "w")
json = json.replace("\"control_points\": []", pointsTxt)
print(json, file=my_file)


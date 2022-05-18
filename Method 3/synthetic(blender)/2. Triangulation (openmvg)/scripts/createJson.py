import os
import sys
from scipy.spatial.transform import Rotation as R

def create_json():
    if os.path.exists(os.path.join(sys.path[0], "../sfm_data.json")):
        print("Json exists, not overwriting.")
        return

    my_file = open(os.path.join(sys.path[0], "../known/images.txt"), "r") # IMAGE_ID, QW, QX, $# reading the file
    image_list = my_file.read()
    my_file.close()

    my_file = open(os.path.join(sys.path[0], "../known/cameras.txt"), "r") # IMAGE_ID, QW, QX, $# reading the file
    camera_list = my_file.read()
    my_file.close()
    # image_list = image_list.split

    image_list = image_list.split("\n")
    image_list = [x for x in image_list if not "#" in x]
    image_list = [ele for ele in image_list if not str(ele)==""]

    for image in image_list:
        image = image.split(" ")


    camera_list = camera_list.split("\n")
    camera_list = [x for x in camera_list if not "#" in x]
    camera_list = [ele for ele in camera_list if not str(ele)==""]
    #camera = [str(1) for ele in camera_list if ele=='PINHOLE']

    for camera in camera_list:
        camera = camera.split(" ")
        camera = ['1' if ele=='PINHOLE' else ele for ele in camera]

    for i in range(len(camera_list)):
        camera_list[i] = camera_list[i].split(" ")


    if os.path.exists(os.path.join(sys.path[0], "../sfm_data.json")):
        os.remove(os.path.join(sys.path[0], "../sfm_data.json"))

    f = open(os.path.join(sys.path[0], "../sfm_data.json"), "w")


    print("""{
        "sfm_data_version": "0.3",
        "root_path": \"""", os.path.join(sys.path[0], "../images"),"""\",
        "views": [ 
        """, sep='', end='', file=f)



    id = 2147483649
    for i in range(len(image_list)):
        image_list[i] = image_list[i].split(" ")
        print("""         {
                "key": """ , int(image_list[i][0])-1, """,
                "value": {
                    "polymorphic_id": 1073741824,
                    "ptr_wrapper": {
                        "id": """, id, """,
                        "data": {
                            "local_path": "",
                            "filename": \"""", image_list[i][9], """\",
                            "width": """, camera_list[0][2], """,
                            "height": """, camera_list[0][3], """,
                            "id_view": """, int(image_list[i][0])-1, """,
                            "id_intrinsic": 0,
                            "id_pose": """, int(image_list[i][0])-1, """
                        }
                    }
                }
            }""", sep='', end='', file=f)
        id+=1
        if i<(len(image_list)-1):
            print(",\n", sep='', end='', file=f)
        else:
            print("\n", sep='', end='', file=f)

    print("""    ],
        "intrinsics": [
            {
                "key": 0,
                "value": {
                    "polymorphic_id": 2147483649,
                    "polymorphic_name": "pinhole",
                    "ptr_wrapper": {
                        "id": """, id, """,
                        "data": {
                            "width": """, camera_list[0][2], """,
                            "height": """, camera_list[0][3], """,
                            "focal_length": """, camera_list[0][4], """,
                            "principal_point": [
                                """, camera_list[0][6], """,
                                """, camera_list[0][7], """
                            ]
                        }
                    }
                }
            }
        ],
        "extrinsics": [""", sep='', end='', file=f)

    #print(image_list)
    for i in range(len(image_list)):
        r = R.from_quat([float(image_list[i][2]), float(image_list[i][3]), float(image_list[i][4]), float(image_list[i][1])])
        print("""
            {
                "key": """, int(image_list[i][0])-1, """,
                "value": {
                    "rotation": [\n"""
    "                [", r.as_matrix()[0][0], ", ", r.as_matrix()[0][1], ", ",r.as_matrix()[0][2], "], \n",
    "                [", r.as_matrix()[1][0], ", ", r.as_matrix()[1][1], ", ",r.as_matrix()[1][2], "], \n",
    "                [", r.as_matrix()[2][0], ", ", r.as_matrix()[2][1], ", ",r.as_matrix()[2][2], """]],
                    "center": [\n"""
    "                ", image_list[i][5], ",\n"
    "                ", image_list[i][6], ",\n"
    "                ", image_list[i][7], """]
                }
            }""", sep='', end='', file=f)
        if i<(len(image_list)-1):
            print(",", sep='', end='', file=f)
        else:
            print("""
    ],
        "structure": [],
        "control_points": []
    }""", sep='', end='', file=f)
    f.close()

if __name__ == "__main__":
    create_json()
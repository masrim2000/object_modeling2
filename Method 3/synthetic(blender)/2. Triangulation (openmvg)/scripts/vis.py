OPENMVG_SFM_BIN = "/usr/local/bin/"

import os
import sys
import subprocess
from scipy.spatial.transform import Rotation as R

def create_json():
    if os.path.exists(os.path.join(sys.path[0], "../sfm_data.json")):
        os.remove(os.path.join(sys.path[0], "../sfm_data.json"))
        # print("Json exists, not overwriting.")
        # return

    my_file = open(os.path.join(sys.path[0], "../known/images.txt"), "r") # IMAGE_ID, QW, QX, $# reading the file
    image_list = my_file.read()
    my_file.close()

    # image_list = image_list.split

    image_list = image_list.split("\n")
    image_list = [x for x in image_list if not "#" in x]
    image_list = [ele for ele in image_list if not str(ele)==""]

    for image in image_list:
        image = image.split(" ")

    camera_list = """# Camera list with one line of data per camera:
#   CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]
# Number of cameras: 1
1 PINHOLE 1920 1080 1866.6666 1575.0 960.0 540.0"""

    camera_list = camera_list.split("\n")
    camera_list = [x for x in camera_list if not "#" in x]
    camera_list = [ele for ele in camera_list if not str(ele)==""]
    #camera = [str(1) for ele in camera_list if ele=='PINHOLE']

    for camera in camera_list:
        camera = camera.split(" ")
        camera = ['1' if ele=='PINHOLE' else ele for ele in camera]

    for i in range(len(camera_list)):
        camera_list[i] = camera_list[i].split(" ")


    # if os.path.exists(os.path.join(sys.path[0], "sfm_data.json")):
        #os.remove(os.path.join(sys.path[0], "sfm_data.json"))

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
                            "width": 1920,
                            "height": 1080,
                            "focal_length": 1866.6666,
                            "principal_point": [
                                960.0,
                                540.0
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








#create json from images.txt
create_json()

#openMVG_main_openMVG2WebGL -i sfm_data.bin -o webgl/
pFeatures = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_openMVG2WebGL"),  "-i", "../sfm_data.json", "-o", "./vis/"] )
pFeatures.wait()


# Read in the file
with open('vis/index.html', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('#extension GL_EXT_frag_depth : enable', '')
filedata = filedata.replace('gl_FragDepthEXT = ( pos.z + 1.0 ) / 2.0;', '')
filedata = filedata.replace("""discard;
      gl_FragColor = vColor;""", """discard;
      gl_FragColor=vec4(1.0,1.0,gl_FragCoord.z,1.0);""")
with open('index.html', 'w') as file:
  file.write(filedata)
file.close()


# Replace the target string
with open(os.path.join(sys.path[0], 'vis/model/model.js'), 'r') as file :
  filedata = file.read()

filedata = filedata.replace("""modelPos=[
];""", 'modelPos=[-0.0062725 , 0.0540101 , 1.14015 , -0.433953 , -0.0615355 , 1.37557 , -0.433953 , -0.0615355 , 1.37557 , 0.0116169 , -0.135637 , 1.05206 ];')
filedata = filedata.replace("""modelNor=[
];""", 'modelNor=[-0.238352 , -0.0730215 , 0.96843 , -0.429386 , -0.185839 , 0.883794 , -0.429386 , -0.185839 , 0.883794 , -0.172013 , -0.332083 , 0.927433 ];')
filedata = filedata.replace("""modelCol=[
];""", 'modelCol=[41 , 58 , 39 , 56 , 110 , 170 , 56 , 110 , 170 , 43 , 57 , 83 ];')
with open(os.path.join(sys.path[0], 'vis/model/model.js'), 'w') as file:
  file.write(filedata)
file.close()

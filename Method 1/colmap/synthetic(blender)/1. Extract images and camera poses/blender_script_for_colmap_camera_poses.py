# Extracts images from blender scene cameras and
# writes camera poses to images.txt in colmap format

import bpy
import numpy as np
import math
import mathutils
import sys
import os

save_path = "C:/Users/masri/OneDrive/Documents/blender/sim14/"
fileName="alignment" # "images" or "alignment"

def get_position_details_json(object):
    world_matrix = object.matrix_world
    blender_to_colmap_rotation = np.diag([1,-1,-1])
    # Convert from blender world space to view space
    blender_world_translation, blender_world_rotation, blender_world_scale = world_matrix.decompose()
    blender_view_rotation = blender_world_rotation.to_matrix().transposed()
    blender_view_translation = -1.0 * blender_view_rotation @ blender_world_translation
    # Convert from blender view space to colmap view space
    colmap_view_rotation = blender_to_colmap_rotation @ blender_view_rotation
    colmap_view_rotation_quaternion = mathutils.Matrix(colmap_view_rotation).to_quaternion()
    colmap_view_translation = blender_to_colmap_rotation @ blender_view_translation
    return {
            "name" : object.name,
            "x_pos" : colmap_view_translation[0],
            "y_pos" : colmap_view_translation[1],
            "z_pos" : colmap_view_translation[2],
            "w_rotation" : colmap_view_rotation_quaternion.w,
            "x_rotation" : colmap_view_rotation_quaternion.x,
            "y_rotation" : colmap_view_rotation_quaternion.y,
            "z_rotation" : colmap_view_rotation_quaternion.z
        }

cameras_obj = [cam for cam in bpy.data.objects if cam.type == 'CAMERA']
images = []
for i in range(1, len(cameras_obj)+1):
    ob = bpy.data.objects[''.join(["Camera.", f"{i:03}"])]
    bpy.context.scene.camera = ob
    
    # Save images
    bpy.context.scene.camera = ob
    file = os.path.join(save_path, ob.name)
    bpy.context.scene.render.image_settings.file_format='JPEG'
    bpy.context.scene.render.filepath = file
    bpy.ops.render.render( write_still=True )
    
    # For images.txt
    image = " ".join([str(i),
    str(get_position_details_json(ob)["w_rotation"]),
    str(get_position_details_json(ob)["x_rotation"]),
    str(get_position_details_json(ob)["y_rotation"]),
    str(get_position_details_json(ob)["z_rotation"]),
    str(get_position_details_json(ob)["x_pos"]),
    str(get_position_details_json(ob)["y_pos"]),
    str(get_position_details_json(ob)["z_pos"]),
    "1",
    ''.join([get_position_details_json(ob)["name"],".jpg"])])
    
    # For alignment.txt
    if fileName=="alignment":
        image = " ".join([
        ''.join([ob.name,".jpg"]),
        str(ob.matrix_world[0][3]),
        str(ob.matrix_world[1][3]),
        str(ob.matrix_world[2][3])
        ])
        
    images.append(image)
    
    if fileName=="images":
        images.append("")
    

fileName = "".join([str(fileName),".txt"])
images = '\n'.join([elem for elem in images])
if os.path.exists(os.path.join(save_path, fileName)):
    os.remove(os.path.join(save_path, fileName))
file = os.path.join(save_path, fileName)
with open(file, "w") as f:
    f.write(str(images))
f.close()

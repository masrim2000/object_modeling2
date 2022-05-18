#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# This file is part of OpenMVG (Open Multiple View Geometry) C++ library.

# Python script to launch OpenMVG SfM tools on an image dataset
#
# usage : python tutorial_demo.py
#
# Indicate the openMVG binary directory
OPENMVG_SFM_BIN = "/usr/local/bin/"

# Indicate the openMVG camera sensor width directory
# CAMERA_SENSOR_WIDTH_DIRECTORY = "/home/masri/openMVG/src/software/SfM" + "/../../openMVG/exif/sensor_width_database"
CAMERA_SENSOR_WIDTH_DIRECTORY = "/opt/OpenMVG/src/openMVG/exif/sensor_width_database"

import os
import subprocess
# import sys

import createJson

createJson.create_json()


def get_parent_dir(directory):
    return os.path.dirname(directory)

os.chdir(os.path.dirname(os.path.abspath(__file__)))
base_dir = os.path.abspath("../")
input_eval_dir = os.path.abspath("../")
# Checkout an OpenMVG image dataset with Git
if not os.path.exists(input_eval_dir):
  pImageDataCheckout = subprocess.Popen([ "git", "clone", "https://github.com/openMVG/ImageDataset_SceauxCastle.git" ])
  pImageDataCheckout.wait()

output_eval_dir = os.path.join(input_eval_dir, "out")
input_eval_dir = os.path.join(input_eval_dir, "images")
if not os.path.exists(output_eval_dir):
  os.mkdir(output_eval_dir)

input_dir = input_eval_dir
output_dir = output_eval_dir
print ("Using input dir  : ", input_dir)
print ("      output_dir : ", output_dir)

matches_dir = os.path.join(output_dir, "matches")
camera_file_params = os.path.join(CAMERA_SENSOR_WIDTH_DIRECTORY, "sensor_width_camera_database.txt")

# Create the ouput/matches folder if not present
if not os.path.exists(matches_dir):
  os.mkdir(matches_dir)

print ("2. Compute features")
pFeatures = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeFeatures"),  "-i", base_dir+"/sfm_data.json", "-o", matches_dir, "-m", "SIFT", "-f" , "1", "-p", "HIGH"] )
pFeatures.wait()

print ("4. Structure from Known Poses (robust triangulation)")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),  "-i", base_dir+"/sfm_data.json", "-m", matches_dir, "-o", base_dir+"/sfm_scene.json"] )
pRecons.wait()

print ("5. Colorize Structure")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"),  "-i", base_dir+"/sfm_scene.json", "-o", os.path.join(base_dir,"result-sparse.ply")] )
pRecons.wait()

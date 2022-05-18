#!/bin/bash

# Downloads tf_bag utilities, installs it and runs 
# a python script to extract TF data to a .txt file
# containing poses in colmap's format.

# Install tf_bag
echo "1. Installing tf_bag..."
source /opt/ros/kinetic/setup.bash
mkdir -p ./catkin_ws/src
cd ./catkin_ws/src
git clone https://github.com/IFL-CAMP/tf_bag.git
cd ..
rosdep install -ryi --from-paths . --ignore-src
catkin_make
source ./devel/setup.bash
cd ..

# Run python script
echo "2. Running pose-extraction script..."
mkdir images
# Following command can be made dynamic by pasing the
# parameters when running this file and changing the
# following command to it to:
python scripts/pose-extractor.py $1 $2 $3 $4 $5
# where,
# $1: bag file
# $2: where to save the images
# $3: image topic
# $4: source (reference) TF frame
# $5: target TF frame
#python pose-extractor.py test.bag ./images /usb_cam/image_raw base_link camera_link_optical

source /opt/ros/kinetic/setup.bash
echo "Done!"

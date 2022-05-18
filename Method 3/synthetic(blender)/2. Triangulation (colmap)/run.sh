#!/bin/sh

# Starts with this script in directory containing the following:
#  |run.sh
#  \scripts\
#   --------|create_db.py
#   --------|db_utilities.py
#   \data\
#    -----\known\ (Input known poses and cameras)
#          ------|images.txt
#          ------|cameras.txt
#          ------|points3D.txt
#    -----\iamges\ (Input images)
#          ------|img1.jpg (or .png)
#          ------|img2.jpg (or .png)
#          ------|...
#          ------|imgN.jpg (or .png)

# create db
echo "1. Create DB..."
python3 scripts/create_db.py

# extract features
echo "2. Extract features..."
colmap feature_extractor --database_path ./data/database.db --image_path ./data/images --ImageReader.existing_camera_id 1

# match features
echo "3. Feature matching..."
colmap exhaustive_matcher --database_path ./data/database.db

# triangulation
echo "4. Triangulating points..."
mkdir ./data/triangulated
colmap point_triangulator \
--database_path ./data/database.db \
--image_path ./data/images \
--input_path ./data/known \
--output_path ./data/triangulated \
--Mapper.ba_refine_focal_length 0 \
--Mapper.ba_refine_extra_params 0
colmap model_converter --input_path ./data/triangulated/ --output_path ./data/triangulated/ --output_type TXT
rm ./data/triangulated/*.bin

# dense reconstruction
echo "5. Dense reconstruction"
mkdir ./data/dense
colmap image_undistorter --image_path ./data/images --input_path ./data/triangulated --output_path ./data/dense
colmap patch_match_stereo --workspace_path ./data/dense --PatchMatchStereo.max_image_size 1000 --PatchMatchStereo.cache_size 8
colmap stereo_fusion --workspace_path ./data/dense --output_path ./data/dense/fused.ply
cp ./data/dense/fused.ply ./result.ply
echo "Done!"

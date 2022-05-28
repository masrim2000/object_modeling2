#!/bin/bash

# Starts with this script in directory containing the following:
#  |run.sh
#   \data\
#    ------\known\
#           -------|images.txt (copy from step 1)
#           -------|cameras.txt (provide camera calibration in colmap format)
#    ------\images\ (Input images)
#           -------|img1.jpg (or .png)
#           -------|img2.jpg (or .png)
#           -------|...
#           -------|imgN.jpg (or .png)

# extract features
echo "1. Extract features..."
colmap feature_extractor --database_path ./data/database.db --image_path ./data/images

# match features
echo "2. Feature matching..."
colmap exhaustive_matcher --database_path ./data/database.db

# mapping
echo "3. Mapping sparse model..."
mkdir ./data/sparse
colmap mapper --database_path ./data/database.db --image_path ./data/images --output_path ./data/sparse

# alignment
echo "4. Transforming model to ROS coordinate system..."
mkdir ./data/sparse-aligned
colmap model_aligner --input_path ./data/sparse/0 --output_path ./data/sparse-aligned --ref_images_path ./data/alignment.txt --robust_alignment_max_error 3.0

# dense reconstruction
echo "5. Dense reconstruction"
mkdir ./data/dense
colmap image_undistorter --image_path ./data/images --input_path ./data/sparse-aligned --output_path ./data/dense
colmap patch_match_stereo --workspace_path ./data/dense --PatchMatchStereo.max_image_size 1000 --PatchMatchStereo.cache_size 8
colmap stereo_fusion --workspace_path ./data/dense --output_path ./data/dense/fused.ply
cp ./data/dense/fused.ply ./result.ply
echo "Done!"

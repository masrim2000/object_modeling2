#!/bin/bash

# Run openMVG to list images in json file and do sequential reconstruction
echo "1. Image Listing & Sequential Reconstruction..."
python3 scripts/SfM_openMVG.py

# convert output sfm_data.bin file to .json
echo "2. Converting Reconstruction Results to json..."
openMVG_main_ConvertSfM_DataFormat -i ./MVG/reconstruction_sequential/sfm_data.bin -o ./sfm_data.json

echo "3. Extracting QR Corners to gcp.txt..."
shopt -s expand_aliases
python3 scripts/qr-pipeline.py

echo "4. Embedding GCP's in json..."
python3 scripts/addGCP.py

echo "5. Registering Structure..."
ui_openMVG_control_points_registration ./sfm_data_gcpAdded.json ./sfm_data_gcpAdded_registered.json

echo "6. Generating Colorized Sparse ply..."
openMVG_main_ComputeSfM_DataColor -i ./sfm_data_gcpAdded_registered.json -o ./result-sparse.ply

echo "7. Exporting Structure to MVS..."
mkdir MVS
cd MVS
openMVG_main_openMVG2openMVS -i ../sfm_data_gcpAdded_registered.json -o ./registered.mvs

echo "8. Generating Dense ply..."
/usr/local/bin/OpenMVS/DensifyPointCloud registered.mvs -v 4
cp ./registered_dense.ply ../result-dense.ply
cd ..

echo "Done!"
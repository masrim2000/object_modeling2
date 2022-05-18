#!/bin/bash

# Run openMVG to list images in json file and do sequential reconstruction
echo "1. Sparse Triangulation..."
python3 scripts/SfM_openMVG.py

echo "2. Exporting Structure to MVS..."
mkdir MVS
cd MVS
openMVG_main_openMVG2openMVS -i ../sfm_scene.json -o ./triangulated.mvs

echo "3. Generating Dense ply..."
/usr/local/bin/OpenMVS/DensifyPointCloud triangulated.mvs -v 4
cp ./triangulated_dense.ply ../result-dense.ply
cd ..

echo "Done!"
replace data/images with your images
replace data/known/images.txt with your poses
replace data/known/cameras.txt with your intrincsics

run viz.py to generate WebGL visualization of camera poses

ensure path of binaries (OPENMVG_SFM_BIN) is correct in SfM_openMVG.py
run SfM_openMVG.py to triangulate images from known poses and generate point cloud (ply)

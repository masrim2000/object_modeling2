# object_modeling

Scripts for generating 3D models using colmap & openMVG.

The scale ambiguity and origin placement problems inherent to SfM are overcome using known camera poses from the eye-in-hand system extracted from ROS tf data. Alternatively, a paradigm for using a QR-code with known world location is presented (using a modified version of openMVG).

Blender simulation scenes are provided and used to demonstrate the proposed solutions.

The dependencies are described in BUILDING/docker-colmap-fresh-ubuntu16.txt and BUILDING/docker-openmvg-fresh-ubuntu16.txt. Alternatively, use the following commands to run a docker container containing all the dependencies to run the project (recommended):

***colmap***
```
docker pull masrim2000/colmap:latest
docker run -w /working -v c:\Users\masri\working:/working -e "TERM=xterm-256color" --gpus=all -e "DISPLAY=$((ping -n 1 host.docker.internal | findstr /c:Reply) -Split '[: ]' | findstr /c:.):0" -it masrim2000/colmap:latest
```

***openMVG & openMVS***
```
docker pull masrim2000/openmvgmvs:latest
docker run -w /working -v c:\Users\masri\working:/working -e "TERM=xterm-256color" --gpus=all -e "DISPLAY=$((ping -n 1 host.docker.internal | findstr /c:Reply) -Split '[: ]' | findstr /c:.):0" -it masrim2000/openmvgmvs:latest
```

***Note: For the project to run correctly, a specially modified version of openMVG must be used:
```
https://github.com/masrim2000/openMVG.git
```
***

# Method 1: Registration using known poses (using colmap)

Produces a dense colmap SfM model and registers it to the world coordinate system using the known camera poses. Does not require camera calibration but takes longer to compute than the other methods.


## Real data (ros bag)

### 1. Extract images and poses

This folder contains scripts to extract the images and camera poses and formats it such that its ready to be used in the next step (images.txt or alignment.txt).

Usage:
```
sudo chmod +x run.sh
./run.sh rita_bottle.bag images/ /usb_cam/image_raw base_link camera_link_optical
or generally,
./run.sh /path/to/bag/file.bag images/ /topic/image_raw tf_reference_frame_name tf_target_frame_name
```

### 2. Dense reconstruction and registration

Generates a dense 3D reconstruction and registers it using the formatted output from step 1.

Usage:
```
replace data/images with your images
replace data/alignment.txt with your poses for images (minimum 3 poses)
sudo chmod +x run.sh
*then run the script using command: ./run.sh
```


## Synthetic data (blender)
TODO


# Method 2: Registration using QR-code (using openMVG)

Produces a sparse openMVG SfM model, registers it to the world coordinate system using a QR code with known world coordinates then performs a dense reconstruction using openMVS. Does not require camera calibration but depends on good detection and localization of a QR-code in the images.

Usage:
```
replace images/ with your images
replace c*_world vaiables in qr-pipeline.py with world coordinates of qr code 3 corners (top-left, top-right, bottom-left). TODO: extract this info from QR-code

ensure path of binaries (OPENMVG_SFM_BIN) and sensor width dabatase is correct in SfM_openMVG.py
ensure X11 server is woking by making sure export DISPLAY is correct and works (can run guis)

then:
./run.sh
```


# Method 3: Triangulation

This method generates a dense 3D reconstruction by triangulating matched SIFT features given camera poses and calibration parameters. Requires accurate poses and camera calibration.

## Real data (ros bag)

TODO

### 1. Extract images and poses

This folder contains scripts to extract the images and camera poses then formats them such that they are ready to be used in the next step (images.txt).

Usage:
```
sudo chmod +x run.sh
./run.sh rita_bottle.bag images/ /usb_cam/image_raw base_link camera_link_optical
or generally,
./run.sh /path/to/bag/file.bag images/ /topic/image_raw tf_reference_frame_name tf_target_frame_name
```

### 2. Triangulation (colmap)

This script generates a dense 3D reconstruction by triangulating matched SIFT features given camera poses and calibration parameters. Requires accurate poses and camera calibration.

Usage:
```
replace data/images with your images
replace data/known/images.txt with your poses
replace data/known/cameras.txt with your intrincsics
sudo chmod +x run.sh
*then run the script using command: ./run.sh
```

### 2. Triangulation (openmvg)

This script generates a dense 3D reconstruction by triangulating matched SIFT features given camera poses and calibration parameters. Requires accurate poses and camera calibration.

Usage:
```
replace images/ with your images
replace known/images.txt with your poses
replace known/cameras.txt with your intrincsics
sudo chmod +x run.sh
*then run the script using command: ./run.sh
```


## Synthetic data (blender)

### 1. Extract camera parameters from blender

This folder contains an example blender scene with multiple cameras, as well as the needed scripts to render and export images, camera calibration and camera poses. The output is formatted to be used directly in the next step (images.txt and cameras.txt).

Usage:
```
Copy scripts to blender, change save location and run script.
```

### 2. Triangulation (colmap)

This script generates a dense 3D reconstruction by triangulating matched SIFT features given camera poses and calibration parameters. Requires accurate poses and camera calibration.

Usage:
```
replace data/images with your images
replace data/known/images.txt with your poses
replace data/known/cameras.txt with your intrincsics
sudo chmod +x run.sh
*then run the script using command: ./run.sh
```

### 2. Triangulation (openmvg)

This script generates a dense 3D reconstruction by triangulating matched SIFT features given camera poses and calibration parameters. Requires accurate poses and camera calibration.

Usage:
```
replace images/ with your images
replace known/images.txt with your poses
replace known/cameras.txt with your intrincsics
sudo chmod +x run.sh
*then run the script using command: ./run.sh
```





***
***This script assumes that colmap is installed and functional (i.e. the command "colmap gui" runs without errors and opens colmap gui).
This is challenging on some distributions as it requires cuda.
One easy way around this is to use colmap pre-installed with cuda enabled within a docker container. Given that cuda is enabled on the host machine and docker is installed and running, a functioning colmap container can be started using the following commands:**
```
docker pull masrim2000/colmap:latest
docker run -it -v c:\:/mnt/c --gpus=all masrim2000/colmap:latest
```
***
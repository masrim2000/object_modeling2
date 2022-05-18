# Visual 3D Reconstruction

Scripts for generating 3D models using colmap & OpenMVG.

The scale ambiguity and origin placement problems inherent to SfM are overcome using known camera poses from the eye-in-hand system extracted from ROS tf data. Alternatively, a paradigm for using a QR-code with known world location is presented (using a modified version of OpenMVG).

Blender simulation scenes are provided and used to demonstrate the proposed solutions.

# Dependencies
The dependencies are described in BUILDING/docker-colmap-fresh-ubuntu16.txt and BUILDING/docker-openmvg-fresh-ubuntu16.txt. Alternatively, use the following commands to run a docker container containing all the dependencies to run the project (recommended):

***colmap***
```
docker pull masrim2000/colmap:latest
docker run -w /mnt/c -v c:\:/mnt/c -e "TERM=xterm-256color" --gpus=all -e "DISPLAY=$((ping -n 1 host.docker.internal | findstr /c:Reply) -Split '[: ]' | findstr /c:.):0" -it masrim2000/colmap:latest
```

***OpenMVG & OpenMVS***
```
docker pull masrim2000/openmvgmvs:latest
docker run -w /mnt/c -v c:\:/mnt/c -e "TERM=xterm-256color" --gpus=all -e "DISPLAY=$((ping -n 1 host.docker.internal | findstr /c:Reply) -Split '[: ]' | findstr /c:.):0" -it masrim2000/openmvgmvs:latest
```

***Note: For the project to run correctly, a specially modified version of OpenMVG must be used:***
```
https://github.com/masrim2000/openmvg.git
```


# Method 1: Registration using known poses (using colmap)

Produces a dense colmap SfM model and registers it to the world coordinate system using the known camera poses. Does not require camera calibration but takes longer to compute than the other methods.

**Inputs**
* Set of images
* Camera centre translation

## Real data (ros bag)

### 1. Extract images and poses

This folder contains scripts to extract the images and camera poses and formats it such that its ready to be used in the next step (images.txt or alignment.txt).

Usage
```
sudo chmod +x run.sh
./run.sh rita_bottle.bag images/ /usb_cam/image_raw base_link camera_link_optical
or generally,
./run.sh /path/to/bag/file.bag images/ /topic/image_raw tf_reference_frame_name tf_target_frame_name
```

### 2. Dense reconstruction and registration

Generates a dense 3D reconstruction and registers it using the formatted output from step 1.

<p float="left">
<!-- <em>Scene & some cameras</em>
<img src="https://github.com/masrim2000/object_modeling2/blob/master/images/M2-synth-scene.jpg" /> -->
<em>47 input images</em>
<img src="https://github.com/masrim2000/object_modeling2/blob/master/images/M1-real-input.gif" />
</p>

Usage
```
replace data/images with your images
replace data/alignment.txt with your poses for images (minimum 3 poses)
sudo chmod +x run.sh
./run.sh
```
**Results**
<p>
<em>Using the camera poses extracted from the last step, aligning the 3D model using colmap yields the following dense pointcloud:</em>
<img src="https://github.com/masrim2000/object_modeling2/blob/master/images/M1-real-result.jpg" />
<em>Height measurement reads 22.465 cm, ground truth is 22.5 cm</em>
<img src="https://github.com/masrim2000/object_modeling2/blob/master/images/M1-real-result_measurement.jpg" />
</p>

## Synthetic data (blender)

### 1. Extract images and camera poses

This folder contains an example blender scene with multiple cameras, as well as the needed scripts to render and export images and camera poses. The output is formatted to be used directly in the next step (alignment.txt).

Usage
```
Copy scripts to blender, change save location, change fileName to "alignment" and run script.
```

### 2. Dense reconstruction and registration

Generates a dense 3D reconstruction and registers it using the formatted output from step 1.

<p float="left">
<!-- <em>Scene & some cameras</em>
<img src="https://github.com/masrim2000/object_modeling2/blob/master/images/M2-synth-scene.jpg" /> -->
<em>20 input images</em>
<img src="https://github.com/masrim2000/object_modeling2/blob/master/images/M1-synth-input.gif" />
</p>

Usage
```
replace data/images with your images
replace data/alignment.txt with your poses for images (minimum 3 poses)
sudo chmod +x run.sh
./run.sh
```
**Results**
<p>
<em>Using the camera poses extracted from the last step, aligning the 3D model using colmap yields the following dense pointcloud:</em>
<img src="https://github.com/masrim2000/object_modeling2/blob/master/images/M1-synth-result.jpg" />
<em>White: obtained dense pointcloud, Blue: ground-truth</em>
<img src="https://github.com/masrim2000/object_modeling2/blob/master/images/M1-synth-result_vs_ground_truth.jpg" />
</p>

# Method 2: Registration using QR-code (using OpenMVG)

Produces a sparse OpenMVG SfM model, registers it to the world coordinate system using a QR code with known world coordinates then performs a dense reconstruction using openMVS. Requires camera calibration. The QR-code should not be too distorted in the images (due to the camera angle) for good detection and corner localization.

**Inputs**
* Set of images containing a QR code encoding the world coordinate position of 3 of its corners
* Camera calibration

<p float="left">
<em>Scene & some cameras</em>
<img src="https://github.com/masrim2000/object_modeling2/blob/master/images/M2-synth-scene.jpg" />
<em>20 input images</em>
<img src="https://github.com/masrim2000/object_modeling2/blob/master/images/M2-synth-input.gif" />
<em>Automatic QR-code detection and corner localization</em>
<img src="https://github.com/masrim2000/object_modeling2/blob/master/images/M2-synth-detectedCorners.gif" />
<em>World coordinates extraction</em>
<img src="https://github.com/masrim2000/object_modeling2/blob/master/images/M2-synth-detectionExplanation.jpg" />
</p>

Usage
```
replace images/ with your images
ensure path of binaries (OPENMVG_SFM_BIN) and sensor width dabatase is correct in SfM_openMVG.py
ensure X11 server is woking by making sure export DISPLAY is correct and works (can run guis)
then:
./run.sh
```
**Results**
<p>
<em>Using the ground-control points extracted from the last step, aligning the 3D model using the customised version of openMVG yields the following dense pointcloud:</em>
<img src="https://github.com/masrim2000/object_modeling2/blob/master/images/M2-synth-result.jpg" />
<em>White: obtained dense pointcloud, Blue: ground-truth</em>
<img src="https://github.com/masrim2000/object_modeling2/blob/master/images/M2-synth-result_vs_ground_truth.jpg" />
</p>


# Method 3: Triangulation

This method generates a dense 3D reconstruction by triangulating matched SIFT features given camera poses and calibration parameters. Requires accurate poses and camera calibration.

**Inputs**
* Set of images
* Camera poses
* Camera calibration

## Real data (ros bag)

TODO

### 1. Extract images and poses

This folder contains scripts to extract the images and camera poses then formats them such that they are ready to be used in the next step (images.txt).

Usage
```
sudo chmod +x run.sh
./run.sh rita_bottle.bag images/ /usb_cam/image_raw base_link camera_link_optical
or generally,
./run.sh /path/to/bag/file.bag images/ /topic/image_raw tf_reference_frame_name tf_target_frame_name
```

### 2. Triangulation (colmap)

This script generates a dense 3D reconstruction by triangulating matched SIFT features given camera poses and calibration parameters. Requires accurate poses and camera calibration.

Usage
```
replace data/images with your images
replace data/known/images.txt with your poses
replace data/known/cameras.txt with your intrincsics
sudo chmod +x run.sh
./run.sh
```

### 2. Triangulation (OpenMVG)

This script generates a dense 3D reconstruction by triangulating matched SIFT features given camera poses and calibration parameters. Requires accurate poses and camera calibration.

Usage
```
replace images/ with your images
replace known/images.txt with your poses
replace known/cameras.txt with your intrincsics
sudo chmod +x run.sh
./run.sh
```


## Synthetic data (blender)

### 1. Extract camera parameters from blender

This folder contains an example blender scene with multiple cameras, as well as the needed scripts to render and export images, camera calibration and camera poses. The output is formatted to be used directly in the next step (images.txt and cameras.txt).

Usage
```
Copy scripts to blender, change save location and run script.
```

### 2. Triangulation (colmap)

This script generates a dense 3D reconstruction by triangulating matched SIFT features given camera poses and calibration parameters. Requires accurate poses and camera calibration.

Usage
```
replace data/images with your images
replace data/known/images.txt with your poses
replace data/known/cameras.txt with your intrincsics
sudo chmod +x run.sh
./run.sh
```

### 2. Triangulation (OpenMVG)

This script generates a dense 3D reconstruction by triangulating matched SIFT features given camera poses and calibration parameters. Requires accurate poses and camera calibration.

Usage
```
replace images/ with your images
replace known/images.txt with your poses
replace known/cameras.txt with your intrincsics
sudo chmod +x run.sh
./run.sh
```


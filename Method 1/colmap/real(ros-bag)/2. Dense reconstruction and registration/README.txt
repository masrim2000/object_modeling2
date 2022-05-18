Produces a dense colmap SfM model and registers it to ROS coordinate system using the known poses extracted from TF. Does not require camera calibration but takes longer to compute than method 2.

Example usage:
replace data/images with your images
replace data/alignment.txt with your poses for images (minimum 3 poses)
make the script executable by running the command: sudo chmod +x run.sh
then run the script using command: ./run.sh

This script assumes that colmap is installed and functional (i.e. the command "colmap gui" runs without errors and opens colmap gui).
This is challenging on some distributions as it requires cuda.
One easy way around this is to use colmap pre-installed with cuda enabled within a docker container. Given that cuda is enabled on the host machine and docker is insstalled and running, a functioning colmap container can be started using the following commands:
docker pull masrim2000/colmap:latest
docker run -it -v c:\:/mnt/c --gpus=all masrim2000/colmap:latest
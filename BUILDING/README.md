docker run -w /working -v c:\Users\masri\working:/working -e "TERM=xterm-256color" --gpus=all -e "DISPLAY=$((ping -n 1 host.docker.internal | findstr /c:Reply) -Split '[: ]' | findstr /c:.):0" -it masrim2000/colmap:latest

docker run -w /working -v c:\Users\masri\working:/working -e "TERM=xterm-256color" --gpus=all -e "DISPLAY=$((ping -n 1 host.docker.internal | findstr /c:Reply) -Split '[: ]' | findstr /c:.):0" -it masrim2000/openmvgmvs:latest

# Custom colmap docker image
To run a docker image containing colmap with all dependecies needed to run the project, use:
```
docker pull masrim2000/colmap:latest
docker run -it -v c:\:/mnt/c -e "TERM=xterm-256color" --gpus=all -e "DISPLAY=$((ping -n 1 host.docker.internal | findstr /c:Reply) -Split '[: ]' | findstr /c:.):0" masrim2000/colmap:latest
```


# Custom OpenMVG docker image
To run a docker image containing openMVG with all dependecies needed to run the project, use:
```
docker pull masrim2000/openmvgmvs:latest
docker run -it -v c:\:/mnt/c -e "TERM=xterm-256color" --gpus=all -e "DISPLAY=$((ping -n 1 host.docker.internal | findstr /c:Reply) -Split '[: ]' | findstr /c:.):0" masrim2000/openmvgmvs:latest
```


# From scratch
Otherwise, you can run a fresh ubuntu-16.04 and install all required dependencies from scratch using:
```
docker pull masrim2000/ubuntu16:1.0
docker run -it -v c:\:/mnt/c -e "TERM=xterm-256color" --gpus=all masrim2000/ubuntu16:1.0
```
then follow the instructions in docker-colmap-from-scratch.txt or docker-openmvg-from-scratch.txt to install all requirements manually.
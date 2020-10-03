# linux_nvidia_gpu_fan_control
This repository contains code for manual tuning of the fan curve of nvidia GPU's on Linux (testen on Ubuntu 18.04). I use this code for setting a custom fan curve on my 4x 1080Ti cards.

## Usage
1. Set the coolbits option to atleast 4 using: `$ nvidia-xconfig --cool-bits=value`
2. Download `gpu_fan_control.py` and adjust the fan curve to your liking. 
3. Start this program with: `python3 gpu_fan_control.py`. (Does not work with python2)
3. If you want, run this program automatically on startup. 

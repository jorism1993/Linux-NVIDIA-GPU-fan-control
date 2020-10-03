# linux_nvidia_gpu_fan_control
This repository contains code for manual tuning of the fan curve of nvidia GPU's on Linux (testen on Ubuntu 18.04). I use this code for setting a custom fan curve on my 4x 1080Ti cards.

## Usage
1. Set the coolbits option to atleast 4 using: `$ nvidia-xconfig --cool-bits=value`
2. Download `gpu_fan_control.py` and adjust the fan curve to your liking. 
3. Start this program with: `python3 gpu_fan_control.py`. (Does not work with python2)
3. If you want, run this program automatically on startup. 

## Troubleshooting
I also added my `xorg.conf` file from `/etc/X11`. You may find it usefull. 

### Upon reboot, my screen hangs on a black screen with a white cross shaped cursor
I encountered this problem too. I solved it by manually changing the values of the `BusID` in the `Device` sections of `xorg.conf`. I swapped the order of the PCI bus values. I needed to do this because in my system GPU 3 is the GPU closest to the CPU (looking at the motherboard), while GPU is the GPU furthest from the CPU. This did not reflect properly in the `xorg.conf` file. To edit this file, boot into save mode, change it, and then reboot.

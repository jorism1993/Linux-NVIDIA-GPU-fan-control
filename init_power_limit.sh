#!/bin/bash
#set persistence mode for all GPU
sudo nvidia-smi -pm 1

#Set gpu max power at 280W
sudo nvidia-smi -pl 280

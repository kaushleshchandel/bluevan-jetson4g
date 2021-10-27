#!/bin/bash

sudo apt-get install python3-pip

#pysimplegui
sudo -H pip3 install pySimpleGUI
#cv2
sudo -H pip3 install opencv-python

# install the dependencies (if not already onboard)
sudo apt-get install python3-pip libjpeg-dev libopenblas-dev libopenmpi-dev libomp-dev
sudo -H pip3 install future
sudo -H pip3 install -U --user wheel mock pillow
sudo -H pip3 install testresources

# upgrade setuptools 47.1.1 -> 57.4.0
sudo -H pip3 install --upgrade setuptools
sudo -H pip3 install Cython
# install gdown to download from Google drive
sudo -H pip3 install gdown
# download the wheel
gdown https://drive.google.com/uc?id=12UiREE6-o3BthhpjQxCKLtRg3u4ssPqb
# download TorchVision 0.10.0
gdown https://drive.google.com/uc?id=1tU6YlPjrP605j4z8PMnqwCSoP6sSC91Z

# install PyTorch 1.9.0
sudo -H pip3 install torch-1.9.0a0+gitd69c22d-cp36-cp36m-linux_aarch64.whl
# install TorchVision 0.10.0
sudo -H pip3 install torchvision-0.10.0a0+300a8a4-cp36-cp36m-linux_aarch64.whl

# clean up
rm torch-1.9.0a0+gitd69c22d-cp36-cp36m-linux_aarch64.whl
rm torchvision-0.10.0a0+300a8a4-cp36-cp36m-linux_aarch64.whl

# update protobuf (3.15.5) Install Caffe2
# $ sudo -H pip3 install -U protobuf

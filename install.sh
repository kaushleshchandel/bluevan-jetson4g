#!/bin/bash

if [ `whoami` != root ]; then
 echo "Please run with sudo!"
 exit 1
fi

WORKDIR="$(dirname "$0")"
cd $WORKDIR
 

# ------ Install files to the correct location -------
# ----------------------------------------------------

# Copy application
echo "Copy appdate"
mkdir -p "/usr/local/bin/bluevan/"
cp -v -r * "/usr/local/bin/bluevan"
chmod 755 -R "/usr/local/bin/bluevan"

cp bluevan.desktop ~/Desktop/
cp portrait.desktop ~/Desktop/
cp landscape.desktop ~/Desktop/

chmod 777 -R ~/Desktop/bluevan.desktop
chmod 777 -R ~/Desktop/landscape.desktop
chmod 777 -R ~/Desktop/portrait.desktop

#chmod +x ~/Desktop/bluevan.desktop
#chmod +x ~/Desktop/landscape.desktop
#chmod +x ~/Desktop/portrait.desktop

# Be sure normal users can't read our config file!
#chmod 600 $DESTPATH_APPDATA"settings.ini"

# --- Install the required distribution packages -----
# ----------------------------------------------------

#echo "Installing required distribution packages"
#apt-get update

if [ ! -e /usr/bin/pip3 ]; then
    apt-get -y install python3-pip
fi

#if [ ! -e /usr/bin/ffprobe ]; then
#    apt-get -y install ffmpeg
#fi

#if [ ! -e /usr/bin/omxplayer ]; then
#    apt-get -y install omxplayer
#fi

# --------- Install required python packages ---------
# ----------------------------------------------------

echo "Installing required python packages"
pip3 show evdev 1>/dev/null
if [ $? != 0 ]; then
    pip3 install evdev==1.2.0
fi

# ---------------- Systemd service -------------------
# ----------------------------------------------------

echo "Installing 'Bluevan' as a systemd service"
cp -v bluevan.service "/lib/systemd/system/"
systemctl daemon-reload
systemctl disable bluevan.service

# ---------------------- pipng -----------------------
# ----------------------------------------------------

#echo "Installing and building pipng"
#git clone https://github.com/raspicamplayer/pipng.git
#cd ./pipng/ && make && make install
#cd ../
#rm -rf pipng

# --------------------- Done! ------------------------
# ----------------------------------------------------

echo "Done!"
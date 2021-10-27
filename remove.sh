#!/bin/bash

if [ `whoami` != root ]; then
 echo "Please run with sudo!"
 exit 1
fi

echo "Stopping the 'Bluevan' service"
systemctl stop bluevan.service

WORKDIR="$(dirname "$0")"
cd $WORKDIR

# ------ Remove files and service correct location -------
# ----------------------------------------------------

# Copy application
echo "Removing Directories"
rm -r "/usr/local/share/bluevan/"
rm -r "/usr/local/bin/bluevan"
rm "~/Desktop/Bluevan"
rm "~/Desktop/Landscape"
rm "~/Portrait"

echo "Removing the 'Bluevan' service"
rm "/lib/systemd/system/bluevan.service"
systemctl daemon-reload

echo "Done!"
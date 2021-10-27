# bluevan-jetson4g
Bluevan for Jetson 4 GB

Install git client:

sudo apt-get update
sudo apt-get install git

git clone -b bluevan https://github.com/kaushleshchandel/bluevan-jetson4g.git

sudo sh ./bluevan-jetson4g/install.sh

sudo systemctl start bluevan.service
To automatically start bluevan at boot:

sudo systemctl enable bluevan.service
To stop bluevan:

sudo systemctl stop bluevan.service

or
Press "q" key.
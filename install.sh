
sudo apt update -y
sudo apt full-upgrade -y

sudo apt install libatlas-base-dev -y
sudo apt install libopenjp2-7 -y
sudo apt install libavcodec-dev -y
sudo apt install libavformat-dev -y
sudo apt install libswscale-dev -y
sudo apt install libgtk-3-dev -y
sudo apt install ffmpeg -y
sudo apt install python3-pip -y
sudo apt-get install zbar-tools -y
sudo apt-get install libhdf5-dev -y
sudo apt-get install libopenexr-dev -y

touch .env 

echo "
API_TOKEN=''

username='pi-robot'
password='qaqsqdqe'

" > .env

echo "
[Unit]
Description=My Python Script
After=multi-user.target

[Service]
Type=idle
User=pi
ExecStart=/usr/bin/python3 /home/pi/WebStream-TelegaBot/main.py

[Install]
WantedBy=multi-user.target

" > telega.service

sudo mv telega.service /etc/systemd/system/telega.service

sudo systemctl daemon-reload


pip3 install -r requirements.txt

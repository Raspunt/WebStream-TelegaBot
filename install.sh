
sudo apt update -y
sudo apt full-upgrade -y

sudo apt install libatlas-base-dev -y
sudo apt install libopenjp2-7 -y
sudo apt install libavcodec-dev -y
sudo apt install libavformat-dev -y
sudo apt install libswscale-dev -y
sudo apt install libgtk-3-dev -y
sudo apt install ffmpeg -y


touch .env 

echo "
    API_TOKEN=''

    username='pi-robot'
    password='qaqsqdqe'

" > .env

whoami

pip3 install -r requirements.txt

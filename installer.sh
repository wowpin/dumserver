sudo apt-get -y install python3
sudo apt-get -y install python3-pip
yes | sudo pip3 install commentjson
yes | sudo pip3 install websocket-client
sudo apt-get -y install git-core

sudo apt-get -y install nodejs
curl -L https://npmjs.org/install.sh | sudo sh

sudo npm install -g forever

git clone https://github.com/wowpin/dumserver.git

cd dumserver

sudo pip3 install -r requirements.txt
cd ..

cd dumserver/webclient
sudo npm install
cd ..

sudo python3 setup.py

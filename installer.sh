# Update and Upgrade your distro before installing anything
sudo apt update && yes | sudo apt upgrade

# Install Python3 and python-related packages
sudo apt-get -y install python3
sudo apt-get -y install python3-pip
yes | sudo pip3 install commentjson
yes | sudo pip3 install websocket-client
sudo apt-get -y install git-core

# Install Webclient pre-requisites - Node.js and NPM 
sudo apt-get -y install nodejs
curl -L https://npmjs.org/install.sh | sudo sh

# Install the server nanny used for restarting the Webclient should it terminate
sudo npm install -g forever

# Clone dumserver
git clone https://github.com/wowpin/dumserver.git

cd dumserver

# Set the home directory environment variable
echo "Setting DUM_HOME_DIR to:"
echo $PWD
sudo export DUM_HOME_DIR="$(pwd)"

# Install required Python modules
sudo pip3 install -r requirements.txt
cd ..

# Install required Node libraries
cd dumserver/webclient
sudo npm install
cd ..

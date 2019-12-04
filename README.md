![Dum!](docs/logo.png)
# dumserver ![Build](https://img.shields.io/badge/build-0.7.0-green.svg) ![Build](https://img.shields.io/badge/grapevine.haus-Supported-green.svg) ![Build](https://img.shields.io/badge/webclient-Supported-green.svg)
A modern Python MU* engine - re-imagined, actively developed and properly tracked.

## What is it?
DUM is a hobby project aiming to develop a feature-rich Python codebase for a sci-fi MUD style game. It is building on brillinat work by Mark Frimston, be sure to check out his Mud-Pi project (https://github.com/Frimkron/mud-pi).

## Try it out!
Go ahead an check out dumserver at http://dum.wowpin.eu

## Features
Head over to the [Wiki](http://dumengine.wikidot.com/dum-v0-1-feature-summary) for small breakdown of core features in the initial version 0.1. All changes/improvements/fixes since 0.1 are being documented in [CHANGELOG.md](CHANGELOG.md)

## Running the Server
```diff
- IMPORTANT - Python >= 3.6.7 is required (Ubuntu >= 18.04 LTS)!
```
1. Update your system with `sudo apt update && sudo apt upgrade`
2. Install the server with `sudo wget -O - https://raw.githubusercontent.com/wowpin/dumserver/master/installer.sh | bash`
3. CD into newly created `dumserver` directory.
3. Edit the webclient configuration file by typing `sudo nano webclient/config/default.js` Amend `socketUrl` amd `host` parameters (around lines 14 and 34) to match the external IP of the server you are running DUM on.
4. Run the server by typing `sudo ./start-server.sh`

You now should be able to connect to your server on `http://<your-server-ip>`

## What now?
I'd love to carry on developing this, it has been pretty fun so far. If anyone feels like they want to take it even further, feel free to get in touch.

## Get in touch
Bartek.Radwanski@gmail.com

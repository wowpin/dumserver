![Dum!](docs/logo.png)
# dumserver ![Build](https://img.shields.io/badge/build-0.5.2-green.svg)
A modern Python MU* engine - re-imagined, actively developed and properly tracked.

## What is it?
DUM is a hobby project aiming to develop a feature-rich Python codebase for a sci-fi MUD style game. It is building on brillinat work by Mark Frimston, be sure to check out his Mud-Pi project (https://github.com/Frimkron/mud-pi).

## Try it out!
**_Please note the webclient is currently down for maintenance, as I move it to a new hosting solution_**

Go ahead an check out the webclient at http://playdum.dynu.net:8000

You can also use a mud client of your choice if you wish - use connection details below:

```
Host: playdum.dynu.net
Port: 35123
```

If you're struggling to connect, it means I'm probably currently playing with the code etc. Try again in a few minutes and it should be up and running.

## Features
Head over to the [Wiki](http://dumengine.wikidot.com/dum-v0-1-feature-summary) for small breakdown of core features in the initial version 0.1. All changes/improvements/fixes since 0.1 are being documented in [CHANGELOG.md](CHANGELOG.md)

## Running the Server
Running your own instance is really straight-forward, instructions below tested on an Ubuntu instance.

1. `sudo apt-get update` and `sudo apt-get upgrade`
2. Install Python3: `sudo apt-get install python3`
3. Install Pip3: `sudo apt-get install python3-pip`
4. Install Commentjson: `sudo pip3 install commentjson`
5. Install git: `sudo apt-get install git-core`
6. Run `git clone https://github.com/wowpin/dumserver.git` to download Dumserver
7. CD into dumserver folder and run the server: `python3 dumserver.py`

You will be greeted by some boot-time messages - your server is up and running!

You now should be able to connect to your server on `<server IP/hostname>:35123`

## What now?
I'd love to carry on developing this, it has been pretty fun so far. If anyone feels like they want to take it even further, feel free to get in touch.

## Get in touch
Bartek.Radwanski@gmail.com

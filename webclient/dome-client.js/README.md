dome-client.js
==============

A socket.io / websocket based MOO & MUD client written in node.

## About

This is designed for games to provide to their players. Requires no flash. Requires no java plugin. Connections from end user's browser to the server occur via web socket to the node web application, which manages socket connections to the moo itself.

## Check it out online
You can see a version of this running that will connect to whatever game you want here: https://pubclient.sindome.org/

You are free to use that public client as much as you want! In fact, it's the default client for connecting to games on http://www.mudverse.com/

## Features

### Run a public client that connects to any game OR a private client that connects only to yours

It's really straight forward, just set the connectAnywhere option to true or false in the configuration! You can let your dome-client connect to any game, or you can lock it in to your own.

### No Software Required For Your Players

Works on a Mac, works on a PC. Use our Webclient without relying on Flash plugins or Java applets, those things are buggy and expose you to security risks. HTML 5 is available in all modern browsers, we already have all the technology we need. And since there isn't anything you need to install, you can log on from your office even if you can't install new software.

### Command Hints & Autocomplete for Players

Type a few characters and a Command Hints overlay will popup. Forgetting a command doesn't have to be so frustrating for experienced players and new players can find commands much easier than ever.

### Command History for Players

Some telnet clients remember your commands as you play. Unfortunately, as soon as you close the program, all that history is gone. This Webclient remembers the last 2000 commands you've entered. Browser crash? Power failure? No problem, we use HTML 5's local storage API and (once again) your modern web browser to keep those commands as long as you want us to.

### Lucid Logging. Full Color.

Every time you disconnect from the game, you're giving an option to save your experience as an HTML-based log file. This keeps the full context of what you said and what you witnessed. Every color we support is preserved exactly as it was.

### Staff Tested

Our Webclient isn't just built for players. We manage our game [Sindome](https://www.sindome.org) using the Webclient every day. One of the most powerful features for the staff is the Webclient's popup editor that lets us edit object properties and commands. This makes it much easier for us to draft notes on your roleplaying, review your history, write new features and understand whats going on in the inner workings of the game.

### Other Features:

* Connect to any MUD game that supports telnet/terminal connections
* Public / Private configuration, you can set the client to allow connections to any games (specified by user) or
* Lock your dome-client to a specific game
* Works on iPad / iPhone /Android well enough to check in when you're away from your computer
* Utilizes Socket.io for Websockets
* Full xterm256 color support
* Standard ANSI color support
* VMOO / Modal Style editor for code/properties/whatever
* Logging support - Download a Log of your session!
* Scroll Pausing/Resuming (double click the screen or hit the pause/resume scroll button)

## Installation

1. Clone the repo & run `npm install` to fetch the required node modules.
2. Run `sudo npm install -g forever` to install the server nanny, which should restart the client if it dies.
3. Edit `config/default.js` to include your game's information
  * **mode** [ *production* / *debug* ] - this mostly determines the amount of debug you will see
  * **port** - where this node app will run  
    	If you want to use a standard port like 80 or 443, you must run our `./run.sh` and `./debug.sh` scripts as root. Instead, you can run on a higher port and proxy through a web server like NGINX or Apache.
  * **socketUrl** - where your browser will look for the fancy websocket that node will serve. If you're running this on your own computer, set socketUrl to `'http://localhost:5555'`. This is the url of your dome-client.js server. 
    * **ip** - optional support if you have more than one ip
  * The MOO section controls where the client will connect. (this isn't designed to connect to a bunch of different games yet)
4. Start the server in debug mode: `./debug.sh` 

## Public / Private Dome Client
If you want your dome client to connect to ONLY your game, you should open default.js and edit the 'connectAnywhere' line to be:
```
'connectAnywhere': false,
```
If you're fine with users connecting with your dome-client to anywhere, just leave that option as it is.

## Local Modal Editing
This feature allows you to edit files locally in a modal window. The window has MOO Syntax highlighting and uses the [Ace editor](https://ace.c9.io/) which is excellent and can be extended pretty easily if you want to add things like VIM support or custom macros. The syntax for doing local modal editing is something like this:
```
@edit obj:verb
```
Or, for a property:
```
@edit obj.prop
```

If you would like to be able to edit code from the webclient in a modal window, you will need to modify your MOO to support this. The code / instructions for adding Local Editing can be found here: https://github.com/SevenEcks/lambda-moo-programming/blob/master/code/LocalEditing.md

### Command Hints Customization

The code comes bundled with a set of command hints that are common to many MOO's, but every game is different. If you want to customize the command hints it's easy. Just edit config/ac/player.txt and add/remove whatever command hints you want. When a player starts typing a command, the web client will pop up an overlay that shows possible commands, and lets them use up/down arrows + enter to autocomplete!

## SSL
SSL is supported, uncomment the config section, change the key,cert,ca according to your ssl key files.

## Additional Configuration
If you want to have multiple configuration files, you can do this by renaming default.js to UNIQUE_NAME.js else and then doing the following:
```bash
export NODE_ENV=UNIQUE_NAME
```

This will tell the app to use your alternate config file. Note that you should not include the file type in the NODE_ENV. 

## Forever
The instructions tell you to install forever. We actually prefer supervisor, but haven't updated this code to that yet.

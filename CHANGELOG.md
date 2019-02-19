### ![Current Version](https://img.shields.io/badge/%20-Current%20Version-green.svg) ![0.6.0](https://img.shields.io/badge/%20-0.6.0-lightgrey.svg) ![Publish Date](https://img.shields.io/badge/19%20FEB%202019-lightgrey.svg)
- **Grapevine.haus support!** Yay! Grapevine is a brilliant initiative, bringing a number of MUDs together by providing cross-game chat channels, player status and tells. DUM is heading towrds full Grapevine support, currently the following has been introduced:

***Default grapevine channels (gossip, testing, announcements)***
***Integration into existing DUM in-game channels***

It is now possible to subscribe, unsubscribe and send messages to '@grapevine' channels. 

Note: Concept of a channel location has been introduced. In this scenario, '@grapevine' is what we call a channel location. This is to signify that we can now use channels both local and external to DUM. To give a quick example - you can subscribe and send a message to a channel local to DUM by invoking the following:

`@subscribe MyTestChannel`
`/MyTestChannel Hello World!`

Lack of '@<channel location>' suffix in channel name means we are talking to a channel local to the server.

At the same time, you can now subscribe and send messages to one of Grapevine's channels by invoking:

`@subscribe gosspi@grapevine`
`/gossip@grapevine Hey there guys!`

From this moment you subscribe, you will receive any messages sent to Gossip channel on Grapevine by any other player in any other game. Keep in mind all three default gossip channels are supported - you can subscribe to them using following commands:

`@subscribe gossip@grapevine`
`@subscribe testing@grapevine`
`@subscribe announcements@grapevine`

Note: Remaining Grapevine functionality will follow soon (player tells, game status, players status etc.)

- **New AT command** `@config` - meant for controlling various admin and non admin aspects of the server/player experience via setting varius `config items`

- **New Config Item** `defaultchannel` - allows setting a default chat channel to post messages to. For example if a player is having a discussion in `announcements@grapevine`, it would quickly become inconvenient to type `/announcements@grapevine` every time he wishes to send a message in that channel. It is now possible to set a default channel using the following command:

`@config defaultchannel <channel>`

From now on, it is possible to send a message by simply typing:

`/ Hello World!`

Note: Mind the space which follows the forward slash! In the above example, lack of space would send message "World!" to channel [Hello]! You would likely not receive any output either (unless by coincidence you had earlier subscribed to Hello by invoking `@subscribe Hello`.

You can check which channel you have set as default and clear it at any time by typing the following:

`@config defaultchannel show`
`@config defaultchannel clear`

Note: 'show' and 'clear' are now reserved words and are no longer valid channel names - it is impossible to subscribe to them.
Note: Default channel is only valid per session - if a player log out and back in, he will have it's default channel cleared.

- Channels names are now case-insensitive
- Updates to in-game help

### ![Legacy Version](https://img.shields.io/badge/%20-Current%20Version-orange.svg) ![0.5.3](https://img.shields.io/badge/%20-0.5.3-lightgrey.svg) ![Publish Date](https://img.shields.io/badge/12%20FEB%202019-lightgrey.svg)
- **New regular command**: `tell <plyer> <message>` for sending tell message to online players wherever they are.
- **New AT command**: `@serverlog <show/clear>` for displaying or clearing the contents of dum runtime log (ServerLog in config.ini). It is an admin command and `permissionLevel=0` (set in players/<name>.player) is required to access it.  
- **Server Installer script**: To make it even easier to get Dum up and running, it is now possible to install it (along with all dependencies) on your machine with a one-liner command - see README.md
- **Webclient overhaul** - removed unused options, added custom graphics etc.
- Fixed .gitignore which would prevent the standard Guest account from being included in the repo.
- Modified the logging function to allow custom log locations. You can now control where server creates it's runtime log by modifying the ServerLog line in `config.ini`.

### ![Legacy Version](https://img.shields.io/badge/%20-Legacy%20Version-orange.svg) ![0.5.2](https://img.shields.io/badge/%20-0.5.2-lightgrey.svg) ![Publish Date](https://img.shields.io/badge/26%20JAN%202019-lightgrey.svg)
- Idle timer now also affects non-authenticated players (You will get disconnected due to inactivity while on the login screen/inside character creation wizard etc.)
- Text formatting fixes
- Unsubscribing from a SYSTEM channel will now give player a warning about potentially missing important game-wide info
- [Webclient](http://playdum.dynu.net "Webclient") has been migrated to a new, improved development environment.
- Small Webclient adaptations 

### ![Legacy Version](https://img.shields.io/badge/%20-Legacy%20Version-orange.svg) ![0.5.1](https://img.shields.io/badge/%20-0.5.1-lightgrey.svg) ![Publish Date](https://img.shields.io/badge/14%20JAN%202019-lightgrey.svg)
- `@who` bugfix - it no longer throws an exception when clients are connected, but not authenticated.
- Formatting changes in new player wizard

### ![Legacy Version](https://img.shields.io/badge/%20-Legacy%20Version-orange.svg) ![0.5](https://img.shields.io/badge/%20-0.5-lightgrey.svg) ![Publish Date](https://img.shields.io/badge/14%20JAN%202019-lightgrey.svg)
- **New player account creation wizard** - accessible by typing `new` on the login screen. It's currently simply asking for player name and password, then creates an account which can later be used to login with.
- **Implemented AT commands (@commands)** - meant to be OOC commands for configuration, server management etc. They are distinguished from standard in-character commands by an '@' prefix (hence the name AT commands).
- **Custom player chat channels have been implemented.** Players can `@subscribe` and `@unsubscribe` from them at any time. It is possible to subscribe and send messages to any valid channel name (alphanumeric, no spaces). Any other players which have subscribed to the same channel name will receive messages which are sent to it. Channel messages can be sent using the `/<channel name>` command. To illustrate:

You and your team can all subscribe to channel "fwends" by typing:

`@subscribe fwends`

Any player can send messages to any channel at any time by typing

`/fwends Hello there guys!`

If you decide you no longer want to receive messages from `fwends`, you can unsubscribe at any time by typing:

`@unsubscribe fwends`

There is a dedicated "system" channel used for server messages. All players are subscribed to it by default, although nothing would stop you if you wanted to unsubscribe by typing:

`@unsubscribe system`

- Webclient is now showing correct command auto-correct suggestions
- Added a `@quit` command for disconnecting from the game.
- Player will now be disconnected and removed from the game world when a webclient browser window is closed.	
- Cosmetic changes to `WHISPER`
- Added a `permissionLevel` attribute to player account. It is meant for controlling access to certain commands. By default all players can access all regular and @ commands, but you might want to lock some management commands to GMs only (highest `permissionLevel=0`) within the command implementation.
- Implemented a `@who` command, which shows all currently logged players to anyone with `permissionLevel=0` (highest GM permission level)
- Restricted dending messages to the SYSTEM channel - it now requires `permissionLevel=0`
- Implemented extended attributes for player accounts. Those are meant to be used for setting player flags during  quests/conversations etc. Currently `exAttribute0`, `exAttribute1` and `exAttribute2` are used for new player creation.




### ![Legacy Version](https://img.shields.io/badge/%20-Current%20Version-orange.svg) ![0.4](https://img.shields.io/badge/%20-0.4-lightgrey.svg) ![Publish Date](https://img.shields.io/badge/12%20JAN%202019-lightgrey.svg)
- **New Web Client!!** (such wow) - courtesy of https://github.com/JavaChilly/dome-client.js - now correctly handling ANSI colours.
- Cosmetic improvements to LOOK
- Text formatting improvements to adapt to new webclient. Improved readability and colour scheme.
- Included WHISPER command in the help page.
- Help page formatting fix.
- **Client connection now properly terminates when idle timer is reached** (rather just removing player from the game world)
- **Commands are now case-insensitive** - helps while using the webclient on a phone
- The 'Unknown command!' message now shows you what you have typed
- Improvements and fixes to escape character handling in cmsg.py

### ![Legacy Version](https://img.shields.io/badge/%20-Legacy%20Version-orange.svg) ![0.3.4](https://img.shields.io/badge/%20-0.3.4-lightgrey.svg) ![Publish Date](https://img.shields.io/badge/21%20DEC%202018-lightgrey.svg)
- Implemented WHISPER command allowing players to send private messages to players in the same room. Usage: `WHISPER <target> <message>`

### ![Legacy Version](https://img.shields.io/badge/%20-Legacy%20Version-orange.svg) ![0.3.3](https://img.shields.io/badge/%20-0.3.3-lightgrey.svg) ![Publish Date](https://img.shields.io/badge/19%20DEC%202018-lightgrey.svg)
- Added NPC ability to drop loot on death. It's controlled within NPC definition (npcs.json) by manipulating the "inv" attribute as per example below:

```
"inv" : [[1,19], [2,12]]
```

In the example above, NPC will drop two items - Item ID:1 with probability of 19% and Item ID:2 with probability of 12%

### ![Legacy Version](https://img.shields.io/badge/%20-Legacy%20Version-orange.svg) ![0.3.2](https://img.shields.io/badge/%20-0.3.2-lightgrey.svg) ![Publish Date](https://img.shields.io/badge/18%20DEC%202018-lightgrey.svg)
- Implemented custom events that can be injected directly from within the code. Function `addToScheduler()` now accepts a string eventID in addition to standard id number. E.g.

Rather than executing predefined event ID:3 on player ID:32 as per below: <br/>
`addToScheduler(3, 32, scheduler, eventDB)`<br/>

It is now possible to inject an event definition directly: <br/>
`addToScheduler('5|msg|Hello World!!', 32, scheduler, eventDB)` <br/>

The above will send `Hello World!!` message to player ID:32 in 5 seconds.

### ![Legacy Version](https://img.shields.io/badge/%20-Legacy%20Version-orange.svg) ![0.3.1](https://img.shields.io/badge/%20-0.3.1-lightgrey.svg) ![Publish Date](https://img.shields.io/badge/14%20DEC%202018-lightgrey.svg)
- Nasty bug causing server crashes in certain scenarios when looking at objects/players/npcs has been fixed. You don't want v0.3.
- Added a functionality to remove idling players from the game. Idle timer is counted from the moment player has sent his last command. When idle time reaches allowed idle time, player is removed from the world without actually disconnecting the client. It's be nice to have them physically disconnected, although it'll require some mudserver.py wizardry..

### ![Legacy Version](https://img.shields.io/badge/%20-Legacy%20Version-orange.svg) ![0.3](https://img.shields.io/badge/%20-0.3-lightgrey.svg) ![Publish Date](https://img.shields.io/badge/14%20DEC%202018-lightgrey.svg)
- Command source code has been separated into individual functions in commands.py
- Issue with multiple logins allowed for one character has been fixed - only one session per character is allowed now.

### ![Legacy Version](https://img.shields.io/badge/%20-Legacy%20Version-orange.svg) ![0.2.1](https://img.shields.io/badge/%20-0.2.1-lightgrey.svg) ![Publish Date](https://img.shields.io/badge/10%20DEC%202018-lightgrey.svg)
- Improvements to LOOK (e.g. 'LOOK item/player/NPC' will show their long_description/lookDescription parameter)
- lookDescription and long_description (for items) are defined within relevant JSON definition files.
- If a number of the same items are found in the room, one description will be shown, followed by "You can see X of those in the vicinity"

### ![Legacy Version](https://img.shields.io/badge/%20-Legacy%20Version-orange.svg) ![0.2](https://img.shields.io/badge/%20-0.2-lightgrey.svg) ![Publish Date](https://img.shields.io/badge/5%20DEC%202018-lightgrey.svg)
- Brief summary of features implemented in 0.1 available at http://dumengine.wikidot.com/dum-v0-1-feature-summary
- MySQL database instance is no longer required. All player, npc, item, room and actor information is stored in JSON files.
- In-game event scheduler has been introduced allowing events to be scheduled for execution at set times. E.g "Send message "ABC" to player X in 5 seconds and make him unable to walk and talk for 30 seconds.".
- Improved cmsg.py addressing efficiency concerns.
- Portions of repetitive code re-written into functions in functions.py
- Fixed server crashes in certain 'take' and 'drop' scenarios
- Introduction of Commentjson module to handle Python (#) and Java (//) style comments inside .json and .player files
- Introduction of reserved evens 1, 2 and 3 - those are executed on server boot after all assets have been loaded. Those are currently used for spawning items, environment actors and NPCs (populating the world)
- Room definitions have been moved out of dumserver.py and into rooms.json.
- Player Prefix has been introduced. As an example - when a player dies, his/her name will be prefixed with [Recovering] for a set time when other players look at him/her.
- Introduced a random factor for NPC and Environment Actor chatter. Any NPC or Actor will send a message every (talkDelay + rnd(randomFactor)) seconds.
- NPCs and Actors will now not repeat the same phrase twice in a row.
- Implemented a 'webclienttest' command to test the color webclient is currently capable of displaying.


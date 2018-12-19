### ![In Development](https://img.shields.io/badge/%20-in%20development-blue.svg)
- INSPECT (showing detailed PC/NPC character sheet. Amount of detail depending on player's perception)
- WHISPER - whispering to players in the same room
- MESSAGE - in game player to player messages (think 'tell')
- Implementation of the CHECK STATS logic for viewing player's own character sheet. Perhaps a different command name?
- Script-able NPC conversation trees (?) - Research needed
- Dynamic room exits / run-time remapping exits to alternative destinations (perhaps via sutom events?)

### ![Current Version](https://img.shields.io/badge/%20-Current%20Version-green.svg) ![0.3.3](https://img.shields.io/badge/%20-0.3.3-lightgrey.svg) ![Publish Date](https://img.shields.io/badge/19%20DEC%202018-lightgrey.svg)
- Added NPC ability to drop loot on death. It's controlled within NPC definition (npcs.json) by manipulating the "inv" attribute as per example below:
<br/>
```
"inv" : [[1,19], [2,12]]
```
<br/>
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


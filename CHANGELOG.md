## 5-DEC-2018
- MySQL database instance is no longer required. All player, npc, item, room and actor information is stored in JSON files.
- In-game event scheduler has been introduced allowing events to bescheduled for execution at set times. E.g "Send message "ABC" to player X in 5 seconds and make him unable to walk and talk for 30 seconds.".
- Improved cmsg.py addressing efficiency concerns.
- Portions of repetitive code re-written into functions in functions.py
- Fixed server crashes in certain 'take' and 'drop' scenarios
- Introduction of Commentjson module to handle Python (#) and Java (//) style comments inside .json and .player files
- Introduction of reserved evens 1, 2 and 3 - those are executed on server boot after all assets ahave been loaded. Those are currently used for spawning items, environment actors and NPCs (populating the world)
- Room definitions have been moved out of dumserver.py and into rooms.json.
- Player Prefix has been introduced. As an example - when a player dies, his/her name will be prefixed with [Recovering] for a set time when other players look at him/her.
- Introduced a random factor for NPC and Environment Actor chatter. Any NPC or Actor will send a message every (talkDelay + rnd(randomFactor)) seconds.
- NPCs and Actors will now not repeat the same phrase twice in a row.
- Implemented a 'webclienttest' command to test the color webclient is currently capable of displaying.


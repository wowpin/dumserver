## Dum Server!
## v0.4

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from cmsg import cmsg

from functions import getFreeKey
from functions import log
from functions import saveState
from functions import addToScheduler
from functions import loadPlayer
from functions import savePlayer
from functions import loadPlayersDB

from events import evaluateEvent

from commands import runCommand

import time

#import gossip
#from gossip import gsocket

# import the MUD server class
from mudserver import MudServer

# import random generator library
from random import randint

# import the deepcopy library
from copy import deepcopy

# import config parser
import configparser

# import the json parser
import commentjson

# import glob module
import glob

log("", "Server Boot")

log("", "Loading configuration file")

# load the configuration file
Config = configparser.ConfigParser()
Config.read('config.ini')

# example of config file usage
# print(str(Config.get('Database', 'Hostname')))

# Declare rooms dictionary
rooms = {}

# Declare NPC database dict
npcsDB = {}

# Declare NPCs dictionary
npcs = {}

# Declare NPCs master (template) dict
npcsTemplate = {}

# Declare env dict
env = {}

# Declare env database dict
envDB = {}

# Declare fights dict
fights = {}

# Declare corpses dict
corpses = {}

# Declare items dict
itemsDB = {}

# Declare itemsInWorld dict
itemsInWorld = {}

# Declare scriptedEventsDB list
scriptedEventsDB = []

# Declare eventSchedule dict
eventSchedule = {}

# Specify allowe player idle time
allowedPlayerIdle = int(Config.get('World', 'IdleTimeBeforeDisconnect'))


# Loading rooms
with open(str(Config.get('Rooms', 'Definition')), "r") as read_file:
	rooms = commentjson.load(read_file)
	
log("Rooms loaded: " + str(len(rooms)), "info")

# Loading environment actors
with open(str(Config.get('Actors', 'Definition')), "r") as read_file:
	envDB = commentjson.load(read_file)

output_dict = {}
for key, value in envDB.items():
	output_dict[int(key)] = value

envDB = output_dict

for k in envDB:
	envDB[k]['vocabulary'] = envDB[k]['vocabulary'].split('|')
	for v in envDB[k]:
		if not(v == "name" or \
		v == "room" or \
		v == "vocabulary"):
			envDB[k][v] = int(envDB[k][v])


log("Environment Actors loaded: " + str(len(envDB)), "info")

# List ENV dictionary for debugging purposes
# print(env)
# print("Test:")
# for x in env:
	# print (x)
	# for y in env[x]:
		# print (y,':',env[x][y])
		
# Loading NPCs
with open(str(Config.get('NPCs', 'Definition')), "r") as read_file:
	npcsDB = commentjson.load(read_file)

output_dict = {}
for key, value in npcsDB.items():
	output_dict[int(key)] = value

npcsDB = output_dict

for k in npcsDB:
	npcsDB[k]['lastRoom'] = None
	npcsDB[k]['whenDied'] = None
	npcsDB[k]['vocabulary'] = npcsDB[k]['vocabulary'].split('|')
	for v in npcsDB[k]:
		if not(v == "name" or \
		v == "room" or \
		v == "inv" or \
		v == "vocabulary" or \
		v == "lookDescription" or \
		v == "lastRoom" or \
		v == "loot" or \
		v == "whenDied"):
			npcsDB[k][v] = int(npcsDB[k][v])

log("NPCs loaded: " + str(len(npcsDB)), "info")

# List NPC dictionary for debugging purposes
#print(" ")
#print("LIVE:")
#print(npcsDB)
#print(" ")
#for x in npcsDB:
	#print (x)
	#for y in npcsDB[x]:
		#print (y,':',npcsDB[x][y])

# Loading Items
with open(str(Config.get('Items', 'Definition')), "r") as read_file:
	itemsDB = commentjson.load(read_file)

output_dict = {}
for key, value in itemsDB.items():
	output_dict[int(key)] = value

itemsDB = output_dict

for k in itemsDB:
	for v in itemsDB[k]:
		if not(v == "name" or \
		v == "long_description" or \
		v == "short_description" or \
		v == "article"):
			itemsDB[k][v] = int(itemsDB[k][v])

log("Items loaded: " + str(len(itemsDB)), "info")

# List items for debugging purposes
# print("TEST:")
# for x in itemsDB:
	# print (x)
	# for y in itemsDB[x]:
		# print(y,':',itemsDB[x][y])
# print(itemsDB)

# Load scripted event declarations from disk
files=glob.glob(str(Config.get('Events', 'Location')) + "/*.event")
counter = 0
for file in files:
	counter += 1
	f=open(file, 'r')
	#print(file)
	lines = [line.rstrip() for line in f.readlines()[2:]]
	for l in lines[1:]:
		if len(l) > 0:
			scriptedEventsDB.append([lines[0]] + l.split('|'))
	#print(lines)
	f.close()

log("Scripted Events loaded: " + str(counter), "info")

# Load registered players DB
playersDB = loadPlayersDB()
log("Registered player accounts loaded: " + str(len(playersDB)), "info")

# Execute Reserved Event 1 and 2
# Using -1 for target since no players can be targeted with an event at this time
log("Executing boot time events", "info")
addToScheduler(1, -1, eventSchedule, scriptedEventsDB)
addToScheduler(2, -1, eventSchedule, scriptedEventsDB)
addToScheduler(3, -1, eventSchedule, scriptedEventsDB)

# Declare number of seconds to elapse between State Saves
# A State Save takes values held in memory and updates the database
# at set intervals to achieve player state persistence
stateSaveInterval = int(Config.get('World', 'StateSaveInterval'))
log("State Save interval: " + str(stateSaveInterval) + " seconds", "info")

# Set last state save to 'now' on server boot
lastStateSave = int(time.time())

# Deepcopy npcs fetched from a database into a master template
npcsTemplate = deepcopy(npcs)

# List items in world for debugging purposes
# for x in itemsInWorld:
	# print (x)
	# for y in itemsInWorld[x]:
		# print(y,':',itemsInWorld[x][y])
		
# stores the players in the game
players = {}

# start the server
mud = MudServer()


	

# main game loop. We loop forever (i.e. until the program is terminated)
while True:
	# print(type(gsocket.outbound_frame_buffer))
	# Gossip test
	#inbound = gsocket.handle_read()
	#if inbound != None:
		#print(type(inbound))
		#print(inbound)
	#gsocket.handle_write()

	#print(type(readtest))
	#print(readtest)
	# pause for 1/5 of a second on each loop, so that we don't constantly
	# use 100% CPU time
	time.sleep(0.1)
	# print(eventSchedule)

	# 'update' must be called in the loop to keep the game running and give
	# us up-to-date information
	mud.update()

	# Check if State Save is due and execute it if required
	now = int(time.time())
	if int(now >= lastStateSave + stateSaveInterval):		
		# State Save logic Start
		for (pid, pl) in list(players.items()):
			if players[pid]['authenticated'] is not None:
				# print('Saving' + players[pid]['name'])
				saveState(players[pid], playersDB)
				playersDB = loadPlayersDB()
		# State Save logic End
		lastStateSave = now

	# Handle Player Deaths
	for (pid, pl) in list(players.items()):
		if players[pid]['authenticated'] == True:
			if players[pid]['hp'] <= 0:
				# Create player's corpse in the room
				corpses[len(corpses)] = { 'room': players[pid]['room'], 'name': str(players[pid]['name'] + '`s corpse'), 'inv': players[pid]['inv'], 'died': int(time.time()), 'TTL': players[pid]['corpseTTL'], 'owner': 1 }
				# Clear player's inventory, it stays on the corpse
				# This is bugged, causing errors when picking up things after death
				# players[pid]['inv'] = ''
				players[pid]['isInCombat'] = 0
				players[pid]['lastRoom'] = players[pid]['room']
				players[pid]['room'] = '$rid=666$'
				fightsCopy = deepcopy(fights)
				for (fight, pl) in fightsCopy.items():
					if fightsCopy[fight]['s1id'] == pid or fightsCopy[fight]['s2id'] == pid:
						del fights[fight]
				for (pid2, pl) in list(players.items()):
					if players[pid2]['authenticated'] is not None \
						and players[pid2]['room'] == players[pid]['lastRoom'] \
						and players[pid2]['name'] != players[pid]['name']:
						mud.send_message(pid2, '<u><f32>{}<r> <f124>has been killed.'.format(players[pid]['name']))
				players[pid]['lastRoom'] = None
				mud.send_message(pid, '<b88><f158>Oh dear! You have died!')

				# Add Player Death event (ID:666) to eventSchedule
				addToScheduler(666, pid, eventSchedule, scriptedEventsDB)

				players[pid]['hp'] = 4

	# Handle Fights
	for (fid, pl) in list(fights.items()):
		# PC -> PC
		if fights[fid]['s1type'] == 'pc' and fights[fid]['s2type'] == 'pc':
			if players[fights[fid]['s1id']]['room'] == players[fights[fid]['s2id']]['room']:
				if int(time.time()) >= players[fights[fid]['s1id']]['lastCombatAction'] + 10 - players[fights[fid]['s1id']]['agi']:
					if players[fights[fid]['s2id']]['isAttackable'] == 1:
						players[fights[fid]['s1id']]['isInCombat'] = 1
						players[fights[fid]['s2id']]['isInCombat'] = 1
						# Do damage to the PC here
						if randint(0, 1) == 1:
							modifier = randint(0, 10)
							if players[fights[fid]['s1id']]['hp'] > 0:
								players[fights[fid]['s2id']]['hp'] = players[fights[fid]['s2id']]['hp'] - (players[fights[fid]['s1id']]['str'] + modifier)
								players[fights[fid]['s1id']]['lastCombatAction'] = int(time.time())
								mud.send_message(fights[fid]['s1id'], 'You manage to hit <f32><u>' + players[fights[fid]['s2id']]['name'] + '<r> for <f0><b2>' + str(players[fights[fid]['s1id']]['str'] + modifier) + '<r> points of damage.')
								mud.send_message(fights[fid]['s2id'], '<f32>' + players[fights[fid]['s1id']]['name'] + '<r> has managed to hit you for <f15><b88>' + str(players[fights[fid]['s1id']]['str'] + modifier) + '<r> points of damage.')

						else:
							players[fights[fid]['s1id']]['lastCombatAction'] = int(time.time())
							mud.send_message(fights[fid]['s1id'], 'You miss trying to hit <f32><u>' + players[fights[fid]['s2id']]['name'] + '')
							mud.send_message(fights[fid]['s2id'], '<f32><u>' + players[fights[fid]['s1id']]['name'] + '<r> missed while trying to hit you!')
					else:
						mud.send_message(fights[fid]['s1id'], '<f225>Suddnely you stop. It wouldn`t be a good idea to attack <f32>' + players[fights[fid]['s2id']]['name'] + ' at this time.')
						fightsCopy = deepcopy(fights)
						for (fight, pl) in fightsCopy.items():
							if fightsCopy[fight]['s1id'] == fights[fid]['s1id'] and fightsCopy[fight]['s2id'] == fights[fid]['s2id']:
								del fights[fight]
		# PC -> NPC
		elif fights[fid]['s1type'] == 'pc' and fights[fid]['s2type'] == 'npc':
			if players[fights[fid]['s1id']]['room'] == npcs[fights[fid]['s2id']]['room']:
				if int(time.time()) >= players[fights[fid]['s1id']]['lastCombatAction'] + 10 - players[fights[fid]['s1id']]['agi']:
					if npcs[fights[fid]['s2id']]['isAttackable'] == 1:
						players[fights[fid]['s1id']]['isInCombat'] = 1
						npcs[fights[fid]['s2id']]['isInCombat'] = 1
						# Do damage to the NPC here
						if randint(0, 1) == 1:
							modifier = randint(0, 10)
							if players[fights[fid]['s1id']]['hp'] > 0:
								npcs[fights[fid]['s2id']]['hp'] = npcs[fights[fid]['s2id']]['hp'] - (players[fights[fid]['s1id']]['str'] + modifier)
								players[fights[fid]['s1id']]['lastCombatAction'] = int(time.time())
								mud.send_message(fights[fid]['s1id'], 'You manage to hit <f220>' + npcs[fights[fid]['s2id']]['name'] + '<r> for <b2><f0>' + str(players[fights[fid]['s1id']]['str'] + modifier)  + '<r> points of damage')

						else:
							players[fights[fid]['s1id']]['lastCombatAction'] = int(time.time())
							mud.send_message(fights[fid]['s1id'], 'You miss <f220>' + npcs[fights[fid]['s2id']]['name'] + '<r> completely!')
					else:
						mud.send_message(fights[fid]['s1id'], '<f225>Suddenly you stop. It wouldn`t be a good idea to attack <u><f21>' + npcs[fights[fid]['s2id']]['name'] + '<r> at this time.')
						fightsCopy = deepcopy(fights)
						for (fight, pl) in fightsCopy.items():
							if fightsCopy[fight]['s1id'] == fights[fid]['s1id'] and fightsCopy[fight]['s2id'] == fights[fid]['s2id']:
								del fights[fight]
		# NPC -> PC
		elif fights[fid]['s1type'] == 'npc' and fights[fid]['s2type'] == 'pc':
			if npcs[fights[fid]['s1id']]['room'] == players[fights[fid]['s2id']]['room']:
				if int(time.time()) >= npcs[fights[fid]['s1id']]['lastCombatAction'] + 10 - npcs[fights[fid]['s1id']]['agi']:
					npcs[fights[fid]['s1id']]['isInCombat'] = 1
					players[fights[fid]['s2id']]['isInCombat'] = 1
					# Do the damage to PC here
					if randint(0, 1) == 1:
						modifier = randint(0, 10)
						if npcs[fights[fid]['s1id']]['hp'] > 0:
							players[fights[fid]['s2id']]['hp'] = players[fights[fid]['s2id']]['hp'] - (npcs[fights[fid]['s1id']]['str'] + modifier)
							npcs[fights[fid]['s1id']]['lastCombatAction'] = int(time.time())
							mud.send_message(fights[fid]['s2id'], '<f220>' + npcs[fights[fid]['s1id']]['name'] + '<r> has managed to hit you for <f15><b88>' + str(npcs[fights[fid]['s1id']]['str'] + modifier) + '<r> points of damage.')
					else:
						npcs[fights[fid]['s1id']]['lastCombatAction'] = int(time.time())
						mud.send_message(fights[fid]['s2id'], '<f220>' + npcs[fights[fid]['s1id']]['name'] + '<r> has missed you completely!')
		elif fights[fid]['s1type'] == 'npc' and fights[fid]['s2type'] == 'npc':
			test = 1
			# NPC -> NPC

	# Iterate through NPCs, check if its time to talk, then check if anyone is attacking it
	for (nid, pl) in list(npcs.items()):
		# Check if any player is in the same room, then send a random message to them
		now = int(time.time())
		if now > npcs[nid]['timeTalked'] + npcs[nid]['talkDelay'] + npcs[nid]['randomizer']:
			rnd = randint(0, len(npcs[nid]['vocabulary']) - 1)
			while rnd is npcs[nid]['lastSaid']:
				rnd = randint(0, len(npcs[nid]['vocabulary']) - 1)
			for (pid, pl) in list(players.items()):
				if npcs[nid]['room'] == players[pid]['room']:
					if len(npcs[nid]['vocabulary']) > 1:
						#mud.send_message(pid, npcs[nid]['vocabulary'][rnd])
						msg = '<f220>' + npcs[nid]['name'] + '<r> says: <f86>' + npcs[nid]['vocabulary'][rnd]
						mud.send_message(pid, msg)
						npcs[nid]['randomizer'] = randint(0, npcs[nid]['randomFactor'])
						npcs[nid]['lastSaid'] = rnd
					else:
						#mud.send_message(pid, npcs[nid]['vocabulary'][0])
						msg = '<f220>' + npcs[nid]['name'] + '<r> says: <f86>' + npcs[nid]['vocabulary'][0]
						mud.send_message(pid, msg)
						npcs[nid]['randomizer'] = randint(0, npcs[nid]['randomFactor'])
			npcs[nid]['timeTalked'] =  now

		# Iterate through fights and see if anyone is attacking an NPC - if so, attack him too if not in combat (TODO: and isAggressive = true)
		for (fid, pl) in list(fights.items()):
			if fights[fid]['s2id'] == nid and npcs[fights[fid]['s2id']]['isInCombat'] == 1 and fights[fid]['s1type'] == 'pc' and fights[fid]['retaliated'] == 0:
				# print('player is attacking npc')
				# BETA: set las combat action to now when attacking a player
				npcs[fights[fid]['s2id']]['lastCombatAction'] = int(time.time())
				fights[fid]['retaliated'] = 1
				npcs[fights[fid]['s2id']]['isInCombat'] = 1
				fights[len(fights)] = { 's1': npcs[fights[fid]['s2id']]['name'], 's2': players[fights[fid]['s1id']]['name'], 's1id': nid, 's2id': fights[fid]['s1id'], 's1type': 'npc', 's2type': 'pc', 'retaliated': 1 }
			elif fights[fid]['s2id'] == nid and npcs[fights[fid]['s2id']]['isInCombat'] == 1 and fights[fid]['s1type'] == 'npc' and fights[fid]['retaliated'] == 0:
				# print('npc is attacking npc')
				# BETA: set las combat action to now when attacking a player
				npcs[fights[fid]['s2id']]['lastCombatAction'] = int(time.time())
				fights[fid]['retaliated'] = 1
				npcs[fights[fid]['s2id']]['isInCombat'] = 1
				fights[len(fights)] = { 's1': npcs[fights[fid]['s2id']]['name'], 's2': players[fights[fid]['s1id']]['name'], 's1id': nid, 's2id': fights[fid]['s1id'], 's1type': 'npc', 's2type': 'npc', 'retaliated': 1 }
		# Check if NPC is still alive, if not, remove from room and create a corpse, set isInCombat to 0, set whenDied to now and remove any fights NPC was involved in
		if npcs[nid]['hp'] <= 0:
			npcs[nid]['isInCombat'] = 0
			npcs[nid]['lastRoom'] = npcs[nid]['room']
			npcs[nid]['whenDied'] = int(time.time())
			fightsCopy = deepcopy(fights)
			for (fight, pl) in fightsCopy.items():
				if fightsCopy[fight]['s1id'] == nid or fightsCopy[fight]['s2id'] == nid:
					del fights[fight]
			corpses[len(corpses)] = { 'room': npcs[nid]['room'], 'name': str(npcs[nid]['name'] + '`s corpse'), 'inv': npcs[nid]['inv'], 'died': int(time.time()), 'TTL': npcs[nid]['corpseTTL'], 'owner': 1 }
			for (pid, pl) in list(players.items()):
				if players[pid]['authenticated'] is not None:
					if players[pid]['authenticated'] is not None and players[pid]['room'] == npcs[nid]['room']:
						mud.send_message(pid, "<f220>{}<r> <f88>has been killed.".format(npcs[nid]['name']))
			npcs[nid]['lastRoom'] = npcs[nid]['room']
			npcs[nid]['room'] = None
			npcs[nid]['hp'] = npcsTemplate[nid]['hp']
			
			# Drop NPC loot on the floor
			droppedItems = []
			for i in npcs[nid]['inv']:
				# print("Dropping item " + str(i[0]) + " likelihood of " + str(i[1]) + "%")
				if randint(0, 100) < int(i[1]):
					addToScheduler("0|spawnItem|" + str(i[0]) + ";" + str(npcs[nid]['lastRoom']) + ";0;0", -1, eventSchedule, scriptedEventsDB)
					# print("Dropped!" + str(itemsDB[int(i[0])]['name']))
					droppedItems.append(str(itemsDB[int(i[0])]['name']))

			# Inform other players in the room what items got dropped on NPC death
			if len(droppedItems) > 0:
				for p in players:
					if players[p]['room'] == npcs[nid]['lastRoom']:
						mud.send_message(p, "Right before <f220>" + str(npcs[nid]['name']) +"<r>'s lifeless body collapsed to the floor, it had dropped the following items: <f220>{}".format(', '.join(droppedItems)))

	# Iterate through ENV elements and see if it's time to send a message to players in the same room as the ENV elements
	for (eid, pl) in list(env.items()):
		now = int(time.time())
		if now > env[eid]['timeTalked'] + env[eid]['talkDelay'] + env[eid]['randomizer']:
			if len(env[eid]['vocabulary']) > 1:
				rnd = randint(0, len(env[eid]['vocabulary']) - 1)
				while rnd is env[eid]['lastSaid']:
					rnd = randint(0, len(env[eid]['vocabulary']) - 1)
			else:
				rnd = 0

			for (pid, pl) in list(players.items()):
				if env[eid]['room'] == players[pid]['room']:
					if len(env[eid]['vocabulary']) > 1:
						msg = '<f58>[' + env[eid]['name'] + ']: <f236>' + env[eid]['vocabulary'][rnd]
						mud.send_message(pid, msg)
						env[eid]['lastSaid'] = rnd
					else:
						msg = '<f58>[' + env[eid]['name'] + ']: <f236>' + env[eid]['vocabulary'][0]
						mud.send_message(pid, msg)
						env[eid]['lastSaid'] = rnd
			env[eid]['timeTalked'] = now
			env[eid]['randomizer'] = randint(0, env[eid]['randomFactor'])

	# Iterate through corpses and remove ones older than their TTL
	corpsesCopy = deepcopy(corpses)
	for (c, pl) in corpsesCopy.items():
		if int(time.time()) >= corpsesCopy[c]['died'] + corpsesCopy[c]['TTL']:
			# print("deleting " + corpses[corpse]['name'])
			del corpses[c]

	# Handle NPC respawns
	for (nid, pl) in list(npcs.items()):
		# print(npcs[nid])
		if npcs[nid]['whenDied'] is not None and int(time.time()) >= npcs[nid]['whenDied'] + npcs[nid]['respawn']:
			#print("IN")
			npcs[nid]['whenDied'] = None
			#npcs[nid]['room'] = npcsTemplate[nid]['room']
			npcs[nid]['room'] = npcs[nid]['lastRoom']
			# print("respawning " + npcs[nid]['name'])
			# print(npcs[nid]['hp'])

	# Evaluate the Event Schedule
	for (event, pl) in list(eventSchedule.items()):
		if time.time() >= eventSchedule[event]['time']:
			# its time to run the event!
			if eventSchedule[event]['type'] == "msg":
				mud.send_message(int(eventSchedule[event]['target']), str(eventSchedule[event]['body']))
			else:
				evaluateEvent(eventSchedule[event]['target'], eventSchedule[event]['type'], eventSchedule[event]['body'], players, npcs, itemsInWorld, env, npcsDB, envDB)
			del eventSchedule[event]
	
	# Evaluate player idle time and disconnect if required
	now = int(time.time())
	playersCopy = deepcopy(players)
	for p in playersCopy:
		if playersCopy[p]['authenticated'] != None:
			if now - playersCopy[p]['idleStart'] > allowedPlayerIdle:
				mud.send_message(p, "<f232><b11>Your body starts tingling. You instinctively hold your hand up to your face and notice you slowly begin to vanish. You are being disconnected due to inactivity...")
				log("Character " + str(players[p]['name']) + " is being disconnected due to inactivity.", "warning")
				del players[p]
				log("Disconnecting client " + str(p), "warning")
				mud._handle_disconnect(p)

	npcsTemplate = deepcopy(npcs)
	
	# go through any newly connected players
	for id in mud.get_new_players():
		# add the new player to the dictionary, noting that they've not been
		# named yet.
		# The dictionary key is the player's id number. We set their room to
		# None initially until they have entered a name
		# Try adding more player stats - level, gold, inventory, etc
		players[id] = {
			'name': None,
			'prefix': None,
			'room': None,
			'lvl': None,
			'exp': None,
			'str': None,
			'per': None,
			'endu': None,
			'cha': None,
			'int': None,
			'agi': None,
			'luc': None,
			'cred': None,
			'inv': None,
			'authenticated': None,
			'clo_head': None,
			'clo_larm': None,
			'clo_rarm': None,
			'clo_lhand': None,
			'clo_rhand': None,
			'clo_chest': None,
			'clo_lleg': None,
			'clo_rleg': None,
			'clo_feet': None,
			'imp_head': None,
			'imp_larm': None,
			'imp_rarm': None,
			'imp_lhand': None,
			'imp_rhand': None,
			'imp_chest': None,
			'imp_lleg': None,
			'imp_rleg': None,
			'imp_feet': None,
			'hp': None,
			'charge': None,
			'isInCombat': None,
			'lastCombatAction': None,
			'isAttackable': None,
			'lastRoom': None,
			'corpseTTL': None,
			'canSay': None,
			'canGo': None,
			'canLook': None,
			'canAttack': None,
			'canDirectMessage': None,
			'lookDescription': None,
			'idleStart': None
			}

		# send the new player a prompt for their name
		# mud.send_message(id, 'Connected to server!')

		mud.send_message(id, "\x00")
		mud.send_message(id, "\x00")
		mud.send_message(id, "<f94>                                                  <f246>,o88888    ")
		mud.send_message(id, "<f94>                                               <f246>,o8888888'    ")
		mud.send_message(id, "<f94>                         ,:o:o:oooo.        <f246>,8O88Pd8888\"     ")
		mud.send_message(id, "<f94>                     ,.::.::o:ooooOoOoO. <f246>,oO8O8Pd888'\"       ")
		mud.send_message(id, "<f94>                   ,.:.::o:ooOoOoOO8O8OOo.<f246>8OOPd8O8O\"         ")
		mud.send_message(id, "<f94>                  , ..:.::o:ooOoOOOO8OOOOo.<f246>FdO8O8\"           ")
		mud.send_message(id, "<f94>                 , ..:.::o:ooOoOO8O888O8O,<f246>COCOO\"             ")
		mud.send_message(id, "<f94>                , . ..:.::o:ooOoOOOO8OOO<f246>OCOCO\"               ")
		mud.send_message(id, "<f94>                 . ..:.::o:ooOoOoOO8O8<f246>OCCCC\"<f94>o                ")
		mud.send_message(id, "<f94>                    . ..:.::o:ooooOo<f246>CoCCC\"<f94>o:o                ")
		mud.send_message(id, "<f94>                    . ..:.::o:o:,<f246>cooooCo\"<f94>oo:o:               ")
		mud.send_message(id, "<f94>                 `   . . ..:.:<f246>cocoooo\"<f94>'o:o:::'               ")
		mud.send_message(id, "<f94>                 <f246>.<f94>`   . ..::<f246>ccccoc\"<f94>'o:o:o:::'                ")
		mud.send_message(id, "<f94>                <f246>:.:.<f94>    <f246>,c:cccc\"'<f94>:.:.:.:.:.'                 ")
		mud.send_message(id, "<f94>              <f246>..:.:\"'`::::c:\"'<f94>..:.:.:.:.:.'                  ")
		mud.send_message(id, "<f94>            <f246>...:.'.:.::::\"<f94>'    . . . . .'                    ")
		mud.send_message(id, "<f94>           <f246>.. . ....:.\"' <f94>`   .  . . ''                       ")
		mud.send_message(id, "<f94>         <f246>. . . ....\"'                                        ")
		mud.send_message(id, "<f94>        <f246> .. . .\"'<f94>     -<f230>DUM<f94>-                                  ")
		mud.send_message(id, "<f94>        <f246>.                                                    ")		
		mud.send_message(id, " ")
		mud.send_message(id, " ")
		mud.send_message(id, "<f250><b24> a modern MU* engine             ")
		mud.send_message(id, "<f250><b24>    github.com/wowpin/dumserver  ")
		mud.send_message(id, " ")
		mud.send_message(id, "<f250><b24> Development Server 1            ")
		mud.send_message(id, " ")
		mud.send_message(id, "<f250><b24> Codebase: v0.4                  ")
		mud.send_message(id, " ")
		mud.send_message(id, "<f15>Following guest accounts are available, get logging!\n")
		mud.send_message(id, "<f15>Username: <r><f220>Guest1<r><f15> Password: <r><f220>Password")
		mud.send_message(id, "<f15>Username: <r><f220>Guest2<r><f15> Password: <r><f220>Password")
		mud.send_message(id, "<f15>Username: <r><f220>Guest3<r><f15> Password: <r><f220>Password")
		mud.send_message(id, "<f15>Username: <r><f220>Guest4<r><f15> Password: <r><f220>Password")
		mud.send_message(id, "<f15>Username: <r><f220>Guest5<r><f15> Password: <r><f220>Password")
		
		mud.send_message(id, " ")
		mud.send_message(id, '<f15>What is your username?\n')

		# mud.send_message(id, " ")
		log("Client ID: " + str(id) + " has connected", "info")

	# go through any recently disconnected players
	for id in mud.get_disconnected_players():

		# if for any reason the player isn't in the player map, skip them and
		# move on to the next one
		if id not in players:
			continue
		
		log("Client ID: " + str(id) + " has disconnected (" + str(players[id]['name']) + ")", "info")
		
		# go through all the players in the game
		for (pid, pl) in list(players.items()):
			# send each player a message to tell them about the diconnected
			# player if they are in the same room
			if players[pid]['authenticated'] is not None:
				if players[pid]['authenticated'] is not None \
					and players[pid]['room'] == players[id]['room'] \
					and players[pid]['name'] != players[id]['name']:
					mud.send_message(pid,
							"<f32><u>{}<r>'s body has vanished.".format(players[id]['name']))

		# Code here to save player to the database after he's disconnected and before removing him from players dictionary
		if players[id]['authenticated'] is not None:
			log("Player disconnected, saving state", "info")
			saveState(players[id], playersDB)
			playersDB = loadPlayersDB()
		
		# TODO: IDEA - Some sort of a timer to have the character remain in the game for some time after disconnection?

		# Create a deep copy of fights, iterate through it and remove fights disconnected player was taking part in
		fightsCopy = deepcopy(fights)
		for (fight, pl) in fightsCopy.items():
			if fightsCopy[fight]['s1'] == players[id]['name'] or fightsCopy[fight]['s2'] == players[id]['name']:
				del fights[fight]


		# remove the player's entry in the player dictionary
		del players[id]

	
	# go through any new commands sent from players
	for (id, command, params) in mud.get_commands():
		# if for any reason the player isn't in the player map, skip them and
		# move on to the next one
		if id not in players:
			continue

		# if the player hasn't given their name yet, use this first command as
		# their name and move them to the starting room.
		if players[id]['name'] is None:
			dbResponse = None
			file = loadPlayer(command, playersDB)
			if file is not None:
				dbResponse = tuple(file.values())

			if dbResponse != None:
				players[id]['name'] = dbResponse[0]

				log("Client ID: " + str(id) + " has requested existing user (" + command + ")", "info")
				mud.send_message(id, 'Hi <u><f32>' + command + '<r>!')
				mud.send_message(id, '<f15>What is your password?')
			else:
				mud.send_message(id, '<f202>User <f32>' + command + '<r> was not found!\n')
				mud.send_message(id, '<f15>What is your username?')
				log("Client ID: " + str(id) + " has requested non existent user (" + command + ")", "info")
		elif players[id]['name'] is not None \
			and players[id]['authenticated'] is None:
			pl = loadPlayer(players[id]['name'], playersDB)
			dbPass = pl['pwd']

			# Iterate through players in game and see if our newly connected players is not already in game.
			playerFound = False
			for pl in players:
				if players[id]['name'] != None and players[pl]['name'] != None and players[id]['name'] == players[pl]['name'] and pl != id:
					playerFound = True

			if dbPass == command:
				if playerFound == False:
					players[id]['authenticated'] = True
					players[id]['prefix'] = "None"
					players[id]['room'] = dbResponse[1]
					players[id]['lvl'] = dbResponse[2]
					players[id]['exp'] = dbResponse[3]
					players[id]['str'] = dbResponse[4]
					players[id]['per'] = dbResponse[5]
					players[id]['endu'] = dbResponse[6]
					players[id]['cha'] = dbResponse[7]
					players[id]['int'] = dbResponse[8]
					players[id]['agi'] = dbResponse[9]
					players[id]['luc'] = dbResponse[10]
					players[id]['cred'] = dbResponse[11]
					players[id]['inv'] = dbResponse[12]#.split(',')
					# Example: item_list = [e for e in item_list if e not in ('item', 5)]
					players[id]['inv'] = [e for e in players[id]['inv'] if e not in ('', ' ')]
					players[id]['clo_head'] = dbResponse[14]
					players[id]['clo_larm'] = dbResponse[15]
					players[id]['clo_rarm'] = dbResponse[16]
					players[id]['clo_lhand'] = dbResponse[17]
					players[id]['clo_rhand'] = dbResponse[18]
					players[id]['clo_chest'] = dbResponse[19]
					players[id]['clo_lleg'] = dbResponse[20]
					players[id]['clo_rleg'] = dbResponse[21]
					players[id]['clo_feet'] = dbResponse[22]
					players[id]['imp_head'] = dbResponse[23]
					players[id]['imp_larm'] = dbResponse[24]
					players[id]['imp_rarm'] = dbResponse[25]
					players[id]['imp_lhand'] = dbResponse[26]
					players[id]['imp_rhand'] = dbResponse[27]
					players[id]['imp_chest'] = dbResponse[28]
					players[id]['imp_lleg'] = dbResponse[29]
					players[id]['imp_rleg'] = dbResponse[30]
					players[id]['imp_feet'] = dbResponse[31]
					players[id]['hp'] = dbResponse[32]
					players[id]['charge'] = dbResponse[33]
					players[id]['lookDescription'] = dbResponse[34]
					players[id]['isInCombat'] = 0
					players[id]['lastCombatAction'] = int(time.time())
					players[id]['isAttackable'] = 1
					players[id]['corpseTTL'] = 60
					players[id]['canSay'] = 1
					players[id]['canGo'] = 1
					players[id]['canLook'] = 1
					players[id]['canAttack'] = 1
					players[id]['canDirectMessage'] = 1
					players[id]['idleStart'] = int(time.time())
					
					
					log("Client ID: " + str(id) + " has successfully authenticated user " + players[id]['name'], "info")

					# go through all the players in the game
					for (pid, pl) in list(players.items()):
						# send each player a message to tell them about the new player
						if players[pid]['authenticated'] is not None \
							and players[pid]['room'] == players[id]['room'] \
							and players[pid]['name'] != players[id]['name']:
							mud.send_message(pid, '{} has materialised out of thin air nearby.'.format(players[id]['name']))
	
					# send the new player a welcome message
					mud.send_message(id, '\n<f220>Welcome to DUM!, {}. '.format(players[id]['name']))
					mud.send_message(id, '\n<f255>Hello there traveller! You have connected to a DUM development server, which currently consists of a few test rooms, npcs, items and environment actors. You can move around the rooms along with other players (if you are lucky to meet any), attack each other (including NPCs), pick up and drop items and chat. Make sure to visit the github repo for further info, make sure to check out the CHANGELOG. Thanks for your interest in DUM, high five!')
					mud.send_message(id, "\n<f255>Type '<r><f220>help<r><f255>' for a list of all currently implemented commands. Have fun!")
				else:
					mud.send_message(id, '<f202>This character is already in the world!')
					log("Client ID: " + str(id) + " has requested a character which is already in the world!", "info")
					players[id]['name'] = None
					mud.send_message(id, '<f15>What is your username?\n')
			else:
				mud.send_message(id, '<f202>Password incorrect!\n')
				log("Client ID: " + str(id) + " has failed authentication", "info")
				players[id]['name'] = None
				mud.send_message(id, '<f15>What is your username?')

		else:
			players[id]['idleStart'] = int(time.time())
			mud.send_message(id, "\x00")
			runCommand(command.lower(), params, mud, playersDB, players, rooms, npcsDB, npcs, itemsDB, itemsInWorld, envDB, env, scriptedEventsDB, eventSchedule, id, fights, corpses)
			


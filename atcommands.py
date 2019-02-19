from functions import addToScheduler
from functions import getFreeKey
from copy import deepcopy
import time
import configparser
from pathlib import Path
import os

# example of config file usage
# print(str(Config.get('Database', 'Hostname')))
Config = configparser.ConfigParser()
Config.read('config.ini')

'''
Command function template:

def atcommandname(params, mud, playersDB, players, rooms, npcsDB, npcs, itemsDB, items, envDB, env, eventDB, eventSchedule, id, fights, corpses):
	print("I'm in!")
'''

def config(params, mud, playersDB, players, rooms, npcsDB, npcs, itemsDB, items, envDB, env, eventDB, eventSchedule, id, fights, corpses):
	configitem = params.split(" ")[0]
	parameter = " ".join(params.split(" ")[1:])
	#print(configitem)
	#print(parameter)
	if configitem.lower() == "defaultchannel":
		if parameter.lower() == "clear":
			players[id]['defaultChannel'] = None
			mud.send_message(id, "Default channel has been cleared.")
		elif parameter.lower() == "show":
			if players[id]['defaultChannel'] != None:
				mud.send_message(id, "Your default channel is currently set to [" + players[id]['defaultChannel'] + "]")
			else:
				mud.send_message(id, "You do not have a default channel set.")
		else:
			mud.send_message(id, "Setting default channel to: " + parameter)
			players[id]['defaultChannel'] = parameter
	else:
		mud.send_message(id, "Not sure what you would like to configure.")

def serverlog(params, mud, playersDB, players, rooms, npcsDB, npcs, itemsDB, items, envDB, env, eventDB, eventSchedule, id, fights, corpses):
	if players[id]['permissionLevel'] == 0:
		if params.lower() == 'show':
			logLocation = str(Config.get('Logs', 'ServerLog'))
			#print(logLocation)
			logFile = Path(logLocation)
			if logFile.is_file():
				'''
				with open(fname) as f:
				content = f.readlines()
				# you may also want to remove whitespace characters like `\n` at the end of each line
				content = [x.strip() for x in content] 
				'''
				with open(logLocation) as f:
					content = f.readlines()
				f.close()
				content = [x.strip() for x in content]
				
				for l in content:
					mud.send_message(id, l.encode('utf-8').decode('latin-1'))
				
				mud.send_message(id, "<f255>Total of " + str(len(content)) + " lines read from server log.")
			else:
				mud.send_message(id, "Nothing to show!")
		elif params.lower() == 'clear':
			logLocation = str(Config.get('Logs', 'ServerLog'))
			logFile = Path(logLocation)
			if logFile.is_file():
				os.remove(logLocation)
				mud.send_message(id, "<f255>Server log has been cleared!")
			else:
				mud.send_message(id, "Nothing to clear!")
		else:
			mud.send_message(id, "Invalid @serverlog parameter '" + params + "'")
	else:
		mud.send_message(id, "You do not have permission to do this.")

def sendAtCommandError(params, mud, playersDB, players, rooms, npcsDB, npcs, itemsDB, items, envDB, env, eventDB, eventSchedule, id, fights, corpses):
	mud.send_message(id, "Unknown @command " + str(params) + "!")

def quit(params, mud, playersDB, players, rooms, npcsDB, npcs, itemsDB, items, envDB, env, eventDB, eventSchedule, id, fights, corpses):
	mud._handle_disconnect(id)

def who(params, mud, playersDB, players, rooms, npcsDB, npcs, itemsDB, items, envDB, env, eventDB, eventSchedule, id, fights, corpses):
	counter = 1
	if players[id]['permissionLevel'] == 0:
		for p in players:
			if players[p]['name'] == None:
				name = "None"
			else:
				name = players[p]['name']
				
			if players[p]['room'] == None:
				room = "None"
			else:
				room = players[p]['room']

			mud.send_message(id, str(counter) + ". Client ID: [" + str(p) + "] Player name: [" + name + "] Room: [" + room + "]")
			counter += 1
	else:
		mud.send_message(id, "You do not have permission to do this.")

def subscribe(params, mud, playersDB, players, rooms, npcsDB, npcs, itemsDB, items, envDB, env, eventDB, eventSchedule, id, fights, corpses):
	# print("Subbing to a channel")
	params = params.replace(" ", "")
	if len(params) > 0:
		if str(params.lower()) in players[id]['channels']:
			mud.send_message(id, "You are already subscribed to [" + params.lower() + "]")
		else:
			if str(params.lower()) != 'clear':
				players[id]['channels'].append(str(params.lower()))
				mud.send_message(id, "You have subscribed to [" + params + "]")
			else:
				mud.send_message(id, "Invalid channel name [" + params + "]")
	else:
		mud.send_message(id, "What channel would you like to subscribe to?")

def unsubscribe(params, mud, playersDB, players, rooms, npcsDB, npcs, itemsDB, items, envDB, env, eventDB, eventSchedule, id, fights, corpses):
	# print("Un-Subbing from a channel")
	params = params.replace(" ", "")
	if len(params) > 0:
		try:
			players[id]['channels'].remove(params.lower())
			mud.send_message(id, "You have unsubscribed from [" + params.lower() + "]")
		except Exception as e:
			mud.send_message(id, "You are not currently subscribed to [" + params.lower() + "]")
	else:
		mud.send_message(id, "What channel would you like to unsubscribe from?")
	
	if params.lower() == "system":
		mud.send_message(id, "<f230>You have un-subscribed from a SYSTEM channel. From now on, you will not receive any game-wide system messages (including server reboot notifications etc.). You can subscribe to SYSTEM at any time by typing '<f255>@subscribe system<r>'")

def channels(params, mud, playersDB, players, rooms, npcsDB, npcs, itemsDB, items, envDB, env, eventDB, eventSchedule, id, fights, corpses):
	if len(players[id]['channels']):
		mud.send_message(id, "You are currently subscribed to the following channels:")
		# print(players[id]['channels'])
		for c in players[id]['channels']:
			mud.send_message(id, "[" + c + "]")
	else:
		mud.send_message(id, "You are not currently subscribed to any channels.")

def runAtCommand(command, params, mud, playersDB, players, rooms, npcsDB, npcs, itemsDB, items, envDB, env, eventDB, eventSchedule, id, fights, corpses):
	switcher = {
		"sendAtCommandError": sendAtCommandError,
		"quit": quit,
		"subscribe": subscribe,
		"unsubscribe": unsubscribe,
		"channels": channels,
		"who": who,
		"serverlog": serverlog,
		"config": config,
	}

	try:
		switcher[command](params, mud, playersDB, players, rooms, npcsDB, npcs, itemsDB, items, envDB, env, eventDB, eventSchedule, id, fights, corpses)
	except Exception as e:
		switcher["sendAtCommandError"](e, mud, playersDB, players, rooms, npcsDB, npcs, itemsDB, items, envDB, env, eventDB, eventSchedule, id, fights, corpses)

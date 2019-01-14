from functions import addToScheduler
from functions import getFreeKey
from copy import deepcopy
import time

'''
Command function template:

def atcommandname(params, mud, playersDB, players, rooms, npcsDB, npcs, itemsDB, items, envDB, env, eventDB, eventSchedule, id, fights, corpses):
	print("I'm in!")
'''
def sendAtCommandError(params, mud, playersDB, players, rooms, npcsDB, npcs, itemsDB, items, envDB, env, eventDB, eventSchedule, id, fights, corpses):
	mud.send_message(id, "Unknown @command " + str(params) + "!")

def quit(params, mud, playersDB, players, rooms, npcsDB, npcs, itemsDB, items, envDB, env, eventDB, eventSchedule, id, fights, corpses):
	mud._handle_disconnect(id)

def who(params, mud, playersDB, players, rooms, npcsDB, npcs, itemsDB, items, envDB, env, eventDB, eventSchedule, id, fights, corpses):
	counter = 1
	if players[id]['permissionLevel'] == 0:
		for p in players:
			mud.send_message(id, str(counter) + ". Client ID: [" + str(p) + "] Player name: [" + players[p]['name'] + "] Room: [" + players[p]['room'] + "]")
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
			players[id]['channels'].append(str(params.lower()))
			mud.send_message(id, "You have subscribed to [" + params + "]")
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
	}

	try:
		switcher[command](params, mud, playersDB, players, rooms, npcsDB, npcs, itemsDB, items, envDB, env, eventDB, eventSchedule, id, fights, corpses)
	except Exception as e:
		switcher["sendAtCommandError"](e, mud, playersDB, players, rooms, npcsDB, npcs, itemsDB, items, envDB, env, eventDB, eventSchedule, id, fights, corpses)

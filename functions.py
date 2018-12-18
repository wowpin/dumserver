import time
import os
import commentjson
import errno
from copy import deepcopy
import configparser

# example of config file usage
# print(str(Config.get('Database', 'Hostname')))
Config = configparser.ConfigParser()
Config.read('config.ini')

# Function to silently remove file 
def silentRemove(filename):
	try:
		os.remove(filename)
	except OSError as e: # this would be "except OSError, e:" before Python 2.6
		if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
			raise # re-raise exception if a different error occurred

# Function to load all registered players from JSON files
# def loadPlayersDB(location = "./players", forceLowercase = True):
def loadPlayersDB(location = str(Config.get('Players', 'Location')), forceLowercase = True):
	DB = {}
	playerFiles = [i for i in os.listdir(location) if os.path.splitext(i)[1] == ".player"]
	for f in playerFiles:
		with open(os.path.join(location,f)) as file_object:
			#playersDB[f] = file_object.read()
			DB[f] = commentjson.load(file_object)

	if forceLowercase is True:
		out = {}
		for key, value in DB.items():
			out[key.lower()] = value

		return(out)
	else:
		return(DB)

	#for i in playersDB:
		#print(i, playersDB[i])

# Function used for loggin messages to stdout and a disk file
def log(content, type):
	logfile = 'dum.log'
	print(str(time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S") + " [" + type + "] " + content))
	if os.path.exists(logfile):
		log = open(logfile, 'a')
	else:
		log = open(logfile, 'w')
	log.write(str(time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S") + " [" + type + "] " + content) + '\n')
	log.close()

# Function for returning a first available key value for appending a new element to a dictionary
def getFreeKey(itemsDict, start = None):
	if start is None:
		try:
			for x in range(0, len(itemsDict) + 1):
				if len(itemsDict[x]) > 0:
					pass
		except Exception:
			pass
		return(x)
	else:
		found = False
		while found is False:
			if start in itemsDict:
				start += 1
			else:
				found = True
		return(start)

# Function for adding events to event scheduler
def addToScheduler(eventID, targetID, scheduler, database):
	if isinstance(eventID, int):
		for item in database:
			if int(item[0]) == eventID:
				scheduler[getFreeKey(scheduler)] = { 'time': int(time.time() + int(item[1])), 'target': int(targetID), 'type': item[2], 'body': item[3] }
	elif isinstance(eventID, str):
		item = eventID.split('|')
		scheduler[getFreeKey(scheduler)] = { 'time': int(time.time() + int(item[0])), 'target': int(targetID), 'type': item[1], 'body': item[2] }

def loadPlayer(name, db):
	try:
		#with open(path + name + ".player", "r") as read_file:
			#dict = commentjson.load(read_file)
			#return(dict)
		return(db[name.lower() + ".player"])
	except Exception:
		pass

def savePlayer(player, masterDB, path = str(Config.get('Players', 'Location')) + "/"):
	#print(path)
	DB = loadPlayersDB(forceLowercase = False)
	for p in DB:
		if (player['name'] + ".player").lower() == p.lower():
			#print("found the file")
			#print(p)
			with open(path + p, "r") as read_file:
				temp = commentjson.load(read_file)
			#print(temp)
			silentRemove(path + player['name'] + ".player")
			#print("removed file")
			newPlayer = deepcopy(temp)
			#print(newPlayer)
			newPlayer['pwd'] = temp['pwd']
			for key in newPlayer:
				if key != "pwd":
					# print(key)
					newPlayer[key] = player[key]
			#print(newPlayer)
			#print("Saving player state")
			with open(path + player['name'] + ".player", 'w') as fp:
				commentjson.dump(newPlayer, fp)
			#print("Updating playerd DB")
			masterDB = loadPlayersDB()
			#print(masterDB)


# State Save Function
def saveState(player, masterDB):
	tempVar = 0
	savePlayer(player, masterDB)
	#masterDB = loadPlayersDB()

def str2bool(v):
  return v.lower() in ("yes", "true", "True", "t", "1")
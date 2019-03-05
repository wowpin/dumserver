__filename__ = "events.py"
__author__ = "Bartek Radwanski"
__credits__ = ["Bartek Radwanski"]
__license__ = "MIT"
__version__ = "0.6.1"
__maintainer__ = "Bartek Radwanski"
__email__ = "bartek.radwanski@gmail.com"
__status__ = "Production"

from functions import str2bool
from functions import getFreeKey
import time

'''
## Function template
def (etarget, ebody, players, npcs, items, env):
	players[etarget]
'''

def setPlayerCanGo(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	if etarget in players:
		players[etarget]['canGo'] = int(ebody)

def setPlayerCanLook(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	if etarget in players:
		players[etarget]['canLook'] = int(ebody)

def setPlayerCanSay(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	if etarget in players:
		players[etarget]['canSay'] = int(ebody)

def setPlayerCanAttack(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	if etarget in players:
		players[etarget]['canAttack'] = int(ebody)

def setPlayerCanDirectMessage(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	if etarget in players:
		players[etarget]['canDirectMessage'] = int(ebody)

def setPlayerPrefix(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	if etarget in players:
		players[etarget]['prefix'] = str(ebody)

def setPlayerName(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['name'] = str(ebody)

def setPlayerRoom(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['room'] = str(ebody)

def setPlayerLvl(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['lvl'] = int(ebody)

def modPlayerLvl(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['lvl'] += int(ebody)

def setPlayerExp(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['exp'] = int(ebody)

def modPlayerExp(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['exp'] += int(ebody)

def setPlayerStr(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['str'] = int(ebody)

def modPlayerStr(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['str'] += int(ebody)

def setPlayerPer(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['per'] = int(ebody)

def modPlayerPer(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['per'] += int(ebody)

def setPlayerEndu(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['endu'] = int(ebody)

def modPlayerEndu(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['endu'] += int(ebody)

def setPlayerCha(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['cha'] = int(ebody)

def modPlayerCha(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['cha'] += int(ebody)

def setPlayerInt(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['inte'] = int(ebody)

def modPlayerInt(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['inte'] += int(ebody)

def setPlayerAgi(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['agi'] = int(ebody)

def modPlayerAgi(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['agi'] += int(ebody)

def setPlayerLuc(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['luc'] = int(ebody)

def modPlayerLuc(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['luc'] += int(ebody)

def setPlayerCred(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['cred'] = int(ebody)

def modPlayerCred(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['cred'] += int(ebody)

def setPlayerInv(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['inv'] = str(ebody)

def setAuthenticated(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['authenticated'] = str2bool(ebody)

def setPlayerClo_head(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0

def setPlayerClo_larm(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0

def setPlayerClo_rarm(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0

def setPlayerClo_lhand(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0

def setPlayerClo_rhand(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0

def setPlayerClo_chest(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0

def setPlayerClo_lleg(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0

def setPlayerClo_rleg(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0

def setPlayerClo_feet(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0

def setPlayerImp_head(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0

def setPlayerImp_larm(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0

def setPlayerImp_rarm(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0

def setPlayerImp_lhand(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0

def setPlayerImp_rhand(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0

def setPlayerImp_chest(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0

def setPlayerImp_lleg(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0

def setPlayerImp_rleg(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0

def setPlayerImp_feet(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0

def setPlayerHp(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['hp'] = int(ebody)

def modPlayerHp(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['hp'] += int(ebody)

def setPlayerCharge(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['charge'] = int(ebody)

def modPlayerCharge(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['charge'] += int(ebody)

def setPlayerIsInCombat(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['isInCombat'] += int(ebody)

def setPlayerLastCombatAction(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['lastCombatAction'] = int(ebody)

def modPlayerLastCombatAction(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['lastCombatAction'] += int(ebody)

def setPlayerIsAttackable(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['isAttackable'] = int(ebody)

def setPlayerLastRoom(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['lastRoom'] = str(ebody)

def setPlayerCorpseTTL(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['corpseTTL'] = int(ebody)

def modPlayerCorpseTTL(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	players[etarget]['corpseTTL'] += int(ebody)

def spawnItem(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0
	body = ebody.split(';')
	items[getFreeKey(items, 200000)] = { 'id': int(body[0]), 'room': body[1], 'whenDropped': int(time.time()), 'lifespan': int(body[2]), 'owner': int(body[3])}

def spawnNPC(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0
	body = ebody.split(';')
	# print(npcsDB)
	# print(body)
	npcs[getFreeKey(npcs, 90000)] = { 'name': npcsDB[int(body[0])]['name'], 'room': body[1], 'lvl': npcsDB[int(body[0])]['lvl'], 'exp': npcsDB[int(body[0])]['exp'], 'str': npcsDB[int(body[0])]['str'], 'per': npcsDB[int(body[0])]['per'], 'endu': npcsDB[int(body[0])]['endu'], 'cha': npcsDB[int(body[0])]['cha'], 'inte': npcsDB[int(body[0])]['inte'], 'agi': npcsDB[int(body[0])]['agi'], 'luc': npcsDB[int(body[0])]['luc'], 'cred': npcsDB[int(body[0])]['cred'], 'inv': npcsDB[int(body[0])]['inv'], 'isAttackable': int(body[2]), 'isStealable': int(body[3]), 'isKillable': int(body[4]), 'isAggressive': int(body[5]), 'clo_head': npcsDB[int(body[0])]['clo_head'], 'clo_larm': npcsDB[int(body[0])]['clo_larm'], 'clo_rarm': npcsDB[int(body[0])]['clo_rarm'], 'clo_lhand': npcsDB[int(body[0])]['clo_lhand'], 'clo_rhand': npcsDB[int(body[0])]['clo_rhand'], 'clo_chest': npcsDB[int(body[0])]['clo_chest'], 'clo_lleg': npcsDB[int(body[0])]['clo_lleg'], 'clo_rleg': npcsDB[int(body[0])]['clo_rleg'], 'clo_feet': npcsDB[int(body[0])]['clo_feet'], 'imp_head': npcsDB[int(body[0])]['imp_head'], 'imp_larm': npcsDB[int(body[0])]['imp_larm'], 'imp_rarm': npcsDB[int(body[0])]['imp_rarm'], 'imp_lhand': npcsDB[int(body[0])]['imp_lhand'], 'imp_rhand': npcsDB[int(body[0])]['imp_rhand'], 'imp_chest': npcsDB[int(body[0])]['imp_chest'], 'imp_lleg': npcsDB[int(body[0])]['imp_lleg'], 'imp_rleg': npcsDB[int(body[0])]['imp_rleg'], 'imp_feet': npcsDB[int(body[0])]['imp_feet'], 'hp': npcsDB[int(body[0])]['hp'], 'charge': npcsDB[int(body[0])]['charge'], 'corpseTTL': int(body[6]), 'respawn': int(body[7]), 'vocabulary': npcsDB[int(body[0])]['vocabulary'], 'talkDelay': npcsDB[int(body[0])]['talkDelay'], 'lookDescription': npcsDB[int(body[0])]['lookDescription'], 'timeTalked': 0, 'isInCombat': 0, 'lastCombatAction': 0, 'lastRoom': None, 'whenDied': None, 'randomizer': 0, 'randomFactor': npcsDB[int(body[0])]['randomFactor'], 'lastSaid': 0 }

def spawnActor(etarget, ebody, players, npcs, items, env, npcsDB, envDB):
	tempVar = 0
	body = ebody.split(';')
	env[int(body[0])] = { 'name': envDB[int(body[0])]['name'], 'vocabulary': envDB[int(body[0])]['vocabulary'], 'talkDelay': envDB[int(body[0])]['talkDelay'], 'randomFactor': envDB[int(body[0])]['randomFactor'], 'room': body[1], 'randomizer': envDB[int(body[0])]['randomizer'], 'timeTalked': envDB[int(body[0])]['timeTalked'], 'lastSaid': envDB[int(body[0])]['lastSaid'] }

# Function for evaluating an Event

def evaluateEvent(etarget, etype, ebody, players, npcs, items, env, npcsDB, envDB):
	switcher = {
		"setPlayerCanGo": setPlayerCanGo, #
		"setPlayerCanLook": setPlayerCanLook, #
		"setPlayerCanSay": setPlayerCanSay, #
		"setPlayerCanAttack": setPlayerCanAttack, #
		"setPlayerCanDirectMessage": setPlayerCanDirectMessage, #
		"setPlayerName": setPlayerName, #
		"setPlayerPrefix": setPlayerPrefix, #
		"setPlayerRoom": setPlayerRoom, #
		"setPlayerLvl": setPlayerLvl, #
		"modPlayerLvl": modPlayerLvl, #
		"setPlayerExp": setPlayerExp, #
		"modPlayerExp": modPlayerExp, #
		"setPlayerStr": setPlayerStr, #
		"modPlayerStr": modPlayerStr, #
		"setPlayerPer": setPlayerPer, #
		"modPlayerPer": modPlayerPer, #
		"setPlayerEndu": setPlayerEndu, #
		"modPlayerEndu": modPlayerEndu, #
		"setPlayerCha": setPlayerCha, #
		"modPlayerCha": modPlayerCha, #
		"setPlayerInt": setPlayerInt, #
		"modPlayerInt": modPlayerInt, #
		"setPlayerAgi": setPlayerAgi, #
		"modPlayerAgi": modPlayerAgi, #
		"setPlayerLuc": setPlayerLuc, #
		"modPlayerLuc": modPlayerLuc, #
		"setPlayerCred": setPlayerCred, #
		"modPlayerCred": modPlayerCred, #
		"setPlayerInv": setPlayerInv, #
		"setAuthenticated": setAuthenticated, #
		"setPlayerClo_head": setPlayerClo_head, #
		"setPlayerClo_larm": setPlayerClo_larm, #
		"setPlayerClo_rarm": setPlayerClo_rarm, #
		"setPlayerClo_lhand": setPlayerClo_lhand, #
		"setPlayerClo_rhand": setPlayerClo_rhand, #
		"setPlayerClo_chest": setPlayerClo_chest, #
		"setPlayerClo_lleg": setPlayerClo_lleg, #
		"setPlayerClo_rleg": setPlayerClo_rleg, #
		"setPlayerClo_feet": setPlayerClo_feet, #
		"setPlayerImp_head": setPlayerImp_head, #
		"setPlayerImp_larm": setPlayerImp_larm, #
		"setPlayerImp_rarm": setPlayerImp_rarm, #
		"setPlayerImp_lhand": setPlayerImp_lhand, #
		"setPlayerImp_rhand": setPlayerImp_rhand, #
		"setPlayerImp_chest": setPlayerImp_chest, #
		"setPlayerImp_lleg": setPlayerImp_lleg, #
		"setPlayerImp_rleg": setPlayerImp_rleg, #
		"setPlayerImp_feet": setPlayerImp_feet, #
		"setPlayerHp": setPlayerHp, #
		"modPlayerHp": modPlayerHp, #
		"setPlayerCharge": setPlayerCharge, #
		"modPlayerCharge": modPlayerCharge, #
		"setPlayerIsInCombat": setPlayerIsInCombat, #
		"setPlayerLastCombatAction": setPlayerLastCombatAction, #
		"modPlayerLastCombatAction": modPlayerLastCombatAction, #
		"setPlayerIsAttackable": setPlayerIsAttackable, #
		"setPlayerLastRoom": setPlayerLastRoom, #
		"setPlayerCorpseTTL": setPlayerCorpseTTL, #
		"modPlayerCorpseTTL": modPlayerCorpseTTL, #
		"spawnItem": spawnItem,
		"spawnNPC": spawnNPC,
		"spawnActor": spawnActor,
		}
	switcher[etype](etarget, ebody, players, npcs, items, env, npcsDB, envDB)

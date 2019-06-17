import bge

from bge.logic import keyboard, mouse, globalDict
from bge.logic import KX_ACTION_MODE_LOOP as LOOP
import bge.events as k

from math import degrees, radians

ATK_COOL = -0.45
ATK_COOL_4 = -0.60
RECOVER_INTERVAL = -1.0
COMBO_INTERVAL = -0.2
HITBOX_TIME = -0.3

def main(cont):
	
	own = cont.owner
	sensor = cont.sensors[0]
	
	if not 'Player' in own.scene:
		own.scene['Player'] = own
	
	if sensor.positive:
		setProps(cont)
		faceDirection(cont)
		move(cont)
		playAnimation(cont)
		cameraCollision(cont)
		toggleMap(cont)
		attack(cont)
		
def setProps(cont):
	own = cont.owner
	kb = keyboard.events
	mo = mouse.events
	
	isUp = kb[k.WKEY] == 2
	isDown = kb[k.SKEY] == 2
	isLeft = kb[k.AKEY] == 2
	isRight = kb[k.DKEY] == 2
	isMap = kb[k.SPACEKEY] == 1
	isAttack = mo[k.LEFTMOUSE] == 1
	isMagic1 = kb[k.ONEKEY] == 1
	isMagic2 = kb[k.TWOKEY] == 1
	isMagic3 = kb[k.THREEKEY] == 1
	isMagic4 = kb[k.FOURKEY] == 1
	
	if isMagic1:
		globalDict['Attributes']['Magic'] = 'Normal'
		globalDict['Attributes']['Strength'] = 10
		
	if isMagic2:
		globalDict['Attributes']['Magic'] = 'Fire'
		globalDict['Attributes']['Strength'] = 15
		
	if isMagic3:
		globalDict['Attributes']['Magic'] = 'Ice'
		globalDict['Attributes']['Strength'] = 20
		
	if isMagic4:
		globalDict['Attributes']['Magic'] = 'Lightning'
		globalDict['Attributes']['Strength'] = 25
	
	if own['Recover'] >= 0:
		
		if globalDict['Attributes']['Energy'] <= globalDict['Attributes']['MaxEnergy'] - 5:
			globalDict['Attributes']['Energy'] += 5
	
		if globalDict['Attributes']['Life'] <= globalDict['Attributes']['MaxLife'] - 1:
			globalDict['Attributes']['Life'] += 1
			
		own['Recover'] = RECOVER_INTERVAL
	
	if True:
		
		action_frame = int(own.childrenRecursive['PlayerArmature'].getActionFrame())
		
		if action_frame > 51 and action_frame < 57:
			own['Step'] = 1
		
		if action_frame > 59 and action_frame < 65:
			own['Step'] = 2
			
		if action_frame not in range(50, 67):
			own['Step'] = 0
	
	if globalDict['Attributes']['Magic'] != 'Normal' and globalDict['Attributes']['Energy'] < globalDict['Attributes']['Strength']:
		globalDict['Attributes']['Magic'] = 'Normal'
	
	if isMap:
		own['ViewMap'] = not own['ViewMap']
	
	if (isUp and not isDown) or (not isUp and isDown) or (isLeft and not isRight) or (not isLeft and isRight):
		own['Moving'] = True
	
	if (isUp and isDown) or (isLeft and isRight) or not (isUp or isDown or isLeft or isRight):
		own['Moving'] = False
	
	if isUp and not (isLeft and isRight and isDown) :
		own['Direction'] = 'U'
	
	if isDown and not (isLeft and isRight and isUp) :
		own['Direction'] = 'D'
	
	if isLeft and not (isUp and isRight and isDown) :
		own['Direction'] = 'L'
	
	if isRight and not (isLeft and isUp and isDown) :
		own['Direction'] = 'R'
	
	if isUp and isLeft and not (isRight and isDown) :
		own['Direction'] = 'UL'
	
	if isUp and isRight and not (isLeft and isDown) :
		own['Direction'] = 'UR'
	
	if isDown and isLeft and not (isRight and isUp) :
		own['Direction'] = 'DL'
	
	if isDown and isRight and not (isLeft and isUp) :
		own['Direction'] = 'DR'
		
	if own['Cooldown'] < 0:
		own['Moving'] = False
		
	if own['Cooldown'] > 0:
		own['Attack'] = 0
		own['Hitboxes'] = {}
		
	if isAttack:
		
		if own['Cooldown'] >= 0 and own['Attack'] == 0:
			own['Cooldown'] = ATK_COOL
			own['Attack'] += 1
		
		if own['Cooldown'] >= COMBO_INTERVAL and own['Cooldown'] < 0 and own['Attack'] in (1, 2, 3, 4):
			own['Cooldown'] = ATK_COOL_4 if own['Attack'] == 3 else ATK_COOL
			own['Attack'] += 1

def faceDirection(cont):
	
	own = cont.owner
	
	track = cont.actuators['Track']
	
	if own['Direction'] and own['Moving']:
		track.object = own.childrenRecursive['Direction' + own['Direction']]
		cont.activate(track)
	
	else:
		cont.deactivate(track)
		
def playAnimation(cont):
	
	own = cont.owner
	
	armature = own.childrenRecursive['PlayerArmature']
	
	anims = {
			'Idle' : (0, 39), 
			'Run' : (50, 65), 
			'Attack1' : (70, 80), 
			'Attack2' : (90, 100), 
			'Attack3' : (110, 120), 
			'Attack4' : (130, 150),
			'Death' : (160, 179)
			}
	
	if globalDict['Attributes']['Life'] > 0:
	
		if own['Moving']:
			armature.playAction('Puppet', start_frame=anims['Run'][0], end_frame=anims['Run'][1], blendin=2, play_mode=LOOP)
			
		else:
			
			if own['Attack'] == 0:
				armature.playAction(
									'Puppet', 
									start_frame=anims['Idle'][0], 
									end_frame=anims['Idle'][1], 
									blendin=2, 
									play_mode=LOOP
									)
				
			if own['Attack'] in (1, 2, 3, 4):
				armature.playAction(
									'Puppet', 
									start_frame=anims['Attack' + str(own['Attack'])][0], 
									end_frame=anims['Attack' + str(own['Attack'])][1], 
									blendin=2
									)
									
	else:
		own['Cooldown'] = -0.5
		own['Dead'] = False if not 'Dead' in own else True
		
		if own['Cooldown'] < 0 and not own['Dead']:
				
				armature.playAction(
									'Puppet', 
									start_frame=anims['Death'][0], 
									end_frame=anims['Death'][1], 
									blendin=2
									)
									
				own['Dead'] = True
				bge.logic.addScene('GameOver', 1)
	
def move(cont):
	
	own = cont.owner
	SPD_INC = 0.075
	
	if own['Moving']:
		own.applyMovement((0, -SPD_INC, 0), True)
		
def cameraCollision(cont):
	
	own = cont.owner
	
	camera = own.childrenRecursive['CameraPlayer']
	axis = own.childrenRecursive['CameraAxis']
	origin = own.childrenRecursive['CameraOrigin']
	smooth = own.childrenRecursive['CameraSmooth']
	
	ray = axis.rayCast(origin, axis, axis.getDistanceTo(origin), 'Obstacle', False, True)
	
	if ray[0]:
		camera.worldPosition = ray[1]
		camera.localPosition.y -= 0.2
		
	else:
		camera.worldPosition = origin.worldPosition
		
def toggleMap(cont):
	
	own = cont.owner
	scene_names = [scn.name for scn in bge.logic.getSceneList()]
	
	if own['ViewMap'] and not 'Map' in scene_names:
		bge.logic.addScene('Map', 1)
	
	elif not own['ViewMap'] and 'Map' in scene_names:
		game_scene = [scn for scn in bge.logic.getSceneList() if scn.name == 'Map'][0]
		game_scene.end()
		
def attack(cont):
	
	own = cont.owner
	
	if not 'Hitboxes' in own:
		own['Hitboxes'] = {}
		
	if own['Attack'] in (1, 2, 3, 4) and own['Cooldown'] > ATK_COOL + 0.1 and own['Cooldown'] < COMBO_INTERVAL - 0.1:
		
		if not own['Attack'] in own['Hitboxes'].keys():
			hitbox = own.scene.addObject('SwordHitbox', own)
			hitbox['Attack'] = own['Attack']
			hitbox['HitboxTime'] = HITBOX_TIME
			hitbox.setParent(own)
			hitbox.localPosition = (0, -0.60, 0)
			own['Hitboxes'][own['Attack']] = hitbox
			own.sendMessage('SwordSwing')
			
def swordHit(cont):
	
	own = cont.owner
	player = own.parent
	
	always = cont.sensors['Always']
	collision = cont.sensors['Collision']
	
	if always.positive:
	
		if collision.positive:
			
			if globalDict['Attributes']['Magic'] != 'Normal' and globalDict['Attributes']['Energy'] >= globalDict['Attributes']['Strength']:
				globalDict['Attributes']['Energy'] -= globalDict['Attributes']['Strength']
			
			collision.hitObject['Life'] -= globalDict['Attributes']['Strength'] * own['Attack']
			player['Hitboxes'][own['Attack']] = None
			own.sendMessage('SwordHit')
			own.endObject()
			
		if own['HitboxTime'] >= 0:
			own.endObject()
			
		if own['Attack'] == 1:
			own.localOrientation = (0, 0, 0)
			
		if own['Attack'] == 2:
			own.localOrientation = (0, radians(30), 0)
			
		if own['Attack'] == 3:
			own.localOrientation = (0, 0, 0)
			
		if own['Attack'] == 4:
			own.localOrientation = (0, radians(15), 0)
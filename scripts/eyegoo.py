import bge

from bge.logic import KX_ACTION_MODE_LOOP as LOOP
from bge.logic import globalDict

from math import degrees, radians

COOL_DMG = -0.3
COOL_ATK = -1.0
DIST_RUN = 5.0
DIST_IDLE = 30
DIST_END = 45

def main(cont):
	
	own = cont.owner
	sensor = cont.sensors[0]
	
	if sensor.positive and 'Player' in own.scene and own.groupObject:
		setProps(cont)
		playAnimation(cont)
		death(cont)
		pursuePlayer(cont)
		
def setProps(cont):
	
	own = cont.owner
	
	if own['LastLife'] > 0:
		
		if own['LastLife'] != own['Life']:
			own['Status'] = 'Damage'
			own['Cooldown'] = COOL_DMG
			own['AttackCooldown'] = COOL_ATK
			own['LastLife'] = own['Life']
			own.scene.addObject('Sword' + globalDict['Attributes']['Magic'], own)

def death(cont):
	
	own = cont.owner
	
	if own['Life'] <= 0:
		
		own['Status'] = 'Idle'
		
		if not own.isSuspendDynamics:
			own.sendMessage('EnemyDie')
		own.suspendDynamics(True)
		own.applyRotation((0, 0, 0.5), True)
		own.localScale.x -= 0.01
		own.localScale.y -= 0.01
		own.localScale.z -= 0.01
		
		if own.localScale.z < 0.1 and own.localScale.z > -0.1:
			globalDict['Attributes']['Exp'] += own['Exp']
			own.groupObject.endObject()

def pursuePlayer(cont):
	
	own = cont.owner
	track = cont.actuators['Track']
	
	dist = own.getDistanceTo(own.scene['Player'])
	
	if own['Life'] > 0:
		
		track.object = own.scene['Player']
		cont.activate(track)
		
		if dist <= DIST_RUN:
			
			if own['Status'] == 'Idle':
				cont.deactivate(track)
			
			if own['AttackCooldown'] >= 0:
				own['Status'] = 'Attack'
				projectile = own.scene.addObject('EyeGooProjectile', own, 120)
				projectile['Strength'] = own['Strength']
				own['AttackCooldown'] = -2.0
		
		if dist > DIST_RUN and dist < DIST_IDLE:
			
			if own['Cooldown'] >= 0:
				own['Status'] = 'Run'
				own.applyMovement((0, -0.02, 0), True)
				
			if own['Cooldown'] < 0:
				own['Status'] = 'Idle'
				
		if dist >= DIST_IDLE and dist < DIST_END:
			own['Status'] = 'Idle'
			cont.deactivate(track)
			
		if dist >= DIST_END:
			own.groupObject.endObject()
		
def playAnimation(cont):
	
	own = cont.owner
	
	anims = {
			'Idle' : (0, 39), 
			'Run' : (50, 69), 
			'Attack' : (80, 95),
			'Damage' : (100, 110)
			}
	
	if own['Cooldown'] >= 0:
		
		if own['Status'] == 'Idle':
			own.playAction(
						'EyeGoo', 
						start_frame=anims['Idle'][0], 
						end_frame=anims['Idle'][1], 
						blendin=2, 
						play_mode=LOOP
						)
						
		if own['Status'] == 'Run':
			own.playAction(
						'EyeGoo', 
						start_frame=anims['Run'][0], 
						end_frame=anims['Run'][1], 
						blendin=2, 
						play_mode=LOOP
						)
						
	
	if own['Cooldown'] < 0:
		
		if own['Status'] == 'Damage':
			own.playAction(
						'EyeGoo', 
						start_frame=anims['Damage'][0], 
						end_frame=anims['Damage'][1], 
						blendin=2
						)
						
			own['Status'] = 'Idle'
		
		if own['Status'] == 'Attack':
			own.playAction(
						'EyeGoo', 
						start_frame=anims['Attack'][0], 
						end_frame=anims['Attack'][1], 
						blendin=2
						)
						
			own['Status'] = 'Idle'
			
def projectileHit(cont):
	
	own = cont.owner
	
	collision = cont.sensors[0]
	
	if collision.positive:
		globalDict['Attributes']['Life'] -= own['Strength']
		own.scene.addObject('AttackHit', collision.hitObject)
		own.endObject()
import bge

from bge.logic import globalDict
from bge.logic import KX_ACTION_MODE_LOOP as LOOP

from math import degrees, radians
from random import choice, randint
from ast import literal_eval

def main(cont):
	
	own = cont.owner
	sensor = cont.sensors[0]
	
	if sensor.positive:
		pass
		
def enemySpawner(cont):
	
	own = cont.owner
	sensor = cont.sensors[0]
	
	dist = own.getDistanceTo(own.scene['Player'])
	group = 1
	probability = 10
	frequency = 60
	
	enemy_groups = {
					'BlueGoo' : (100, 10, (0.0, 0.5, 1.0, 0.7), 50), # Life, str, color
					'GreenGoo' : (200, 15, (0.0, 1.0, 0.2, 0.7), 75),
					'RedGoo' : (300, 20, (1.0, 0.0, 0.0, 0.7), 100),
					'GoldGoo' : (500, 10, (1.0, 0.6, 0.0, 0.7), 150)
					}
					
	if sensor.positive and own.groupObject and dist > 10 and dist < 40 and own['Spawned'] < own.groupObject['Max']:
		
		if 'Group' in own.groupObject:
			try:
				group = literal_eval(own.groupObject['Group'])
				
			except:
				group = ['BlueGoo', 'RedGoo']
			
		if 'Probability' in own.groupObject:
			probability = own.groupObject['Probability']
			
		if 'Frequency' in own.groupObject:
			frequency = own.groupObject['Frequency']
			
		sensor.skippedTicks = frequency
		test = randint(1, 100)
		
		if test <= probability:
			
			enemy_name = choice(group)
			enemy = own.scene.addObject('EnemyEyeGoo', own)
			enemy_parent = [obj for obj in enemy.groupMembers if 'Enemy' in obj][0]
			
			enemy_parent['Life'] = enemy_groups[enemy_name][0]
			enemy_parent['LastLife'] = enemy_groups[enemy_name][0]
			enemy_parent['Strength'] = enemy_groups[enemy_name][1]
			enemy_parent.color = enemy_groups[enemy_name][2]
			enemy_parent['Exp'] = enemy_groups[enemy_name][3]
			
			enemy_parent.worldPosition.x += randint(-5, 5)
			enemy_parent.worldPosition.y += randint(-5, 5)
			
			own['Spawned'] += 1
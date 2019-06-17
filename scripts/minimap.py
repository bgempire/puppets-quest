import bge

from bge.logic import keyboard
from bge.logic import KX_ACTION_MODE_LOOP as LOOP
import bge.events as k

from math import degrees, radians

def main(cont):
	
	own = cont.owner
	sensor = cont.sensors[0]
	
	scene_names = [scn.name for scn in bge.logic.getSceneList()]
	
	if sensor.positive and 'Game' in scene_names:
		addTiles(cont)
		setCursorPosition(cont)
		
def addTiles(cont):
	
	own = cont.owner
	scene_game = [scn for scn in bge.logic.getSceneList() if scn.name == 'Game'][0]
	
	tile_names = (
		'GroundGrass',
		'GroundPathFour',
		'GroundPathThree',
		'GroundPathStraight',
		'GroundPathTurn',
		'SideStraight',
		'SideTurnIn',
		'SideTurnOut'
		)
	
	if not 'Tiles' in own.scene:
		
		own.scene['Tiles'] = {}
		
		for _obj in scene_game.objects:
			for _prop in _obj.getPropertyNames():
				if _prop in tile_names:
					
					_tile_name = 'Tile' + _prop
					tile = own.scene.addObject(_tile_name)
					
					tile.worldPosition = _obj.worldPosition
					tile.localOrientation = _obj.localOrientation
					tile.color = [1, 1, 1, 0.5]
					own.scene['Tiles'][tuple(_obj.worldPosition)] = tile
					
		print('Minimap initializated, total tiles:', len(own.scene['Tiles'].keys()))
					
	else:
		pass

		
def setCursorPosition(cont):
	
	own = cont.owner
	
	scene_game = [scn for scn in bge.logic.getSceneList() if scn.name == 'Game'][0]
	
	if not 'Player' in scene_game:
		scene_game['Player'] = [obj for obj in scene_game.objects if obj.name == 'PlayerCollision'][0]
		
	else:
		own.worldPosition = scene_game['Player'].worldPosition
		own.localOrientation = scene_game['Player'].localOrientation
		own.childrenRecursive['MapCameraAxis'].localOrientation = scene_game['Player'].childrenRecursive['CameraAxis'].localOrientation
		own.childrenRecursive['MapCameraAxis'].applyRotation([radians(-30), 0, 0], True)
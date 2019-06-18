import bge

from bge.logic import globalDict, expandPath

def faceToCamera(cont):
	
	own = cont.owner
	
	sensor = cont.sensors[0]
	track = cont.actuators[0]
	
	if sensor.positive:
		track.object = own.scene.active_camera
		cont.activate(track)
		
def resetAttributes(cont):
	
	globalDict['Attributes'] = {
								'Strength' : 10,
								'Life' : 100,
								'MaxLife' : 100,
								'Energy' : 100,
								'MaxEnergy' : 100,
								'Exp' : 0,
								'Magic' : 'Normal'
								}
import bge

from bge import render, logic
from bge.logic import globalDict, expandPath
from ast import literal_eval
from textwrap import fill

BUT_ALPHA_OVER = 0.75
BUT_ALPHA_NORMAL = 1.0
TXT_RESOLUTION = 2.0

def updateText(cont):
	
	own = cont.owner
	
	sensor = cont.sensors[0]
	
	target_text = ''
	_wrap = 100
	
	if sensor.positive and own.groupObject:
		
		if 'upbge_version' in dir(bge.app):
			
			if own.resolution != TXT_RESOLUTION:
				own.resolution = TXT_RESOLUTION
		
		if 'Wrap' in own.groupObject:
			_wrap = own.groupObject['Wrap']
		
		if 'Update' in own.groupObject:
			sensor.usePosPulseMode = True
		
		if 'Source' in own.groupObject:
			
			try:
				target_text = str(eval(own.groupObject['Source']))
				
			except:
				target_text = own.groupObject['Source']
		
		if 'Text' in own.groupObject:
			target_text = own.groupObject['Text']
			
		target_text = fill(target_text, _wrap)
		
		own['Text'] = target_text

def buttonBehavior(cont):
	
	own = cont.owner
	
	always = cont.sensors['Always']
	lmb = cont.sensors['Lmb']
	over = cont.sensors['Over']
	
	text = [obj for obj in own.childrenRecursive if 'Text' in obj][0]
	
	prefix = ''
	separator = ''
	source = ''
	source_text = ''
	final = ''
	
	if always.positive and own.groupObject:
		
		if 'upbge_version' in dir(bge.app):
			
			if text.resolution != TXT_RESOLUTION:
				text.resolution = TXT_RESOLUTION
		
		if 'Update' in own.groupObject:
			always.usePosPulseMode = True
		
		if 'Prefix' in own.groupObject:
			
			separator = ': '
			
			try:
				prefix = str(eval(own.groupObject['Prefix']))
				
			except:
				prefix = own.groupObject['Prefix']
		
		if 'Source' in own.groupObject:
			
			try:
				source = eval(own.groupObject['Source'])
				source_text = str(eval(own.groupObject['Source']))
				
			except:
				source = own.groupObject['Source']
				source_text = source
			
		if over.positive:
			
			own.color[3] = BUT_ALPHA_OVER
			
			if lmb.positive and 'Exec' in own.groupObject:
					
				if type(source) == bool:
					exec(own.groupObject['Source'] + " = not " + own.groupObject['Source'])
					source = not source
					source_text = str(source)
					
					if '{}' in own.groupObject['Exec']:
						exec_str = own.groupObject['Exec'].format(str(source))
						print(exec_str)
						exec(exec_str)
				
				else:
					if own.groupObject['Exec'].startswith('[') and own.groupObject['Exec'].endswith(']'):
						own.scene.active_camera.worldPosition = literal_eval(own.groupObject['Exec'])
						
					else:
						exec(own.groupObject['Exec'])
		
		if not over.positive:
			own.color[3] = BUT_ALPHA_NORMAL
		
		if source_text in ('False', 'True'):
			source_text = globalDict['Lang']['True'] if source_text == 'True' else globalDict['Lang']['False']
			
		text['Text'] = (prefix + separator + source_text).center(35)
import bge

from bge.logic import globalDict, expandPath
from pathlib import Path
from ast import literal_eval

bge.logic.setExitKey(bge.events.F12KEY)

def main():
	
	globalDict['Attributes'] = {
								'Strength' : 10,
								'Life' : 100,
								'MaxLife' : 100,
								'Energy' : 100,
								'MaxEnergy' : 100,
								'Exp' : 0,
								'Magic' : 'Normal'
								}
								
	loadSettings()
	loadLang()

def loadSettings():
	
	path = Path(expandPath('//settings.txt')).resolve()
	
	with path.open() as opened_file:
		globalDict['Settings'] = literal_eval(opened_file.read())
		print('>', path.name, 'loaded')

def loadLang():
	
	path = Path(expandPath('//lang/')).resolve()
	
	for _file in path.iterdir():
		if _file.stem == globalDict['Settings']['Lang']:
			with open(_file.as_posix(), encoding='utf_8') as opened_file:
				globalDict['Lang'] = literal_eval(opened_file.read())
				print('>', _file.stem, 'language loaded')
				break

main()
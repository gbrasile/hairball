"""This module provides plugins for basic csv report data generation"""

from __future__ import print_function
import os
from hairball.plugins import HairballPlugin
from hairball.plugins.globalvar import GlobalVar
from hairball.plugins.clone import CloneDestruction
from hairball.plugins.empty import EmptyCode
from hairball.plugins.dead import DeadCode
import unicodecsv as csv


class GenerateCsv(HairballPlugin):

	"""Plugin that generates a csv file"""

	def __init__(self):
		self.path = ''

	def finalize(self):
		"""Output the success message after the file creation."""
		print('Csv success created in path {}'.format(self.path))

	def analyze(self, scratch, **kwargs):
		"""Run and generate the csv file"""
		# gets the directory and the file name
		for key, value in kwargs.iteritems():
			# value xxx/xxxx/xx.sb2
			path, fileName = os.path.split(value)
			# path xxx/xxxx | # file xx.sb2

			spritesVerified = []
			new_rows_list = []
		# for each sprite
		for sprite, script in self.iter_sprite_scripts(scratch):
			if sprite not in spritesVerified:
				spritesVerified.append(sprite)
				############################ CLONE DESTRUCTION ##############################
				pluginClone = CloneDestruction()
				dataClone = pluginClone.analyze(scratch)
				createdClones = 0
				destroyedClones = 0
				for key in dataClone.keys():
					if key == sprite:
						createdClones = dataClone[key][-1:][0][0]
						destroyedClones = dataClone[key][-1:][0][1]
						break

				############################ GLOBAL VAR #####################################
				pluginGlobalVar = GlobalVar()
				dataGlobalVar = pluginGlobalVar.analyze(scratch)
				globalVarsTotal = 0
				globalVarsUsed = 0
				# if 0 is returned, there's no global variable
				if dataGlobalVar != 0:
					globalVarsTotal = dataGlobalVar[1]
					for var in dataGlobalVar[0]:
						if var[0] == sprite:
							globalVarsUsed = var[1]
							break

				############################ EMPTY CODE #####################################
				pluginEmptyCode = EmptyCode()
				dataEmptyCode = pluginEmptyCode.analyze(scratch)
				quantityEmptyCode = 0
				for code in dataEmptyCode:
					if code[0] == sprite:
						quantityEmptyCode = code[1]
						break

				############################ DEAD CODE #####################################
				pluginDeadCode = DeadCode()
				dataDeadCode = pluginDeadCode.analyze(scratch)
				quantityDeadCode = 0
				for deadCode in dataDeadCode:
					if deadCode[0] == sprite:
						quantityDeadCode = deadCode[1]
						break

				new_row = [fileName, sprite, createdClones, destroyedClones,
				globalVarsTotal, globalVarsUsed, quantityDeadCode, quantityEmptyCode]
				new_rows_list.append(new_row)

		absolutePath = path + os.sep
		if not os.path.exists(absolutePath):
			os.makedirs(absolutePath)

		self.path = fileOutput = absolutePath + 'hairball_data.csv'
		csvExists = False
		if os.path.isfile(fileOutput):
			csvExists = True

		# Adds the lines
		with open(fileOutput, 'ab') as csvfile:
			writer = csv.writer(csvfile, delimiter=';',
				quoting=csv.QUOTE_MINIMAL, encoding='utf-8')
			if csvExists == False:
				header = ["File", "Sprite", "Created Clones", "Destroyed Clones", "Total of global variables",
				"Global Variables used", "Quantity of dead code", "Quantity of empty code"]
				writer.writerow(header)
			writer.writerows(new_rows_list)
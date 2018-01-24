"""This module provides plugins for basic empty code validation"""

from __future__ import print_function
from collections import Counter
from hairball.plugins import HairballPlugin

class EmptyCode(HairballPlugin):


	"""Plugin that detects dead code instances"""

	def __init__(self):
		self.mapping = ['repeat', 'forever', 'if', 'else']
		self.emptyInstances = 0

	def finalize(self):
		"""Output the number of empty code instances."""
		print('It has been found {} instances of empty code.'.format(self.emptyInstances))

	def analyze(self, scratch, **kwargs):
		"""Run and return the results from the EmptyCode plugin"""		
		commands = {}
		counter = 0
		spriteScripts = {}
		for sprite in scratch.sprites:
			for script in sprite.scripts:
				spriteScripts.setdefault(sprite.name, []).append(script.stringify().encode('utf-8').split('\n'))
		for sprite in spriteScripts.keys():
			for element in spriteScripts[sprite]:
				for command in element:
					for char in command:
						if char != ' ':
							commands.setdefault(sprite, []).append(command)
							break
		emptySprite = []
		for actor in commands.keys():
			counter = 0
			for i in range(len(commands[actor])):
				for item in self.mapping:
					if str(commands[actor][i]).find(item) != -1:
						if i+1 < len(commands[actor]):
							if commands[actor][i].__contains__('if') and (commands[actor][i+1].__contains__('else') or commands[actor][i+1].__contains__('end')):
								counter += 1
								self.emptyInstances += 1
							elif commands[actor][i+1].__contains__('end'):
								counter += 1
								self.emptyInstances += 1
						else:
							counter += 1
							self.emptyInstances += 1
			result = (actor, counter)
			emptySprite.append(result)
		return emptySprite				


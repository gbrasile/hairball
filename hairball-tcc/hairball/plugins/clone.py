"""This module provides plugins for basic clone deletion validation"""

from __future__ import print_function
import kurt
from hairball.plugins import HairballPlugin

class CloneDestruction(HairballPlugin):

	"""Plugin that detects non-destroyed clones"""

	def __init__(self):
		super(CloneDestruction, self).__init__()
		self.mapping = {}

	def finalize(self):
		"""Output the number of created and destroyed clones of each sprite"""
		for key in self.mapping.keys():
			print(key)
			print('-------------------------------------------------------------------------------------------')
			print('\tNumber of created clones => {}\n\tNumber of destroyed clones => {}\n'.format(self.mapping[key][-1:][0][0], self.mapping[key][-1:][0][1]))

	def analyze(self, scratch, **kwargs):
		"""Run and return the results from the CloneDestruction plugin"""
		#grouping the commands by sprite
		for sprite, script in self.iter_sprite_scripts(scratch):
			for name, depth, block in self.iter_blocks(script.blocks):
				commands = []
				if len(block.args) > 1:
					if type(block.args[1]) != list:
						commands.append(('\t'*depth + name % tuple(block.args)).encode('utf-8'))
					else:
						name = name.replace(' %s', ' {}')
						name = name.replace('%s', '')
						commands.append(('\t'*depth + name.format(block.args[0])).encode('utf-8'))
				else:
					if len(block.args) > 0:
						if not isinstance(block.args[0], kurt.Block) and not type(block.args[0]) == list:
							commands.append(('\t'*depth + name % block.args[0]).encode('utf-8'))
						else:
							name = name.replace(' %s', '')
							name = name.replace('%s', '')
							commands.append(('\t'*depth + name).encode('utf-8'))
					else:
						commands.append(('\t'*depth + name).encode('utf-8'))
				#creates the index if doesn't exists yet
				if not self.mapping.has_key(sprite):
					self.mapping.setdefault(sprite)
					self.mapping[sprite] = []
					self.mapping[sprite].extend(commands)
				#otherwise, adds the command to the current sprite
				else:
					self.mapping[sprite].extend(commands)
		#running through the sprites counting the number of created and destroyed clones
		for key in self.mapping.keys():
			createdClones = 0
			destroyedClones = 0
			countingClones = []
			for command in self.mapping[key]:
				if command.__contains__('create clone of'):
					createdClones += 1
				if command.__contains__('delete this clone'):
					destroyedClones += 1
			countingClones.append(createdClones)
			countingClones.append(destroyedClones)
			self.mapping[key].extend([countingClones])
		return self.mapping

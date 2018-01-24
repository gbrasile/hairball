"""This module provides plugins for basic global variables use detection"""

from __future__ import print_function
import kurt
from hairball.plugins import HairballPlugin

class GlobalVar(HairballPlugin):

	"""Plugin that reports info about global variables use"""

	def __init__(self):
		super(GlobalVar, self).__init__()
		self.globalVariables = []
		self.result = []
		self.sprite = 0
		self.hasGlobalVars = False

	def finalize(self):
		"""Output the the variable and the where it's utilized."""
		if self.hasGlobalVars == True:
			for var in self.globalVariables:
				used = []
				notUsed = []
				for item in self.result:
					if var == item[1]:
						if item[2] == True:
							used.append(item[0])
						else:
							notUsed.append(item[0])
				print('\n------------------------------------------------------------------------------------------------')
				print('Variable =>', var)

				print('\nUsed in {} of {} Sprites'.format(len(used), self.sprite))
				for usedSprite in used:
					print('- {}'.format(usedSprite))

				print('\nNot used in {} of {} Sprites'.format(len(notUsed), self.sprite))
				for notUsedSprite in notUsed:
					print('- {}'.format(notUsedSprite))
				print('\n------------------------------------------------------------------------------------------------')
		else: 
			print('------------------------------------------------------------------------------------------------')
			print("\nThere is no global variables")
			print('\n------------------------------------------------------------------------------------------------')

	  
	def analyze(self, scratch, **kwargs):
		"""Run and return the results from the GlobalVar plugin"""
		# verify if there's global variables and organize them in a list
		for variable in scratch.variables:
			self.globalVariables.append(variable.encode('utf-8'))
		# if there's global variable
		if len(self.globalVariables) > 0:
			self.hasGlobalVars = True
			# for each sprite
			for sprite, script in self.iter_sprite_scripts(scratch):
				self.sprite = self.sprite + 1
				lista = []
				# organize the blocks for verification
				for name, depth, block in self.iter_blocks(script.blocks):
					if len(block.args) > 1:
						if type(block.args[1]) != list:
							lista.append(('\t'*depth + name % tuple(block.args)).encode('utf-8'))
						else:
							name = name.replace(' %s', ' {}')
							name = name.replace('%s', '')
							lista.append(('\t'*depth + name.format(block.args[0])).encode('utf-8'))
					else:
						if len(block.args) > 0:
							if not isinstance(block.args[0], kurt.Block) and not type(block.args[0]) == list:
								lista.append(('\t'*depth + name % block.args[0]).encode('utf-8'))
							else:
								name = name.replace(' %s', '')
								name = name.replace('%s', '')
								lista.append(('\t'*depth + name).encode('utf-8'))
						else:
							lista.append(('\t'*depth + name).encode('utf-8'))

				# for each global variable
				for var in self.globalVariables:
					isUsed = False
					for item in lista:
						if item.__contains__(var):
							isUsed = True
					result = (sprite.encode('utf-8'), var, isUsed)
					self.result.append(result)

		# there's not global variable
		else: 
			self.hasGlobalVars = False

		if self.hasGlobalVars == True:
			variablesForSprite = []
			oldSprite = ''
			countUsed = 0
			first = True
			for num, item in enumerate(self.result, start=1):
				if item[2] == True:
					countUsed += 1

				sprite = item[0]
				# if it goes for the next sprite or is the last element of the last sprite
				if ((sprite != oldSprite) | (len(self.result) == num) ) & (first == False):
					result = (oldSprite, countUsed)
					variablesForSprite.append(result)
					countUsed = 0

				oldSprite = sprite
				first = False
			return (variablesForSprite, len(self.globalVariables))
		else: 
			return 0

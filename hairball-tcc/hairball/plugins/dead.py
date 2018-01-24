"""This module provides plugins for basic dead code validation"""

from __future__ import print_function
import kurt
from hairball.plugins import HairballPlugin

class DeadCode(HairballPlugin):

	"""Plugin that detects dead code instances"""

	def __init__(self):
		super(DeadCode, self).__init__()
		self.total_instances = 0
		self.dead_code_instances = 0
		self.unreachable = []

	def finalize(self):
		"""Output the number of instances that contain dead code."""
		print('--------------------------------------------------------------')
		if self.total_instances > 1:
			print(' {} instance(s) of dead code in a total of {} blocks.    |'
				  .format(self.dead_code_instances, self.total_instances))
		print('--------------------------------------------------------------')
		for dead in self.unreachable:
			  print(' ',dead)
			  
	def analyze(self, scratch, **kwargs):
		"""Run and return the results from the DeadCode plugin"""
		#runs through the scripts and stores the unreachable scripts
		for script in self.iter_scripts(scratch):
			self.total_instances += 1
			for name, depth, block in self.iter_blocks(script.blocks):
				if not script.reachable:
					if len(block.args) > 1:
						if type(block.args[1]) != list:
							self.unreachable.append(('\t'*depth + name % tuple(block.args)).encode('utf-8'))
						else:
							name = name.replace(' %s', ' {}')
							name = name.replace('%s', '')
							self.unreachable.append(('\t'*depth + name.format(block.args[0])).encode('utf-8'))
					else:
						if len(block.args) > 0:
							if not isinstance(block.args[0], kurt.Block):
								self.unreachable.append(('\t'*depth + name % block.args[0]).encode('utf-8'))
							else:
								name = name.replace(' %s', '')
								self.unreachable.append(('\t'*depth + name).encode('utf-8'))
						else:
							self.unreachable.append(('\t'*depth + name).encode('utf-8'))
		sprites = {}
		for sprite, script in self.iter_sprite_scripts(scratch):
			if not script.reachable:
				sprites.setdefault(sprite, []).append(script)
		if sprites:
			self.dead_code_instances += 1
		deadSprite = []
		for actor in sprites.keys():
			count = len(sprites[actor])
			if len(sprites[actor]) <= 0:
				count = 0
			result = (actor, count)
			deadSprite.append(result)
		return deadSprite


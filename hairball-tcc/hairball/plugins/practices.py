"""This module provides plugins for basic good programming practices validation"""

from __future__ import print_function
from hairball.plugins import HairballPlugin
from collections import OrderedDict
import kurt

class GoodPractices(HairballPlugin):

	"""Plugin that detects some bad programming practices"""

	def __init__(self):
		super(GoodPractices, self).__init__()
		self.actors = []
		self.badNames = []
		self.badReferences = []
		self.badMessages = []
		self.specialChars = False
		self.duplicatedInitializers = []

	def finalize(self):
		"""Output the info about good programming practices."""
		print('Sprites =>')
		for actor in self.actors:
			print('\t',actor)
		print('Bad Names =>')
		for name in self.badNames:
			print('\t',name),
		print('References to sprites with bad names =>')
		for reference in self.badReferences:
			print('\t',reference)
		print('Inappropriate message names =>')
		for message in self.badMessages:
				print('\t',message)
		print('Special chars =>', self.specialChars)
		for starter in self.duplicatedInitializers:
			print('-----------------------------------------')
			for element in starter:
				if starter[element]    == 0 and element != 'Quantity': starter[element] = 'when @green flag clicked'
				elif starter[element]  == 1 and element != 'Quantity': starter[element] = 'when I receive @message'
				elif starter[element]  == 2 and element != 'Quantity': starter[element] = 'when this @sprite clicked'
				elif starter[element]  == 3 and element != 'Quantity': starter[element] = 'when @key pressed' 
				elif starter[element]  == 4 and element != 'Quantity': starter[element] = 'when backdrop switches to @backdrop' 
				elif starter[element]  == 5 and element != 'Quantity': starter[element] = 'when @condition > @number' 
				elif starter[element]  == 6 and element != 'Quantity': starter[element] = 'when I start as a @clone' 
				elif starter[element]  == 7 and element != 'Quantity': starter[element] = 'no hat'
				print('{} -> {}'.format(element.encode('utf-8'), starter[element]))

	def analyze(self, scratch, **kwargs):
		"""Run and set the results the of the GoodPractices plugin"""
		broadcasts = []
		messages = []
		initializer = []
		duplicates = []
		#running through the sprites and their scripts
		for sprite, script in self.iter_sprite_scripts(scratch):
			#if the sprite has not been added
			if not self.actors.__contains__(sprite): self.actors.append(sprite)
			#if there's a sprite with inapropriate name, it's added in the self.badNames
			if(sprite.__contains__('Sprite') and not self.badNames.__contains__(sprite)):
				self.badNames.append(sprite.encode('utf-8'))
				#verifying if there's some reference to an actor with inappropriate name in their scripts
				if(script.stringify().__contains__(sprite)):
					self.badReferences.append(sprite.encode('utf-8'))
			#getting the name of all the messages triggered by the scripts
			broadcasts.append(self.get_broadcast_events(script))
			#getting the initializers of each sprite
			initializer.append(OrderedDict({sprite : self.script_start_type(script)}))
			#verifying if there's especial characters
			if any(ord(char) > 126 for char in script.stringify()):
				self.specialChars = True
		#structuring the messages to help the verification
		for broadcast in broadcasts:
			messages.append(broadcast.keys())
		#checking if there's some message with inadequate name
		for item in messages:
			for message in item:
				if(message.__contains__('message')):
					self.badMessages.append(message.encode('utf-8'))
		#creating the quantity's index
		for init in initializer:
			init.setdefault('Quantity')
		#storing the number of repetitions of each initializer
		for init in initializer:
			duplicates.append(initializer.count(init))
		#the range of each initializer
		for i in range(len(initializer)):
			initializer[i]['Quantity'] = duplicates[i]
		#the initializers without repetition 
		for element in initializer:
			if element not in self.duplicatedInitializers:
				self.duplicatedInitializers.append(element)
		#alphabetical sorting
		self.badMessages.sort()
		self.badNames.sort()
		self.badReferences.sort()

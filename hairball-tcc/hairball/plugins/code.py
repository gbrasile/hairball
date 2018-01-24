"""This module provides plugins for basic scratch code visualization"""

from __future__ import print_function
import kurt
from hairball.plugins import HairballPlugin

class CodePrinter(HairballPlugin):

	"""Plugin that outputs the project code"""

	def __init__(self):
		super(CodePrinter, self).__init__()
		self.commands = []

	def finalize(self):
		"""Output the project code"""
		for command in self.commands:
			print(command)

	def analyze(self, scratch, **kwargs):
		"""Run and return the results from the CodePrinter plugin"""
		for script in self.iter_scripts(scratch):
			self.commands.append(script.stringify())
"""This module provides plugins for basic cyclomatic complexity visualization"""

from collections import Counter
from hairball.plugins import HairballPlugin

class CyclomaticComplexity(HairballPlugin):

	"""Plugin that calculates the cyclomatic complexity from a project"""

	def __init__(self):
		super(CyclomaticComplexity, self).__init__()
		self.cc = []
		self.total = 0
		self.media = 0

	def finalize(self):
		"""Output the cyclomatic complexity score"""
		print '-------------------------------------------------------'
		print ("Cyclomatic Complexity: %i" % self.total)
		print ("Cyclomatic Complexity's average: %.2f" % self.media)
		print ("Cyclomatic Compleity by script:")
		print  self.cc
		print '-------------------------------------------------------'

	def analyze(self, scratch, **kwargs):
		"""Run and return the results from the CyclomaticComplexity plugin"""
		conditionals = (['if %s then%s', 'repeat until %s%s',
			'wait until %s', '%s and %s', '%s or %s'])
		for script in self.iter_scripts(scratch):
			conditions = 0
			for name, _, _ in self.iter_blocks(script.blocks):
				if name in conditionals:
					conditions += 1
				elif name == 'if %s then%selse%s':
					conditions +=2
			self.cc.append(conditions + 1)
			self.total += conditions +1
		self.media = float (self.total) / len(self.cc)
#!/bin/usr/python
"""
Test driver for payload displays
TODO:
	update data from radio
	keep track of uptime
	determine what/where data is displayed
@author: RIT Launch Initiative
"""
from display import Display
import sys

class PayloadDriver(object):

	def __init__(self):
		self.display = Display()
		self.add_vars()
		self.display.unlock()
		self.run()

	def add_vars(self):
		self.display.add_variable("Altitude (m)", "nan / 0", "left")
		self.display.add_variable("Lat", "nan", "left")
		self.display.add_variable("Long", "nan", "left")
		self.display.add_variable("uT", "nan", "left")

	def run(self):
		while 1:
			#update variables from radio
			self.display.update()

	def __check_lock(self):
		self.display.unlock()

if __name__ == "__main__":
	pl = PayloadDriver()

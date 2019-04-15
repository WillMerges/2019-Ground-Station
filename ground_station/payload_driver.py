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
import random
import time

class PayloadDriver(object):

	def __init__(self):
		self.display = Display()
		self.add_vars()
		self.display.unlock()

		self.max_altitude = 0
		self.__first_time = time.time()

		self.run()

	def add_vars(self):
		self.display.add_variable("Altitude (ft)", "nan / 0", "left")
		self.display.add_variable("Lat", "nan", "left")
		self.display.add_variable("Long", "nan", "left")
		self.display.add_variable("uT", "nan", "left")

		self.display.add_variable("vel (ft/s)", "nan", "right")
		self.display.add_variable("accel (ft/s)", "nan", "right")
		self.display.add_slider("sig lock", 0, 0, 7, "right")

		self.display.update_slider("sig lock", 3, "right")

	def run(self):
		i = 0
		last_time = time.time()
		while 1:
			self.display.update_var("Altitude (ft)", str(i)+" / "+str(self.max_alt(i)),"left")
			self.display.update_var("Lat", str(random.randint(1,1000)/1000.0*i),"left")
			self.display.update_var("Long", str(random.randint(1,1000)/1000.0*i),"left")
			self.display.update_var("uT", self.up_time(),"left")
			self.display.update_var("vel (ft/s)", str(i * 2.5))
			self.display.update_var("accel (ft/s)", str(i * 1.5))
			i += 1
			self.display.update()

	def max_alt(self, newmax):
		if newmax > self.max_altitude:
			self.max_altitude = newmax
		return self.max_altitude

	def up_time(self):
		self.uptime = time.time() - self.__first_time
		return str(int(self.uptime/360))+":"+str(int(self.uptime/60))+":"+str(int(self.uptime%60))

	def __check_lock(self):
		self.display.unlock()

if __name__ == "__main__":
	pl = PayloadDriver()

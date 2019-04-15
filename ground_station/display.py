"""
file: display.py
description: Dual LCD displays for RIT Launch Initiative 2019 ground station
Hardware:
	2 x 2.2" TFT displays
	Display 1:
		DC to GPIO 18
		RESET to GPIO 23
		LCD CS to CE0
		MOSI to MOSI
		MISO open
		SCK to SCK
		Backlight open
	Display 2:
		DC to GPIO 24(?)
		RESET to GPIO 25(?)
		LCD CS to CE1
		MOSI to MOSI
		MISO open
		SCK to SCK
		Backlight open
compatible with python 2.7
not guaranteed to run with python 3.x
@author: RIT Launch Initiative
"""
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
from collections import OrderedDict
import sys
import string

class Display(object):

	disp_width = 320
	disp_height = 240

	try:
		launch_logo = Image.open("images/launch_logo.png").resize((disp_width, disp_height)).rotate(90, expand=1)
		#font = ImageFont.truetype("fonts/Ubuntu-Light.ttf", 20)
                font = ImageFont.truetype("fonts/FiraCode-Bold.ttf", 24)
	except:
		launch_logo = Image.new('RGB', (disp_height, disp_width))
		font = ImageFont.load_default()

	def __init__(self):
		DC1 = 18
		RST1 = 23
		SPI_PORT1 = 0
		SPI_DEVICE1 = 0
		try:
			self.dispL = TFT.ILI9341(DC1, rst=RST1, spi=SPI.SpiDev(SPI_PORT1, SPI_DEVICE1, max_speed_hz=64000000)) #fill these in
		except:
			self.dispL = None
		DC2 = 24
		RST2 = 25
		SPI_PORT2 = 0
		SPI_DEVICE2 = 1
		try:
			self.dispR = TFT.ILI9341(DC2, rst=RST2, spi=SPI.SpiDev(SPI_PORT2, SPI_DEVICE2, max_speed_hz=64000000)) #fill these in
		except:
                        print("nah")
			self.dispR = None

		if self.dispL is not None:
			self.dispL.begin()
		if self.dispR is not None:
			self.dispR.begin()

		self.variablesL = OrderedDict()
		self.variablesR = OrderedDict()

		self.__locked = True

	#strings
	def add_variable(self, varName, defVal, screen):
		if string.lower(screen) == "left" or string.lower(screen) == "l":
			self.variablesL[varName] = defVal
		if string.lower(screen) == "right" or string.lower(screen) == "r":
			self.variablesR[varName] = defVal

	class Slider(object):
		def __init__(self, name, min, max, curr):
			self.name = name
			self.min = min
			self.max = max
			self.curr = curr

	def add_slider(self, varName, defVal, min, max, screen):
		if string.lower(screen) == "left" or string.lower(screen) == "l":
			self.variablesL[varName] = Display.Slider(varName, min, max, defVal)
		if string.lower(screen) == "right" or string.lower(screen) == "r":
			self.variablesR[varName] = Display.Slider(varName, min, max, defVal)

	def update_slider(self, varName, curr, screen = None):
		if screen is None:
			if varName in self.variablesL:
				if type(self.variablesL[varName]) is Display.Slider:
					self.variablesL[varName].curr = curr
			elif varName in self.variablesR:
				if type(self.variablesR[varName]) is Display.Slider:
					self.variablesR[varName].curr = curr
		elif string.lower(screen) == "left" or string.lower(screen) == "l":
			if varName in self.variablesL:
				if type(self.variablesL[varName]) is Display.Slider:
					self.variablesL[varName].curr = curr
		elif string.lower(screen) == "right" or string.lower(screen) == "r":
			if varName in self.variablesR:
				if type(self.variablesR[varName]) is Display.Slider:
					self.variablesR[varName].curr = curr
		else:
			sys.stderr.write("unable to recognize screen '"+screen+"'")

	#strings
	def update_var(self, varName, newVal, screen = None):
		if screen is None:
			if varName in self.variablesL:
				self.variablesL[varName] = newVal
			elif varName in self.variablesR:
				self.variablesR[varName] = newVal
		elif string.lower(screen) == "left" or string.lower(screen) == "l":
			if varName in self.variablesL:
				self.variablesL[varName] = newVal
		elif string.lower(screen) == "right" or string.lower(screen) == "r":
			if varName in self.variablesR:
				self.variablesR[varName] = newVal
		else:
			sys.stderr.write("unable to recognize screen '"+screen+"'")

	#returns (Image left_image, Image right_image)
	def __format_image(self):
		imgL = Image.new('RGB', (Display.disp_width, Display.disp_height))
		im_drawL = ImageDraw.Draw(imgL)

		if len(self.variablesL) == 0:
			offset = 0
		else:
			offset = int(Display.disp_height / len(self.variablesL))
		i = 0
		for variable in self.variablesL:
			if type(self.variablesL.get(variable)) is Display.Slider:
				slider = self.variablesL.get(variable)
				label = slider.name+": "+str(slider.curr)+" / "+str(slider.max)
				im_drawL.text((2, i*offset), label, font=Display.font, fill='white')
				width = 285
				height = 30
				im_drawL.rectangle(((5,i*offset + 35),(5+width, i*offset+20+height)), fill=None, outline='white')
				fill_width = slider.curr*1.0 / (slider.max-slider.min) * width
				im_drawL.rectangle(((5,i*offset + 35),(5+fill_width, i*offset+20+height)), fill="white", outline=None)
			else:
				label = variable+":\n "+self.variablesL.get(variable)
				im_drawL.text((2, i*offset), label, font=Display.font, fill='white')
			i += 1

		imgR = Image.new('RGB', (Display.disp_width, Display.disp_height))
		im_drawR = ImageDraw.Draw(imgR)

		if len(self.variablesR) == 0:
			offset = 0
		else:
			offset = int(Display.disp_height / len(self.variablesR))
		i = 0
		for variable in self.variablesR:
			if type(self.variablesR.get(variable)) is Display.Slider:
				slider = self.variablesR.get(variable)
				label = slider.name+": "+str(slider.curr)+" / "+str(slider.max)
				im_drawR.text((2, i*offset), label, font=Display.font, fill='white')
				width = 285
				height = 30
				im_drawR.rectangle(((5,i*offset + 35),(5+width, i*offset+20+height)), fill=None, outline='white')
				fill_width = slider.curr*1.0 / (slider.max-slider.min) * width
				im_drawR.rectangle(((5,i*offset + 35),(5+fill_width, i*offset+20+height)), fill="white", outline=None)
			else:
				label = variable+":\n "+self.variablesR.get(variable)
				im_drawR.text((2, i*offset), label, font=Display.font, fill='white')
			i += 1

		return (imgL.rotate(90, expand=1), imgR.rotate(90, expand=1))

	def update(self):
		if not self.__locked:
			img = self.__format_image()
			if self.dispL is not None:
				self.dispL.clear()
				self.dispL.display(img[0])
			if self.dispR is not None:
				self.dispR.clear()
				self.dispR.display(img[1])
		else:
			if self.dispL is not None:
				self.dispL.clear()
				self.dispL.display(Display.launch_logo)
			if self.dispR is not None:
				self.dispR.clear()
				self.dispR.display(Display.launch_logo)

	def unlock(self):
		self.__locked = False

	def lock(self):
		self.__locked = True

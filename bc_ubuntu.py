#!/usr/bin/python

import os, os.path, sys, signal
import time
from datetime import datetime,date
from threading import Thread
import fcntl

class Scanner(Thread):
	def __init__(self):
		Thread.__init__(self)

		self.hid = { 4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm', 17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y', 29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ', 45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';' , 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'  }
		self.hid2 = { 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M', 17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y', 29: 'Z', 30: '!', 31: '@', 32: '#', 33: '4', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ', 45: '-', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':' , 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'  }

		self.barcode = ""
		self.DevicePath = ""
		self.stop = False
		self.Run = True
		self.ShowScannerName = True
	
	def run(self):
		while self.Run == True:
			self.DetectScenner()
			if self.DevicePath != "":
				bc = open(self.DevicePath, 'rb', 1024)
				
				fd = bc.fileno()
				flag = fcntl.fcntl(fd,fcntl.F_GETFL)
				fcntl.fcntl(fd,fcntl.F_SETFL,flag | os.O_NONBLOCK)

				barcode = self.CheckBarcode(bc)
				if barcode != "":
					print " Your barcode is:", barcode
					self.barcode = barcode
				bc.close()
			time.sleep(0.001)
		return

	def Stop(self):
		self.Run = False
		self.stop = True
		time.sleep(0.03)

	def DetectScenner(self):
		self.DevicePath = ""
		for i in range(0,100):
			pt = "/sys/class/input/input"+str(i)+"/device/"
			if os.path.exists(pt+"interface"):
				f = open(pt+"interface","r")
				sor = f.readline()
				f.close()
				if "HID Keyboard Emulation" in sor:
					for root, dirs, files in os.walk(pt, topdown=False):
						for name in dirs:
						  ezkell = os.path.join(root, name)
						  if "hidraw" in name:
							hidraw_id = name.strip("hidraw")
							if hidraw_id.isdigit():
								self.DevicePath = "/dev/hidraw" + hidraw_id
								scannernameobject = open("/sys/class/input/input"+str(i)+"/name")
								scannername=scannernameobject.readline()								
								if self.ShowScannerName is True:
									print "Your reader is: "+ scannername
									self.ShowScannerName = False
					break

	def CheckBarcode(self,device):
		barcode = ""
		shift = False
		self.stop = False
		buff = ""

		while self.stop != True:	
			if os.path.exists(self.DevicePath):
				try:
					time.sleep(0.001)
					buff = device.read(1)
				except:
					pass
							
				for x in buff:
					if ord(x) == 2:
						shift = True
					if ord(x) > 0 and ord(x) < 48 and ord(x) != 2:
						
						if (ord(x) == 40):
							self.stop = True
						else:
							if shift == True:
								barcode += str(self.hid2[int(ord(x))])
								shift = False
							else:
								barcode += str(self.hid[int(ord(x))])
			else:
				print("Your scanner has been disconnected!")
				self.ShowScannerName = True
				return ""
									
		bcode = ""
		if " " in barcode:
			bcode, acode = barcode.split()
			print "It contained space therefore we use the beginning part."
		else:
			bcode = barcode
		return bcode

if __name__ == "__main__":

	scanner = Scanner()
	scanner.start()
	print "You have 30 seconds to test the scanning, then the program will exit.."
	time.sleep(30)
	print "My thread is off for now, i've exited well"
	scanner.Stop()
	exit()

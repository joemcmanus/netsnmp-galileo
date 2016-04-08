#!/usr/bin/env python
# File    : temp.py a simple temperature monitoring script for net-snmp
# Author  : Joe McManus josephmc@alumni.cmu.edu
# Version : 0.1  02/25/2016
# Copyright (C) 2016 Joe McManus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#For this  example a TMP36 is hooked to Analog pin 1 Change Aio to whatever pin you use.

import sys 
import mraa
import time

try: 
	#Initialize the MRAA pin
	pin = mraa.Aio(1) 
	#Set it to a 12 bit value
	pin.setBit(12)
except Exception,e:
	print("Error: {:s}". format(e))
	sys.exit()
	
rawReading = pin.read()
			
#Galileo voltage should be the raw reading divided by 819.0
#The reading is from 0-4095 to cover 0-5 volts
#Or 4095/5=819.0
galVoltage=float(rawReading / 819.0)
tempC= (galVoltage * 100 ) - 50 
tempF= (tempC * 9.0 / 5.0) + 32.0
print(round(tempF,2))

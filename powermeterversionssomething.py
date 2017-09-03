import numpy as np
import math
import serial
from threading import Timer 
from flask import Flask, render_template, jsonify
from multiprocessing import Process, Value
import wx
# Globals.. still needed?	
totalVolt=0.0
totalAmp=0.0
tcnt=0
avgwattdataidx=0
wattAve = 0
print "test"
avgwattdata = [0] * 1800
s = serial.Serial('COM8', 115200, timeout=0)
s.isOpen()

def parsePacket(packet):
	data=[]
	T = packet.split(";")
	for t in T:
		timestep=[]
		readings = t.split(",")
		#print readings
		if len(readings) == 2:
			for z in readings:
				# todo: error checking/handeling 
				if z != "":
					timestep.append(int(z))
			data.append(timestep)	
	return data


def processData(data):
	N_samples = 160
	WaveLength = (74*2)+1 # we want 2 waves to even out random noise.. 149 samples is good
	VoltSense = 1
	AmpSense = 0
	# to calibrate attach no load, set CURRENTNORM to 1 and run average for a few mins
	VREF = 470.97
	VREF2 = 474.2
	# to calibrate, first calibrate VREF then attach a load and view the AMP out put on the display
	# then adjust the CURRENTNORM factor to get the right result
	CURRENTNORM = 0.00578  # conversion to amperes from ADC
	VOLTNORM = 0.479 # conversion to volts from ADC

	# init empty arrays
	voltagedata=[0]*N_samples
	ampdata=[0]*N_samples
	vRMS=0.0
	aRMS=0.0

	# populate our data arrays
	for i in range(len(data)):
		if data[i] > 0:
			#e.g. [107,0]
			voltagedata[i]=data[i][VoltSense]
			ampdata[i]=data[i][AmpSense]
		#e.g. voltagedata = [0,0,0,0]
		#amdpata = 107
		# find peaks to get averages from
		ave1=0.0
		ave2=0.0
		for i in range(0,WaveLength):
			ave1 += voltagedata[i]
			ave2 += ampdata[i]
			
		#print "V/A>>>>>>>>>>", ave1/WaveLength, ave2/WaveLength, WaveLength

	vave=0.0
	#gets rid of bias
	for i in range(len(voltagedata)):
		# subtract average/remove DC bias (shift)
		voltagedata[i] -= ave1/WaveLength
		# scale readings from ADC realm to real values
		voltagedata[i] *= VOLTNORM
		if i < 149:
			vave+=abs(voltagedata[i])
			# calculate V^2 for RMS
			vRMS+=voltagedata[i]**2    
	# get peakVoltages
	for i in range(120):
		voltagedata[i] = 120

	vmax = max(voltagedata)
	vmin = min(voltagedata)

	#this gives us the mean of the sum of squares
	# then sqrt to get the RMS
	vRMS /= 149
	vRMS = math.sqrt(vRMS)

	aave=0.0
	wattdata=[0] * 149
	# normalize current readings to amperes
	for i in range(len(ampdata)):

		# VREF is the hardcoded 'DC bias' value, its
		# about 492 but would be nice if we could somehow
		# get this data once in a while maybe using xbeeAPI
		ampdata[i] -= VREF
		# the CURRENTNORM is our normalizing constant
		# that converts the ADC reading to Amperes
		ampdata[i] *= CURRENTNORM
		if i < 149:
			aave+=abs(ampdata[i])
			aRMS+=ampdata[i]**2
			wattdata[i] = ampdata[i] * voltagedata[i]

	ampdata, aave/149
	wattAve=0.0
	for w in wattdata:
		wattAve+=w
	wattAve /= len(wattdata) #for 1/30 of a second, since 2 cycles for 60 HZ
	return ampdata, aave/149, wattAve


def readDataEvent(event):
	readData()
		
def readData():
	global totalVolt
        global totalAmp
	global tcnt
        if s.isOpen:
		p = s.readline().strip()
		data = parsePacket(p)
		if data != []:
			processData(data)
#!/usr/bin/env python

# Misc imports
import numpy as np
import math
# Globals.. still needed?	
totalVolt=0.0
totalAmp=0.0
tcnt=0
avgwattdataidx=0
plotGraph=True
wattAve = 0

  

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

print processData([[502, 0], [501, 0], [505, 0], [505, 0], [501, 0], [501, 0], [500, 0], [496, 0], [498, 0], [500, 0], [496, 0], [492, 0], [493, 0], [497, 0], [495, 0], [492, 0], [492, 0], [476, 0], [471, 0], [474, 0], [476, 0], [476, 0], [474, 0], [478, 0], [484, 0], [486, 0], [488, 0], [495, 0], [497, 0], [498, 0], [499, 0], [503, 0], [501, 0], [502, 0], [504, 0], [505, 0], [504, 0], [502, 0], [505, 0], [507, 0], [506, 0], [505, 0], [508, 0], [508, 0], [508, 0], [512, 0], [513, 2], [509, 0], [509, 0], [514, 0], [518, 1], [514, 1], [515, 1], [516, 0], [529, 3], [536, 5], [536, 5], [537, 5], [532, 5], [531, 4], [533, 5], [532, 5], [523, 4], [516, 1], [517, 1], [515, 0], [511, 0], [511, 1], [509, 0], [505, 0], [503, 0], [508, 0], [507, 0], [504, 0], [502, 0], [505, 0], [505, 0], [501, 0], [502, 0], [502, 0], [499, 0], [503, 0], [500, 0], [498, 0], [497, 0], [494, 0], [498, 0], [496, 0], [494, 0], [492, 0], [494, 0], [485, 0], [473, 0], [475, 0], [475, 0], [473, 0], [476, 0], [481, 0], [482, 0], [483, 0], [487, 0], [495, 0], [494, 0], [497, 0], [499, 0], [498, 0], [500, 0], [501, 0], [506, 0], [503, 0], [499, 0], [504, 0], [506, 0], [506, 0], [505, 0], [507, 0], [506, 0], [506, 0], [511, 1], [513, 1], [510, 0], [509, 1], [512, 0], [516, 1], [515, 1], [514, 1], [515, 1], [516, 0], [519, 2]]);
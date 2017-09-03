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
	VREF = 512
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
	return wattAve

print processData([[518, 0], [517, 0], [517, 0], [516, 0], [517, 0], [518, 0], [517, 0], [517, 0], [517, 0], [518, 0], [519, 0], [518, 0], [517, 0], [518, 0], [517, 0], [518, 0], [518, 0], [518, 0], [517, 0], [517, 0], [518, 0], [517, 0], [545, 0], [594, 0], [592, 0], [559, 0], [540, 0], [528, 0], [526, 0], [526, 0], [523, 0], [516, 0], [517, 0], [516, 0], [517, 0], [516, 0], [517, 0], [516, 0], [518, 0], [517, 0], [516, 0], [517, 0], [517, 0], [516, 0], [517, 0], [517, 0], [516, 0], [517, 0], [515, 0], [516, 0], [518, 0], [515, 0], [516, 0], [515, 0], [517, 0], [516, 0], [518, 0], [516, 0], [515, 0], [516, 0], [434, 0], [444, 0], [465, 0], [487, 0], [506, 0], [510, 0], [509, 0], [517, 0], [517, 0], [520, 0], [517, 0], [517, 0], [517, 0], [517, 0], [518, 0], [518, 0], [517, 0], [518, 0], [517, 0], [517, 0], [516, 0], [518, 0], [517, 0], [517, 0], [519, 0], [518, 0], [517, 0], [516, 0], [516, 0], [517, 0], [517, 0], [518, 0], [518, 0], [518, 0], [519, 0], [518, 0], [517, 0], [593, 0], [590, 0], [568, 0], [545, 0], [539, 0], [528, 0], [529, 0], [530, 0], [521, 0], [517, 0], [517, 0], [517, 0], [516, 0], [518, 0], [518, 0], [515, 0], [517, 0], [516, 0], [517, 0], [517, 0], [517, 0], [517, 0], [518, 0], [517, 0], [517, 0], [517, 0], [516, 0], [518, 0], [516, 0], [516, 0], [516, 0], [515, 0], [516, 0], [516, 0], [517, 0], [517, 0], [516, 0], [470, 0], [446, 0], [457, 0], [480, 0], [500, 0], [507, 0], [506, 0], [506, 0], [511, 0], [518, 0], [517, 0], [517, 0], [517, 0], [519, 0], [518, 0], [516, 0]]);
import numpy as np
import math

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
	return wattAve
def parsePacket(packet):
	data=[]
	T = packet.split(";")
	for t in T:
		timestep=[]
		readings = t.split(",")
		#print readings
		if len(readings) == 2:
			for s in readings:
				# todo: error checking/handeling 
				if s != "":
					timestep.append(int(s))
			data.append(timestep)	
	return processData(data[0:150])


print parsePacket("646,0;648,0;646,0;644,0;645,0;644,0;642,0;639,0;635,0;628,0;625,0;618,0;610,0;603,0;594,0;585,0;573,0;559,0;550,0;537,0;527,0;519,0;508,0;499,0;491,0;478,0;467,0;456,0;446,0;437,0;429,0;421,0;412,0;407,0;400,0;395,0;391,0;389,0;386,0;387,0;386,0;389,0;389,0;391,0;394,0;398,0;403,0;409,0;415,0;422,0;431,0;440,0;449,0;459,0;472,0;484,0;494,0;505,0;513,0;525,0;532,0;542,0;551,0;565,0;574,0;585,0;596,0;605,0;612,0;619,0;627,0;632,0;636,0;639,0;644,0;646,0;646,0;647,0;645,0;645,0;644,0;641,0;637,0;631,0;626,0;620,0;614,0;606,0;597,0;589,0;578,0;564,0;553,0;543,0;531,0;520,0;511,0;503,0;494,0;483,0;469,0;461,0;450,0;441,0;432,0;423,0;417,0;408,0;403,0;397,0;393,0;388,0;387,0;387,0;388,0;387,0;388,0;389,0;392,0;389,0;390,0;391,0;394,0;401,0;405,0;411,0;416,0;425,0;432,0;442,0;452,0;463,0;474,0;485,0;496,0;508,0;517,0;526,0;533,0;544,0;555,0;566,0;578,0;587,0;596,0;606,0;614,0;621,0;628,0;634,0;639,0;642,0;645,0;645,0;646,0;646,0;645,0;643,0;643,0;640,0;636,0;631,0;625,0;619,0;611,0;603,0;594,0;586,0;573,0;560,0;550,0;540,0;529,0;519,0;509,0;497,0;491,0;480,0;467,0;458,0;449,0;438,0;428,0;421,0;414,0;407,0;402,0;395,0;392,0;390,0;387,0;388,0;387,0;388,0;388,0;392,0;394,0;396,0;403,0;409,0;414,0;422,0;430,0;436,0;447,0;459,0;469,0;482,0;492,0;504,0;514,0;523,0;533,0;541,0;551,0;563,0;573,0;583,0;593,0;602,0;610,0;616,0;623,0;631,0;637,0;640,0;644,0;646,0;646,0;646,0;647,0;646,0;644,0;641,0;638,0;633,0;627,0;621,0;615,0;606,0;600,0;590,0;577,0;568,0;555,0;545,0;532,0;523,0;514,0;505,0;496,0;485,0;473,0;461,0;451,0;443,0;434,0;425,0;418,0;411,0;404,0;398,0;395,0;389,0;389,0;388,0;388,0;389,0;389,0;389,0;391,0;396,0;400,0;405,0;412,0;417,0;427,0;433,0;443,0;422,0;432,0;440,0;451,0;463,0;475,0;484,0;496,0;508,0;516,0;525,0;")
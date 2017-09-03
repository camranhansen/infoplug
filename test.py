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


print parsePacket("455,0;467,0;480,0;490,0;501,0;513,0;521,0;530,0;540,0;549,0;563,0;571,0;582,0;591,0;600,0;609,0;616,0;623,0;631,0;636,0;639,0;642,0;646,0;646,0;646,0;645,0;645,0;645,0;644,0;639,0;633,0;627,0;621,0;615,0;609,0;602,0;592,0;580,0;568,0;557,0;545,0;535,0;525,0;515,0;507,0;497,0;487,0;475,0;464,0;455,0;445,0;435,0;427,0;418,0;411,0;404,0;399,0;395,0;392,0;389,0;389,0;388,0;387,0;387,0;389,0;391,0;394,0;400,0;406,0;410,0;416,0;424,0;432,0;439,0;450,0;462,0;474,0;486,0;497,0;507,0;518,0;527,0;535,0;543,0;557,0;567,0;577,0;588,0;598,0;606,0;614,0;620,0;627,0;633,0;637,0;641,0;644,0;645,0;646,0;644,0;646,0;644,0;644,0;641,0;636,0;628,0;624,0;618,0;612,0;605,0;594,0;586,0;574,0;560,0;550,0;540,0;531,0;519,0;508,0;501,0;492,0;480,0;468,0;458,0;448,0;438,0;430,0;421,0;414,0;407,0;401,0;395,0;393,0;390,0;389,0;387,0;388,0;390,0;387,0;389,0;392,0;396,0;401,0;407,0;413,0;420,0;429,0;437,0;446,0;459,0;470,0;480,0;453,0;465,0;479,0;490,0;501,0;511,0;521,0;530,0;537,0;549,0;560,0;571,0;581,0;591,0;600,0;608,0;617,0;624,0;631,0;636,0;639,0;642,0;645,0;647,0;645,0;646,0;645,0;644,0;643,0;638,0;633,0;629,0;622,0;615,0;609,0;601,0;592,0;582,0;570,0;558,0;546,0;535,0;524,0;516,0;506,0;497,0;488,0;476,0;465,0;454,0;445,0;435,0;426,0;419,0;411,0;405,0;399,0;394,0;390,0;388,0;389,0;389,0;388,0;389,0;389,0;393,0;395,0;399,0;405,0;409,0;416,0;423,0;432,0;440,0;449,0;463,0;473,0;485,0;497,0;506,0;517,0;526,0;534,0;543,0;556,0;566,0;577,0;587,0;596,0;604,0;613,0;621,0;627,0;634,0;638,0;641,0;644,0;645,0;646,0;645,0;644,0;644,0;643,0;641,0;636,0;631,0;623,0;621,0;611,0;605,0;595,0;586,0;576,0;563,0;551,0;539,0;528,0;521,0;510,0;501,0;492,0;480,0;468,0;458,0;448,0;440,0;432,0;421,0;415,0;407,0;401,0;395,0;393,0;390,0;387,0;388,0;387,0;389,0;389,0;391,0;392,0;394,0;402,0;408,0;413,0;419,0;430,0;437,0;445,0;457,0;469,0;481,0;491,0;503,0;515,0;524,0;531,0;540,0;551,0;563,0;538,0;547,0;560,0;570,0;580,0;591,0;600,0;608,0;617,0;623,0;629,0;636,0;640,0;643,0;646,0;646,0;645,0;646,0;644,0;643,0;643,0;640,0;635,0;630,0;624,0;617,0;610,0;601,0;593,0;583,0;571,0;558,0;547,0;536,0;527,0;515,0;507,0;499,0;488,0;476,0;464,0;456,0;446,0;435,0;428,0;419,0;412,0;405,0;398,0;394,0;391,0;387,0;389,0;388,0;389,0;390,0;390,0;391,0;394,0;397,0;404,0;411,0;415,0;422,0;431,0;438,0;447,0;460,0;473,0;484,0;494,0;506,0;516,0;524,0;535,0;543,0;555,0;566,0;574,0;586,0;596,0;603,0;612,0;620,0;628,0;633,0;639,0;641,0;645,0;644,0;646,0;646,0;644,0;645,0;643,0;642,0;637,0;631,0;626,0;620,0;614,0;604,0;598,0;589,0;578,0;565,0;553,0;542,0;531,0;521,0;513,0;501,0;494,0;480,0;470,0;459,0;449,0;440,0;429,0;423,0;414,0;409,0;402,0;398,0;392,0;390,0;388,0;387,0;388,0;389,0;389,0;391,0;393,0;396,0;401,0;406,0;413,0;420,0;427,0;436,0;444,0;456,0;467,0;480,0;490,0;501,0;512,0;521,0;531,0;538,0;549,0;563,0;574,0;582,0;593,0;602,0;610,0;616,0;624,0;630,0;")
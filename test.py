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
	return data


s = serial.Serial('COM6', 115200, timeout=0)
	s.isOpen()
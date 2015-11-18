import serial, time, sys, getopt
port = '/dev/ttyS0'
debug = True
isLoading = True
initial = True
def main(argv):
	try:
		opts, args = getopt.getopt(argv,"hp:d:", ["port=", "debug="])
	except getopt.GetoptError:
		print('reset.py -p /dev/ttyS0 -d True')
	for opt, arg in opts:
		if opt == '-p':
			port = arg
		elif opt == '-d':
			if(arg == 'True'):
				debug = True
			else:
				debug = False
			
			 
	ser = serial.Serial(port, 9600, timeout=1.0, rtscts=False)
	if(ser.isOpen() == False):
		ser.open()
		print("Opening port")
	else:
		print("Port already open")
	isNotResetting = True
	hasConnected = False
	while isNotResetting == True:
		if(hasConnected == False and debug == False):
			print("Waiting for ROMMON/connection")
		elif(debug == True and hasConnected == False):
			print("You are in debug mode!")
		theOutput = ser.readline()
		if(theOutput and debug == True):
			print(theOutput)
		if ("ROMMON" in theOutput and hasConnected == False):
			ser.sendBreak()
			hasConnected = True
			print('Booting into ROMMON')
					
		if("boot" in theOutput):
			print("Initial config")
			ser.write('confreg 0x2141\r\n')
			time.sleep(1)
			ser.write('reset\r'.encode())
			print("Resetting")
	
		if("yes/no" in theOutput):
	
			print("Skipping system configuration utility")
			ser.write('no\r'.encode())
			print("Waiting on proper 	commandline")				
		if("RETURN" in theOutput):
			print("Entering terminal")
			ser.write('enable\r'.encode())
			time.sleep(5)
			print("We should be in the terminal")	
			ser.write(b'\rL1\r')
			try:
				ser.flushInput()
			except:
				print("different version of pyserial")

			ser.write('enable\r'.encode())
		if("Router#" in theOutput and initial == True):
			ser.write("configure terminal\r".encode())
			print("Entering terminal configuration")

		if("Router(config)#" in theOutput):
			ser.write("config-register 0x2102\r".encode())
			print("Eraseing all traces of configuration known to man...er...this router I mean")
			
			

if __name__ == "__main__":
	main(sys.argv[1:])

import serial, time, sys, getopt
port = '/dev/ttyS0'
debug = True

global ending
global initial
global hasConfigured 
global hasErased
global x


def main(argv):
	initial = True
	hasConfigured = False
	ending = False
	hasErased = False
	debug = False
	x = 1
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
				
			
		else:
			print('usage: sudo python reset.py -h -d False')
				 
	ser = serial.Serial(port, 9600, timeout=1.0, rtscts=False)
	if(ser.isOpen() == False):
		ser.open()
		print("Opening port")
	else:
		print("Port already open")
	isNotResetting = True
	hasConnected = False
	while isNotResetting == True:
		
		if(hasConnected == False and debug == False and x < 4):
			
			print("Waiting for ROMMON/connection")
			x = x + 1
		elif(x == 4):
			print('Debug mode is not enabled, add "-d True" to your command to enable debug mode')
			print("Still waiting, connect at your leisure")
			x = x +1
		elif(debug == True and hasConnected == False):
			print("You are in debug mode!")
		theOutput = ser.readline()
		if(theOutput and debug == True):
			print(theOutput)
		if ("ROMMON" in theOutput and hasConnected == False):
			ser.sendBreak()
			hasConnected = True
			print('Booting into ROMMON')
					
		if("rommon 1" in theOutput):
			print("Initial config")
			ser.write('confreg 0x2141\r\n')
			time.sleep(1)
			ser.write('reset\r'.encode())
			print("Resetting")
	
		if("yes/no" in theOutput and "been modified" not in theOutput):
	
			print("Skipping system configuration utility")
			ser.write('no\r'.encode())
			print("Waiting on proper 	commandline")	
		elif("yes/no" in theOutput):
			ser.write('no\r'.encode())
			
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
		if("Router" in theOutput and initial == True and "(config)" not in theOutput and "Proceed with reload? [confirm]" not in theOutput):
			ser.write("configure terminal\r".encode())
	

			print("Entering terminal configuration")
	

		if('Router(config)'  in theOutput and hasConfigured == False and "Proceed with reload? [confirm]" not in theOutput):
			ser.write("config-register 0x2102\r".encode())
			try:
				ser.flushInput()
			except:
				print("different version of pyserial")
			time.sleep(2)
			ser.write("config-register 0x2102\r".encode())
			initial = False
			time.sleep(1)
			hasConfigured = True
			ser.write("end\r".encode())
		elif(initial and "Proceed with reload? [confirm]" not in theOutput and hasConfigured == True):
			ser.write("end\r".encode())
			initial = False

		if(ending == False and "(config)" in theOutput and "Proceed with reload? [confirm]" not in theOutput):
			print("Almost done")
			ser.write("end\r".encode())
			ending = True
		if(initial == False and "(config)" not in theOutput and "Router#" in theOutput and "[confirm]" not in theOutput and "of nvmram: complete" not in theOutput and hasErased == False):
			ser.flushInput()
			time.sleep(2)
			ser.write("write erase\r".encode())
			time.sleep(1)
			ser.write("\r".encode())
			ser.flushInput()	
			hasErased = True
		if("Initialized the geometry" in theOutput and hasErased == True):
			ser.flushInput()
			ser.write("reload\r".encode())
				
		if("Proceed with reload? [confirm]" in theOutput and hasErased == True):
			ser.flushInput()
			ser.write("\r".encode())
			ser.flushInput()
			ser.write(b"\rL1\r")
			time.sleep(5)
			print("Erased! Bye!")
			sys.stdout.write('\a')
			sys.stdout.flush()
			print('\a')
			time.sleep(2)
			ser.close()
			sys.exit()
			

if __name__ == "__main__":
	main(sys.argv[1:])

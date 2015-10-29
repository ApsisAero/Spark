import serial, thread, sys, datetime, itertools

ZERO_PRECISION = 100
SERIAL_BAUD = 9600
SERIAL_PORT = "/dev/cu.usbmodem1028921"

def input_thread(L):
	raw_input("Running. Press enter to end test.")
	L.append(None)

def main():
	try:
		teensy = serial.Serial(SERIAL_PORT,SERIAL_BAUD)
		print "Successfully connected to Spark board."
	except OSError:
		print "Could not find Spark board.  Verify connection."
		return

	raw_input("Press enter to zero the load cell.")
	sys.stdout.write("Zeroing ")

	spinner = itertools.cycle(['-', '/', '|', '\\'])

	n = 0
	subThrust=0.0;
	for i in range(ZERO_PRECISION):
		subThrust += float(teensy.readline().split(",")[1])
		if n%(ZERO_PRECISION/10) == 0:
			sys.stdout.write(spinner.next())
			sys.stdout.flush()
			sys.stdout.write('\b')
	subThrust /= ZERO_PRECISION

	passcode = raw_input('complete. Type passcode to launch: ')
	if passcode != 'spark':
		print "Passcode incorrect.  Exiting."
		return

	firstReadVal = teensy.readline().split(",")
	subMils = long(firstReadVal[0])

	teensy.write("i".encode('ascii'))

	wFile = open(sys.argv[1],"w")
	wFile.write("Generated "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				+"\nTime (ms),Thrust (lb)\n")

	L = []
	thread.start_new_thread(input_thread, (L,))
	while True:
		readVal = teensy.readline().split(",")

		time = str(long(readVal[0])-subMils)
		val = str(float(readVal[1])-subThrust)

		wFile.write(time+","+val+"\n")

		if L: break

	teensy.write("o".encode('ascii'));
	wFile.close()

main()
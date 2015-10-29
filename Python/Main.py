import serial, thread, sys, datetime

ZERO_PRECISION = 20

def input_thread(L):
	raw_input("Running. Press enter to end test.")
	L.append(None)

def main():
	try:
		teensy = serial.Serial("/dev/cu.usbmodem1028921",9600)
	except OSError:
		print "Could not find Spark board.  Verify connection."
		return

	raw_input("Press enter to zero the load cell.")

	subThrust=0.0;
	for i in range(ZERO_PRECISION):
		subThrust += float(teensy.readline().split(",")[1])
	subThrust /= ZERO_PRECISION

	passcode = raw_input('Type passcode to launch: ')
	if passcode != 'spark':
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
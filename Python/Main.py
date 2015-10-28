import time, serial, thread, sys, datetime

def input_thread(L):
    raw_input()
    L.append(None)

def main():
	storedVals = []
	storedTimes = []
	teensy = serial.Serial('/dev/cu.usbmodem1028921',9600)

	passcode = raw_input('Type passcode to launch: ')

	if passcode != 'spark':
		return

	teensy.write("i".encode('ascii'))

	firstReadVal = teensy.readline().split(",")
	subMils = float(readVal[0])

	L = []
	thread.start_new_thread(input_thread, (L,))
	while True:

		readVal = teensy.readline().split(",")

		storedTimes.append(float(readVal[0])-subMils)
		storedVals.append(float(readVal[1]))

		if L: break

	teensy.write("o".encode('ascii'));
	wFile = open(sys.argv[0],"w")

	wFile.write("Generated " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 + "\n")

	for t,v in zip(storedTimes,storedVals):
		wFile.write(str(storedTimes)+","+str(storedVals)+"\n")


	wFile.close()

main()
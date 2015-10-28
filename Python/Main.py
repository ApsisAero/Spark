import numpy as np
import time, serial, thread

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

	L = []
	thread.start_new_thread(input_thread, (L,))
	while True:

		readVal = teensy.readline().split(",")

		storedTimes.append(float(readVal[0]))
		storedVals.append(float(readVal[1]))

		if L: break

	teensy.write("o".encode('ascii'));

main()
from easygui import *
import serial, threading, datetime

ZERO_PRECISION = 100
SERIAL_BAUD = 9600
SERIAL_PORT = "/dev/cu.usbmodem1028921"
GUI_TITLE = "Spark Control GUI"

die = False

def dieThread():
	while not die:
		readVal = teensy.readline().split(",")
		time = str(long(readVal[0])-subMils)
		val = str(float(readVal[1])-subThrust)
		wFile.write(time+","+val+"\n")
	teensy.write("o".encode('ascii'));
	wFile.close()

def main():
	global teensy,subMils,subThrust,wFile

	if not msgbox("Connect to Spark board?",GUI_TITLE):
		return

	try:
		teensy = serial.Serial(SERIAL_PORT,SERIAL_BAUD)
	except OSError:
		msgbox("Could not find Spark board, please verify connection.",GUI_TITLE)
		return

	teensy.write("c".encode('ascii'))

	if not msgbox("Successfully connected to the Spark board.\nClick OK to zero the load cell.",GUI_TITLE):
		return

	teensy.write("y".encode('ascii'))

	subThrust=0.0;
	for i in range(ZERO_PRECISION):
		subThrust += float(teensy.readline().split(",")[1])
	subThrust /= ZERO_PRECISION

	teensy.write("z".encode('ascii'))

	fileName = enterbox("Input the output results filename.",GUI_TITLE)
	if fileName == None:
		return;
	fileName += ".csv"

	while not enterbox("Enter the passcode to launch.",GUI_TITLE) == "spark":
		msgbox("Incorrect passcode.  Exiting.",GUI_TITLE)
		return

	firstReadVal = teensy.readline().split(",")
	subMils = long(firstReadVal[0])

	teensy.write("i".encode('ascii'))

	wFile = open(fileName,"w")
	wFile.write("Generated "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				+",Motor Weight: "+str(subThrust)+"lb\nTime (ms),Thrust (lb)\n")

	global die
	threading.Thread(target=dieThread).start()
	die = msgbox("Running.  Press OK to end the test.",GUI_TITLE)

main()

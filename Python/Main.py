import serial
import numpy as np
import matplotlib.pyplot as plt

storedVals = []
teensy = serial.Serial('/dev/cu.usbmodem1028921',9600)


def liveVisual():
	plt.ion()
	ydata = [0] * 100
	ax1=plt.axes()
	line, = plt.plot(ydata)
	plt.ylim([0,10])

	while True:
		readVal = float(teensy.readline())
		storedVals.append(readVal)

		ymin = float(min(ydata))-10
		ymax = float(max(ydata))+10
		plt.ylim([ymin,ymax])
		ydata.append(readVal)
		del ydata[0]
		line.set_xdata(np.arange(len(ydata)))
		line.set_ydata(ydata)
		plt.draw()
		plt.pause(.001)

liveVisual()
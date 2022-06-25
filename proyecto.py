from twisted.internet import task					#librerias reactor para trabajar con ciclos de tiempo
from twisted.internet import reactor				#
import serial 										#libreria puerto comunicacion GPS
import time 										#libreria con metodos de tiempo
import string 										#libreria para trabajar los datos ASCII
import pynmea2
import os
from csv import reader

while True:
	port="/dev/ttyAMA0"
	ser =serial.Serial(port, baudrate=9600, timeout=1)
	dataout=pynmea2.NMEAStreamReader()
	newdata=ser.readline()
	
	if newdata[0:6] == "$GPRMC":
		newmsg=pynmea2.parse(newdata)
		lat=newmsg.latitude
		lng=newmsg.longitude
		os.system('rtl_power -f 400M:475M:8k -g 50 -1 -e 10s /media/pi/GABINO/datost.scv')
		time.sleep(5)
		with open('/media/pi/GABINO/datost.scv','r') as csv_file:
			csv_reader = reader(csv_file)
			listadatos = list(csv_reader)
			
			print "\n Tomando Datos . . . \n"							
			gps = "Latitud = " + str(lat) + " Longitud = " + str(lng) + " fecha: " + time.strftime("%x") + " hora: " + time.strftime("%X")
			
			with open('/media/pi/GABINO/Datos.scv','a') as file:
				file.write("\n")
				file.write(gps)
				file.write("\n")
				for line in listadatos:
					file.write("\n")
					for cell in line:
						file.write(cell)
		time.sleep(5)


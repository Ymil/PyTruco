'''Cliente de truco
05-01-15 04:09
Lautaro Linquiman'''
from socket import socket
from time import sleep

#debuggin
debuggin = 0
import sys
import traceback
#debuggin

from controlador import Controlador
from vista import Vista
c = Controlador()
v = Vista()
x = 0

while(1 == 1):
	try:
		s = socket()
		s.connect(('localhost',9999))		
		while 1 == 1:
			msgServidor = s.recv(1024)
			status = c.getStatus()		
			response = c.response(msgServidor)
			if(debuggin):
				print ('%d msg: %s\nresponse: %d\nstatus: %d') % (x, msgServidor, response, status)
				x = x + 1
			#print response
			if(response == 1):
				msgSend = raw_input(">")
				s.send(msgSend)				
			if(status == 1):		
				print msgServidor
			elif(status == 2):
				c.setCartas(msgServidor)
				print(v.mostrarCartas(c.getCartas()))
			sleep(.02)
		s.close()
	except Exception as error:
		print("Ocurrio un error con la conexion!")
		print("%s") % "\n"*10
		print("Reconectando...")
		if(debuggin):
			traceback.print_exc(file=sys.stdout)
		sleep(5)
		
	
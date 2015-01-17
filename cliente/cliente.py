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
c = Controlador(0)
v = Vista()
x = 0
timing = .02
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
				x =   x + 1
			if(response == 1 or response == 4):
				msgSend = raw_input(">")
				s.send(msgSend)
			
			if(response >= 1):
				continue
				
			#print response
						
			if(status == 1):		
				print msgServidor
			elif(status == 2):
				print('Obteniendo Cartas')
				c.setCartas(msgServidor)				
				print(v.mostrarCartas(c.getCartas()))
			sleep(timing)
		s.close()
	except Exception as error:
	    print('%s') % ('#' * 50)
	    print("Ocurrio un error con la conexion!")
	    print("Reconectando...")
	    print('%s') % ('#' * 50)
	    if(1 == 1):
	        traceback.print_exc(file=sys.stdout)
	    
	    sleep(5)
		
	

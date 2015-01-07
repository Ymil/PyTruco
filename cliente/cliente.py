'''Cliente de truco
05-01-15 04:09
Lautaro Linquiman'''
from socket import socket
from time import sleep
while(1 == 1):
	try:
		s = socket()
		s.connect(('localhost',9999))
		statusMsg = 0
		while 1 == 1:
			msgServidor = s.recv(1024)
			if(msgServidor[0] == "["):
				1+1
			elif(statusMsg == 1):
				print msgServidor
				
			if(msgServidor == "[msg]"):
				statusMsg = statusMsg + 1
				if(statusMsg == 2):
					statusMsg = 0
					
			elif(msgServidor == '[get]'):
				msgSend = raw_input(">")
				s.send(msgSend)
				
		s.close()
	except Exception as error:
		print("Ocurrio un error con la conexion!")
		print("%s") % "\n"*10
		print("Reconectando...")
		sleep(5)
		
	
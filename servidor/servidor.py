'''Servidor de truco
05-01-15 04:05
Lautaro Linquiman'''
import threading
from time import sleep
from socket import socket
print('------------------ Iniciando Servidor -------------------')
print('------------------Esto puede tardar un momento-----------')
s = socket()
s.bind(('localhost', 9999))
print('------------------Servidor Operativo  -------------------')

s.listen(1)
jugadores = []
status = []
conexiones = []
threadsEscucha = []

timing = .01
def escuchar():
	print('------------------ Servidor En Escucha ------------------')
	conN = 0
	while 1 == 1:		
		sc, addr = s.accept()
		conexiones.append((sc,addr))
		#print('%s') % conexiones
		threadsEscucha.append(threading.Thread(target=escucharMsg,args=(sc,conN,)))
		threadsEscucha[conN].start()		
		conN = conN + 1
		print(addr)
		sleep(.02)
		
		
def escucharMsg(con,idCon):
	try:
		con.send('[msg]')
		sleep(timing)
		con.send('Bienvenido a PyTruco\nNesecitamos que ingreses tu nombre de usuario')
		sleep(timing)
		con.send('[msg]')
		sleep(timing)
		con.send('[get]')
		status.append(0)
		print(status[idCon] == 0)
		while 1 == 1:			
			if(status[idCon] == 0):
				msg = con.recv(1024)
				jugadores.append([idCon,con,msg])	
				con.send('[msg]')
				sleep(timing)
				con.send('Excelente %s, en este momento te estamos ubicando'% msg)
				con.send('Espere un momento...')				
				sleep(timing)
				con.send('[msg]')
			sleep(.02)
			print("Mensaje de id(%d): %s") % (idCon, msg)
	except Exception as error:
		print("%s") % error
		
def juego():
	while( 1 == 1 ):
		if(len(jugadores) == 2):
			print ( ' Si! Hay dos jugadores ! ')
			print ( ' Armando mesa para %s ' ) % jugadores
			for(jugador in jugadores):
				jugador[1].send('[msg]')
				sleep(timing)
				jugador[1].send('La mesa ya esta armada')
				jugador[1].send('Espera un momento...')
				sleep(timing)
				jugador[1].send('[msg]')
			break
		sleep(5)
jg = threading.Thread(target=juego)
jg.start()
es = threading.Thread(target=escuchar)
es.start()


	

'''Servidor de truco
05-01-15 04:05
Lautaro Linquiman'''
import threading


import controlador
import modelo

from cartas import cartas
from jugador import Jugador
#debuggin
import sys
import traceback
debuggin = 1
#debuggin
from time import sleep
from socket import socket
print('------------------ Iniciando Servidor -------------------')
print('------------------Esto puede tardar un momento-----------')
s = socket()
s.bind(('localhost', 9999))
print('------------------Servidor Operativo  -------------------')

s.listen(1)
jugadores = []
status = {} #Define el estado de una conexion
conexiones = {}
threadsEscucha = []

c = controlador.Controlador()
m = modelo.Modelo()
j = {}

cartas_ = cartas(2) #Cartas

timing = .02

def escuchar():
	print('------------------ Servidor En Escucha ------------------')
	idCon = 0 #Asignador de ids de conexion
	while 1 == 1:		
		sc, addr = s.accept()		
		conexiones[idCon] = {'sc':sc,'addr':addr}		
		threadsEscucha.append(threading.Thread(target=escucharMsg,args=(sc,idCon,))) #Se inicia la escucha al cliente de forma continua
		threadsEscucha[idCon].start()		
		id = c.nuevaConexion(sc,addr)		
		j[idCon] = Jugador(id)
		idCon = idCon + 1
		sleep(.02)
		
'''
Status = 0. Obitiene el nombre del jugador 
'''	
def escucharMsg(con,idCon):
	try:
		for msgs in m.bienvenida():
			con.send(msgs)
			sleep(timing)			
		j[idCon].setStatus(0)
		con.send(c.obtener()) #Consulta el nombre
		while 1 == 1:			
			if(j[idCon].getStatus() == 0):
				msg = con.recv(1024)
				registro = c.regNick(msg,j[idCon].getId())
				if(registro == 0):
					for msgs in m.errorNick():
						con.send(msgs)
						sleep(timing)	
					con.send(c.obtener())
				else:
					for msgs in m.okNick():
						con.send(msgs)
						sleep(timing)
				
			sleep(.02)
			#print("Mensaje de id(%d): %s") % (idCon, msg)
	except Exception as error:
		traceback.print_exc(file=sys.stdout)
		#sys.exit()
		
def juego():
	while( 1 == 1 ):
		estadoDelJuego = c.getStatus()
		if(estadoDelJuego == 0):
			if(c.contarJugadores() == 1):
				print ( ' Si! Hay dos jugadores ! ')
				print ( ' Armando mesa para %s ' ) % jugadores
				for msg in m.mesaArmada():
					for jugador in c.jugadores: #Envia el mensaje a todos los jugadores
						c.jugadores[jugador]['sc'].send(msg)
					sleep(timing)
				c.setStatus(1)
		elif(estadoDelJuego == 1): #Mesa de juego armada todo Listo para iniciar ( Al pedo ... )
			c.setStatus(2)
			continue
		elif(estadoDelJuego == 2):
			cartasJugadores = ()
			cartasJugadores = cartas_.repartir()
			if(debuggin):
				print cartasJugadores	
			idCartas = 0
			for jugador in c.jugadores:				
				if(debuggin):
					print('Cartas Jugador(%d)-idCartas(%d): %s') % (jugador,idCartas,cartasJugadores[idCartas])
				for msg in m.darCartas(cartasJugadores[idCartas]):
					c.jugadores[jugador]['sc'].send(msg)						
					sleep(timing)
				idCartas = idCartas + 1				
		if(estadoDelJuego == 0):
			sleep(5)
		else:
			sleep(20)
jg = threading.Thread(target=juego)
jg.start()


es = threading.Thread(target=escuchar)
es.start()


	

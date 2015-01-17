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
while(1 == 1):
    try:
        s = socket()
        s.bind(('localhost', 9999))
        break
    except Exception:
        print('Error de conexion')
        print('Intentado reconectar en 5 segundos')
        sleep(5)
        continue
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
				j[idCon].setStatus(1)
				if(msg == "adios"):
				    adios()
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
			juegoActivo = 1
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
			numeroRonda = 1
			while(1 == 1):
			    if(debuggin):
			        print ('Anunciando primera ronda')
			    for msg in m.anunciarRonda(numeroRonda):
			        '''Indica el numero de ronda de la partida'''
			        if(debuggin):
			            print msg
			        for jugador in c.jugadores:      
			            c.jugadores[jugador]['sc'].send(msg)
			            sleep(timing)
			        sleep(timing)
				manoDeJuego = c.getTurnoID() #Obtiene el id del primer jugador de l partida
				contrincanteDeJuego = c.getSiguienteTurnoID() #Obtiene el id del contrincante de partida
				conJugador1 = c.jugadores[manoDeJuego]['sc'] #Obtiene la conexion del jugador1
				conJugador2 = c.jugadores[contrincanteDeJuego]['sc'] #Obtiene la conexion del jugador2
				while(1 == 1):													
					try:
						for msg in m.indicarTurno():
							conJugador1.send(msg)
							sleep(timing)
						conJugador1.send(c.obtenerJugada())
						jugada = int(esperarRespuesta(manoDeJuego)) #obtiene la carta o jugada
						cartaJugada = cartas_.obtener(manoDeJuego,jugada)
						print("El jugador %d jugo la carta %s") % (manoDeJuego, cartaJugada)
						for jugador in c.jugadores:
						    for msg in m.mostrarCarta(cartaJugada,manoDeJuego):
						        c.jugadores[jugador]['sc'].send(msg)
						        sleep(timing)						
						break
					except TypeError:
						for msg in m.errorJugada():
							conJugador1.send(msg)
							sleep(timing)
						conJugador1.send(c.obtenerJugada())
						continue
						
				while(1 == 1):
					try:
						for msg in m.indicarTurno():
							conJugador2.send(msg)
							sleep(timing)
						conJugador2.send(c.obtenerJugada())
						jugada = int(esperarRespuesta(contrincanteDeJuego)) #obtiene la carta o jugada
						cartaJugada = cartas_.obtener(contrincanteDeJuego,jugada)
						print("El jugador %d jugo la carta %s") % (contrincanteDeJuego, cartaJugada)
						for jugador in c.jugadores:
						    for msg in m.mostrarCarta(cartaJugada,manoDeJuego):
						        c.jugadores[jugador]['sc'].send(msg)
						        sleep(timing)
						break
					except TypeError:
						for msg in m.errorJugada():
							conJugador2.send(msg)
							sleep(timing)
						conJugador2.send(c.obtenerJugada())
						continue
				numeroRonda += 1
				if(numeroRonda == 4):
				    break	
		if(estadoDelJuego == 0):
			sleep(5)
		else:
			sleep(20)

def esperarRespuesta(id):
	msg = c.jugadores[id]['sc'].recv(1024)
	return msg
	
	
def adios():
    s.close()
    sys.exit()
jg = threading.Thread(target=juego)
jg.start()


es = threading.Thread(target=escuchar)
es.start()


	

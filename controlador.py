''' Clase Controlador 
06-01-2015
Programador: Lautaro Linquiman
'''
import vista
from random import randrange

class cartas():
	'''Clase Hija encargada de manejar las cartas, acomplada al controlador'''
	def __init__(self,cantidadJugadores):
		self.cantidadJugadores = cantidadJugadores
		print('Clase cartas iniciada')
		self.cartas = ['oro_1','oro_2','oro_3','oro_4','oro_5','oro_6','oro_7','oro_10','oro_11','oro_12',
		'espada_1','espada_2','espada_3','espada_4','espada_5','espada_6','espada_7','espada_10','espada_11','espada_12',
		'basto_1','basto_2','basto_3','basto_4','basto_5','basto_6','basto_7','basto_10','basto_11','basto_12',
		'copa_1','copa_2','copa_3','copa_4','copa_5','copa_6','copa_7','copa_10','copa_11','copa_12']
	
	def repartir(self):
		#print 'Hola'
		print('Repartiendo carta')
		cartasJugadores = [] #Cartas de los juegador repartidas
		for x in range(self.cantidadJugadores): #Recorre cada uno de los jugadores
			cartasJugador = [] #Acomoda las cartas de cada jugador			
			for c in range(3): #reparte las tres cartas a cada jugadores				
				carta = randrange(0,len(self.cartas) - 1)
				cartaValor = self.cartas[carta]
				cartasJugador.append(cartaValor)
				self.cartas.remove(cartaValor)				
			cartasJugadores.append(cartasJugador)		
		print('Cartas Repartidas a jugar!')
		return cartasJugador
	
class controlador():
	def __init__(self):
		self.cantidadJugadores = 0
		self.nombres = ()
		self.v = vista.vista() #Se carga la vista para la comunicacion
		
		
	def iniciarJuego(self, cantidadJugadores, nombres):
		'''Carga las variables nesesarias para iniciar el juego'''
		print(" *** Iniciando truco *** ")	
		'''self.getCantidadJugadores()
		self.getNombres()'''
		self.nombres = nombres 
		try:
			self.cantidadJugadores = int(cantidadJugadores)
		except:
			print('La cantidad de jugadores que ingreso no es un numero')
		try:
			if (self.cantidadJugadores % 2 == 0 and len(self.nombres) == self.cantidadJugadores):
				self.v.iniciar(self.cantidadJugadores, self.nombres)
				self.jugar()
				return (self.cantidadJugadores, (self.nombres))
			else:
				print("Error: La cantidad de jugadores puede ser 2 , 4 o 6")	
				return 0
		except Exception as error:
			print("%s") % error
			return 0
		return 0
		
		
	def jugar(self):
		'''Comenzemos a jugar'''
		self.cartas = cartas(self.cantidadJugadores) #Se carga la clase cartas para iniciar el juego
		self.cartas.repartir()
		
		
	def getCantidadJugadores(self):
		''' Obtiene la cantidad de jugadores que habra en la partida '''
		self.cantidadJugadores = raw_input("Ingrese la cantidad de jugador ( 2 , 4 , 6 ): \n")
		try:
			self.cantidadJugadores = int(self.cantidadJugadores)
		except:
			print('La cantidad de jugadores que ingreso no es un numero')
			self.getCantidadJugadores()
			
			
	def getNombres(self):
		''' Obtiene los nombres de los jugadores que habra en la partida '''
		self.nombres = raw_input("Ingrese los nombres de los jugadores separados por comas (Juan,Pedro): \n")
		self.nombres = self.nombres.split(",")
		#print("%s %d") % (self.nombres, len(self.nombres)) #Prueba de ingreso
		if(len(self.nombres) == 0):
			print("No ingresastes ningun nombre!!")
			self.getNombres()
		

		
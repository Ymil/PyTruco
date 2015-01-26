'''
Clase Cartas del juego
06-01-2015
Programador: Lautaro Linquiman
'''
from random import randrange

class Cartas():
	'''Clase encargada de el manejo de las cartas del juego'''
	def __init__(self,cantidadJugadores, debuggin = 1):
		self.debuggin = debuggin		
		
		if(self.debuggin):
			print('Clase cartas iniciada')
			
		self.cantidadJugadores = cantidadJugadores	
		self.cartas = ['oro_1','oro_2','oro_3','oro_4','oro_5','oro_6','oro_7','oro_10','oro_11','oro_12',
		'espada_1','espada_2','espada_3','espada_4','espada_5','espada_6','espada_7','espada_10','espada_11','espada_12',
		'basto_1','basto_2','basto_3','basto_4','basto_5','basto_6','basto_7','basto_10','basto_11','basto_12',
		'copa_1','copa_2','copa_3','copa_4','copa_5','copa_6','copa_7','copa_10','copa_11','copa_12']
		self.clonCartas = []
		self.cartasRepartidas = []
		
		self.cartasJugador = [] #Almacena las cartas de los jugadores
	
	def __clonarCartas(self):
		self.clonCartas = self.cartas[:]
	
	
	#def obtener(self, cartasN):
		
	def obtener(self, jugadorID,cartaID):
		return self.cartasJugadores[jugadorID-1][cartaID-1]
	
	def repartir(self):
		''' Return list ((1,2,3),(1,2,3))'''
		
		self.__clonarCartas()
		
		#debuggin
		if(self.debuggin):
			print('Repartiendo carta')
		#debuggin
		
		cartasJugadores = [] #Cartas de los juegador repartidas
		for x in range(self.cantidadJugadores): #Recorre cada uno de los jugadores
			
			#debuggin
			if(self.debuggin):
				print(x)
			#debuggin
			
			cartasJugador = [] #Acomoda las cartas de cada jugador	
			
			for c in range(3): #reparte las tres cartas a cada jugadores				
				carta = randrange(0,len(self.clonCartas) - 1)
				cartaValor = self.clonCartas[carta]
				cartasJugador.append(cartaValor)
				self.clonCartas.remove(cartaValor)				
			cartasJugadores.append(cartasJugador)	
			
			cartasJugador = None
			
		#debuggin
		if(self.debuggin):
			print('Cartas Repartidas a jugar!')
			print(cartasJugadores)
		#debuggin
		
		self.cartasJugadores = cartasJugadores
		return cartasJugadores

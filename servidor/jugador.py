'''
clase Jugador Servidor
09-01 06:24
Lautaro Linquiman
'''

class Jugador():
	def __init__(self, id):
		self.idJugador = id #IdCon
		self.status = 0
		self.nombre = ''
		self.cartas = [] #Almacena las cartas del jugador
		self.cartasJugadas = [] #Almacena las cartas que el jugador ya jugo
		self.ultimaCartaJugada = 0 #Almacena el id de la ultima carta jugada

	def setName(self, nombre):
		self.nombre = nombre
		
	def getName(self):
		''' Devuelve el nombre del jugador '''
		return self.nombre
	
	def getID(self):
		'''devuelve el id (IDCON) del jugador '''
		return self.idJugador
	
	def setCartas(self, cartas):
		''' Se ingresan la cartas que les da el juego '''
		self.resetCartas()
		self.cartas = cartas	
	
	def resetCartas(self):
		self.cartas = []
		self.cartasJugadas = []
		self.ultimaCartaJugada = 0
		
	def jugarCarta(self, cartaID):
		''' Corrobora que las cartas del jugador sea valida y la juega '''
		carta = self.cartas[cartaID]
		if(carta in self.cartasJugadas):
			return 0
		else:
			self.cartasJugadas.append(carta)
			self.ultimaCartaJugada = cartaID
			return 1
		
	def getCartaJugada(self):
		''' Devuelve el nombre completa de la ultima carta jugada '''
		return self.cartas[self.ultimaCartaJugada]
		
	def setStatus(self, valor):
		self.status = valor
	
	def getStatus(self):
		return self.status
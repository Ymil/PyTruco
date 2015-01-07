''' Clase Vista 
06-01-2015
Programador: Lautaro Linquima
'''

class vista:
	''' Clase encargada de la interaccion con el y los jugadores '''
	def __init__(self):
		pass
		'''self.cantidadJugadores = 0
		self.nombres = ()'''
		
	def iniciar(self, cantidadJugadores, nombres):
		self.cantidadJugadores = cantidadJugadores
		self.nombres = nombres
		print ( " Hay %d jugadores y se llaman %s" ) % ( self.cantidadJugadores,  ','.join(self.nombres) )
		
	def mostrarCartas(cartas)
		#Muestra las cartas al jugadores
		cartas = ''
		nCartas = 1 #Numero de carta
		for carta in cartas:
			if( nCartas == 1 ):
				cartas = '%d: %s' % ' '.join(carta.split("_"))
			else:
				cartas = '%s\n%d: %s' % (cartas, ' '.join(carta.split("_")))
		print('%s') % cartas
		return
'''
clase Jugador Servidor
09-01 06:24
Lautaro Linquiman
'''

class Jugador():
	def __init__(self, id):
		self.idJugador = id
		self.status = 0
		self.nombre = ''

	def setName(self, nombre):
		self.nombre = nombre
		
	def getName(self):
		return self.nombre
	
	def getID(self):
		return self.idJugador
	
	def setStatus(self, valor):
		self.status = valor
	
	def getStatus(self):
		return self.status
'''
Controlador de jugador PyTruco
09-01-2015 Son las 3 de la manana
Lautaro Linquman
'''

class Controlador:
	def __init__(self):
		self.id = 0
		self.nombre = ''
		self.cartas = []
		self.puntaje = 0
		
		self.status = 0
		
		
	def response(self, cmds):		
		if(cmds == '[msg]'):
			if(self.getStatus() == 0):
				self.setStatus(1)
			else:
				self.setStatus(0)
			return 2
		elif(cmds == '[cartas]'):
			if(self.getStatus() == 0):
				self.setStatus(2)
			else:
				self.setStatus(0)
			return 3
		elif(cmds == '[get]'):
			return 1
		else:
			self.setStatus(0)
			return 0
		
	#cartas
	def setCartas(self, cartas):
		self.cartas = cartas.split(',')
		
	def getCartas(self):
		return self.cartas
	#cartas
	
	#jugadas

	#jugadas
	
	#Status		
	def getStatus(self):
		return self.status
	
	def setStatus(self, status):
		self.status = status
	#Status
		
		
'''
Modelo de servidor
09-01 06:11
Lautaro Linquiman
'''
from cmds import cmds
class Modelo(cmds):
	def bienvenida(self):	
		return self.enviarMsg('Bienvenido a PyTruco\nNesecitamos que ingreses tu nombre de usuario')
	
	def darCartas(self,cartas):
		return self.enviarCartas(cartas)
	
	def mesaArmada(self):
		return self.enviarMsg("La mesa ya esta armada\nEspere un momento")
	
	def errorNick(self):
		return self.enviarMsg('Deves ingresar un nombre')
	
	def okNick(self):
		return self.enviarMsg('Excelente! Ahora espera a que encontremos a otro jugador disponible')
	
	
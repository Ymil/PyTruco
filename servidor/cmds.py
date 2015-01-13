''' Clase de Cmds
Controlar de cliente por comandos
09-01 son las 17:44 Hs
Lautaro Linquiman'''

class cmds:
	def enviarMsg(self,texto):
		''' Return List '''
		return ('[msg]',texto,'[msg]')

	def enviarCartas(self,cartas):
		cartas = ','.join(cartas)
		return ('[cartas]',cartas,'[cartas]')
	
	def indicarMano(self):
		return '[mano]'
	
	def errorJugada(self):
		return ('[errorj]')
	
	def obtener(self):
		return '[get]'
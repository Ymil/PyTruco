''' Clase de Cmds
Controlar de cliente por comandos
09-01 son las 17:44 Hs
Lautaro Linquiman'''

class Cmds:
	def enviarMsgID(self,ID,params = ''):
		''' Return List '''
		if(len(params) > 0):
			msg = '[msg#%d(%s)]' % (ID,params.join(','))
		else:
			msg = '[msg#%d]' % ID
			
		return msg

	def enviarCartas(self,cartas):
		cartas = ','.join(cartas)
		return ('[cartas]',cartas,'[cartas]')

	
	def indicarMano(self):
		return '[mano]'
	
	def errorJugada(self):
		return ('[errorj]')
	
	def obtenerJugada(self):
		return '[getJugada]'
	
	def obtener(self):
		return '[get]'
	
	def okRegNick(self):
		return '[okRegNick]'
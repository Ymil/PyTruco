''' Clase de Cmds
Controlar de cliente por comandos
09-01 son las 17:44 Hs
Lautaro Linquiman'''

class Cmds:
	def enviarMsgID(self,ID,params = ()):
		''' Return List '''		
		if(len(params) > 0):
			if(type(params) == str):
				msg = '[msg#%d(%s)]' % (ID,params)
			else:
				msg = '[msg#%d(%s)]' % (ID,','.join(str(x) for x in params))
		else:
			msg = '[msg#%d]' % ID
			
		return msg

	def enviarCartas(self,cartas):
		cartas = ','.join(cartas)
		return '[cartas]%s[cartas]' % cartas

	def enviarAccion(self, accionID):
		return '[ac]%d[ac]' % accionID
	
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
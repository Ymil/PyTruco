'''
Vista del cliente Pytruco
11-01-15 12:51
Lautaro Linquiman
'''

class Vista:
	def __init__(self):
		pass
	
	def mostrarCartas(self, cartas):
		print ("Mostras cartas:%s") % cartas
		str = ''
		n = 1
		for carta in cartas:
			str += '%d - %s\n' % (n, carta)
			n += 1			
		return str
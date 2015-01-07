'''Truco Argentino
Programador: Lautaro Linquiman
Fecha: 20:49hs 05-01-14'''
import vista
import controlador
def saltosDeLinea():
	print '\n' * 100
def decorador(funcion):
	def nueva(*args):
		print ( "La Funcion %s ...\N" ) % funcion.__name__
		print ( "%s" ) % funcion(*args)
def main():
	#try:
	#saltosDeLinea()
	print('###################### - ####################')
	c = controlador.controlador()
	Djuego = c.iniciarJuego()
	if( Djuego == 0 ):
		print("[Error] La partida no puede iniciarze")
		return
	print('---------------------- # --------------------')
		#saltosDeLinea()
	'''except Exception as error:
		print '%s\n%s\n%s\n' % (type(error), error.args, error)'''
while( 0 == 0):
	main()
	
	
	

''' Clase Controlador 
06-01-2015
Programador: Lautaro Linquiman
'''
import vista

	
class controlador():
	def __init__(self):
		self.cantidadJugadores = 0
		self.nombres = ()
		self.v = vista.vista() #Se carga la vista para la comunicacion
		
		
	def iniciarJuego(self, cantidadJugadores, nombres):
		'''Carga las variables nesesarias para iniciar el juego'''
		print(" *** Iniciando truco *** ")	
		'''self.getCantidadJugadores()
		self.getNombres()'''
		self.nombres = nombres 
		try:
			self.cantidadJugadores = int(cantidadJugadores)
		except:
			print('La cantidad de jugadores que ingreso no es un numero')
		try:
			if (self.cantidadJugadores % 2 == 0 and len(self.nombres) == self.cantidadJugadores):
				self.v.iniciar(self.cantidadJugadores, self.nombres)
				self.jugar()
				return (self.cantidadJugadores, (self.nombres))
			else:
				print("Error: La cantidad de jugadores puede ser 2 , 4 o 6")	
				return 0
		except Exception as error:
			print("%s") % error
			return 0
		return 0
		
		
	def jugar(self):
		'''Comenzemos a jugar'''
		self.cartas = cartas(self.cantidadJugadores) #Se carga la clase cartas para iniciar el juego
		self.cartas.repartir()
		
		
	def getCantidadJugadores(self):
		''' Obtiene la cantidad de jugadores que habra en la partida '''
		self.cantidadJugadores = raw_input("Ingrese la cantidad de jugador ( 2 , 4 , 6 ): \n")
		try:
			self.cantidadJugadores = int(self.cantidadJugadores)
		except:
			print('La cantidad de jugadores que ingreso no es un numero')
			self.getCantidadJugadores()
			
			
	def getNombres(self):
		''' Obtiene los nombres de los jugadores que habra en la partida '''
		self.nombres = raw_input("Ingrese los nombres de los jugadores separados por comas (Juan,Pedro): \n")
		self.nombres = self.nombres.split(",")
		#print("%s %d") % (self.nombres, len(self.nombres)) #Prueba de ingreso
		if(len(self.nombres) == 0):
			print("No ingresastes ningun nombre!!")
			self.getNombres()
		

		
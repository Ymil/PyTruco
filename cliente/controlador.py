'''
Controlador de jugador PyTruco
09-01-2015 Son las 3 de la manana
Lautaro Linquman
'''
import re
import traceback
import sys
from msg import Msg
from time import sleep

class Controlador(Msg):
	def __init__(self, debuggin = 1):
		self.id = 0
		self.nombre = ''
		self.cartas = []
		self.puntaje = 0
		
		self.status = 0
		
		self.ultimoCmd = '' 
		
		#debuggin
		self.debuggin = debuggin
		#debuggin
		
		
	def response(self, cmds):
		'''Decodifica el mensaje enviado por el servidor
		Return 1: Mensaje [msg]
		Return 3: Cartas [cartas]
		Return 2: Obtiene [get]
		Return 4: Obtiene Jugada [getJugada]
		'''
		#sleep(.02)
		self.ultimoCmd = cmds
		if(re.match('\[msg#\d{1,10}\]', cmds) or re.match('\[msg#\d{1,10}\((.*)\)\]', cmds)):
			print('Recibiendo Mensaje'.center(50,'='))
			return 1
		elif(cmds == '[get]'):
			return 2
		elif(cmds == '[cartas]'):
			if(self.debuggin):
				print('[cartas]')
			if(self.getStatus() == 0):
				self.setStatus(2)
			else:
				self.setStatus(0)
			return 3		
		elif(cmds == '[getJugada]'):
			return 4
	
	def getMsgID(self):
		'''Decodifica y obtiene los ids de los mensajes y los parametros'''
		mo = re.match('\[msg#(.+)\]',self.ultimoCmd)
		mo1 = re.match('\[msg#(.+)\((.+)\)]',self.ultimoCmd)
		msgReturn = {'msg':'','params':''}
		if(mo1):
			msgReturn['msg'] = mo1.group(1)
			msgReturn['params'] = mo1.group(2)
		elif(mo):
			msgReturn['msg'] = mo.group(1)			
		return msgReturn
	
	def getMsg(self, params):
		print('Decodificando Mensaje'.center(50,' '))
		if(len(params['params']) > 0):
			try:
				msgID = int(params['msg'])
				params = params['params'].split(',')
				print params
				params = tuple(params)
				return self.mensaje[msgID] % params
			except Exception as error:
				#traceback.print_exc(file=sys.stdout)
				print('[ERROR] %s') % error
				return ''
		else:
			msgID = int(params['msg'])
			return self.mensaje[msgID]
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
		
		
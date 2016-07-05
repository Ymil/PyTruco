'''
Programa de ejecucion del servidor PyTruco
16-01-2015
Lautaro Linquiman
'''

import logging
import threading
logging.basicConfig(format='%(levelname)s [%(asctime)s][SVR]: %(message)s',filename='../logs/servidor.log')
import cservidor
import traceback
import threading
import sys
from time import sleep

servidor = cservidor.servidor()
servidor.iniciar()
if(servidor.getStatusConexion):
	print("Conexion establecida")
else:
	print("Ocurrio un error al intentar establecer conexion")

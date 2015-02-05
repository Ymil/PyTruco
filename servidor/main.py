'''
Programa de ejecucion del servidor PyTruco
16-01-2015
Lautaro Linquiman
'''
import cservidor
import traceback
import sys
try:
    s = cservidor.servidor()
    s.conectar()
except Exception:
    s.desconexionForzada()
    traceback.print_exc(file=sys.stdout)


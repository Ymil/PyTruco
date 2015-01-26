class Juego:
    ''' Clase controlador del Juego 
    20-01-15 05:07 Lautaro Linquiman'''
    def __init__(self, cantidadJugadores):
        self.status = 0
        self.cantidadJugadores = cantidadJugadores
        
    def getStatus(self):
        return self.status
    
    def setStatus(self,status):
        self.status = status
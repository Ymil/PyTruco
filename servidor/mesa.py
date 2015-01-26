class Mesa():
    def __init__(self, cantidadJugadores, creadaPor, mesaID):
        self.cantidadJugadores = cantidadJugadores
        self.creadaPor = creadaPor
        self.mesaID = mesaID
        self.jugadores = []
        self.status = 0
    
    def getInfo(self):
        return (self.mesaID, self.cantidadJugadores, len(self.jugadores), self.creadaPor)
    
    def getStatus(self):
        if(self.cantidadJugadores == len(self.jugadores)):
            self.status = 1
            return 1
        else:
            self.status = 0
            return 0
    
    def nuevoJugador(self, ID):
        self.jugadores.append(ID)
    
    def jugadores(self):
        return self.jugadores
    
    
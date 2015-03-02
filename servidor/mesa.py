class Mesa():
    def __init__(self, cantidadJugadores, creadaPor, mesaID):
        self.cantidadJugadores = cantidadJugadores
        self.creadaPor = creadaPor
        self.mesaID = mesaID
        self.jugadores = []
        self.equipoJugadores = []
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
        ''' ID: IDCon '''
        self.jugadores.append(ID)
        self.equipoJugadores.append(self.equipo)
        if(self.equipo == 1):
            self.equipo = 2
        else:
            self.equipo = 1
    
    def getJugadores(self):
        return self.jugadores
    
    def getEquipos(self):
        return self.equipoJugadores
    
    
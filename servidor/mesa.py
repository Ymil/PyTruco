class Mesa():
    def __init__(self, cantidadJugadores, creadaPor, mesaID):
        self.cantidadJugadores = cantidadJugadores
        self.creadaPor = creadaPor
        self.mesaID = mesaID
        self.jugadores = []
        self.equipoJugadores = []
        self.equipo = 1
        self.status = 0
    
    def getInfo(self):
        ''' Retorna informacion sobre la mesa '''
        return (self.mesaID, self.cantidadJugadores, len(self.jugadores), self.creadaPor)
    
    def getStatus(self):
        ''' Devuelve true si la cantidad de jugadores en la mesa es igual a la que se indico'''
        if(self.cantidadJugadores == len(self.jugadores)):
            self.status = 1
            return 1
        else:
            self.status = 0
            return 0
    
    def nuevoJugador(self, ID):
        
        ''' ID: IDCon 
        Ingresa un nuevo jugador a la mesa'''
        self.jugadores.append(ID)
        self.equipoJugadores.append(self.equipo)
        if(self.equipo == 1):
            self.equipo = 2
        else:
            self.equipo = 1
    
    def getJugadores(self):
        ''' Obitne las id de los jugadores '''
        return self.jugadores
    
    def getEquipos(self):
        '''Retorna la configuracion de equipos '''
        return self.equipoJugadores
    
    
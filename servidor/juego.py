from cartas import Cartas
class Juego():
    ''' Clase controlador del Juego 
    20-01-15 05:07 Lautaro Linquiman'''
    def __init__(self, jugadores, jEquipos):
        self.status = 0
        self.jugadores = jugadores
        self.jEquipos = jEquipos
        self.cantidadJugadores = len(jugadores) #Obtiene la cantidad de jugadores
        self.cartasJugador = []
        self.cartasJugadas = {}
        self.puntosEquipos = {1:0,2:0}
        self.equipoGanadorPrimeraRonda = 0    
        #self.primerJugadorPartida = 0  
        self.parda = 0        
        self.ronda = 0
        self.rondas = {}
        self.mano = 0,
        self.turno = 0
        self.c_ = Cartas(self.cantidadJugadores, 0)
        
    def getStatus(self):
        return self.status
    
    def setStatus(self,status):
        self.status = status
    
    def getTurno(self):
        ''' Obtiene el id del jugador que es mano '''
        print('Turno %d') % self.turno
        turno = self.jugadores[self.turno]
        self.cambiarTurno()
        return turno
    
    def cambiarTurno(self):
        ''' Cambia la mano del juego '''
        if(self.turno == self.cantidadJugadores):
            self.turno = 0
        else:
            self.turno += 1
    
    def setTurno(self, jugadorID):
        self.turno = self.jugadores.index(jugadorID)
        self.turno = self.turno - 1
    '''def sigTurnoJuego(self):
         Devuelve el turno siguiente al jugador actual
        self.turno += 1
        if(self.turno == self.cantidadJugadores):
            self.turno = 0        
        return self.jugadores[self.turno]'''
    
    def decCartaID(self, carta):
        ''' Valida que el valor ingresado por el jugador sea valido '''
        try:
            cartaID = int(carta)
            if(cartaID <= 3):
                return cartaID-1
            else:
                return 20
        except ValueError:
            return 20
    
    def iniciarRonda(self):
        ''' Inicia la ronda '''
        self.ronda += 1
        self.rondas[self.ronda] = []
        return self.ronda
    
    def getRonda(self):
        return self.ronda
             
    def repartirCartas(self):
        ''' Reparte la carta de los jugaodres '''
        self.cartasJugador = self.c_.repartir()
        return self.cartasJugador
    
    def darCartas(self, nJugador):
        self.cartasJugadas[nJugador] = []
        return self.cartasJugador[nJugador]
    
    def setCarta(self, jugadorID, cartaID):
        nRonda = self.getRonda()        
        self.rondas[nRonda].append((jugadorID, cartaID))
    
    def darPuntoEquipo(self, equipo, puntos):
        self.puntosEquipos[equipo] += puntos 
    
    def getPuntosEquipos(self):
        return self.puntosEquipos
    
    def obtenerGanador(self):
        nRonda = self.getRonda()
        cartaMayor = [0,0]
        cartasAnteriores = []
        parda = 0
        for ronda in self.rondas[nRonda]:
            dir(cartaMayor)
            #print(ronda)
            jugadorID = ronda[0]
            cartaSTR = ronda[1]
            puntajeCartaJugador = self.c_.cartasPuntaje[cartaSTR]
            if(len(cartasAnteriores) == 0):
                puntajeCartaMayor = 0
            else:
                if(self.parda):
                    puntajeCartaMayor = self.c_.cartasPuntaje[cartaMayor[0]]
                else:
                    puntajeCartaMayor = self.c_.cartasPuntaje[cartaMayor[1]]
                #puntajeCartaMayor = 0
            #puntajeCartaTotales = self.c_.cartasPuntaje[carta]
            cartasAnteriores.append(1)
            if(puntajeCartaJugador > puntajeCartaMayor):
                cartaMayor = (cartaSTR, jugadorID)
                parda = 0
            elif(puntajeCartaJugador == puntajeCartaMayor):
                cartaMayor = (cartaSTR)
                parda = 1
        if(parda == 1):
            ''' Hay una parda en la mesa '''
            if(self.ronda == 1):
                self.parda = 1
                return ('parda', cartaMayor[0])
            elif(self.ronda == 2 and self.parda == 1):
                return ('parda', cartaMayor[0])
            #elif(self.ronda == )
            else:
                return ('win', self.equipoGanadorPrimeraRonda)
        else:
            if(self.ronda == 1):
                jPos = cartaMayor[1]
                self.equipoGanadorPrimeraRonda = self.jEquipos[jPos]
                self.setTurno(jPos)
                return ('continue', cartaMayor[0], cartaMayor[1])
            elif(self.ronda == 2 or self.ronda == 3):
                equipoWinPrimeraRonda = self.equipoGanadorPrimeraRonda
                jPos = cartaMayor[1] #Ganador de la ronda
                equipoWinManoActual = self.jEquipos[jPos]
                if(equipoWinManoActual == equipoWinPrimeraRonda):
                    return ('win', self.equipoGanadorPrimeraRonda)
                else:
                    self.setTurno(jPos-1)
                    return ('continue', cartaMayor[0], cartaMayor[1])
            
                
            
                
        
        
                
        
        
                
    
    
                 
        
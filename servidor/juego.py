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
        self.equipoGanadorSegundaRonda = 0 
        #self.primerJugadorPartida = 0  
        self.parda = 0        
        self.ronda = 0
        self.rondas = {}
        self.mano = 0
        self.turno = 0
        self.c_ = Cartas(self.cantidadJugadores, 0)
        
    def getStatus(self):
        return self.status
    
    def setStatus(self,status):
        self.status = status
    
    def getTurno(self):
        ''' Obtiene el id del jugador que es mano '''
        print('[debuggin-getTurno-turno] %d') % self.turno
        if(self.turno == self.cantidadJugadores):
            self.turno = 0
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
        if(self.turno == self.cantidadJugadores):
            self.turno = 0
        self.turno = self.turno

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
        self.mano = self.getTurno()
        return self.ronda
    
    def resetRonda(self):
        self.ronda = 0
        
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
    
    def darPuntosEquipo(self, equipo, puntos):
        self.puntosEquipos[equipo] += puntos 
    
    def getPuntosEquipos(self):
        return self.puntosEquipos
    
    def obtenerGanador(self):
        print('[debuggin-obtenerGanador] Iniciando Funcion')
        nRonda = self.getRonda()
        cartaMayor = [0,0]
        
        '''
        cartaMayor[0] Indica la carta ganadora
        cartaMayor[1] Indica el IDjugador ganador
        '''

        parda = 0
        for ronda in self.rondas[nRonda]:
            print('[debuggin-obtenerGanador-ronda]',ronda)
            print('[debuggin-obtenerGanador-cartaMayor]',cartaMayor)
            #print(ronda)
            jugadorID = ronda[0]
            cartaSTR = ronda[1]
            print('[debuggin-obtenerGanador-cartaSTR]', cartaSTR)
            puntajeCartaJugador = self.c_.cartasPuntaje[cartaSTR]
            if(nRonda == 1):
                ''' Se setean la variables para iniciar el juego '''
                self.equipoGanadorPrimeraRonda = 0
                self.equipoGanadorSegundaRonda = 0
                self.parda = 0      
                        
            if(cartaMayor[0] == 0):
                puntajeCartaMayor = 0   
            else:                
                puntajeCartaMayor = self.c_.cartasPuntaje[cartaMayor[0]]
                       
            print('[debuggin-obtenerGanador-puntajeCartaJugador] %d') % puntajeCartaJugador
            print('[debuggin-obtenerGanador-puntajeCartaMayor] %d') % puntajeCartaMayor
            
            ''' Compara las cartas para determinar la carta mayor '''
            if(puntajeCartaJugador > puntajeCartaMayor):
                cartaMayor = (cartaSTR, jugadorID)
                parda = 0
            elif(puntajeCartaJugador == puntajeCartaMayor):
                cartaMayor = (cartaSTR)
                parda = 1
                
        if(self.ronda == 1):
            if(parda == 1):
                self.parda = 1
                return ('parda', cartaMayor[0])
            jPos = cartaMayor[1]
            self.equipoGanadorPrimeraRonda = self.jEquipos[jPos]
            self.setTurno(jPos)
            return ('continue', cartaMayor[0], cartaMayor[1])
        elif(self.ronda == 2):
            jPos = cartaMayor[1] #Ganador de la ronda
            equipoWinManoActual = self.jEquipos[jPos]                
            if(self.parda == 1):
                if(parda == 0):
                    return ('win', equipoWinManoActual)
                elif(parda == 1):
                    return ('parda', cartaMayor[0])
            self.equipoGanadorSegundaRonda = equipoWinManoActual
            if(equipoWinManoActual == self.equipoGanadorPrimeraRonda):
                return ('win', self.equipoGanadorPrimeraRonda)
            else:
                self.setTurno(jPos)
                return ('continue', cartaMayor[0], cartaMayor[1])
        elif(self.ronda == 3):                
            jPos = cartaMayor[1] #Ganador de la ronda
            equipoWinManoActual = self.jEquipos[jPos]
            if(self.parda == 1):
                if(parda == 0):
                    return ('win', equipoWinManoActual)
                elif(parda == 1):
                    return ('empate', cartaMayor[0], self.mano)
            print('[debuggon-obtenerGanador-equipoWinManoActual] %d') % equipoWinManoActual
            print('[debuggon-obtenerGanador-equipoGanadorPrimeraRonda] %d') % self.equipoGanadorPrimeraRonda
            print('[debuggon-obtenerGanador-equipoGanadorSegundaRonda] %d') % self.equipoGanadorSegundaRonda
            if(equipoWinManoActual == self.equipoGanadorPrimeraRonda):
                return ('win', self.equipoGanadorPrimeraRonda)
            elif(equipoWinManoActual == self.equipoGanadorSegundaRonda):
                return ('win', self.equipoGanadorSegundaRonda)
            
                
            
                
        
        
                
        
        
                
    
    
                 
        
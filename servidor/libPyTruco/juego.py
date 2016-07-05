from cartas import Cartas
from accionesJuego import AccionesJuego
import logging
logging.basicConfig(format='%(levelname)s [%(asctime)s][SVR]: %(message)s',filename='./logs/libjuego.log', level='DEBUG')
import inspect
import time
global cuentaEjecucion
cuentaEjecucion = 0
import string
def msg_debug(str1):
    global cuentaEjecucion
    #if(type(str1) is list):
    #    str1 = ' | '.join(tuple(list(str1))[0:])
    #print cuentaEjecucion
    str1 = 'EC %d' % cuentaEjecucion, str1
    #str1 = string.join(, ' ')
    logging.debug(str1)
    cuentaEjecucion += 1
class Juego:
    ''' Clase controlador del Juego
    20-01-15 05:07 Lautaro Linquiman'''
    def __init__(self, jugadores, jEquipos, mesaID):
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
        self.mesaID = mesaID
        self.parda = 0
        self.ronda = 0
        self.rondas = {}
        self.mano = 0
        self.turno = 0
        self.c_ = Cartas(self.cantidadJugadores, 0)
        self.actionGame = AccionesJuego()

    def setActionGame(self, classActionGame):
        self.actionGame = classActionGame()

    def getStatus(self):
        return self.status

    def setStatus(self,status):
        self.status = status

    def getTurno(self):
        ''' Obtiene el id del jugador que es mano '''
        msg_debug('[getTurno-turno] %d' % self.turno)
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
        self.turno = self.jugadores[jugadorID].getID()
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
        self.parda = 0
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
        nRonda = self.getRonda()
        cartaMayor = [0,0]

        '''
        cartaMayor[0] Indica la carta ganadora
        cartaMayor[1] Indica el IDjugador ganador
        '''

        parda = 0
        msg_debug('Ejecutando %s' % inspect.stack()[0][3])
        for ronda in self.rondas[nRonda]:
            msg_debug("Ronda %d" % self.ronda)
            msg_debug(cartaMayor)
            #print(ronda)
            jugadorID = ronda[0]
            cartaSTR = ronda[1]
            msg_debug('obtenerGanador-cartaSTR] %s' % cartaSTR)
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


            if(puntajeCartaJugador > puntajeCartaMayor):
                cartaMayor = (cartaSTR, jugadorID)
                parda = 0
            elif(puntajeCartaJugador == puntajeCartaMayor):
                cartaMayor = (cartaSTR)
                parda = 1
        msg_debug('Carta Mayor')
        msg_debug(cartaMayor)

        msg_debug("Parda %d" % parda)
        if(self.ronda == 1):
            if(parda == 1):
                self.parda = 1
                return ('parda', cartaMayor)
            jPos = cartaMayor[1]
            self.equipoGanadorPrimeraRonda = self.jEquipos[jPos]
            self.setTurno(jPos)
            return ('continue', cartaMayor[0], cartaMayor[1])
        elif(self.ronda == 2):
            if(parda == 0):
                jPos = cartaMayor[1]
                equipoWinManoActual = self.jEquipos[jPos]
            if(self.parda == 1 or parda == 1):
                if(parda == 0):
                    return ('win', equipoWinManoActual)
                elif(parda == 1 and self.parda == 1):
                    return ('parda', cartaMayor)
                elif(parda == 0 and self.parda == 1):
                    return ('win', self.equipoGanadorPrimeraRonda)
                elif(parda == 1 and self.parda == 0):
                    return ('win', self.equipoGanadorPrimeraRonda)
            self.equipoGanadorSegundaRonda = equipoWinManoActual
            if(equipoWinManoActual == self.equipoGanadorPrimeraRonda):
                return ('win', self.equipoGanadorPrimeraRonda)
            else:
                self.setTurno(jPos)
                return ('continue', cartaMayor[0], cartaMayor[1])
        elif(self.ronda == 3):
            print parda
            if(parda == 0):
                jPos = cartaMayor[1]
                equipoWinManoActual = self.jEquipos[jPos]
            if(self.parda == 1 or parda == 1):
                if(parda == 0):
                    return ('win', equipoWinManoActual)
                elif(parda == 1):
                    return ('empate', cartaMayor, self.mano)
            msg_debug("Equipo Ganador Mano Actual: %s" % equipoWinManoActual)
            msg_debug("Equipo Ganador Mano 2: %s" % self.equipoGanadorSegundaRonda)
            msg_debug("Equipo Ganador Mano 1: %s" % self.equipoGanadorPrimeraRonda)
            if(equipoWinManoActual == self.equipoGanadorPrimeraRonda):
                return ('win', self.equipoGanadorPrimeraRonda)
            elif(equipoWinManoActual == self.equipoGanadorSegundaRonda):
                return ('win', self.equipoGanadorSegundaRonda)
            msg_debug("No return")

    def iniciar(self):
        self.actionGame.setTeams(self.jEquipos)
        self.actionGame.setPlayers(self.jugadores)
        while 1:
            for equipo in self.getPuntosEquipos():
                self.actionGame.showPoints(equipo, self.puntosEquipos[equipo])
                #print ('puntos equipo %d: %d') %(equipo, self.puntosEquipos[equipo])
            ''' Repartir cartas '''
            cartasJugadores = self.repartirCartas()
            cx = 0
            for jugador in self.jugadores:
                cartas = cartasJugadores[cx]
                self.actionGame.giveCards(jugador.getID(), cartas);
                jugador.setCards(cartas)
                self.actionGame.showCards(jugador.getID(), cartas)
                cx += 1

            while 1:
                nRonda = self.iniciarRonda()
                ''' Se inicia el juego con el jugador que es mano '''
                cJugadas = 0 #Alamacena la cantidad de jugadas en la ronda
                while cJugadas < self.cantidadJugadores:
                    '''Se inicia el juego'''
                    cJugadas += 1
                    jugador = self.getTurno()

                    while 1:
                        cartaAJugar = self.actionGame.getActionPlayer(jugador.getID())
                        carta = self.decCartaID(cartaAJugar) #Corrobora que el valor de la carta sea correcto
                        if(not carta == 20):
                            if(jugador.playingCard(carta)): #Juega la carta y se comprueba que este disponible
                                cartaJ = jugador.getCardPlayed() #Obitene el nombre completo de la carta
                                self.setCarta(jugador.getID(),cartaJ)
                                self.actionGame.showJugada(jugador.getID(), jugador.getName(),cartaJ)
                                break
                            else:
                                self.actionGame.showError(jugador.getID(), 'cardPlayerd')
                        else:
                            self.actionGame.showError(jugador.getID(), 'invalidAction')
                Ganador = self.obtenerGanador()
                self.actionGame.returnStatus(Ganador)
                if(Ganador[0] == 'parda'):
                    self.actionGame.Parda()
                elif(Ganador[0] == 'continue'):
                    self.actionGame.showResultMano(Ganador[2], self.jugadores[Ganador[2]].getName(),  self.jugadores[Ganador[2]].getTeam(), Ganador[1])
                elif(Ganador[0] == 'win'):
                    self.actionGame.win(Ganador[1])
                    self.darPuntosEquipo(Ganador[1],2)
                    self.resetRonda()
                    break
                elif(Ganador[0] == 'empate'):
                    self.actionGame.winEmpate(Ganador[2].getTeam())
                    self.darPuntosEquipo(Ganador[2].getTeam(),2)
                    self.resetRonda()
                    break
            time.sleep(5)

'''
Simulacion de ejemplo de como utilizar la libreria PyTruco
@Autor: Lautaro Linquiman
@Email: acc.limayyo@gmail.com

Paso 1: Definir parametros de la Simulacion
    CantidadDeJugadores

Paso 2: Definir jugadores
Se importa el modulo jugador, el cual alamacena todos los parametros y funcionalidades.
'''
from jugador import Jugador

'''
Paso 3: Crear mesa
Se importa el modulo mesa, el cual alamacena todos los parametros y funcionalidades.
'''
from mesa import Mesa

''' Paso 5: Crear una nueva partida
Se importa el modulo Juego, el cual alamacena todos los parametros y funcionalidades.
'''
from juego import Juego


class EjemploDeTruco:
    def __init__(self):
        ''' Paso 1: Definiendo parametros de la simulacion '''
        self.cantidadDeJugadores = 2

        '''Paso 2: Definiendo jugadores'''
        self.jugadores = []
        self.jugadores.append(Jugador(0))
        self.jugadores.append(Jugador(1))

        ''' Paso : Creando mesa '''
        self.mesa = Mesa(self.cantidadDeJugadores, self.jugadores[0].getID(), 0)

        '''Paso 4: Asignando nuevos jugadores a la mesa'''
        self.mesa.newPlayer(self.jugadores[0])
        self.mesa.newPlayer(self.jugadores[1])

        #Se verifica que se pueda iniciar la partida
        if(self.mesa.getStatus()):
            ''' Paso 5: Creando una nueva partida '''
            equipos = self.mesa.getTeams() #Obtiene la configuracion de jugadores respecto a los equipos.
            self.juego = Juego(self.jugadores, equipos, self.mesa.getID())

            self.juego.iniciar()
            '''cartasJugadores = self.juego.repartirCartas()


            while 1:
                for equipo in self.juego.getPuntosEquipos():
                    print ('puntos equipo %d: %d') %(equipo, self.juego.puntosEquipos[equipo])

                cartasJugadores = self.juego.repartirCartas()
                cx = 0
                for jugador in jugadores:
                    cartas = cartasJugadores[cx]
                    self.jugadores[jugador].setCards(cartas)
                    cx += 1
                while 1:
                    nRonda = self.juego.iniciarRonda()

                    cJugadas = 0 #Alamacena la cantidad de jugadas en la ronda
                    while cJugadas < self.juego.cantidadJugadores:

                        cJugadas += 1
                        idJugador = self.juego.getTurno()
                        while 1:
                            cartaAJugar = random.randint(1,3)
                            carta = self.juego.decCartaID(cartaAJugar) #Corrobora que el valor de la carta sea correcto
                            if(not carta == 20):
                                if(self.jugadores[idJugador].playingCard(carta)): #Juega la carta y se comprueba que este disponible

                                    cartaJ = self.jugadores[idJugador].getCardPlayed() #Obitene el nombre completo de la carta
                                    self.juego.setCarta(idJugador,cartaJ)
                                    print ('%scartaJugada %s' ) % (self.jugadores[idJugador].getName(),cartaJ,) #Informa a los demas jugadores la carta que se jugo

                                    break
                                else:
                                    print ('errorCartaJugada') #La carta que se ingreso ya fue jugada
                            else:
                                print ('errorCartaInvalida') #El valor ingresado no es valido
                    Ganador = self.juego.obtenerGanador()
                    print('[debuggin-cServidor-juego-Ganador]', Ganador)
                    if(Ganador[0] == 'parda'):
                        print ('%sparda' ) % (Ganador[1],)
                    elif(Ganador[0] == 'continue'):
                        print ('%scontinue %s' ) % (self.jugadores[Ganador[2]].getName(),Ganador[1])
                    elif(Ganador[0] == 'win'):
                        print ('%swin') % (Ganador[1],)
                        self.juego.darPuntosEquipo(Ganador[1],2)
                        self.juego.resetRonda()
                        break
                    elif(Ganador[0] == 'empate'):
                        print ('%sempate') % (Ganador[2])
                        self.juego.darPuntosEquipo(Ganador[1],2)
                        self.juego.resetRonda()
                        break
                break
'''


if __name__ == "__main__":
    EjemploDeTruco()

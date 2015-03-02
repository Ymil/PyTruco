'''
Clase Servidor - Socket
2015-01-15 23:55:29 
'''
import threading


from controlador import Controlador
from modelo import Modelo
from cmds import Cmds
from msg import Msg
from mesa import Mesa

from cartas import Cartas
from jugador import Jugador
from juego import Juego
#debuggin
import sys
import traceback

#debuggin

from time import sleep
from socket import socket
class servidor(Msg):
    def __init__(self, config = {}):
        self.socket = socket()
        self.debuggin = 0
        if('ip' in config):
            self.ip = config['ip']
        else:
            self.ip = 'localhost'
        if('port' in config):
            self.port = config['port']
        else:
            self.port = 9999
        
        self.conexion = 0
        
        self.conexiones = {} #Almacena las conexiones con clientes
        self.escucha = [] #Almacena los threading con de cada cliente
        
        self.timing = .3 #Tiempo de espera entre mensaje y mensaje (Recepcion y emision)
        ''' Threads '''
        tConexionesEntrantes = 0
        
        ''' Clases Externas '''
        self.c = Controlador()
        self.m = Modelo()
        self.cmds = Cmds()
        
        #self.debuggin = debuggin
        
        ''' Mesas '''
        self.cantidadMesas = 0 #Almacena la cantidad de mesas armadas
        self.mesa = [] #Aloja las mesas
        
        ''' Juego '''
        self.juego_ = {}
        self.juegosActivos = 0
        
        ''' Jugadores '''
        self.jugador_ = {}
        
        self.errorFatal = 0
        self.desconexion = 0
            
    def conectar(self):
        while(1 == 1):
            try:                
                self.conexion = self.socket.bind((self.ip,self.port))
                
                self.socket.listen(1)  
                
                self.tConexionesEntrantes = threading.Thread(target=self.conexionesEntrantes)
                self.tConexionesEntrantes.start()
                
                #self.conexionesEntrantes()
                print('------------------ Conexion Establecida------------------')
                self.conexion = 1
                #return 1
            except Exception as error:
                self.conexion = 0
                #return 0
            
    def getStatusConection(self):
        return self.conexion
            
  
    def conexionesEntrantes(self):
        ''' Esta funcion escucha las conexiones entrantes de clientes constantemente '''
        print('------------------ Servidor En Escucha ------------------')
        #print(self.socket)
        idCon = 0 #Asignador de ids de conexion
        while(1 == 1):
            if(self.desconexion == 1):
                break            
            sc, addr = self.socket.accept() #Acepta la conexion entrante del cliente
            
            print('[Nueva Conexion] %s:%d') % (addr[0],addr[1])      
            self.conexiones[idCon] = {'sc':sc,'addr':addr}
            
            id = self.c.nuevaConexion(sc,addr)
                    
            self.jugador_[idCon] = Jugador(id)
            thread = threading.Thread(target=self.bienvenida, args=(idCon,))
            thread.start()
            #self.bienvenida(idCon)
            idCon = idCon + 1
            sleep(self.timing)            
            
    
    def bienvenida(self,idCon):
        '''Paso 1: del servidor [Mensaje de bienvenida]'''
        #print(idCon)
        #print('[Nueva conexion] %s %d') % (self.conexiones[idCon]['addr'][0],self.conexiones[idCon]['addr'][1])
        msg = self.cmds.enviarMsgID(self.mensajeID['bienvenida'])
        self.conexiones[idCon]['sc'].send(msg)
        sleep(self.timing)
        '''thread = threading.Thread(target=self.registrarNick, args=(idCon,))
        thread.start()'''
        self.registrarNick(idCon)
            
    def registrarNick(self, idCon):
        '''Paso 2: Obtiene el nombre del cliente y lo registra'''
        conexion = self.conexiones[idCon]['sc']
        while(1 == 1):
            msg = self.cmds.obtener()
            conexion.send(msg)
            sleep(self.timing)
            nick = self.obtenerRespuesta(idCon)
            registro = self.c.regNick(nick,self.jugador_[idCon].getID())
            print registro        
            if(registro == 0):
                msg = self.cmds.enviarMsgID(self.mensajeID['nickError'])
                conexion.send(msg)
                sleep(self.timing)
            else:
                self.jugador_[idCon].setName(nick)
                msg = self.cmds.enviarMsgID(self.mensajeID['nickOK'])
                conexion.send(msg)
                sleep(self.timing)
                break
            if(self.desconexion == 1):
                break
        print("[Cliente]Nuevo nick registrado: %s") % nick
        '''thread = threading.Thread(target=self.opcionesJuego, args = (idCon,))
        thread.start()'''
        self.opcionesJuego(idCon)
        #self.conexion[idCon]['sc'].send(self.cmds.okRegNick())   
    
    def opcionesJuego(self, idCon):
        '''Paso 3: Muestra al jugador las opciones de juego'''        
        conexion = self.conexiones[idCon]['sc']
        msg = self.cmds.enviarMsgID(self.mensajeID['opcionesJuego'])
        conexion.send(msg)
        sleep(self.timing)
        while(1 == 1):
            msg = self.cmds.obtener()
            conexion.send(msg)
            sleep(self.timing)
            try:
                opcion = self.obtenerRespuesta(idCon)
                opcion = int(opcion)
                if(opcion == 1):
                    thread = threading.Thread(target=self.crearMesa, args = (idCon,))
                    thread.start()
                    #self.crearMesa(idCon)
                    #self.(idCon)
                    break
                elif(opcion == 2):
                    '''thread = threading.Thread(target=self.ingresarMesa, args = (idCon,))
                    thread.start()'''
                    self.ingresarMesa(idCon)
                    #self.ingresarMesa(idCon)
                    break
                elif(opcion == 3):
                    '''thread = threading.Thread(target=self.verMesas, args = (idCon,))
                    thread.start()
                    sleep(self.timing)'''
                    self.verMesas(idCon)
                    #self.verMesas(idCon)
                    continue
                else:
                    raise()
            except:
                msg = self.cmds.enviarMsgID(self.mensajeID['errorOpcion'], ('entre 1 y 3'))
                conexion.send(msg)
                sleep(self.timing)               
                continue
            if(self.desconexion == 1):
                break
    
    def crearMesa(self,idCon):
        ''' Esta funcion crea una nueva mesa '''
        conexion = self.conexiones[idCon]['sc']     
        msg = self.cmds.enviarMsgID(self.mensajeID['crearMesa'])
        conexion.send(msg)
        sleep(self.timing)
        while(1 == 1):
            msg = self.cmds.obtener()
            conexion.send(msg)
            sleep(self.timing)
            try:
                opcion = self.obtenerRespuesta(idCon)
                opcion = int(opcion)
                if(opcion == 1):
                    cantidadJugadores = 2
                elif(opcion == 2):
                    cantidadJugadores = 4
                elif(opcion == 3):
                    cantidadJugadores = 6
                else:
                    raise()
                break
            except:
                traceback.print_exc(file=sys.stdout)
                msg = self.cmds.enviarMsgID(self.mensajeID['errorOpcion'], 'entre 1 y 3')
                conexion.send(msg)
                sleep(self.timing)               
                continue
            if(self.desconexion == 1):
                break
        nombreCreador = self.jugador_[idCon].getName()
        idJugador = self.jugador_[idCon].getID()
        mesaCreada = Mesa(cantidadJugadores, nombreCreador, self.cantidadMesas)
        self.cantidadMesas += 1
        self.mesa.append(mesaCreada)
        mesaCreada.nuevoJugador(idCon)
        self.enviarMsgID(idCon, 'mesaCreada')
        
    def verMesas(self,idCon):
        ''' Esta funcion muestra las mesas actuales '''
        if(self.debuggin): print(self.mesa)
        if(len(self.mesa) > 0):       
            for mesa in self.mesa:
                info = mesa.getInfo()
                self.enviarMsgID(idCon, 'infoMesas', info)
        else:
            self.enviarMsgID(idCon, 'noMesas')
    
    def ingresarMesa(self,idCon):
        ''' Esta funcion ingresa el jugador a una mesa '''
        j = 1
        while(1 == j):            
            self.enviarMsgID(idCon, 'ingresarMesa')
            self.obtenerMsg(idCon)
            respuesta = self.obtenerRespuesta(idCon)            
            try:
                idMesa = int(respuesta)
                idJugador = self.jugador_[idCon].getID()
                nombreJugador = self.jugador_[idCon].getName()
                self.enviarMsgIDMesa(idMesa, 'nuevoJugador', nombreJugador) # Se le avisa a los jugadores el ingreso del nuevo jugador                
                self.mesa[idMesa].nuevoJugador(idCon)               
                creadaPor = self.mesa[idMesa].getInfo()[3]
                self.enviarMsgID(idCon, 'bienvenidoMesa', creadaPor)
                j = 0
                if(self.mesa[idMesa].getStatus()):
                    self.iniciarJuego(idMesa)
                
            except IndexError:
                self.enviarMsgID(idCon, 'mesaNoExistente')
                continue
            except ValueError:
                self.enviarMsgID(idCon, 'errorOpcion', 'numerico')
                continue
            except Exception as error:
                traceback.print_exc(file=sys.stdout)
                #print 'Error'
                continue
            finally:
                traceback.print_exc(file=sys.stdout)
            if(self.desconexion == 1):
                break
         
    def iniciarJuego(self, mesaID):
        self.enviarMsgIDMesa(mesaID, 'iniciandoPartida')
        self.enviarMsgIDMesa(mesaID, 'haJugador')
        self.juego(mesaID)
    
    def juego(self,mesaID):        
        jugadores = self.mesa[mesaID].getJugadores()
        equipos = self.mesa[mesaID].getEquipos()        
        self.juego_[mesaID] = Juego(jugadores,equipos)
        j_ = self.juego_[mesaID]
        while 1:
            for equipo in j_.getPuntosEquipos():
                self.enviarMsgIDMesa(mesaID, 'puntos', (equipo, j_.puntosEquipos[equipo]))
            ''' Repartir cartas '''
            cartasJugadores = j_.repartirCartas()
            cx = 0
            for jugador in jugadores:
                cartas = cartasJugadores[cx]           
                self.enviarCartas(jugador, cartas)
                self.jugador_[jugador].setCartas(cartas)
                self.enviarAccion(jugador,1)
                cx += 1
            while 1:
                nRonda = j_.iniciarRonda()
                self.enviarMsgIDMesa(mesaID, 'infoRonda', (nRonda,))  
                ''' Se inicia el juego con el jugador que es mano '''
                cJugadas = 0 #Alamacena la cantidad de jugadas en la ronda 
                while cJugadas < j_.cantidadJugadores:                
                    '''Se inicia el juego'''
                    cJugadas += 1
                    idJugador = j_.getTurno()            
                    self.enviarMsgID(idJugador, 'infoTurno') #Inidica el turno al jugador
                    while 1:
                        self.obtenerMsg(idJugador)
                        carta = self.obtenerRespuesta(idJugador) 
                        carta = j_.decCartaID(carta) #Corrobora que el valor de la carta sea correcto
                        if(not carta == 20):
                            if(self.jugador_[idJugador].jugarCarta(carta)): #Juega la carta y se comprueba que este disponible
                                
                                cartaJ = self.jugador_[idJugador].getCartaJugada() #Obitene el nombre completo de la carta
                                j_.setCarta(idJugador,cartaJ)
                                self.enviarMsgIDMesa(mesaID, 'cartaJugada', (self.jugador_[idJugador].getName(),cartaJ,)) #Informa a los demas jugadores la carta que se jugo
                                
                                break
                            else:
                                self.enviarMsgID(idJugador, 'errorCartaJugada') #La carta que se ingreso ya fue jugada
                        else:
                            self.enviarMsgID(idJugador, 'errorCartaInvalida') #El valor ingresado no es valido
                Ganador = j_.obtenerGanador()
                if(Ganador[0] == 'parda'):
                    self.enviarMsgIDMesa(mesaID, 'parda', (Ganador[1]))
                elif(Ganador[0] == 'continue'):
                    self.enviarMsgIDMesa(mesaID, 'continue', (self.jugador_[Ganador[2]].getName(),Ganador[1]))
                elif(Ganador[0] == 'win'):
                    self.enviarMsgIDMesa(mesaID, 'win', (Ganador[1]))
                    j_.darPuntosEquipo(Ganador[1],2)
                    break
            break
            if(self.desconexion == 1):
                break
                   
               
    def obtenerRespuesta(self,idCon):
        '''Esta funcion obtiene y decodifica todos los mensajes de los clientes'''        
        try:
            conexion = self.conexiones[idCon]['sc'] #Indica la conexion (SC) del cliente a escuchar
            msg = conexion.recv(1024)
            if(self.debuggin):
                print('msg cliente[%s]: %s') % (self.conexiones[idCon]['addr'][0],msg)
            return msg        
        except Exception as error:
            traceback.print_exc(file=sys.stdout)
            if(self.errorFatal == 1):
                self.desconexionForzada()  
        finally:
            pass                      
    
    def enviarMsgIDTodos(self, msgID, params = ()):
        msg = self.cmds.enviarMsgID(self.mensajeID[msgID], params)
        self.socket.sendall(msg)
        sleep(self.timing)
    
    def enviarMsgIDMesa(self, mesaID, msgID, params = ()):
        for jugadorID in self.mesa[mesaID].getJugadores():
            if(self.debuggin): print jugadorID
            idCon = jugadorID
            conexion = self.conexiones[idCon]['sc']
            msg = self.cmds.enviarMsgID(self.mensajeID[msgID], params)
            conexion.send(msg)
            sleep(self.timing)        
    
    def enviarMsgID(self,idCon, msgID, params = ()):
        conexion = self.conexiones[idCon]['sc'] 
        msg = self.cmds.enviarMsgID(self.mensajeID[msgID],params)
        conexion.send(msg)
        sleep(self.timing)
    
    def enviarCartas(self, idCon, cartas):
        conexion = self.conexiones[idCon]['sc']
        msg = self.cmds.enviarCartas(cartas)
        conexion.send(msg)
        sleep(self.timing)
        
    def enviarAccion(self, idCon, accionID):
        conexion = self.conexiones[idCon]['sc']
        msg = self.cmds.enviarAccion(accionID)
        conexion.send(msg)
        sleep(self.timing)
        
    def obtenerMsg(self, idCon):
        conexion = self.conexiones[idCon]['sc'] 
        msg = self.cmds.obtener()
        conexion.send(msg)
        sleep(self.timing)
    
    def desconectar(self):
        self.socket.close()
        self.desconexion = 0
        for conexion in self.conexiones:
            self.conexiones[conexion]['sc'].close()
        #exit()
    
    def desconexionForzada(self):
        self.desconectar()
        exit()
        
    
        
               


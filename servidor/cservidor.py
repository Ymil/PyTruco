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
#debuggin
import sys
import traceback

#debuggin

from time import sleep
from socket import socket

class servidor(Msg):
    def __init__(self, config = {}):
        if('ip' in config):
            self.ip = config['ip']
        else:
            self.ip = 'localhost'
        if('port' in config):
            self.port = config['port']
        else:
            self.port = 9999
            
        self.conectar()
        
        self.conexion = {} #Almacena las conexiones con clientes
        self.escucha = [] #Almacena los threading con de cada cliente
        
        self.timing = .05 #Tiempo de espera entre mensaje y mensaje (Recepcion y emision)
        ''' Threads '''
        tConexionesEntrantes = 0
        
        ''' Clases Externas '''
        self.c = Controlador()
        self.m = Modelo()
        self.cmds = Cmds()
        
        ''' Mesas '''
        self.cantidadMesas = 0 #Almacena la cantidad de mesas armadas
        self.mesa = [] #Aloja las mesas
        
        ''' Jugadores '''
        self.jugador_ = {}
        
        self.errorFatal = 0
            
    def conectar(self):
        while(1 == 1):
            try:
                self.socket = socket()
                self.conexion = self.socket.bind((self.ip,self.port))
                
                self.socket.listen(1)  
                
                self.tConexionesEntrantes = threading.Thread(target=self.conexionesEntrantes)
                self.tConexionesEntrantes.start()
                
                print('------------------ Conexion Establecida------------------')
                break
            except Exception as error:
                print error
                con = raw_input('Desea reintentar la conexion (Y/N)?')
                if ( con == 'y' or con == 'Y'):
                    continue
                self.errorFatal = 1
                self.desconexionForzada()
                break
            
  
    def conexionesEntrantes(self):
        ''' Esta funcion escucha las conexiones entrantes de clientes constantemente '''
        print('------------------ Servidor En Escucha ------------------')
        #print(self.socket)
        idCon = 0 #Asignador de ids de conexion
        while(1 == 1):
            sc, addr = self.socket.accept() #Acepta la conexion entrante del cliente
            
            print('[Nueva Conexion] %s:%d') % (addr[0],addr[1])      
            self.conexion[idCon] = {'sc':sc,'addr':addr}
                    
              
            
            id = self.c.nuevaConexion(sc,addr)
                    
            self.jugador_[idCon] = Jugador(id)
            
            self.bienvenida(idCon)
            
            idCon = idCon + 1
            
            sleep(.02)
            if(self.errorFatal == 1):
                self.desconexionForzada()
                break
    
    def bienvenida(self,idCon):
        '''Paso 1: del servidor [Mensaje de bienvenida]'''
        msg = self.cmds.enviarMsgID(self.mensajeID['bienvenida'])
        self.conexion[idCon]['sc'].send(msg)
        sleep(self.timing)
        self.registrarNick(idCon) #Paso dos
            
    def registrarNick(self, idCon):
        '''Paso 2: Obtiene el nombre del cliente y lo registra'''
        conexion = self.conexion[idCon]['sc']
        while(1 == 1):
            msg = self.cmds.obtener()
            conexion.send(msg)
            sleep(self.timing)
            nick = self.obtenerRespuesta(idCon)
            registro = self.c.regNick(nick,self.jugador_[idCon].getId())
            print registro        
            if(registro == 0):
                msg = self.cmds.enviarMsgID(self.mensajeID['nickError'])
                conexion.send(msg)
                sleep(self.timing)
            else:
                print "1_2"
                self.jugador_[idCon].setName(nick)
                msg = self.cmds.enviarMsgID(self.mensajeID['nickOK'])
                conexion.send(msg)
                sleep(self.timing)
                break
        print("[Cliente]Nuevo nick registrado: %s") % nick
        self.opcionesJuego(idCon)
        #self.conexion[idCon]['sc'].send(self.cmds.okRegNick())   
    
    def opcionesJuego(self, idCon):
        '''Paso 3: Muestra al jugador las opciones de juego'''        
        conexion = self.conexion[idCon]['sc']
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
                    self.crearMesa(idCon)
                    break
                elif(opcion == 2):
                    continue
                elif(opcion == 3):
                    self.verMesas(idCon)
                else:
                    raise()
            except:
                msg = self.cmds.enviarMsgID(self.mensajeID['errorOpcion'], 'entre 1 y 3')
                conexion.send(msg)
                sleep(self.timing)               
                continue
    
    def crearMesa(self,idCon):
        ''' Esta funcion crea una nueva mesa '''
        conexion = self.conexion[idCon]['sc']     
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
                msg = self.cmds.enviarMsgID(self.mensajeID['errorOpcion'], 'entre 1 y 3')
                conexion.send(msg)
                sleep(self.timing)               
                continue
        nombreCreador = self.jugador_[idCon].getName()
        idJugador = self.jugador_[idCon].getID()
        mesaCreada = Mesa(cantidadJugadores, nombreCreador, self.cantidadMesas)
        self.cantidadMesas += 1
        self.mesa.append(mesaCreada)
        mesaCreada.nuevoJugador(idJugador)
        self.enviarMsgID(idCon, 'mesaCreada')
        
    def verMesas(self,idCon):
        ''' Esta funcion muestra las mesas actuales '''        
        for mesa in self.mesa:
            info = mesa.getInfo()
            self.enviarMsgID(idCon, 'infoMesas', info)
    
    def ingresarMesa(self,idCon):
        ''' Esta funcion ingresa el jugador a una mesa '''
        while(1 == 1):            
            self.enviarMsgID(idCon, 'ingresarMesa')
            self.obtenerMsg(idCon)
            respuesta = self.obtenerRespuesta(self,idCon)
            try:
                idMesa = int(respuesta)
                idJugador = self.jugador_[idCon].getID()
                nombreJugador = self.jugador_[idCon].getName()
                self.enviarMsgIDMesa(idMesa, 'nuevoJugador', nombreJugador) # Se le avisa a los jugadores el ingreso del nuevo jugador                
                self.mesa[idMesa].nuevoJugador(idJugador)               
                creadaPor = self.getInfo()[3]
                self.enviarMsgID(idCon, 'bienvenidoMesa', creadaPor)
                if(self.mesa[idMesa].getStatus()):
                    self.iniciarJuego(idMesa)
                break
            except IndexError:
                self.enviarMsgID(idCon, 'mesaNoExistente')
                continue
            except ValueError:
                self.enviarMsgID(idCon, 'errorOpcion', 'numerico')
                continue
            except:
                continue
         
    def iniciarJuego(self, mesaID):
        self.enviarMsgIDMesa(mesaID, 'iniciandoPartida')
        self.enviarMsgIDMesa(mesaID, 'haJugador')
    
    def obtenerRespuesta(self,idCon):
        '''Esta funcion obtiene y decodifica todos los mensajes de los clientes'''        
        try:
            conexion = self.conexion[idCon]['sc'] #Indica la conexion (SC) del cliente a escuchar
            msg = conexion.recv(1024)
            return msg
            '''for msgs in self.m.bienvenida():
                conexion.send(msgs)
                sleep(self.timing)            
            self.jugador_[idCon].setStatus(0)
            conexion.send(self.c.obtener()) #Consulta el nombre     
            while 1 == 1:            
                if(self.jugador_[idCon].getStatus() == 0):
                    msg = conexion.recv(1024)                    
                    registro = self.c.regNick(msg,self.jugador_[idCon].getId()) #Registra el nombre del jugador
                    if(registro == 0):
                        for msgs in self.m.errorNick():
                            conexion.send(msgs)
                            sleep(self.timing)
                        conexion.send(self.c.obtener())
                    else:
                        for msgs in self.m.okNick():
                            conexion.send(msgs)
                            sleep(self.timing)
                    self.jugador_[idCon].setStatus(1)                   
                sleep(.02)
                #print("Mensaje de id(%d): %s") % (idCon, msg)'''
        except Exception as error:
            traceback.print_exc(file=sys.stdout)
            if(self.errorFatal == 1):
                self.desconexionForzada()  
        finally:
            pass                      
    
    def juego(self):
        pass
    
    def enviarMsgIDTodos(self, msgID, params = ()):
        msg = self.cmds.enviarMsgID(self.mensajeID[msgID], params)
        self.socket.sendall(msg)
        sleep(self.timing)
    
    def enviarMsgIDMesa(self, mesaID, msgID, params = ()):
        for jugadorID in self.mesa[mesaID].jugadores():
            idCon = self.jugador_[jugadorID]
            conexion = self.conexion[idCon]['sc']
            msg = self.cmds.enviarMsgID(self.mensajeID[msgID], params)
            conexion.send(msg)
            sleep(self.timing)        
    
    def enviarMsgID(self,idCon, msgID, params = ()):
        conexion = self.conexion[idCon]['sc'] 
        msg = self.cmds.enviarMsgID(self.mensajeID[msgID],params)
        conexion.send(msg)
        sleep(self.timing)
    
    def obtenerMsg(self, idCon):
        conexion = self.conexion[idCon]['sc'] 
        msg = self.cmds.obtener()
        conexion.send(msg)
        sleep(self.timing)
    
    def desconectar(self):
        self.socket.close()
    
    
    def desconexionForzada(self):
        self.desconectar()
        exit()
        
    
        
               


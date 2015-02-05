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
    def __init__(self, config = {}, debuggin = 1):
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
        
        self.timing = .05 #Tiempo de espera entre mensaje y mensaje (Recepcion y emision)
        ''' Threads '''
        tConexionesEntrantes = 0
        
        ''' Clases Externas '''
        self.c = Controlador()
        self.m = Modelo()
        self.cmds = Cmds()
        
        self.debuggin = debuggin
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
                
                #self.conexionesEntrantes()
                
                print('------------------ Conexion Establecida------------------')
                break
            except Exception as error:
                print error
                continue
                '''con = raw_input('Desea reintentar la conexion (Y/N)?')
                if ( con == 'y' or con == 'Y'):
                    continue
                self.errorFatal = 1
                self.desconexionForzada()
                break'''
            
  
    def conexionesEntrantes(self):
        ''' Esta funcion escucha las conexiones entrantes de clientes constantemente '''
        print('------------------ Servidor En Escucha ------------------')
        #print(self.socket)
        idCon = 0 #Asignador de ids de conexion
        while(1 == 1):            
            sc, addr = self.socket.accept() #Acepta la conexion entrante del cliente
            
            print('[Nueva Conexion] %s:%d') % (addr[0],addr[1])      
            self.conexiones[idCon] = {'sc':sc,'addr':addr}
            
            id = self.c.nuevaConexion(sc,addr)
                    
            self.jugador_[idCon] = Jugador(id)
            thread = threading.Thread(target=self.bienvenida, args=(idCon,))
            thread.start()
            #self.bienvenida(idCon)
            
            idCon = idCon + 1
            
            sleep(.02)            
            if(self.errorFatal == 1):
                self.desconexionForzada()
                break
    
    def bienvenida(self,idCon):
        '''Paso 1: del servidor [Mensaje de bienvenida]'''
        print(idCon)
        print(self.conexiones[idCon])
        msg = self.cmds.enviarMsgID(self.mensajeID['bienvenida'])
        self.conexiones[idCon]['sc'].send(msg)
        sleep(self.timing)
        thread = threading.Thread(target=self.registrarNick, args=(idCon,))
        thread.start()
            
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
                print "1_2"
                self.jugador_[idCon].setName(nick)
                msg = self.cmds.enviarMsgID(self.mensajeID['nickOK'])
                conexion.send(msg)
                sleep(self.timing)
                break
        print("[Cliente]Nuevo nick registrado: %s") % nick
        thread = threading.Thread(target=self.opcionesJuego, args = (idCon,))
        thread.start()
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
                    #self.(idCon)
                    break
                elif(opcion == 2):
                    thread = threading.Thread(target=self.ingresarMesa, args = (idCon,))
                    thread.start()
                    #self.ingresarMesa(idCon)
                    break
                elif(opcion == 3):
                    thread = threading.Thread(target=self.verMesas, args = (idCon,))
                    thread.start()
                    #self.verMesas(idCon)
                    continue
                else:
                    raise()
            except:
                msg = self.cmds.enviarMsgID(self.mensajeID['errorOpcion'], ('entre 1 y 3'))
                conexion.send(msg)
                sleep(self.timing)               
                continue
    
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
                msg = self.cmds.enviarMsgID(self.mensajeID['errorOpcion'], 'entre 1 y 3')
                conexion.send(msg)
                sleep(self.timing)               
                continue
        nombreCreador = self.jugador_[idCon].getName()
        idJugador = self.jugador_[idCon].getID()
        mesaCreada = Mesa(cantidadJugadores, nombreCreador, self.cantidadMesas)
        self.cantidadMesas += 1
        self.mesa.append(mesaCreada)
        mesaCreada.nuevoJugador(idCon)
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
            respuesta = self.obtenerRespuesta(idCon)            
            try:
                idMesa = int(respuesta)
                idJugador = self.jugador_[idCon].getID()
                nombreJugador = self.jugador_[idCon].getName()
                self.enviarMsgIDMesa(idMesa, 'nuevoJugador', nombreJugador) # Se le avisa a los jugadores el ingreso del nuevo jugador                
                self.mesa[idMesa].nuevoJugador(idCon)               
                creadaPor = self.mesa[idMesa].getInfo()[3]
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
            except Exception as error:
                traceback.print_exc(file=sys.stdout)
                #print 'Error'
                continue
         
    def iniciarJuego(self, mesaID):
        self.enviarMsgIDMesa(mesaID, 'iniciandoPartida')
        self.enviarMsgIDMesa(mesaID, 'haJugador')
    
    def obtenerRespuesta(self,idCon):
        '''Esta funcion obtiene y decodifica todos los mensajes de los clientes'''        
        try:
            conexion = self.conexiones[idCon]['sc'] #Indica la conexion (SC) del cliente a escuchar
            msg = conexion.recv(1024)
            if(self.debuggin):
                print('msg cliente[%s]: %s') % (self.conexiones[idCon]['addr'][0],msg)
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
        for jugadorID in self.mesa[mesaID].getJugadores():
            print jugadorID
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
    
    def obtenerMsg(self, idCon):
        conexion = self.conexiones[idCon]['sc'] 
        msg = self.cmds.obtener()
        conexion.send(msg)
        sleep(self.timing)
    
    def desconectar(self):
        self.socket.close()
    
    
    def desconexionForzada(self):
        self.desconectar()
        exit()
        
    
        
               


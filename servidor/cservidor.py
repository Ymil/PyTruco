'''
Clase Servidor - Socket
2015-01-15 23:55:29 
'''
import threading


from controlador import Controlador
from modelo import Modelo

from cartas import cartas
from jugador import Jugador
#debuggin
import sys
import traceback

#debuggin

from time import sleep
from socket import socket

class servidor:
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
        self.enlacesEstablecidos = [] #Almacena los threading con de cada cliente
        
        self.timing = .02 #Tiempo de espera entre mensaje y mensaje (Recepcion y emision)
        ''' Threads '''
        tConexionesEntrantes = 0
        
        ''' Clases Externas '''
        self.c = Controlador()
        
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
                    
            self.nuevoNick(idCon) #Se obtiene el nombre de usuario del cliente
            
            id = self.c.nuevaConexion(sc,addr)
                    
            self.jugador_[idCon] = Jugador(id)
            
            idCon = idCon + 1
            
            sleep(.02)
            if(self.errorFatal == 1):
                self.desconexionForzada()
                break
    
    def nuevoNick(self,idCon):
        '''Esta funcion obtiene el nombre del jugador'''
        try:
            conexion = self.conexion[idCon] #Indica la conexion (SC) del cliente a escuchar
            for msgs in self.m.bienvenida():
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
                #print("Mensaje de id(%d): %s") % (idCon, msg)
        except Exception as error:
            traceback.print_exc(file=sys.stdout)
            if(self.errorFatal == 1):
                self.desconexionForzada()
                break            
    
    def desconectar(self):
        self.socket.close()
    
    
    def desconexionForzada(self):
        self.desconectar()
        exit()
        
    
        
               


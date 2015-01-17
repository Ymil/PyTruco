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
        
        self.conexiones = {} #Almacena las conexiones con clientes
        self.enlacesEstablecidos = [] #Almacena los threading con de cada cliente
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
        print('------------------ Servidor En Escucha ------------------')
        print(self.socket)
        idCon = 0 #Asignador de ids de conexion
        while(1 == 1):
            sc, addr = self.socket.accept()
            print('[Nueva Conexion] %s:%d') % (addr[0],addr[1])      
            self.conexiones[idCon] = {'sc':sc,'addr':addr}        
            self.enlacesEstablecidos.append(threading.Thread(target=self.escucharMensajes,args=(sc,idCon,))) #Se inicia la escucha al cliente de forma continua
            self.enlacesEstablecidos[idCon].start()
            id = self.c.nuevaConexion(sc,addr)        
            self.jugador_[idCon] = Jugador(id)
            idCon = idCon + 1
            sleep(.02)
            if(self.errorFatal == 1):
                self.desconexionForzada()
    
    def escucharMensajes(self,sc,idCon):
        pass
    
    def desconectar(self):
        self.socket.close()
    
    
    def desconexionForzada(self):
        self.desconectar()
        exit()
        
    
        
               


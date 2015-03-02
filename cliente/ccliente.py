from msg import Msg

from socket import socket
from time import sleep

from controlador import Controlador
from vista import Vista
debuggin = 0
c = Controlador(debuggin)

class cliente(Msg):
    ''' Clase encarga de controlar la interconexion con el servidor jugador-servidor
        21-enero-2015 02:57
        Lautaro Linquiman
        '''
    def __init__(self):       
        self.reconexionTime = 5 #Tiempo de reconexion
        self.conexion = None #Conexion con el servidor
        self.ipServidor = 'localhost' #IP del servidor
        self.portServidor = 9999 #Puerto del servidor
        
        if(self.conectar()):
            print(self.mensaje[100].center(50,'='))
            self.escucha()   
    
    def conectar(self):
        while(1 == 1):
            try:
                self.conexion = socket()
                self.conexion.connect((self.ipServidor,self.portServidor))
                return 1
            except Exception as error:
                print(self.mensaje['error'][0]) % self.reconexionTime
                sleep(self.reconexionTime)
                
    def escucha(self):
        while(1 == 1):
            msgServidor = self.conexion.recv(1024)
            response = c.response(msgServidor)
            if(debuggin):
                print(msgServidor)
                print(response)
            if(response == 1):
                params = c.getMsgID() #Obtiene el ID del mensaje enviado por el servidor
                print('%s') % c.getMsg(params) #Imprimide el mensaje
            elif(response == 2):
                msg = raw_input('>')
                self.conexion.send(msg)
            elif(response == 3):
                c.getCartasFromMsg()
            elif(response == 4):
                print('Acion id %d') % c.getActionID()
                if(c.getActionID() == 1):
                    if(debuggin):
                        print('Mostrando cartas')
                    cartasOrdenadas = c.mostrarCartas()
                    print(cartasOrdenadas)
                    
                    
                
    
    
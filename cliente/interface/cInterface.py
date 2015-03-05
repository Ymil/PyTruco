import pygame
import sys
import time
class interface():
    def __init__(self, cantidadJugadores):
        self.cantidadJugadores = cantidadJugadores
        self.width = 1280
        self.height = 960
        self.PlayerPos = {2:((self.width/2-128,100), (self.width/2-128, self.height-228))}
        self.CardsPos = (self.width/2-90,self.width/2-40,self.width/2+10)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.image = pygame.image.load('user.png')
        if(self.image == 0):
            print("No se pudo cargar la imagen error(%s)") % pygame.get_error()
            sys.exit()
        self.drawPlayers()
        self.screen.fill((150,255,0))
        
    def drawPlayers(self):
        if(self.cantidadJugadores == 2):            
            for x in range(self.cantidadJugadores):
                print(x)
                posDraw = self.PlayerPos[2][x]
                self.rect = self.screen.blit(self.image, posDraw)
                
    
    def drawCards(self):
        posY = (self.height-328)
        for posX in self.CardsPos:
            imge = pygame.image.fromstring('Ancho', 5, 'RGBA')
            self.rect = self.screen.blit(imge, (posX,posY))
            #pygame.draw.rect(self.screen, (0,0,0), (posX,posY,40,40), 1)
            
    def gameLoop(self):       
        while 1:
            self.screen.fill((150,255,0))
            self.drawPlayers()
            self.drawCards()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
            pygame.display.update()
            time.sleep(0.5)
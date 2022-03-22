#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------- 
# Módulos
# --------------------------------------------------------------------- 
import sys, pygame 
from pygame.locals import *
from random import randint
# --------------------------------------------------------------------- 
# Constantes
# --------------------------------------------------------------------- 
WIDTH = 600
HEIGHT = 500
SpacemanX = 10
SpacemanY = 368
XiXf = {}
Inv_XiXf = {}
direccion = True
i = 0
cont = 3
disparo = False
AsteroideX = 0
AsteroideY = 0
JUEGO = False
Suelo = 370
Vidas = 3
# --------------------------------------------------------------------- 
# Clases
# ---------------------------------------------------------------------
class Spaceman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('spaceman.png',True)
        self.rect = self.image.get_rect()
        self.rect.left = SpacemanX
        self.rect.top = SpacemanY
        self.direccion = direccion
        self.cont = cont
        self.i = i
    def posiciones(self):
        XiXf[0]=(47,62,60,75)
        XiXf[1]=(94,62,141,80)
        XiXf[2]=(0,62,35,80)
         
        Inv_XiXf[0]=(47,187,60,250)
        Inv_XiXf[1]=(0,187,47,250)
        Inv_XiXf[2]=(94,187,141,250)
         
        p = 3
         
        if self.cont == p:
            self.i = 0
        if self.cont == p*2:
            self.i = 1
        if self.cont == p*3:
            self.i = 2
            self.cont = 0
    def teclado(self,keys,time):
        
        if self.rect.left <= WIDTH-40 :
            if keys[K_RIGHT] and not keys[K_LEFT]:
                self.rect.left += 5
                self.direccion = True
                self.cont += 1

        if self.rect.left >= 0:
            if keys[K_LEFT] and not keys[K_RIGHT]:
                self.rect.left -= 5
                self.cont += 1
                self.direccion = False
        
# ---------------------------------------------------------------------
class Bola(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('bullet.png',True)
        self.image = pygame.transform.scale(self.image,(50,47))

        self.rect = self.image.get_rect()
        self.rect.left = SpacemanX + 15
        self.rect.top = SpacemanY + 40
        self.speed = 4.5
        self.listaDisparoY = []
        self.listaDisparoX = []
        self.disparo = disparo
        self.contador = 0
    def teclado(self,keys,time):
        
        if self.rect.left < WIDTH-25 :
            if keys[K_RIGHT]:
                self.rect.left += 5

        if self.rect.left >= 16:
            if keys[K_LEFT] :
                self.rect.left -= 5
        
        if keys[K_SPACE] and self.contador == 0:
            self.disparo = True
            self.listaDisparoY.append(self.rect.top)
            self.listaDisparoX.append(self.rect.left)
            self.contador = 8
        
        if self.contador <= 8 and self.contador>0:
            self.contador -= 1
            
        
        for l in range(len(self.listaDisparoY)):
            if self.disparo == True:
                self.listaDisparoY[l-1] -= self.speed 
                if self.listaDisparoY[l-1] <= 0:
                    self.listaDisparoY.pop(l-1)
                    self.listaDisparoX.pop(l-1)
                
# ---------------------------------------------------------------------
class Asteroide(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('asteroide.png',True)
        self.image = pygame.transform.scale(self.image,(50,47))
        self.rect = self.image.get_rect()
        self.speed = 3
        self.rect.left = randint(0,500)
        self.rect.top = AsteroideY
        self.juego = JUEGO
        
        self.asteroide = True
    def caida(self,time,spaceman):
            
        if self.asteroide == True:
            self.rect.top += self.speed 
            if self.rect.top > 390:
                self.asteroide = False
                
        if self.asteroide == False:
            self.rect.top = AsteroideY
            self.rect.left = randint(0,500)    
            self.asteroide = True
        
        
# ---------------------------------------------------------------------
# Funciones generales
# ---------------------------------------------------------------------
    
def load_image(filename, transparent = False):
    try: image = pygame.image.load(filename)
    except pygame.error as message:
        raise SystemExit ("Error")
    image = image.convert()
    if transparent:
        color = image.get_at((0,0))
        image.set_colorkey(color, RLEACCEL)
    return image
# ---------------------------------------------------------------------
       
def texto(texto,posx,posy,color=(255,255,255)):
    fuente = pygame.font.Font("Arial.ttf",25)
    salida = pygame.font.Font.render(fuente,texto,1,color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida,salida_rect
# ---------------------------------------------------------------------
# Funciones del juego
# ---------------------------------------------------------------------
def choque(jugador,asteroide,bolas):
    if pygame.sprite.collide_rect(jugador,asteroide):
        asteroide.asteroide = False
    for bola in range(len(bolas.listaDisparoY)):
        if pygame.sprite.collide_rect(bolas,asteroide):
            bolas.listaDisparoY.pop(bola)
            asteroide.asteroide = False
            bolas.disparo = False
            Vidas -= 1
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------

        
# ---------------------------------------------------------------------
# Programa Principal
# --------------------------------------------------------------------- 

def main():
# Inicializaciones pygame
    pygame.init()
# Inicializaciones elementos de juego
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("RUSH")
    
    background_image = load_image('fondo_juego.jpg')
    background_image = pygame.transform.scale(background_image,(WIDTH,HEIGHT))
    
    spaceman = Spaceman()
    bola = Bola()
    asteroide = Asteroide()
    
    
    clock = pygame.time.Clock()
    
#Bucle Juego
    while True:
        
        keys = pygame.key.get_pressed()
        time = clock.tick(60)
        
        
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
        
        spaceman.posiciones()
        spaceman.teclado(keys,time)
        bola.teclado(keys,time)
        asteroide.caida(time,spaceman.rect.top)
        choque(spaceman,asteroide,bola)
        
        screen.blit(background_image, (0, 0))
        
        if spaceman.direccion == False:
            screen.blit(spaceman.image,spaceman.rect,Inv_XiXf[spaceman.i])
            screen.blit(bola.image,(spaceman.rect.left +15,spaceman.rect.top+40))
        if spaceman.direccion == True:
            screen.blit(spaceman.image,spaceman.rect,XiXf[spaceman.i])
            screen.blit(bola.image,(spaceman.rect.left+15,spaceman.rect.top+40))
            
        if bola.disparo == True:
            for x in range(len(bola.listaDisparoY)):
                screen.blit(bola.image,(bola.listaDisparoX[x],bola.listaDisparoY[x]))
                
        if bola.disparo == False:
            bola.rect.left = spaceman.rect.left+15
            screen.blit(bola.image,(bola.rect.left,spaceman.rect.top + 40))
        if asteroide.asteroide == True:
            screen.blit(asteroide.image,(asteroide.rect.left,asteroide.rect.top))
        
        pygame.display.flip()
            
    return 0
    
if __name__ == '__main__':
    main()

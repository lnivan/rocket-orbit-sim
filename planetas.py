from dibujo import Dibujador
import pygame
import time
import random
import math

gameLength = 800
gameWidth = 800
grosorLineas = 1
escalaGlobal = 1
lastFrame = time.time()
deltaTime = 0
velocidadTiempo = 10


white = (255, 255, 255)
black = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode([gameLength, gameWidth])

fuente = pygame.font.Font('freesansbold.ttf', 20)

def pitagoras(catetos):
    return(math.sqrt(math.pow(catetos[0], 2) + math.pow(catetos[1], 2)))


class Planeta():

    def __init__(self, masa, radio, posicion):

        self.tipo = 'planeta'

        self.masa = masa
        self.radio = radio
        self.posicion = posicion

    def draw(self, puntoVista):

        pygame.draw.circle(screen, white, (self.posicion - puntoVista) / escalaGlobal + (gameLength / 2, gameWidth / 2), self.radio / escalaGlobal, grosorLineas)


class Sprite:
    def __init__(self, posicion, masa, polarPoints, size, width):

        self.tipo = 'sprite'
        self.acelerando = True
    
        self.polarPoints = polarPoints
        for polarPoint in self.polarPoints:
            polarPoint[1] = polarPoint[1] * size

        self.trayectoria = [(0, 0), (0, 0)]

        self.fuerzaAceleracion = 8 * (10**6) * 20
        self.masa = masa
        self.width = width
        self.radio = 0
        for punto in self.polarPoints:
            if punto[1] > self.radio:
                self.radio = punto[1]

        self.posicion = posicion
        self.velocidad = pygame.Vector2(0, 0)
        self.aceleracion = pygame.Vector2(0, 0)

        self.rotacion = 0
        self.velocidadRotacion = 0
        self.aceleracionRotacion = 0
        


    def actualizar(self):
        self.aceleracion = pygame.Vector2(0, 0)
        for objeto in listaObjetos:
            if objeto != self:
                vectorDistancia = objeto.posicion - self.posicion
                fuerza = 6.67 * (10 ** (-11)) * (self.masa * objeto.masa) / pitagoras(vectorDistancia) ** 2
                vectorFuerza = vectorDistancia.normalize() * fuerza
                self.aceleracion = self.aceleracion + vectorFuerza / self.masa

        if self.acelerando == True:
            self.aceleracion = self.aceleracion + pygame.Vector2(math.cos(math.radians(self.rotacion) + math.pi / 2), math.sin(math.radians(self.rotacion) + math.pi / 2)) * self.fuerzaAceleracion / self.masa
        
        self.velocidad = self.velocidad + self.aceleracion * deltaTime
        for objeto in listaObjetos:
            if objeto != self and objeto.tipo == 'planeta' and self.radio + objeto.radio > abs(pitagoras((objeto.posicion + self.velocidad * deltaTime) - self.posicion)):
                self.velocidad = pygame.Vector2(0, 0)
                if self.acelerando == True:
                    self.velocidad = self.velocidad + pygame.Vector2(math.cos(math.radians(self.rotacion) + math.pi / 2), math.sin(math.radians(self.rotacion) + math.pi / 2)) * self.fuerzaAceleracion / self.masa * deltaTime

        self.posicion = self.posicion + self.velocidad * deltaTime


        self.velocidadRotacion = self.velocidadRotacion + self.aceleracionRotacion * deltaTime

        self.rotacion = self.rotacion + self.velocidadRotacion * deltaTime
        for polarPoint in self.polarPoints:
            polarPoint[0] = polarPoint[0] + self.velocidadRotacion * deltaTime



        tamanoPaso = 50
        aTrayectoria = self.aceleracion
        vTrayectoria = self.velocidad
        pTrayectoria = self.posicion
        self.trayectoria = []
        self.trayectoria.append(pTrayectoria)
        for i in range(1000):
            aTrayectoria = pygame.Vector2(0, 0)
            for objeto in listaObjetos:
                if objeto != self:
                    vectorDistancia = objeto.posicion - pTrayectoria
                    fuerza = 6.67 * (10 ** (-11)) * (self.masa * objeto.masa) / pitagoras(vectorDistancia) ** 2
                    vectorFuerza = vectorDistancia.normalize() * fuerza
                    aTrayectoria = aTrayectoria + vectorFuerza / self.masa
        
            vTrayectoria = vTrayectoria + aTrayectoria * tamanoPaso
            for objeto in listaObjetos:
                if objeto != self and objeto.tipo == 'planeta' and self.radio + objeto.radio > abs(pitagoras((objeto.posicion + vTrayectoria * deltaTime) - pTrayectoria)):
                    vTrayectoria = pygame.Vector2(0, 0)
                
            pTrayectoria = pTrayectoria + vTrayectoria * tamanoPaso
            self.trayectoria.append(pTrayectoria)










    def draw(self, puntoVista):

        cartesianPoints = []
        for polarPoint in self.polarPoints:
            xPosition = math.cos(math.radians(polarPoint[0])) * polarPoint[1] / escalaGlobal
            yPosition = -math.sin(math.radians(polarPoint[0])) * polarPoint[1] / escalaGlobal
            cartesianPoint = [xPosition + (self.posicion[0] - puntoVista.x) / escalaGlobal + gameLength / 2, yPosition + (self.posicion[1] - puntoVista.y) / escalaGlobal + gameWidth / 2]
            cartesianPoints.append(cartesianPoint)

        pygame.draw.polygon(screen, white, cartesianPoints, self.width)


'''
class Nave(Sprite):
    def __init__(self, masa):
        super().__init__(pygame.Vector2(0, -6.371 * (10**6) - 300), [[90, 5], [71.5, 3.16], [63.5, 2.24], [284, 4.12], [63.5, 2.24], [33.7, 1.8], [290.5, 4.27], [284, 4.12], [286.7, 5.22], [253.3, 5.22], [256, 4.12], [249.4, 4.27], [146.3, 1.8], [116.5, 2.24], [256, 4.12], [116.5, 2.24], [108.4, 3.16]], 10, grosorLineas)
        self.masa = masa
        self.velocidad = pygame.Vector2(0, 0)
        self.aceleracion = pygame.Vector2(0, 0)
'''



#
dibujador = Dibujador()
listaObjetos = []
tierra = Planeta(5.972 * (10**24), 6 * (10**6), pygame.Vector2(0, 0))
listaObjetos.append(tierra)
nave = Sprite(pygame.Vector2(0, 6 * (10**6) + 500), 8 * (10**6), [[90, 5], [71.5, 3.16], [63.5, 2.24], [284, 4.12], [63.5, 2.24], [33.7, 1.8], [290.5, 4.27], [284, 4.12], [286.7, 5.22], [253.3, 5.22], [256, 4.12], [249.4, 4.27], [146.3, 1.8], [116.5, 2.24], [256, 4.12], [116.5, 2.24], [108.4, 3.16]], 10, grosorLineas)
listaObjetos.append(nave)
#

frame = 0
corriendo = True
while corriendo == True:
    deltaTime = time.time() - lastFrame
    lastFrame = time.time()
    deltaTime = deltaTime * velocidadTiempo

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            corriendo = False
        
        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_d:
                nave.aceleracionRotacion = -0.5

            if evento.key == pygame.K_a:
                nave.aceleracionRotacion = 0.5

            if evento.key == pygame.K_w:
                nave.acelerando = True

            if evento.key == pygame.K_PLUS:
                escalaGlobal = escalaGlobal * 2

            if evento.key == pygame.K_MINUS:
                escalaGlobal = escalaGlobal / 2

        if evento.type == pygame.KEYUP:

            if evento.key == pygame.K_d or evento.key == pygame.K_a:
                nave.aceleracionRotacion = 0

            if evento.key == pygame.K_w:
                nave.acelerando = False

    nave.actualizar()

    screen.fill(black)

    estadisticasNave = fuente.render('velocidad: ' + str(['{0:.1f}'.format(nave.velocidad[0]), '{0:.1f}'.format(nave.velocidad[1])]) + ' ' + 'rotacion: ' + str('{0:.1f}'.format(nave.rotacion)), True, white, black)
    textRect = estadisticasNave.get_rect()
    textRect.center = (gameLength - textRect.width / 2, textRect.height / 2)
    screen.blit(estadisticasNave, textRect)

    dibujador.dibujarObjetos(listaObjetos, nave.posicion, escalaGlobal, screen)
    pygame.display.flip()

#librerias usadas
import pygame
import math

#variables globales
blanco = (255, 255, 255)

#hipotenusa de dos catetos
def pitagoras(catetos):

    return(math.sqrt(math.pow(catetos[0], 2) + math.pow(catetos[1], 2)))

def dibujarArco(centro, radio, pantalla):
    largo, ancho = pantalla.get_size()
    paso = 20
    radianCentral = math.atan2(centro.y, centro.x)
    listaPuntos = []

    radianComprobado = radianCentral
    while centro.x - math.cos(radianComprobado) * radio + largo / 2 > 0 and centro.x - math.cos(radianComprobado) * radio + largo / 2 < largo and centro.y - math.sin(radianComprobado) * radio + ancho / 2 > 0 and centro.y - math.sin(radianComprobado) * radio + ancho / 2 < ancho:
        listaPuntos.append((centro.x - math.cos(radianComprobado) * radio + largo / 2, centro.y - math.sin(radianComprobado) * radio + ancho / 2))
        radianComprobado = radianComprobado + paso * (2 * math.pi) / (radio * 2 * math.pi)

    radianComprobado = radianCentral
    radianComprobado = radianComprobado - paso * (2 * math.pi) / (radio * 2 * math.pi)
    while centro.x - math.cos(radianComprobado) * radio + largo / 2 > 0 and centro.x - math.cos(radianComprobado) * radio + largo / 2 < largo and centro.y - math.sin(radianComprobado) * radio + ancho / 2 > 0 and centro.y - math.sin(radianComprobado) * radio + ancho / 2 < ancho:
        listaPuntos.insert(0, (centro.x - math.cos(radianComprobado) * radio + largo / 2, centro.y - math.sin(radianComprobado) * radio + ancho / 2))
        radianComprobado = radianComprobado - paso * (2 * math.pi) / (radio * 2 * math.pi)

    if len(listaPuntos) > 1:
        pygame.draw.lines(pantalla, blanco, False, listaPuntos, 1)

class Dibujador:

    #no hace falta definir variables para este objeto
    def __init__(self) -> None:

        pass

    def dibujarCirculo(self, circulo, puntoVista, escala, pantalla):

        #obtener el largo y el ancho de la pantalla
        largo, ancho = pantalla.get_size()

        #solo dibujar si va a salir en la pantalla
        if (pitagoras(circulo.posicion - puntoVista) - circulo.radio) / escala < pitagoras((largo / 2, ancho / 2)) * escala:

            #dibujarlo entero si es pequeño
            if circulo.radio / escala < pitagoras([largo, ancho]) + 200:

                pygame.draw.circle(pantalla, blanco, pygame.Vector2(-(puntoVista - circulo.posicion)[0], (puntoVista - circulo.posicion)[1]) / escala + (largo / 2, ancho / 2), circulo.radio / escala, 1)
            
            #dibujar solo una parte si es grande
            else:
                '''
                pygame.draw.circle(pantalla, blanco, (puntoVista - circulo.posicion) / escala + (largo / 2, ancho / 2), circulo.radio / escala, 1)
                print("siuuuu")
                centro = puntoVista - circulo.posicion
                anguloMedio = math.atan2(centro.y, centro.x)
                amplitudAngulo = math.radians((pitagoras([largo, ancho]) * 3) / (circulo.radio * math.pi * 2 / escala) * 360)
                if amplitudAngulo < 0.1:
                    amplitudAngulo = amplitudAngulo + 0.1
                #pygame.draw.rect(pantalla, blanco, pygame.Rect((centro.x - circulo.radio) / escala + largo * 2, (centro.y - circulos.radio) / escala + ancho / 2, circulo.radio * 2 / escala, circulo.radio * 2 / escala), 1)
                pygame.draw.arc(pantalla, blanco, pygame.Rect((centro.x - circulo.radio) / escala + largo / 2, (centro.y - circulo.radio) / escala + ancho / 2, circulo.radio * 2 / escala, circulo.radio * 2 / escala), anguloMedio - amplitudAngulo / 2, anguloMedio + amplitudAngulo / 2, 1)
                '''
                dibujarArco(pygame.Vector2(-puntoVista[0], puntoVista[1]) / escala, circulo.radio / escala, pantalla)
                
    def dibujarSprite(self, sprite, puntoVista, escala, pantalla):

        #obtener el largo y el ancho de la pantalla
        largo, ancho = pantalla.get_size()

        #las coordenadas de los vertices del sprite son polares. Antes de dibujarlas hay que pasarlas a cartesianas
        cartesianPoints = []
        for polarPoint in sprite.polarPoints:
            xPosition = math.cos(math.radians(polarPoint[0])) * polarPoint[1] / escala
            yPosition = -math.sin(math.radians(polarPoint[0])) * polarPoint[1] / escala
            cartesianPoint = [xPosition + (sprite.posicion[0] - puntoVista.x) / escala + largo / 2, yPosition + (sprite.posicion[1] - puntoVista.y) / escala + ancho / 2]
            cartesianPoints.append(cartesianPoint)
        
        #dibujar el sprite con los puntos cartesianos
        pygame.draw.polygon(pantalla, blanco, cartesianPoints, 1)

        #dibujar trayectoria estimada del sprite
        trayectoriaDibujada = []
        for punto in sprite.trayectoria:
            vector = (punto - puntoVista) / escala
            vector[1] = vector[1] * (-1)
            vector = vector + pygame.Vector2(largo / 2, ancho / 2)
            trayectoriaDibujada.append([int(vector[0]), int(vector[1])])

        print(trayectoriaDibujada)
        print(puntoVista)
        pygame.draw.lines(pantalla, blanco, False, trayectoriaDibujada)

    
    def dibujarObjetos(self, listaObjetos, puntoVista, escala, pantalla):
        
        #dibujar todos los objetos de la lista
        for elemento in listaObjetos:

            #si es un planeta, dibujar un circulo
            if elemento.tipo == 'planeta':

                self.dibujarCirculo(elemento, puntoVista, escala, pantalla)

            #si es un sprite, dibujar un sprite
            elif elemento.tipo == 'sprite':

                self.dibujarSprite(elemento, puntoVista, escala, pantalla)


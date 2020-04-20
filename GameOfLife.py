#! /usr/bin/python2.7

import pygame
import numpy as np
import time

pygame.init()

# Ancho y alto de nuestra pantalla
width = 650
heigth = 650

#creacion de la pantalla
screen = pygame.display.set_mode((heigth, width))

bg = 25, 25, 25
screen.fill(bg)

nxC, nyC = 65, 65

dimCW = width / nxC
dimCH = heigth / nyC

# Estado de las celdas. Viva = 1; Muerta = 0
gameState = np.zeros((nxC, nyC))

#Automata palo.
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 2] = 1

#Automata Movil
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

# Control de la ejecucion juego.
pauseExect = False 

# Bucle de ejecucion.
while True:
    
    newGameState = np.copy(gameState)

    screen.fill(bg)
    time.sleep(0.1)

    # Registramos eventos de teclado y raton
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect
        
        # Dectectamos si se presiona el raton
        mouseClick = pygame.mouse.get_pressed()
        
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]

    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExect:

                n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                        gameState[(x) % nxC, (y - 1) % nyC] + \
                        gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                        gameState[(x - 1) % nxC, (y) % nyC] + \
                        gameState[(x + 1) % nxC, (y) % nyC] + \
                        gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                        gameState[(x) % nxC, (y + 1) % nyC] + \
                        gameState[(x + 1) % nxC, (y + 1) % nyC]

                # Rule #1 : Una celular muerta con exactamente 2 vecinas vivas, "revive".
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Rule #2 : Unacelula viva con menos de 2 o mas de 3 vecinas, "Muere"
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            # Creamos el poligino de cada celda  a dibujar
            poly = [((x) * dimCW, y * dimCH),
                    ((x+1) * dimCW, y * dimCH),
                    ((x+1) *dimCW, (y+1) * dimCH),
                    ((x) * dimCW, (y+1) * dimCH)]

            # Y dibujamos la celda para cada par de x e y.
            if newGameState[x, y] == 0:    
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)

            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
    
    # Actualizamos el estado del juego.
    gameState = np.copy(newGameState)
    
    # Actualizamos la pantalla.
    pygame.display.flip()

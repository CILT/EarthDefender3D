# -*- coding: utf-8 -*-
"""
Programa que implementa el juego "Earth Defender 3D".
Autor: Cristián Llull T.
Creado en Python 2.7.1
Controles:
- Del menú inicial:
  - flechas: cambiar nave
  - espacio: seleccionar nave
- Del juego:
  - flechas: desplazar nave
  - z: encender luz de la nave
  - x: disparar misil
  - c: disparo especial
  - espacio: disparo normal
"""

# Importar PyGame
import pygame
from pygame.locals import *

# Importar OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Vista import *
from Escenario import *
from Nave import *

#############################################################################################
# Configuración de Vista
width = 640
height = 480
title = 'Earth Defender!'

# Iniciar PyGame y OpenGL
init_pygame([width, height])
init_opengl([width, height])
glutInit([])

glEnable(GL_LIGHTING)
initLight()

ejes = generarEjes(20000)
grilla = generarGrilla(2000)

############################################################################################
# Configuración del Controlador
FPS = 30.0
# Parámetros de PyGame
reloj = pygame.time.Clock()
DT = 1 / FPS
t = 0.0
angGiroMeteo = 0.0
omega = 90

#############################################################################################
# MENÚ DEL JUEGO
#############################################################################################
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(60.0, float(width)/float(height), 0.1, 20000.0)
# Ahora los comandos para matriz modifican Model_View
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
# Configuración de cámara
glLoadIdentity()
gluLookAt(150.0, 0.0, 100.0, # Pos. ojo
          -2000.0, 0.0, -1000.0, # Apunte
          0.0, 0.0, 1.0 # Qué eje arriba
         )
modelos = []
# Naves
millenium_falcon = Nave('stl')
millenium_falcon.cargar()
modelos.append(millenium_falcon)
nave_glut = Nave('glut')
nave_glut.cargar()
modelos.append(nave_glut)
nave_mano = Nave('mano')
nave_mano.cargar()
modelos.append(nave_mano)

ang = 0.0
ejeRot = [0,0,1]
modelo = 0
contador = 0
run = True
while run:
    # 0: Ajustar tiempo de la aplicación
    reloj.tick(FPS)
    # Ajuste de título
    pygame.display.set_caption('Menú: presione espacio para seleccionar nave')
    # 1: Manejo de eventos de teclado, mouse, etc.
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_q or event.key == K_ESCAPE:
                run = False
            if event.key == K_SPACE:
                run = False
            if event.key == K_LEFT:
                contador += 1
                modelo = contador%len(modelos)
            if event.key == K_RIGHT:
                contador -= 1
                modelo = contador%len(modelos)
    # 2: Ejecutar "lógica" de la aplicación
    ang += omega*DT
    if ang >= 360:
        ang = 0.0
    # 3: Dibujar los elementos
    # Limpiar pantalla
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    dibujarLista(modelos[modelo].lista, angRot=ang, ejeRot=ejeRot)
    pygame.display.flip()
        
nave = modelos[modelo].tipo

##########################################################################################
# JUEGO PRINCIPAL
##########################################################################################
escenario = Escenario(Nave(nave), [width, height])

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(-width,width,-height,height,1,20000)
# Ahora los comandos para matriz modifican Model_View
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
# Configuración de cámara
glLoadIdentity()
gluLookAt(0.0, 0.0, 500.0, # Pos. ojo
          0.0, 0.0, -2000.0, # Apunte
          0.0, -1.0, 0.0 # Qué eje arriba
         )
glEnable(GL_LIGHTING)
initLight()

run = True
while run:
    ############### Controlador ##################################################
    # 0: Ajustar tiempo de la aplicación
    reloj.tick(FPS)
    # Ajuste de título
    pygame.display.set_caption(title)
    
    # 1: Manejo de eventos de teclado, mouse, etc.
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        
        if event.type == KEYDOWN:
            if event.key == K_q or event.key == K_ESCAPE:
                run = False
            if event.key == K_SPACE:
                escenario.nave.disparar()
            if event.key == K_z:
                escenario.nave.luz = not escenario.nave.luz
            if event.key == K_x:
                if escenario.nave.cant_misil > 0:
                    escenario.nave.dispararMisil()
                else:
                    print 'Lo lamento, no hay más misiles!!'
            if event.key == K_c:
                if escenario.nave.cant_especial > 0:
                    escenario.nave.dispararEspecial()
                else:
                    print 'Lo lamento, no hay más ataques especiales!!'
                
    # Para tecla mantenida apretada
    keys_pressed = pygame.key.get_pressed()
    angRot = 0
    ejeRot=[0,0,1]
    if keys_pressed[K_LEFT]:
        escenario.nave.moverIzq()
        angRot = 30
        ejeRot = [0,1,0]
    if keys_pressed[K_RIGHT]:
        escenario.nave.moverDer()
        angRot = -30
        ejeRot = [0,1,0]
    if keys_pressed[K_UP]:
        escenario.nave.subir()
        angRot = 20
        ejeRot = [1,0,0]
    if keys_pressed[K_DOWN]:
        escenario.nave.bajar()
        angRot = -20
        ejeRot = [1,0,0]
        
    # 2: Ejecutar "lógica" de la aplicación
    # Luz de la nave
    if escenario.nave.luz:
        escenario.nave.encenderLinterna()
    else:
        escenario.nave.apagarLinterna()
    
    # Giro de meteoritos
    angGiroMeteo += omega*DT
    if angGiroMeteo >= 360:
        angGiroMeteo = 0.0
    
    escenario.actualizar(DT)
    escenario.limpiar()
    
    if escenario.vidas_tierra <= 0:
        run = False

    ############### Vista #######################################################
    # 3: Dibujar los elementos
    # Limpiar pantalla
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    dibujarLista(escenario.nave.lista, pos=escenario.nave.pos, angRot=angRot, ejeRot=ejeRot)
    dibujarLista(escenario.tierra.lista, scale=[8.5,8.5,8.5])
    for bala in escenario.nave.balas:
        dibujarLista(bala.lista, pos=bala.pos)
    for misil in escenario.nave.misiles:
        dibujarLista(misil.lista, pos=misil.pos)
    for meteorito in escenario.meteoritos:
        dibujarLista(meteorito.lista, pos=meteorito.pos, angRot=angGiroMeteo, ejeRot=[1.0,0.5,1.0], scale=meteorito.escala)
    #dibujarLista(ejes)
    #dibujarLista(grilla)
    
    pygame.display.flip()
    
print 'Juego Terminado!'
print 'Puntuación: ' + str(escenario.puntuacion)

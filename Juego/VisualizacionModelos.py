# -*- coding: utf-8 -*-
"""
Programa para visualizar los modelos que compondrán el juego "Earth Defender 3D".
Autor: Cristián Llull T.
Creado en Python 2.7.1
Controles:
 - flechas: cambiar modelo
 - espacio: cambiar eje de rotación
 - p: pausa
 - g: mostrar o no grilla de tamaño 50
 - a: mostrar o no ejes de coordenadas
"""

# Importar PyGame
import pygame
from pygame.locals import *

# Importar OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from FuncionesAuxiliares import *
from Nave import *
from Bala import *
from Meteorito import *
from Tierra import *
from Misil import *

##################################################################
# Inicialización

def init_pygame((w, h)):
    pygame.init()
    pygame.display.set_mode((w,h), OPENGL|DOUBLEBUF)
    
def init_opengl((w,h)):
    reshape((w,h))
    init()
    
def init():
    # Color de fondo
    glClearColor(0.0,0.0,0.0,1.0)
    
    # Habilitar transparencia
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # Con esto, los colores deben tener una cuarta componente correspon-
    # diente a "alpha".
    # alpha = 0 -> completamente transparente
    # alpha = 1 -> completamente opaco
    
    glShadeModel(GL_SMOOTH)
    
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    # Habilitar para normalizar normales luego de escalamiento
    glEnable(GL_NORMALIZE)
    
def reshape((w,h)):
    if h == 0:
        h == 1
    glViewport(0, 0, w, h)
    # La matriz Projection controla la perspectiva aplicada a las primitivas
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # gluPerspective — set up a perspective projection matrix
    # - fovy: field of view angle, in degrees, in the y direction
    # - aspect: field of view in x direction. Aspect ratif event.key == K_1:
    # - zNear: distnace from the viewer to the near clipping plane (positive)
    # - zFar: distance from the viewer to the far clipping plane (positive)
    gluPerspective(60.0, float(w)/float(h), 0.1, 20000.0)
    #glOrtho(-w,w,-h,h,1,20000)
    # Ahora los comandos para matriz modifican Model_View
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
#################################################################

def initLight():
    # Ajuste de parámetros de luminosidad (ambiente, difusa, etc.)
    
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0]) # Ambient intensity of light
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0]) # Diffuse intensity of light
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0]) # Specular intensity of light
    
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 3000.0, 3000.0, 1.0]) # (x,y,z,w) position of light
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [0.0, -1.0, -1.0]) # (x,y,z) direction of Spotlight (spot es foco)
    
    glLightfv(GL_LIGHT0, GL_SPOT_EXPONENT, 0.0) # Spotlight exponent
    glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, 180.0) # Spot cutoff angle (como hasta donde llega)
    
    glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0) # Constant attenuation factor
    glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.0) # Linear attenuation factor
    glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.0) # Quadratic attenuation factor
    
    glEnable(GL_LIGHT0)

####################################################################
# Inicializar ventana de aplicación

# Parámetros
width = 640
height = 480
title = 'Visualización de Modelos'
FPS = 30.0
ang = 30.0
omega = 90 # grad/seg
rotacionZ = True
contador = 0
modelo = 0
pausa = False
show_grid = True
show_axes = True

# Parámetros de PyGame
reloj = pygame.time.Clock()
DT = 1 / FPS
t = 0.0

# Iniciar PyGame y OpenGL
init_pygame([width, height])
init_opengl([width, height])
glutInit([])

# Cargar Objetos
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
# Bala
bala = Bala()
bala.cargar()
modelos.append(bala)
# Meteorito
meteorito = MeteoritoMadre()
meteorito.cargar()
modelos.append(meteorito)
# Tierra
tierra = Tierra()
tierra.cargar()
modelos.append(tierra)
# Misil
misil = MisilMadre()
misil.cargar()
modelos.append(misil)

ejes = generarEjes(20000)
grilla = generarGrilla(2000)

# Configuración de cámara
glLoadIdentity()
gluLookAt(150.0, 0.0, 100.0, # Pos. ojo
          -2000.0, 0.0, -1000.0, # Apunte
          0.0, 0.0, 1.0 # Qué eje arriba
         )

glEnable(GL_LIGHTING)
initLight()

# Bucle de la aplicación
run = True
while run:
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
                rotacionZ = not rotacionZ
            if event.key == K_LEFT:
                contador += 1
                modelo = contador%len(modelos)
            if event.key == K_RIGHT:
                contador -= 1
                modelo = contador%len(modelos)
            if event.key == K_p:
                pausa = not pausa
            if event.key == K_g:
                show_grid = not show_grid
            if event.key == K_a:
                show_axes = not show_axes
        
    # 2: Ejecutar "lógica" de la aplicación
    if not pausa:
        ang += omega*DT
    if ang >= 360:
        ang = 0.0
        
    if rotacionZ:
        ejeRot = [0,0,1]
    else:
        ejeRot = [0,1,0]
    
    # 3: Dibujar los elementos
    # Limpiar pantalla
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    if show_axes:
        glCallList(ejes)
    if show_grid:
        glCallList(grilla)
    dibujarLista(modelos[modelo].lista, angRot=ang, ejeRot=ejeRot)
    
    pygame.display.flip()


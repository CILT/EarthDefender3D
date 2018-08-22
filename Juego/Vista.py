# -*- coding: utf-8 -*-
"""
Archivo que se encarga del escenario del juego.
Autor: Cristián Llull T.
"""

# Importar PyGame
import pygame
from pygame.locals import *
import os

# Importar OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from FuncionesAuxiliares import *      
        
##################################################################
# Inicialización

def init_pygame((w, h)):
	pygame.init()
	pygame.display.set_mode((w,h), OPENGL|DOUBLEBUF)
	os.environ['SDL_VIDEO_CENTERED'] = '1'

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
	#gluPerspective(60.0, float(w)/float(h), 0.1, 20000.0)
	glOrtho(-w,w,-h,h,1,20000)
	# Ahora los comandos para matriz modifican Model_View
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

#################################################################

def initLight():
	# Ajuste de parámetros de luminosidad (ambiente, difusa, etc.)

	glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0]) # Ambient intensity of light
	glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0]) # Diffuse intensity of light
	glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0]) # Specular intensity of light

	glLightfv(GL_LIGHT0, GL_POSITION, [-3000.0, -3000.0, 3000.0, 1.0]) # (x,y,z,w) position of light
	glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [1.0, 1.0, -1.0]) # (x,y,z) direction of Spotlight (spot es foco)

	glLightfv(GL_LIGHT0, GL_SPOT_EXPONENT, 0.0) # Spotlight exponent
	glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, 180.0) # Spot cutoff angle (como hasta donde llega)

	glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0) # Constant attenuation factor
	glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.0) # Linear attenuation factor
	glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.0) # Quadratic attenuation factor

	glEnable(GL_LIGHT0)





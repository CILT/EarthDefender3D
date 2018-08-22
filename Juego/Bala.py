# -*- coding: utf-8 -*-
"""
Archivo que genera la bala.
Autor: Cristián Llull T.
"""

# Importar PyGame
import pygame
from pygame.locals import *

# Importar OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from FuncionesAuxiliares import *

class Bala:
	def __init__(self, pos=[0,0,0]):
		self.pos = pos
		self.vel = -20.0
		self.vida = True
		self.lista = None
		
	def avanzar(self, dt):
		# Se actualiza con aceleración
		self.vel += dt * 95.0
		self.pos[1] -= self.vel
		
	def cargar(self):
		lista = glGenLists(1)
		glNewList(lista, GL_COMPILE)
		glPushMatrix()
		glColor4f(pardo_cobre[0], pardo_cobre[1], pardo_cobre[2], 1.0)
		glMaterialfv(GL_FRONT, GL_AMBIENT, [0.19125,0.0735,0.0225,1.0])
		glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.7038,0.27048,0.0828,1.0])
		glMaterialfv(GL_FRONT, GL_SPECULAR,[0.356777,0.237622,0.186014,1.0])
		glMaterialfv(GL_FRONT, GL_SHININESS, [0.1*128])
		glMaterialfv(GL_FRONT, GL_EMISSION, [0.0,0.0,0.0,1.0])
		glRotate(90,1,0,0)
		glScalef(1.5,1.5,1.5)
		
		esferaGlut([0,0,10], 5)
		cilindroGlut([0,0,0], 5, 20)
		
		glPopMatrix()
		glEndList()
		
		self.lista = lista
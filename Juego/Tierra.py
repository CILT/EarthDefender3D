# -*- coding: utf-8 -*-
"""
Archivo que se encarga de crear al planeta Tierra.
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

class Tierra():
	def __init__(self, pos=[0,0,0]):
		self.pos = pos
		self.vidas = 10
		self.lista = None
		
	
	def cargar(self):
		lista = glGenLists(1)
		glNewList(lista, GL_COMPILE)
		glPushMatrix()
		glColor4f(azul_senales[0],azul_senales[1],azul_senales[2],1.0)
		esferaGlut(self.pos, 100)
		glPopMatrix()
		glEndList()
		
		self.lista = lista
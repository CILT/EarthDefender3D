# -*- coding: utf-8 -*-
"""
Archivo que genera el meteorito.
Autor: Cristián Llull T.
"""

# Importar PyGame
import pygame
from pygame.locals import *

# Importar OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random

from FuncionesAuxiliares import *

class MeteoritoMadre:
    def __init__(self, pos=[0,0,0]):
        self.pos = pos
        self.lista = None
        
        
    def cargar(self):
        fileName = 'Archivos/My_Scan_17.stl'
        if stl_is_text(fileName):
            lista = load_text_stl(fileName)
        else:
            lista = load_binary_stl(fileName)
        lista_aux = glGenLists(1)
        
        glNewList(lista_aux, GL_COMPILE)
        glPushMatrix()
        glShadeModel(GL_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)

        glScalef(0.7, 0.7, 0.7)
        glTranslatef(0, 0, -20) # Para que el centro quede en [0,0,0]

        glMaterialfv(GL_FRONT, GL_AMBIENT, [1.0,1.0,1.0,1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0,1.0,1.0,1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR,[1.0,1.0,1.0,1.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [10.0])
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0,0.0,0.0,1.0])
        glColor4f(pardo_corzo[0],pardo_corzo[1],pardo_corzo[2], 1.0)
        glCallList(lista)
        glPopMatrix()
        glEndList()
        
        self.lista = lista_aux
        
class Meteorito:
    def __init__(self, pos, lista, escala=None):
        self.pos = pos
        self.vel = 0.0
        if escala == None:
            escala = random.randint(1,6)
            division = random.randint(1,4)
            self.escala = [1.0*escala/division, 1.0*escala/division, 1.0*escala/division]
        else:
            self.escala = escala
        self.lista = lista
        self.vida = True
        pygame.mixer.init(44100, -16, 2, 2048) # Frecuencia
        self.sonido_explosion = pygame.mixer.Sound("Archivos/explosion.ogg")
        self.sonido_explosion.set_volume(0.2)
    
    def avanzar(self, dt):
        # Realiza movimiento del meteorito
        # Itinerario: v = v0 + a*t
        self.vel += self.escala[0] * 6.0 * dt
        # Se modifica la posición con su velocidad
        self.pos[1] += self.vel
        
    def choca(self, bala):
        pos_neta_bala_x = bala.pos[0] + 1000
        pos_neta_meteorito_x = self.pos[0] + 1000
        dif_neta_x = abs(pos_neta_bala_x - pos_neta_meteorito_x)
        pos_neta_bala_y = bala.pos[1] + 1000
        pos_neta_meteorito_y = self.pos[1] + 1000
        dif_neta_y = abs(pos_neta_bala_y - pos_neta_meteorito_y)
        
        if dif_neta_x <= 60*self.escala[0] and dif_neta_y <= 50*self.escala[0]:
            return True
        return False

    
        
        
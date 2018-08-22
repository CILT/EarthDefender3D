# -*- coding: utf-8 -*-
"""
Programa para visualizar los modelos que compondrán el juego "Earth Defender 3D".
Autor: Cristián Llull T.
Creado en Python 2.7.1
"""

# Importar PyGame
import pygame
from pygame.locals import *

# Importar OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from FuncionesAuxiliares import *
from Bala import *
from Misil import *

class Nave:
    def __init__(self, tipo, pos=[0,0,0], luz=False):
        self.lista = None
        self.tipo = tipo
        self.pos = pos
        self.luz = luz
        self.vel = 30
        self.scale = [1,1,1]
        self.balas = []
        self.misil_madre = MisilMadre()
        self.misiles = []
        self.cant_especial = 5
        self.cant_misil = 5
        # Explosiones
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096) # Frecuencia
        self.sonido_disparo = pygame.mixer.Sound("Archivos/laser.ogg")
        self.sonido_disparo.set_volume(0.2)
        
    def disparar(self):
        bala = Bala([self.pos[0], self.pos[1] + 5, self.pos[2] + 5])
        bala.cargar()
        self.balas.append(bala)
        self.sonido_disparo.play()
        
    def dispararMisil(self):
        misil = Misil([self.pos[0], self.pos[1], self.pos[2] + 5], self.misil_madre.lista)
        self.misiles.append(misil)
        self.sonido_disparo.play()
        self.cant_misil -= 1
        
    def dispararEspecial(self):
        for i in range(22):
            bala = Bala([self.pos[0] + 640 - i*1200/20.0 , self.pos[1] + 5, self.pos[2] + 5])
            bala.cargar()
            self.balas.append(bala)
        self.sonido_disparo.play()
        self.cant_especial -= 1
        
    def moverDer(self):
        self.pos[0] -= self.vel
        
    def moverIzq(self):
        self.pos[0] += self.vel
        
    def subir(self):
        self.pos[1] -= self.vel
        
    def bajar(self):
        self.pos[1] += self.vel
        
    def cargar(self):
        if self.tipo == 'stl':
            self.lista = self.cargarMilleniumFalcon()
        elif self.tipo == 'glut':
            self.lista = self.cargarNaveGlut()
        elif self.tipo == 'mano':
            self.lista = self.cargarNaveMano()
            
    def encenderLinterna(self):
        glLightfv(GL_LIGHT1, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0]) # Ambient intensity of light
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [verde_puro[0], verde_puro[1], verde_puro[2], 1.0]) # Diffuse intensity of light
        glLightfv(GL_LIGHT1, GL_SPECULAR, [verde_puro[0], verde_puro[1], verde_puro[2], 1.0]) # Specular intensity of light

        glLightfv(GL_LIGHT1, GL_POSITION, [self.pos[0], self.pos[1], self.pos[2], 1.0]) # (x,y,z,w) position of light
        glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, [0.0, -1.0, 0.0]) # (x,y,z) direction of Spotlight (spot es foco)

        glLightfv(GL_LIGHT1, GL_SPOT_EXPONENT, 0.0) # Spotlight exponent
        glLightfv(GL_LIGHT1, GL_SPOT_CUTOFF, 20.0) # Spot cutoff angle (como hasta donde llega)

        glLightfv(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 1.0) # Constant attenuation factor
        glLightfv(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.0) # Linear attenuation factor
        glLightfv(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.0) # Quadratic attenuation factor
        glEnable(GL_LIGHT1)
        
    def apagarLinterna(self):
        glDisable(GL_LIGHT1)
        
        
            
##############################################################################
# Dibujos
# Se retorna la lista

    def cargarMilleniumFalcon(self):
        lista = load_binary_stl('Archivos/MilleniumFalcon2.STL')
        lista_aux = glGenLists(1)
        glNewList(lista_aux, GL_COMPILE)
        # Le vamos a dar material
        glPushMatrix()
        glShadeModel(GL_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)

        glScalef(1.0, 1.0, 1.0)
        glTranslatef(-45, -55, 0) # Para que el centro quede en [0,0,0]

        glMaterialfv(GL_FRONT, GL_AMBIENT, [1.0,1.0,1.0,1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.4,0.4,0.4,1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR,[1.0,1.0,1.0,1.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [6.0])
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0,0.0,0.0,1.0])
        glColor4f(127/255.0, 118/255.0, 121/255.0, 1.0) # Gris Platino
        glCallList(lista)
        glPopMatrix()
        glEndList()
        return lista_aux
        
    def cargarNaveGlut(self):
        
        lista = glGenLists(1)
        glNewList(lista, GL_COMPILE)
        
        glPushMatrix()
        glShadeModel(GL_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)
        
        glRotatef(90, 1, 0, 0)
        
        # Material
        glColor4f(blanco_perla[0], blanco_perla[1], blanco_perla[2], 1.0)
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.6,0.6,0.6,1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0,1.0,1.0,1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR,[1.0,1.0,1.0,1.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [3.0])
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0,0.0,0.0,1.0])
        
        # Cuerpo
        cilindroGlut([0,0,0], 10, 100) # pos, radio, alto
        
        # Alas
        paralelepipedoGlut([10,0,12], 15, 3, 2.23*20, -18, [0,1,0]) # pos, anch_x, anch_y, anch_z, ang_rot, eje_rot
        glPushMatrix()
        glRotatef(120, 0, 0, 1)
        paralelepipedoGlut([10,0,12], 15, 3, 2.23*20, -18, [0,1,0])
        glPopMatrix()
        glPushMatrix()
        glRotatef(240, 0, 0, 1)
        paralelepipedoGlut([10,0,12], 15, 3, 2.23*20, -18, [0,1,0])
        glPopMatrix()
        
        # Punta
        glColor4f(rojo_trafico[0], rojo_trafico[1], rojo_trafico[2], 1.0)
        conoGlut([0,0,50], 10, 100/5.0) # pos, radio, alto
        
        # Cabina bacán
        glColor4f(azul_azur[0], azul_azur[1], azul_azur[2], 0.5)
        toroideGlut([0,0,-25], 10, 27, 0.5) # pos, radio_int, radio_ext, «achatamiento»
        
        glPopMatrix()
        glEndList()
        return lista
        
        
    def cargarNaveMano(self):
        
        lista = glGenLists(1)
        
        glNewList(lista, GL_COMPILE)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)
        # Parámetros de cromo
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.25,0.25,0.25,1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.4,0.4,0.4,1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR,[0.774597,0.774597,0.774597,1.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [0.6*128])
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0,0.0,0.0,1.0])
        
        glRotate(90,1,0,0)
        
        # Antena
        glPushMatrix()
        # Parámetros de plástico
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.0,0.0,0.0,1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.5,0.0,0.0,1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR,[0.7,0.6,0.6,1.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [0.25*128])
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0,0.0,0.0,1.0])
        glColor4f(azul_azur[0],azul_azur[1],azul_azur[2],1.0)
        
        glTranslatef(0,0,45)
        glScalef(3,3,15)
        generarCono(200)
        glPopMatrix()
        
        # Punta arriba
        glPushMatrix()
        glColor4f(gris_platino[0],gris_platino[1],gris_platino[2],1.0)
        glTranslatef(0,0,35)
        glScalef(20,20,15)
        generarCono(200)
        glPopMatrix()
        
        # Punta abajo
        glPushMatrix()
        glColor4f(gris_platino[0],gris_platino[1],gris_platino[2],1.0)
        glTranslatef(0,0,30)
        glScalef(20,20,10)
        generarCilindro()
        glPopMatrix()
        
        # Cuerpo
        glPushMatrix()
        glColor4f(gris_platino[0],gris_platino[1],gris_platino[2],1.0)
        glTranslatef(0,0,-10)
        glScalef(14,14,75)
        generarCilindro()
        glPopMatrix()
        
        # Anillo Naranjo
        glPushMatrix()
        glColor4f(naranja_palido[0],naranja_palido[1],naranja_palido[2],1.0)
        glTranslatef(0,0,20)
        glScalef(17,17,10)
        generarCilindro()
        glPopMatrix()
        
        # Propulsores
        glPushMatrix()
        glTranslate(6,0,-47)
        glScale(20,20,45)
        generarCono(200)
        glPopMatrix()
        
        glPushMatrix()
        glRotate(120,0,0,1)
        glPushMatrix()
        glTranslate(6,0,-47)
        glScale(20,20,45)
        generarCono(200)
        glPopMatrix()
        glPopMatrix()
        
        glPushMatrix()
        glRotate(240,0,0,1)
        glPushMatrix()
        glTranslate(6,0,-47)
        glScale(20,20,45)
        generarCono(200)
        glPopMatrix()
        glPopMatrix()
        
        glEndList()
        return lista
        
        
        
        
        
        
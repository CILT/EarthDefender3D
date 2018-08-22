# -*- coding: utf-8 -*-
"""
Archivo que se encarga del escenario del juego.
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
from Nave import *
from Bala import *
from Meteorito import *
from Tierra import *

class Escenario():
    def __init__(self, nave, tamano_ventana):
        self.width = tamano_ventana[0]
        self.height = tamano_ventana[1]
        self.nave = nave
        self.tierra = Tierra()
        self.meteoritoInicial = MeteoritoMadre()
        self.meteoritos = []
        
        self.contadorTiempo = 0.0
        self.tiempoGeneracionMeteoritos = 3.0
        self.puntuacion = 0
        self.vidas_tierra = 10
        
        self.comenzarJuego()
        
        # Música de fondo
        pygame.mixer.music.load("Archivos/background.ogg")
        pygame.mixer.music.play(-1,0.0)
        
    def comenzarJuego(self):
        print 'Cargando escenario...'
        self.nave.pos = [0,0,0]
        print 'Cargando nave...'
        self.nave.cargar()
        print 'Cargando misil...'
        self.nave.misil_madre.cargar()
        self.tierra.pos = [0, self.height/4.0, -200]
        print 'Cargando tierra...'
        self.tierra.cargar()
        print 'Cargando meteoritos...'
        self.meteoritoInicial.cargar()
        
        
    def actualizar(self, DT):
        
        # Movimiento de objetos
        # Meteorito
        for meteorito in self.meteoritos:
            meteorito.avanzar(DT)
            if meteorito.pos[1] >= self.height + 250:
                self.tierra.vidas -= 1
                meteorito.vida = False
                print 'Auch! Un meteorito ha impactado la Tierra!'
                self.vidas_tierra -= 1
                
            # Aprovechamos el for para ver los choques:
            for bala in self.nave.balas:
                if meteorito.choca(bala):
                    if meteorito.escala[0] >= 3:
                        escala = meteorito.escala[0]/4.0
                        self.crearNuevoMeteorito([meteorito.pos[0] + 100, meteorito.pos[1], meteorito.pos[2]], [escala,escala,escala])
                        self.crearNuevoMeteorito([meteorito.pos[0] - 100, meteorito.pos[1], meteorito.pos[2]], [escala,escala,escala])

                    meteorito.vida = False
                    bala.vida = False
                    self.puntuacion += 1
                    print 'Meteorito destruido! -- Puntuación: ' + str(self.puntuacion)
                    if self.puntuacion%10 == 0:
                        if self.tiempoGeneracionMeteoritos >= 0.3: # Si no, se empiezan a generar infinitos
                            self.tiempoGeneracionMeteoritos /= 1.2
                            print '10 meteoritos destruidos! Incremento de dificultad :o'
                            
        # Misiles
        destruir = False
        for misil in self.nave.misiles:
            misil.avanzar(DT)
            if misil.pos[1] <= -self.height - 250:
                misil.vida = False
            for meteorito in self.meteoritos:
                if meteorito.choca(misil):
                    destruir = True
                    misil.vida = False
                    break
            if destruir:
                for meteorito in self.meteoritos:
                    meteorito.vida = False
                    self.puntuacion += 1 # Suma cada meteorito
                print 'Meteorito destruido! -- Puntuación: ' + str(self.puntuacion)
                        
                        
        # Bala
        for bala in self.nave.balas:
            bala.avanzar(DT)
            if bala.pos[1] <= -self.height - 250:
                bala.vida = False
                
        
        # Generación de nuevos meteoritos
        self.contadorTiempo += DT
        if self.contadorTiempo >= self.tiempoGeneracionMeteoritos:
            self.crearNuevoMeteorito()
            self.contadorTiempo = 0.0
                
    # Limpia el escenario de objetos muertos
    def limpiar(self):
        # Limpiar
        k = 0
        for meteorito in self.meteoritos:
            if not meteorito.vida:
                self.meteoritos.pop(k)
                meteorito.sonido_explosion.play()
            k += 1
        k = 0
        for bala in self.nave.balas:
            if not bala.vida:
                self.nave.balas.pop(k)
            k += 1
            
        k = 0
        for misil in self.nave.misiles:
            if not misil.vida:
                self.nave.misiles.pop(k)
            k += 1
                
    # Crea un meteorito en posición aleatoria
    def crearNuevoMeteorito(self, pos=None, escala=None):
        if pos == None:
            posicion = random.randint(0,self.width)
            lado = random.randint(1,2)
            if lado == 1:
                costado = -1.0
            else:
                costado = 1.0
            nuevo_meteorito = Meteorito([costado*posicion, -self.height - 250, 0], self.meteoritoInicial.lista, escala)
        else:
            nuevo_meteorito = Meteorito(pos, self.meteoritoInicial.lista, escala)
            
        self.meteoritos.append(nuevo_meteorito)
            
# -*- coding: utf-8 -*-
"""
Funciones auxiliares destinadas a alivianar trabajo de dibujo e interacciones.
Autor: Cristián Llull T.
"""
import struct
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

########################################################################
# Colores
blanco_perla = [234/255.0, 230/255.0, 202/255.0]
azul_luminoso = [59/255.0, 131/255.0, 189/255.0]
gris_luminoso = [215/255.0, 215/255.0, 215/255.0]
gris_seda = [202/255.0, 196/255.0, 176/255.0]
gris_platino = [127/255.0, 118/255.0, 121/255.0]
rojo_trafico = [204/255.0,6/255.0,5/255.0]
azul_azur = [2/255.0,86/255.0,105/255.0]
pardo_cobre = [142/255.0,64/255.0,42/255.0]
pardo_corzo = [89/255.0,53/255.0,31/255.0]
naranja_palido = [255/255.0,117/255.0,20/255.0]
azul_senales = [30/255.0,45/255.0,110/255.0]
amarillo_azufre = [237/255.0, 255/255.0, 33/255.0]
verde_puro = [36/255.0,231/255.0,17/255.0]

########################################################################
# Figuras GLUT

def cilindroGlut(pos, radio, alto):
    glPushMatrix()
    # Se orienta según z
    glTranslatef(pos[0], pos[1], pos[2] - alto/2.0)
    glutSolidCylinder(radio, alto, 200, 200) # radius, height, slices, stacks
    glPopMatrix()
    
def paralelepipedoGlut(pos, ancho_x, ancho_y, ancho_z, angRot, ejeRot):
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    glRotatef(angRot, ejeRot[0], ejeRot[1], ejeRot[2])
    glScalef(ancho_x, ancho_y, ancho_z)
    glutSolidCube(1)
    glPopMatrix()
    
def conoGlut(pos, radio, alto):
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    glutSolidCone(radio, alto, 200, 200) # base radius, height, slices, stacks
    glPopMatrix()
    
def toroideGlut(pos, innerRadius, outerRadius, achatamiento):
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    glScalef(1.0,1.0,achatamiento)
    glutSolidTorus(innerRadius, outerRadius, 100, 200) # innerRadius, outerRadius, nsides, rings
    glPopMatrix()
    
def esferaGlut(pos, radio):
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    glutSolidSphere(radio, 200, 200) # radio, slices, stacks
    glPopMatrix()

#############################################################################
# Generación de objetos A MANO

# Genera cubo unitario
def generarCubo_FLAT():
    # vértices
    a = (-0.5,-0.5, -0.5)
    b = (0.5, -0.5, -0.5)
    c = (0.5, 0.5, -0.5)
    d = (-0.5, 0.5, -0.5)
    e = (-0.5, 0.5, 0.5)
    f = (0.5, 0.5, 0.5)
    g = (-0.5, -0.5, 0.5)
    h = (0.5, -0.5, 0.5)
    
    # Normales (una por cada cara)
    n1 = [0, 0, -1]
    n2 = [0, 1, 0]
    n3 = [0, 0, 1]
    n4 = [0, -1, 0]
    n5 = [-1, 0, 0]
    n6 = [1, 0, 0]
    
    lista = glGenLists(1)
    
    glNewList(lista, GL_COMPILE)
    glBegin(GL_QUADS)
    # Se diibujam las caras
    glNormal3fv(n1)
    glVertex3fv(a)
    glVertex3fv(b)
    glVertex3fv(c)
    glVertex3fv(d)
    
    glNormal3fv(n2)
    glVertex3fv(c)
    glVertex3fv(d)
    glVertex3fv(e)
    glVertex3fv(f)
    
    glNormal3fv(n3)
    glVertex3fv(e)
    glVertex3fv(f)
    glVertex3fv(h)
    glVertex3fv(g)
    
    glNormal3fv(n4)
    glVertex3fv(a)
    glVertex3fv(g)
    glVertex3fv(h)
    glVertex3fv(b)
    
    glNormal3fv(n5)
    glVertex3fv(a)
    glVertex3fv(d)
    glVertex3fv(e)
    glVertex3fv(g)
    
    glNormal3fv(n6)
    glVertex3fv(b)
    glVertex3fv(c)
    glVertex3fv(f)
    glVertex3fv(h)
    
    glEnd()
    glEndList()
    
    return lista

# Genera cubo unitario
def generarCubo_SMOOTH():
    # vértices
    a = (-0.5,-0.5, -0.5)
    b = (0.5, -0.5, -0.5)
    c = (0.5, 0.5, -0.5)
    d = (-0.5, 0.5, -0.5)
    e = (-0.5, 0.5, 0.5)
    f = (0.5, 0.5, 0.5)
    g = (-0.5, -0.5, 0.5)
    h = (0.5, -0.5, 0.5)
    
    # Normales (una por cada cara)
    n1 = [0, 0, -1]
    n2 = [0, 1, 0]
    n3 = [0, 0, 1]
    n4 = [0, -1, 0]
    n5 = [-1, 0, 0]
    n6 = [1, 0, 0]
    
    # Definimos ahora las normales en las esquinas
    na = vectorPromedio(n1, n4, n5)
    nb = vectorPromedio(n1, n4, n6)
    nc = vectorPromedio(n1, n2, n6)
    nd = vectorPromedio(n1, n2, n5)
    ne = vectorPromedio(n2, n3, n5)
    nf = vectorPromedio(n2, n3, n6)
    ng = vectorPromedio(n3, n4, n5)
    nh = vectorPromedio(n3, n4, n6)
    
    lista = glGenLists(1)
    
    glNewList(lista, GL_COMPILE)
    glBegin(GL_QUADS)
    # Se diibujam las caras
    glNormal3fv(na)
    glVertex3fv(a)
    glNormal3fv(nb)
    glVertex3fv(b)
    glNormal3fv(nc)
    glVertex3fv(c)
    glNormal3fv(nd)
    glVertex3fv(d)
    
    glNormal3fv(nc)
    glVertex3fv(c)
    glNormal3fv(nd)
    glVertex3fv(d)
    glNormal3fv(ne)
    glVertex3fv(e)
    glNormal3fv(nf)
    glVertex3fv(f)
    
    glNormal3fv(ne)
    glVertex3fv(e)
    glNormal3fv(nf)
    glVertex3fv(f)
    glNormal3fv(nh)
    glVertex3fv(h)
    glNormal3fv(ng)
    glVertex3fv(g)
    
    glNormal3fv(na)
    glVertex3fv(a)
    glNormal3fv(ng)
    glVertex3fv(g)
    glNormal3fv(nh)
    glVertex3fv(h)
    glNormal3fv(nb)
    glVertex3fv(b)
    
    glNormal3fv(na)
    glVertex3fv(a)
    glNormal3fv(nd)
    glVertex3fv(d)
    glNormal3fv(ne)
    glVertex3fv(e)
    glNormal3fv(ng)
    glVertex3fv(g)
    
    glNormal3fv(nb)
    glVertex3fv(b)
    glNormal3fv(nc)
    glVertex3fv(c)
    glNormal3fv(nf)
    glVertex3fv(f)
    glNormal3fv(nh)
    glVertex3fv(h)
	
    glEnd()
    glEndList()
    
    return lista

# Genera cilindro de altura 1, centrado en origen
def generarCilindroLista():
    radio = 0.5
    z = 0.5
    vertices_cara_sup = []
    vertices_cara_inf = []
    normal_sup = [0,0,1]
    normal_inf = [0,0,-1]
    normales_manto = []
    ang_i = 0
    cant_vertices = 100
    ang = 2*math.pi/cant_vertices
    for i in range(cant_vertices + 1):
        ang_i = ang*i
        radio_x = radio*math.cos(ang_i)
        radio_y = radio*math.sin(ang_i)
        vertices_cara_sup.append([radio_x, radio_y, z])
        vertices_cara_inf.append([radio_x, radio_y, -z])
        radio_x_normal = radio*math.cos(ang_i/2 + ang*(i+1)/2)
        radio_y_normal = radio*math.sin(ang_i/2 + ang*(i+1)/2)
        normales_manto.append(vectorPromedio([radio_x_normal,0.0,0.0], [0.0,radio_y_normal,0.0]))
    
    lista = glGenLists(1)
    
    glNewList(lista, GL_COMPILE)
    
    # Tapa
    glBegin(GL_TRIANGLE_FAN)
    glNormal3fv(normal_sup)
    glVertex3fv([0,0,z])
    for vert in vertices_cara_sup:
        glVertex3fv(vert)
    glEnd()
    
    # Suelo
    glBegin(GL_TRIANGLE_FAN)
    glNormal3fv(normal_inf)
    glVertex3fv([0,0,-z])
    for vert in vertices_cara_inf:
        glVertex3fv(vert)
    glEnd()
    
    # Caras
    glBegin(GL_QUADS)
    for i in range(cant_vertices):
        glNormal3fv(normales_manto[i])
        glVertex3fv(vertices_cara_sup[i])
        glVertex3fv(vertices_cara_sup[i+1])
        glVertex3fv(vertices_cara_inf[i+1])
        glVertex3fv(vertices_cara_inf[i])
    glNormal3fv(normales_manto[cant_vertices])
    glVertex3fv(vertices_cara_sup[cant_vertices])
    glVertex3fv(vertices_cara_sup[0])
    glVertex3fv(vertices_cara_inf[0])
    glVertex3fv(vertices_cara_inf[cant_vertices])
    
    glEnd()
    
    glEndList()
    
    return lista

# Genera cilindro de altura 1, centrado en origen
def generarCilindro():
    radio = 0.5
    z = 0.5
    vertices_cara_sup = []
    vertices_cara_inf = []
    normal_sup = [0,0,1]
    normal_inf = [0,0,-1]
    normales_manto = []
    ang_i = 0
    cant_vertices = 200
    ang = 2*math.pi/cant_vertices
    for i in range(cant_vertices + 1):
        ang_i = ang*i
        radio_x = radio*math.cos(ang_i)
        radio_y = radio*math.sin(ang_i)
        vertices_cara_sup.append([radio_x, radio_y, z])
        vertices_cara_inf.append([radio_x, radio_y, -z])
        radio_x_normal = radio*math.cos(ang_i/2 + ang*(i+1)/2)
        radio_y_normal = radio*math.sin(ang_i/2 + ang*(i+1)/2)
        normales_manto.append(vectorPromedio([radio_x_normal,0.0,0.0], [0.0,radio_y_normal,0.0]))
    
    glPushMatrix()
    # Tapa
    glBegin(GL_TRIANGLE_FAN)
    glNormal3fv(normal_sup)
    glVertex3fv([0,0,z])
    for vert in vertices_cara_sup:
        glVertex3fv(vert)
    glEnd()
    
    # Suelo
    glBegin(GL_TRIANGLE_FAN)
    glNormal3fv(normal_inf)
    glVertex3fv([0,0,-z])
    for vert in vertices_cara_inf:
        glVertex3fv(vert)
    glEnd()
    
    # Caras
    glBegin(GL_QUADS)
    for i in range(cant_vertices):
        glNormal3fv(normales_manto[i])
        glVertex3fv(vertices_cara_sup[i])
        glVertex3fv(vertices_cara_sup[i+1])
        glVertex3fv(vertices_cara_inf[i+1])
        glVertex3fv(vertices_cara_inf[i])
    glNormal3fv(normales_manto[cant_vertices])
    glVertex3fv(vertices_cara_sup[cant_vertices])
    glVertex3fv(vertices_cara_sup[0])
    glVertex3fv(vertices_cara_inf[0])
    glVertex3fv(vertices_cara_inf[cant_vertices])
    
    glEnd()
    
    glPopMatrix()

# Genera Cono con el centro de su base en el origen, altura 1
def generarCono(cant_caras):
    """
    cant_caras: número de caras. Se puede hacer una pirámide, por ejemplo, con 4.
    """
    # Definir los vértices
    cuspide = [0,0,1]
    base = []
    normales = []
    radio = 0.5
    # Vertices base
    ang_i = 0.0
    cant_vertices = cant_caras
    ang = 2*math.pi/cant_vertices
    for i in range(cant_vertices):
        ang_i = ang * i
        radio_x = radio * math.cos(ang_i)
        radio_y = radio * math.sin(ang_i)
        base.append([radio_x, radio_y, 0])
        normal_prom = vectorPromedio([radio_x,0.0,0.0], [0.0,radio_y,0.0], [0.0,0.0,1.0])
        normales.append([normal_prom[0], normal_prom[1], normal_prom[2]])
    
    # Se genera el cono
    glPushMatrix()
    # Base
    glBegin(GL_TRIANGLE_FAN)
    glNormal3fv([0.0,0.0,-1.0])
    glVertex3fv([0,0,0]) # Origen
    for vert in base:
        glVertex3fv(vert)
    glVertex3fv(base[0])
        
    glEnd()
    
    # Manto
    glBegin(GL_TRIANGLES)
    
    for i in range(cant_vertices - 1):
        normal = vectorPromedio(base[i], [0,0,1]) # Asociada a las aristas
        glNormal3fv(normales[i])
        glVertex3fv(cuspide)
        glVertex3fv(base[i])
        glVertex3fv(base[i+1])
    ultimo = base[cant_vertices - 1]
    normal = normales[cant_vertices - 1]
    #normal = vectorPromedio(ultimo, [0,0,1])
    glNormal3fv(normal)
    glVertex3fv(cuspide)
    glVertex3fv(ultimo)
    glVertex3fv(base[0])
    
    glEnd()
    
    glPopMatrix()


##############################################################################################
# Lectura de archivos STL

# Detecta si un archivo dado es binario o de texto
# Retorna True si es de texto
def stl_is_text(fileName):
    file = open(fileName, 'r')
    h = file.read(80)
    type = h[0:5]
    file.close()
    if type == 'solid':
        return True
    else:
        return False
    
# Lee un archivo stl en forma de texto
def load_text_stl(fileName):
    """ Los archivos stl vienen con triángulos """
    file = open(fileName, 'r')
    
    lista = glGenLists(1)
    
    glNewList(lista, GL_COMPILE)
    
    glBegin(GL_TRIANGLES)
    for line in file.readlines():
        words = line.split()
        if len(words) > 0:
            if words[0] == 'solid': # Si la primera palabra es solid, viene el nombre del archivo
                continue
                
            elif words[0] == 'facet': # Vienen las normales
                glNormal3fv([float(words[2]), float(words[3]), float(words[4])])
                
            elif words[0] == 'vertex': # Vienen los vértices
                glVertex3fv([float(words[1]), float(words[2]), float(words[3])])
    glEnd()
    glEndList()
    file.close()
    return lista
    
def load_binary_stl(fileName):
    file = open(fileName, 'rb')
    h = file.read(80) # 80 primeros bits son extraños
    # struct: pasa de carácter 'C' a 'Python'
    l = struct.unpack('I', file.read(4))[0] # Número de triángulos
    
    lista = glGenLists(1)
    
    glNewList(lista, GL_COMPILE)
    
    glBegin(GL_TRIANGLES)
    
    count = 0
    while True:
        try:
            p = file.read(12)
            if len(p) == 12: # Verificación
                # Primera lectura: normal
                # Importa como: n = a, b, c -> n = [a, b, c]
                n = struct.unpack('f', p[0:4])[0], struct.unpack('f', p[4:8])[0], struct.unpack('f', p[8:12])[0]
            
            p = file.read(12)
            if len(p) == 12:
                # Segunda lectura: primer punto
                p1 = struct.unpack('f', p[0:4])[0], struct.unpack('f', p[4:8])[0], struct.unpack('f', p[8:12])[0]
                
            p = file.read(12)
            if len(p) == 12:
                # Tercera lectura: segundo punto
                p2 = struct.unpack('f',p[0:4])[0], struct.unpack('f', p[4:8])[0], struct.unpack('f', p[8:12])[0]
                
            p = file.read(12)
            if len(p) == 12:
                # Cuarta lectura: tercer punto
                p3 = struct.unpack('f', p[0:4])[0], struct.unpack('f', p[4:8])[0], struct.unpack('f', p[8:12])[0]
            
            # Generar el triángulo
            glNormal3fv(n)
            glVertex3fv(p1)
            glVertex3fv(p2)
            glVertex3fv(p3)
            
            # Verificamos fin de archivo
            p = file.read(2)
            if len(p) == 0:
                break
        except EOFError:
            break
    glEnd()
    glEndList()
    file.close()
    return lista
    
                
############### Ejes #############################################################
                
def generarEjes(h):
    """
    h: tamaño de los ejes
    Los colores son:
     - eje x: rojo
     - eje y: verde
     - eje z: azul
    """
    # Vértices para los ejes
    x = [h, 0, 0, 1]
    y = [0, h, 0, 1]
    z = [0, 0, h, 1]
    origen = [0, 0, 0, 1]
    
    # Originamos la lista
    lista = glGenLists(1)
    glNewList(lista, GL_COMPILE)
    
    glBegin(GL_LINES)
    # Eje x
    glColor4fv([1,0,0,1])
    glVertex4fv(origen)
    glVertex4fv(x)
    
    # Eje y
    glColor4fv([0,1,0,1])
    glVertex4fv(origen)
    glVertex4fv(y)
    
    # Eje z
    glColor4fv([0,0,1,1])
    glVertex4fv(origen)
    glVertex4fv(z)
    
    glEnd()
    glEndList()
    
    return lista

def generarGrilla(h):
    """
    Genera una grilla para ver bien los tamaños
    """
    lista = glGenLists(1)
    glNewList(lista, GL_COMPILE)
    
    glBegin(GL_LINES)
    glColor4f(1.0,1.0,1.0,1.0)
    for i in range(-h,h,50):
        nuevoOrigen = [0,i,0,1] # Se va desplazando en y
        x = [h,i,0,1]
        y = [0,h,0,1]
        z = [0,i,h,1]
        glVertex4fv(nuevoOrigen)
        glVertex4fv(x)
        glVertex4fv(nuevoOrigen)
        glVertex4fv(y)
        glVertex4fv(nuevoOrigen)
        glVertex4fv(z)
    glEnd()
    glEndList()
    return lista

########### Funciones de dibujo ####################################################

def dibujarLista(lista, pos=[0.0,0.0,0.0], angRot=0.0, ejeRot=None, scale=None, color=None):
    
    glPushMatrix()
    
    glTranslatef(pos[0], pos[1], pos[2])
    
    if not ejeRot == None: # Hay que rotar
        glRotatef(angRot, ejeRot[0], ejeRot[1], ejeRot[2])
        
    if not scale == None:
        glScalef(scale[0], scale[1], scale[2])
    
    if not color == None:
        glColor4fv(color)
        
    glCallList(lista)
    
    glPopMatrix()
    
    
######################## SOPORTE #########################################################
def vectorPromedio(vec1, vec2, vec3=None):
    n = len(vec1)
    prom = []
    if not vec3 == None:
        for i in range(n):
            prom.append( (vec1[i] + vec2[i] + vec3[i]) / 3.0 )
    else:
        for i in range(n):
            prom.append( (vec1[i] + vec2[i]) / 2.0 )
    
    return prom


                
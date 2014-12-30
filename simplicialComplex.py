#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
#import testSimplicialComplex

class Process:
    def __init__(self, id):
        self.id=id
        self.view=str(id)

    def write(self,mem):
        mem[self.id] = self.view

    def snapshot(self,mem):
        temp = ''
        for i in range(len(mem)):
            temp += mem[i]
        self.view = temp

    def __str__(self):
        return '(%d,%s)'%(self.id,self.view)

    __repr__=__str__

# Las funciones 'execution' representan las posibles 
# formas de interacción de los procesos con la memoria
# compartida.
def execution1(simplex):
    mem = ['']*len(simplex) # crea una memoria con número de entradas igual al número de procesos.
    p0 = copy.copy(simplex[0])
    p1 = copy.copy(simplex[1])
    p0.write(mem)
    p0.snapshot(mem)
    p1.write(mem)
    p1.snapshot(mem)
    return [p0,p1]

def execution2(simplex):
    mem = ['']*len(simplex)
    p0 = copy.copy(simplex[0])
    p1 = copy.copy(simplex[1])
    p0.write(mem)
    p1.write(mem)
    p0.snapshot(mem)
    p1.snapshot(mem)
    return [p0,p1]

def execution3(simplex):
    mem = ['']*len(simplex)
    p0 = copy.copy(simplex[0])
    p1 = copy.copy(simplex[1])
    p1.write(mem)
    p1.snapshot(mem)
    p0.write(mem)
    p0.snapshot(mem)
    return [p0,p1]

# <Descripción> Asocia el simplejo s a la entrada de diccionario que le corresponde. 
# <Parámetros> d: Diccionario que representa la lista de adyacencia 
#              s: Simplejo
def addToDict(d,s):
    v0 = (s[0].id,s[0].view)
    v1 = (s[1].id,s[1].view)
    if not(d.has_key(v0)):
        d[v0]=[v1]
    else:
        d[v0].append(v1)

    if not(d.has_key(v1)):
        d[v1]=[v0]
    else:
        d[v1].append(v0)

# <Descripción> Genera una representación de lista de adyacencia del complejo simplicial.
# Esto porque el objeto Graph de SAGE requere una lista de adyacencia que represente
# la gráfica para poder desplegar su visualización.
def toAdjacencyList(complex):
    d = {}
    for s in complex:
        addToDict(d,s)
    return d

# <Descripción> Crea un diccionario que asigna a cada vértice del complejo un color.
# <Parámetros> dc: Es el diccionario que representa la lista de adyacencia del complejo.
def assignColors(dc):
    c = {}
    c['#585858'] = [s for s in dc.keys() if s[0]==0]
    c['#FFFFFF'] = [s for s in dc.keys() if s[0]==1]
    return c

# <Descripción> Genera un complejo simplicial de protocolo de acuerdo a todas las 
# posibles ejecuciones de los procesos cuando se comunican por memoria compartida 
# tipo immediate snapshot. 
# <Parámetros> k: número de rondas de comunicación
#              pcomplex: complejo simplicial que se subdividirá
def generateComplexProtocol(pcomplex, k):
    tcomplex = []
    for i in xrange(k):
        tcomplex = []
        for s in pcomplex:
            simplex1 = execution1(s)
            simplex2 = execution2(s)
            simplex3 = execution3(s)
            tcomplex.extend([simplex1,simplex2,simplex3])
        pcomplex = copy.copy(tcomplex)
    #testComplex(pcomplex)
    return pcomplex

def plot(pcomplex): 
    dc = toAdjacencyList(pcomplex)
    gc = Graph(dc)
    #testMerge(dc)
    color = assignColors(dc)
    #testAssignColors(color)
    gc.show(vertex_colors=color)

k = 2
p0 = Process(0)
p1 = Process(1)
icomplex = [[p0,p1]]
pcomplex = generateComplexProtocol(icomplex,k)
print pcomplex

#plot(pcomplex)










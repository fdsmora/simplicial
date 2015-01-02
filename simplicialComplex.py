#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import testSimplicialComplex as ts
import collections as c
import pdb
import igraph as ig

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
    #TODO: REMOVER CLASE VERTEX Y DEJARLO COMO TUPLAS
    class Vertex(object):
        def __init__(self, id, view):
            self.id = (id,view)
            # self.index = 0
        def __str__(self):
            # return "({},{})".format(self.id, self.index)
            return str(self.id)
        __repr__=__str__


    v0 = Vertex(s[0].id,s[0].view)
    v1 = Vertex(s[1].id,s[1].view)

    # v0 = (s[0].id,s[0].view)
    # v1 = (s[1].id,s[1].view)

    if (v0.id not in d):
        # v0.index = next(ig)
        d[v0.id]=[]
    if (v1.id not in d):
        # v1.index = next(ig)
        d[v1.id]=[]    
    d[v0.id].append(v1.id)
    d[v1.id].append(v0.id)

    #     d[v0.id]=[v1]
    # else:
    #     d[v0.id].append(v1)

    # if (v1.id not in d):
    #     v1.index = next(ig)
    #     d[v1.id]=[v0]
    # else:
    #     d[v1.id].append(v0)

#TODO: CHECAR LO DE LISTA DE VERTICES
def buildVerticesEdges(d):
    edges = []
    vertices = list(d)
    print ("vertices todos")
    print (vertices)

    for i, k in enumerate(d):
        # print ("solo vertices en lista")
        # # print([v for v in d[k]])
        # for v in d[k]:
        #     print ("%s -- %d"%(v,vertices.index(v)))
        #     print (vertices.index(v))
        edges.extend([(i, (lambda x: vertices.index(x))(v)) for v in d[k]])
    return vertices, edges
# <Descripción> Genera una representación de lista de adyacencia del complejo simplicial.
# Esto porque el objeto Graph de SAGE requere una lista de adyacencia que represente
# la gráfica para poder desplegar su visualización.

#TODO: CAMBIAR NOMBRE
def toAdjacencyList(complex):

    # def indexGenerator():
    #     index = 0
    #     while(True):
    #         yield index
    #         index+=1

    # ig = indexGenerator();
    d = c.OrderedDict()
    for s in complex:
        addToDict(d,s)
    (vertices,edges) = buildVerticesEdges(d)
    ts.testEdges(edges)
    print ('test vertices')
    print (vertices)
    return (vertices,edges)

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
    for i in range(k):
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
    (vertices, edges) = toAdjacencyList(pcomplex)
    # testMerge(dc)
    g = ig.Graph(len(vertices))
    g.add_edges(edges)
    layout = g.layout("rt")
    ig.plot(g, layout=layout)
    #testAssignColors(color)
    # gc.show(vertex_colors=color)

k = 2
p0 = Process(0)
p1 = Process(1)
icomplex = [[p0,p1]]
pcomplex = generateComplexProtocol(icomplex,k)
print(pcomplex)
# toAdjacencyList(pcomplex)
# ts.testMerge(dc)

plot(pcomplex)










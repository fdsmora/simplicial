#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import testSimplicialComplex as ts
import pdb
import igraph as ig
import sys

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

# <Descripción> Con el complejo simplicial s, obtiene un diccionario con los vértices únicos y a cada uno de ellos asocia un indice.
# <Parámetros> d: Diccionario al cual se agregan los vértices. 
#              s: simplejo que contiene los procesos de los cuales se obtienen los vértices. 
#             xg: generador que produce los indices que se asignan a cada proceso. 
def addToDictAndIndex(d,s,xg):
    v0 = (s[0].id,s[0].view)
    v1 = (s[1].id,s[1].view)

    if (v0 not in d):
        index = next(xg)
        d[v0]=index
    if (v1 not in d):
        index = next(xg)
        d[v1]=index

def buildEdges(d, complex):
    edges = []
    print (complex)
    for s in complex:
        v0 = (s[0].id,s[0].view)
        v1 = (s[1].id,s[1].view)
        edges.append((d[v0],d[v1]))
    ts.testEdges(edges)
    return edges

def buildVertices(d,complex):
    vertices = [0]*len(d)
    for v in d:
        vertices[d[v]]=v
    return vertices

def buildVerticesEdges(complex):

    def indexGenerator():
        index = 0
        while(True):
            yield index
            index+=1
    xg = indexGenerator();

    d = {}
    for s in complex:
        addToDictAndIndex(d,s,xg)
    ts.testDict(d)
    edges = buildEdges(d,complex)
    vertices = buildVertices(d,complex)

    return vertices,edges

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
    # ts.testComplex(pcomplex)
    return pcomplex

def plot(pcomplex): 
    (vertices, edges) = buildVerticesEdges(pcomplex)
    g = ig.Graph(len(vertices))
    g.add_edges(edges)
    g.vs["pid"]=[s[0] for s in vertices]
    g.vs["label"]=[s[1] for s in vertices]
    g.vs["label_dist"]=-3
    color_dict={1:'black',0:'white'}
    layout = g.layout('fr')
    ig.plot(g, layout=layout,bbox = (900, 900),vertex_color = [color_dict[pid] for pid in g.vs["pid"]], margin=50)


k = int(sys.argv[1])
p0 = Process(0)
p1 = Process(1)
icomplex = [[p0,p1]]
pcomplex = generateComplexProtocol(icomplex,k)
plot(pcomplex)










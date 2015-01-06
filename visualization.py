#!/usr/bin/env python
# -*- coding: utf-8 -*-

import igraph as ig
import testSimplicialComplex as ts

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
    # print (complex)
    for s in complex:
        v0 = (s[0].id,s[0].view)
        v1 = (s[1].id,s[1].view)
        edges.append((d[v0],d[v1]))
    # ts.testEdges(edges)
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
    # ts.testDict(d)
    edges = buildEdges(d,complex)
    vertices = buildVertices(d,complex)

    return vertices,edges

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
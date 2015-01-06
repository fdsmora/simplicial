#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import testSimplicialComplex as ts
import pdb
import sys
import visualization as vz

class Process:
    def __init__(self, id):
        self.id=id
        self.__view=str(id)

    def write(self,mem):
        mem[self.id] = self.view

    def snapshot(self,mem):
        self.__view = copy.copy(mem)

    @property
    def view(self):
        if self.__view==str(self.id):
            return self.__view
        temp = ''
        prefix = ''
        for v in self.__view:
            temp += prefix + v
            prefix = ','
        return '('+temp+')' 

    def __str__(self):
        return '(%d,%s)'%(self.id,self.view)

    __repr__=__str__

# Las funciones 'execution' representan las posibles 
# formas de interacción de los procesos con la memoria
# compartida.
def execution1(simplex):
    mem = ['-']*len(simplex) # crea una memoria con número de entradas igual al número de procesos.
    p0 = copy.copy(simplex[0])
    p1 = copy.copy(simplex[1])
    p0.write(mem)
    p0.snapshot(mem)
    p1.write(mem)
    p1.snapshot(mem)
    return [p0,p1]

def execution2(simplex):
    mem = ['-']*len(simplex)
    p0 = copy.copy(simplex[0])
    p1 = copy.copy(simplex[1])
    p0.write(mem)
    p1.write(mem)
    p0.snapshot(mem)
    p1.snapshot(mem)
    return [p0,p1]

def execution3(simplex):
    mem = ['-']*len(simplex)
    p0 = copy.copy(simplex[0])
    p1 = copy.copy(simplex[1])
    p1.write(mem)
    p1.snapshot(mem)
    p0.write(mem)
    p0.snapshot(mem)
    return [p0,p1]

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

k = int(sys.argv[1])
p0 = Process(0)
p1 = Process(1)
icomplex = [[p0,p1]]
pcomplex = generateComplexProtocol(icomplex,k)
vz.plot(pcomplex)










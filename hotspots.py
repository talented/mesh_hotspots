#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 11:24:23 2019

#@author: Özgür Yarikkas - www.rikkas.com

"""

import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import matplotlib.collections
import numpy as np
import argparse


class MeshGrid: 
    
    nodes = []
    elements = []
    values = []
    
    def __init__(self, filename):
        file = self.__readFile(filename)
        self.nodes = file[0]
        self.elements = file[1]
        self.values = file[2]
    
    # ------------------------------------------------------------------------ # 
    
    # Ausgabe:
    # Liste von N Paaren (Hotspot-Element-ID, Funktionswert für dieses Element),
    # geordnet nach Wert vom größten zum niedrigsten.
    
    # Mit einem gegebenen Mesh und eine Ganzzahl N, finden Sie die ersten N Hotspots, d. H
    # Elemente, bei denen die Funktion ihre lokalen Maxima erreicht.
       
    # params - nodes, elements, values -> die numpy arrays, die vom gegebenen text datei extrahiert werden
    # param - N -> Anzahl der zu findenden Hotspots
    # return None
    def findHotspots(self, nodes, elements, values, N):
        
        if N < 1:
            print("\nDer Mindeswert für N ist 1\n")
            return
        
        # Eine Liste von Tupeln aus Werten mit Indizes
        vals = [(idx, x) for idx, x in enumerate(values)]
        
        # Die sortierte Liste nach Wert (2. Element) absteigend 
        sortedVals = sorted(vals, key=lambda x: x[1], reverse=True)
        
        # Addiere den ersten Wert der sortierten Liste als lokales Maxima mit dem größten Wert
        result = [sortedVals[0]]
        
        # Wenn der Hotspot-Wert N gleich 1 ist, wird der größte Wert und das entsprechende Dreieckselement zurückgegeben
        if N == 1:
            print("\nDer größte Hotspot-Wert als Liste von N Paaren\n(Hotspot Element ID, Funktionswert für dieses Element):\n") 
            print(result)
            print("\nder zu dem Dreieckselement gehört, wie unten angegeben:\n")
            print([elements[x[0]] for x in result]) 
            return
        
        # Vergleich zwei Listen und gebt True zurück, wenn sie irgendeinen Wert haben, der gleich ist
        # params - a, b -> Zu vergleichende Listen
        # return False, wenn das Ergebnis der Intersection leer ist (d. H es gibt keine Nachbarschafts-Dreiecke)
        def compare(a, b):
            c = set(a).intersection(b)
            return bool(c)
        
        
        check = []  # die Liste, um die Nachbar nodes im Vergleich zu verwenden
        
        # Ausgehend von idx 1 in der SortedValues Liste, überprüft die elements liste mit demselben Index
        # und einen Vergleich durchführen, wenn sich Schnittwerte befinden (bedeutet, dass sie denselben nodes verwenden)
        # Wenn nicht, fügt diesen Skalar values zum result liste hinzu. Dies ist ein Hotspot!
        for i in range(1, len(sortedVals)):
            index = sortedVals[i][0]  # 
            
            for v in elements[sortedVals[i-1][0]]:
                check.append(v)
                
            if not compare(elements[index], check):
                result.append(sortedVals[i])
                if len(result) == N:
                    print("\nDie ersten %d Hotspot-Werte als Liste von N Paaren\n(Hotspot Element ID, Funktionswert für dieses Element):\n" % N)
                    print(result)
                    print("\ndie zu den jeweiligen Dreieckselementen gehören, wie unten angegeben:\n")
                    print([elements[x[0]] for x in result])    
                    return
                
        print("\nEs gibt nicht so viele Hotspots in dieser Datei, reduzieren Sie Ihren N-Wert\n")
        

    # ------------------------------------------------------------------------ # 
    
    # Diese Methode stellt eine Matplotlib mit gegebenen Nodes, Elements und Skalar values dar, 
    # die mit einer Farbskala implementiert wurden.
    # 
    # @params - nodes, elements, values -> die numpy arrays, die vom gegebenen text datei extrahiert werden
    # @return - None
    def showMeshPlot(self, nodes, elements, values):
    
        x = nodes[:,0]
        y = nodes[:,1]
        
        # interne Methode 
        def triplot(x,y, triangles, values, ax=None, **kwargs):
    
            if not ax: ax=plt.gca()
            verts = nodes[triangles]
            pc = matplotlib.collections.PolyCollection(verts, **kwargs)
            pc.set_array(values)
            ax.add_collection(pc)
            ax.autoscale()
            return pc
          
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_aspect('equal')
    
        pc = triplot(x,y, elements, values, ax=ax, 
                 edgecolor="crimson", cmap="rainbow")
        fig.colorbar(pc, ax=ax)        
        ax.plot(x,y, marker="o", ls="", color="crimson")
    
        ax.set(title='Dreieck Mesh in 2D', xlabel='X Axis', ylabel='Y Axis')
    
        plt.show(block=True)

    # ------------------------------------------------------------------------ # 
    
    # Diese Method liest die angegebenen .txt datei und zerlegt und extrahiert
    # die nodes, elements und scalar function values als numpy arrays
    # @params - filename als txt file 
    # @return - nodes, elements und values als numpy arrays in einem list
    
    def __readFile(self, filename):   
        
        # interne Methode
        def parseArray(arr):  
            temp = []
            for ele in arr:
                temp.append([int(x) for x in ele.split(',')][1:])
            return np.array(temp)
        
        delimiters = []
        
        file = open(filename, 'r')
        data = file.read().splitlines()
        
        for idx, line in enumerate(data):
            
            if line == 'NODES':
                delimiters.append(idx)
            elif line == 'ELEMENTS':
                delimiters.append(idx)
            elif line == 'VALUES':
                delimiters.append(idx)
       
        nodesTemp = data[delimiters[0]+1 : delimiters[1]]
        nodes = parseArray(nodesTemp)
        
        elementsTemp = data[delimiters[1]+1 : delimiters[2]]
        elements = parseArray(elementsTemp)
        
        valuesTemp = data[delimiters[2]+1 : ]
        
        values = []
        
        for ele in valuesTemp:
            values.append(float(ele.split(',')[1]))
        
        return [nodes, elements, np.array(values)]
        
# ------------------------------------------------------------------------ # 
  
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="filename")
    parser.add_argument("hotspots", help="hotspots")
      
    args = parser.parse_args()
  
#    mesh = MeshGrid("mesh.txt")
    mesh = MeshGrid(args.filename)
    mesh.findHotspots(mesh.nodes, mesh.elements, mesh.values, int(args.hotspots))
    mesh.showMeshPlot(mesh.nodes, mesh.elements, mesh.values)





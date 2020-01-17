#!/usr/bin/env python

import random
import GrapheXY
from os import sep, pardir
from time import *

graphe = GrapheXY.GrapheXY(pardir+sep+'graphe'+sep+'graphe.gr')

rand = random.Random()
tempsTotal = 0.0


i = 1
while 1:
    a = graphe.listeArcs()[rand.randrange(len(graphe.listeSommets()))]
    b = graphe.listeArcs()[rand.randrange(len(graphe.listeSommets()))]
    #print a,b
    t = time()
    chemin = graphe.cheminPlusCourt(a, b)

    tempsChemin = time()-t
    tempsTotal += tempsChemin
    if not i%20: print 'temps chemin courant - temps moyen - nb sommet du chemin (CTRL+C pour finir)'
    print tempsChemin, '-', tempsTotal/float(i), '-', chemin.nbSommets()
    i += 1



#import profile
#profile.run('graphe.cheminPlusCourt((90, 61), (79, 80))','profChemin')



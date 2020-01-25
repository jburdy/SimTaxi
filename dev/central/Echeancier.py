#!/usr/bin/python2
# -*- coding: utf-8 -*-
"""
Module contenant l'�ch�ancier.

$Id: Echeancier.py,v 1.6 2003/01/08 09:24:07 vega01 Exp $
"""
__version__ = '$Revision: 1.6 $'
__author__ = 'EI5A, eivd, SimTaxi (Groupe Burdy)'
__date__ = '2002-12-01'

from QueuePriorite import *


class Echeancier(QueuePriorite):
    """
    Implemente un echeancier.
    """


    def initEcheancier(self, listeEv):
        """
        Initialise la liste d'evenements.

        listeEv (List) -- la liste des evenements a inserer dans l'echeancier

        - depuis - 1.0

        - auteur - Alexandre D'Amico
        """
        self._queue = listeEv
        # tri des evenement dans l'ordre chronologique
        self._queue.sort(self._foncComp)


    def tempsProchainEv (self):
        """
        Retourne le temps auquel aura lieu le prochain evenement.

        retourne (Temps) -- le temps auquel aura lieu le prochain evenement

        - depuis - 1.4

        - auteur - Alexandre D'Amico
        """
        if not self.vide():
        # la queue contient un ou plusieurs element(s)

            return self._queue[0].temps()
        else:
            raise ErreurQueueVide
            

if __name__ == '__main__' :

    def foncComp(e1, e2):
        """
        Fonction de comparaison des evenements, pour l'insertion dans
        l'echeancier.
    
        e1, e2 -- les elements a comparer

        - depuis - 1.0

        - auteur - Alexandre D'Amico
        """
        return e1 < e2


    x = Echeancier(foncComp)
    x.initEcheancier([1000, 2, 500])

    if x.vide():
        print "vide"
    else:
        print "pas vide"

    print "insertion 3"
    x.deposer(3)

    print "insertion 1"
    x.deposer(1)

    print "insertion 20"
    x.deposer(20)
    
    if x.vide():
        print "vide"
    else:
        print "pas vide"

    print "suppression"
    a = x.prelever()
    print a

    print "suppression"
    a = x.prelever()
    print a

    print "suppression"
    a = x.prelever()
    print a

    print "suppression"
    a = x.prelever()
    print a    
    
    print "suppression"
    a = x.prelever()
    print a

    print "suppression"
    a = x.prelever()
    print a


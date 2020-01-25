#!/usr/bin/python2
# -*- coding: utf-8 -*-
"""
Module contenant une queue de priorit§.

$Id: QueuePriorite.py,v 1.8 2003/01/08 09:15:27 vega01 Exp $
"""
__version__ = '$Revision: 1.8 $'
__author__ = 'EI5A, eivd, SimTaxi (Groupe Burdy)'
__date__ = '2002-12-01'



class ErreurQueueVide(Exception):
    """
    Erreur propagee lorsque la Queue est vide.
    """
    pass

    

class ErreurInsertionQueue(Exception):
    """
    Erreur propagee lorsqu'il y a une erreur lors de l'insertion d'un element
    dans la Queue.
    """
    pass

    

class QueuePriorite:
    """
    Implemente une Queue de priorite dynamique.
    """


    def __init__(self, foncComp):
        """
        Constructeur.

        Cree une Queue vide.

        foncComp (Function) -- fonction de comparaison, accepte 2 parametres 
                               et retourne 0, 1 ou -1

        - depuis - 1.0

        - auteur - Alexandre D'Amico
        """
        self._queue = []
        self._foncComp = foncComp
     

    def deposer(self, element):
        """
        Deposer l'element avec la priorite voulue au bon endroit de la queue.

        Leve l'exception ErreurQueuePleine si la queue est pleine.

        element -- element a inserer dans la queue

        - depuis - 1.0

        - auteur - Alexandre D'Amico
        """
        try:

            indiceBas = 0
            indiceHaut = len(self._queue)
            
            while indiceBas < indiceHaut:
                indiceMilieu = (indiceHaut + indiceBas) / 2
                
                if self._foncComp(element, self._queue[indiceMilieu]):
                    indiceHaut = indiceMilieu
                else:
                    indiceBas = indiceMilieu + 1

            self._queue.insert(indiceBas, element)

        except:
            raise ErreurInsertionQueue

    
    def prelever(self):
        """
        Prelever l'element le plus prioritaire de la queue (premier element
        de la queue).

        Leve l'exception ErreurQueueVide si la queue est vide.

        retourne -- l'element de tete de la queue

        - depuis - 1.0

        - auteur - Alexandre D'Amico
        """
        if not self.vide():
        # la queue contient un ou plusieurs element(s)

            element = self._queue.pop(0) # suppression de l'element de tete
            
            return element
        else:
            raise ErreurQueueVide

    
    def vide(self):
        """
        Savoir si la Queue est vide.

        retourne entier -- 1 si la Queue est vide, 0 sinon

        - depuis - 1.0
        
        - auteur - Alexandre D'Amico        
        """
        return not self._queue


if __name__ == '__main__' :
    
    def foncComp(a, b):
        return a < b
        
    x = QueuePriorite(foncComp)

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


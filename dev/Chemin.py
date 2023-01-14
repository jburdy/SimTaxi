#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Module contenant la classe Chemin.

$Id: Chemin.py,v 1.10 2003/02/20 02:00:39 leyonel Exp $
"""
__version__ = '$Revision: 1.10 $'
__author__ = 'EI5a, eivd, SimTaxi (Groupe Burdy)'
__date__ = '2002-12-10'


class Chemin:
    """
    Un chemin du Graphe.

    Un chemin est statique, apres sa creation, uniquement des selecteurs sont
    a disposition.
    """

    def __init__(self, listeSommets, listeDistances):
        """
        Creation du chemin.
        listeSommets (List) -- liste ordonnee des sommets du parcour.
        listeDistances (List) -- liste des distances cummul§es pour chaque sommet
        - depuis - 1.0
        - auteur - Julien Burdy
        """
        from GrapheXY import GrapheXY
        self.__graphe = GrapheXY()
        self.__sommets = listeSommets
        self.__distances = listeDistances

    def posDepart(self):
        """
        Renvoie la position (tuple de 2 sommets) de depart du chemin.
        retourne (Tuple(sommetA, sommetB)) -- un tuple position
        - depuis - 1.0
        - auteur - Julien Burdy
        """
        return (self.__sommets[0], self.__sommets[1])

    def posDepartXY(self):
        """
        Renvoie la coordonn§e (tuple x, y) de depart du chemin.
        retourne (Tuple(x,y))
        - depuis - 1.6
        - auteur - Julien Burdy
        """
        sA, sB = self.posDepart()

        sAx = self.__graphe.attributsSommet(sA).getX()
        sAy = self.__graphe.attributsSommet(sA).getY()
        sBx = self.__graphe.attributsSommet(sB).getX()
        sBy = self.__graphe.attributsSommet(sB).getY()

        return (sAx / 2.0 + sBx / 2.0, sAy / 2.0 + sBy / 2.0)

    def posArrivee(self):
        """
        Renvoie la position (tuple de 2 sommets) d'arrivee du chemin.
        retourne (Tuple(sommetA, sommetB)) -- un tuple position
        - depuis - 1.0
        - auteur - Julien Burdy
        """
        return (self.__sommets[-2], self.__sommets[-1])

    def posArriveeXY(self):
        """
        Renvoie la coordonn§e (tuple x, y) d'arrivee du chemin.
        retourne (Tuple(x,y))
        - depuis - 1.6
        - auteur - Julien Burdy
        """
        sA, sB = self.posArrivee()

        sAx = self.__graphe.attributsSommet(sA).getX()
        sAy = self.__graphe.attributsSommet(sA).getY()
        sBx = self.__graphe.attributsSommet(sB).getX()
        sBy = self.__graphe.attributsSommet(sB).getY()

        return (sAx / 2.0 + sBx / 2.0, sAy / 2.0 + sBy / 2.0)

    def listeSommets(self):
        """
        Renvoie la liste ordonnee des sommets.
        retourne (List) -- la liste [0:nbSommet-1]
        - depuis - 1.0
        - auteur - Julien Burdy
        """
        return self.__sommets

    def nbSommets(self):
        """
        Renvoie le nombre de sommets parcourus par le chemin.
        retourne (Int) -- le nombre de sommets
        - depuis - 1.0
        - auteur - Julien Burdy
        """
        return len(self.__sommets)

    def nbArcs(self):
        """
        Renvoie le nombre d'arcs parcourus par le chemin.
        retourne (Int) -- le nombre d'arcs
        - depuis - 1.0
        - auteur - Julien Burdy
        """
        return self.nbSommets()-1

    def distTotalSommets(self):
        """
        Renvoie la distance totale entre le 1er sommet et le dernier.
        retourne (Float) -- la distance
        - depuis - 1.0
        - auteur - Lionel Guelat
        """
        return self.__distances[-1]

    def distTotalPos(self):
        """
        Renvoie la distance totale entre la 1ere position et la derniere.
        retourne (Float) -- la distance
        - depuis - 1.0
        - auteur - Lionel Guelat
        """
        return self.__distances[-1] \
            - (self.__distances[-1] - self.__distances[-2]) / 2.0 \
            - (self.__distances[1] - self.__distances[0]) / 2.0

    def distEntreSommets(self, a, b):
        """
        Renvoie la distance entre le sommet a et le sommet b.
        a, b -- les deux sommets
        retourne (Float) -- la distance
        - depuis - 1.0
        - auteur - Lionel Guelat
        """
        # ! cette m§thode n'a en fait pas lieu d'exister
        # puisque des sommets peuvent §tre § double dans le chemin !

        # rechercher l'index de ces sommet
        index = 0
        d = -1
        # recherche un des deux sommets
        while d < 0 and index < self.nbSommets():
            if self.__sommets[index] == a or self.__sommets[index] == b:
                d = self.__distances[index]
                # trouve = self.__sommets[index]
            index += 1
        # continue pour trouver le deuxi§me depuis la fin
        index = len(self.__sommets)-1
        while index >= 0:
            if self.__sommets[index] == a or self.__sommets[index] == b:
                # attention si le sommet trouve est a double !!!
                # if not self.__sommets[index] == trouve:
                return abs(self.__distances[index] - d)
            index -= 1

        raise Exception("un sommet au moins n'est pas dans le chemin")

    def distEntrePos(self, a, b):
        """
        Renvoie la distance entre la position a et la position b.
        a, b -- les deux arcs (tuple de sommets)
        retourne (Float) -- la distance
        - depuis - 1.0
        - auteur - Lionel Guelat
        """
        # trouver le premier arc
        index = 0
        d = -1
        while (d < 0) and (index+1 < self.nbSommets()):
            if (self.__sommets[index] == a[0]) and (self.__sommets[index+1] == a[1]):
                d = self.__distances[index] \
                    + (self.__distances[index+1] - self.__distances[index]) / 2.0
                # trouve = self.__sommets[index]
            index += 1
        # cherche le deuxi§me depuis la fin
        index = self.nbSommets()-1
        while index > 0:
            if (self.__sommets[index-1] == b[0]) and (self.__sommets[index] == b[1]):
                return self.__distances[index] \
                    - (self.__distances[index] - self.__distances[index-1]) / 2.0 \
                    - d
            index -= 1
        raise Exception("un arc au moins n'est pas dans le chemin")

    def __repr__(self):

        return str(self.nbArcs())+' arcs'


# seulement pour tester cette classe
if __name__ == '__main__':
    from os import pardir, sep

    from .GrapheXY import GrapheXY

    graphe = GrapheXY(pardir+sep+'graphe'+sep+'graphe.gr')

    l = [1, 2, 3, 4, 5, 6]
    c = Chemin(l, [0.0, 1.0, 2.0, 4.0, 7.0, 10.0])
    assert c.posDepart() == (1, 2)
    assert c.posArrivee() == (5, 6)
    print(c.posDepartXY())
    assert c.nbSommets() == 6
    assert c.nbArcs() == 5
    assert c.distTotalSommets() == 10.0
    assert c.distTotalPos() == 8.0
    assert c.distEntreSommets(2, 5) == 6.0
    assert c.distEntrePos((2, 3), (3, 4)) == 1.5
    assert c.distEntrePos((l[0], l[1]), (l[-2], l[-1])) == c.distTotalPos()

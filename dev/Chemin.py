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

    def __init__(self, liste_sommets, liste_distances):
        """
        Creation du chemin.
        listeSommets (List) -- liste ordonnee des sommets du parcour.
        listeDistances (List) -- liste des distances cummul§es pour chaque sommet
        - depuis - 1.0
        - auteur - Julien Burdy
        """
        from GrapheXY import GrapheXY
        self.__graphe = GrapheXY()
        self.__sommets = liste_sommets
        self.__distances = liste_distances

    def pos_depart(self):
        """
        Renvoie la position (tuple de 2 sommets) de depart du chemin.
        retourne (Tuple(sommetA, sommetB)) -- un tuple position
        - depuis - 1.0
        - auteur - Julien Burdy
        """
        return (self.__sommets[0], self.__sommets[1])

    def pos_depart_xy(self):
        """
        Renvoie la coordonn§e (tuple x, y) de depart du chemin.
        retourne (Tuple(x,y))
        - depuis - 1.6
        - auteur - Julien Burdy
        """
        s_a, s_b = self.pos_depart()

        s_a_x = self.__graphe.attributsSommet(s_a).getX()
        s_a_y = self.__graphe.attributsSommet(s_a).getY()
        s_b_x = self.__graphe.attributsSommet(s_b).getX()
        s_b_y = self.__graphe.attributsSommet(s_b).getY()

        return (s_a_x / 2.0 + s_b_x / 2.0, s_a_y / 2.0 + s_b_y / 2.0)

    def pos_arrivee(self):
        """
        Renvoie la position (tuple de 2 sommets) d'arrivee du chemin.
        retourne (Tuple(sommetA, sommetB)) -- un tuple position
        - depuis - 1.0
        - auteur - Julien Burdy
        """
        return (self.__sommets[-2], self.__sommets[-1])

    def pos_arrivee_xy(self):
        """
        Renvoie la coordonn§e (tuple x, y) d'arrivee du chemin.
        retourne (Tuple(x,y))
        - depuis - 1.6
        - auteur - Julien Burdy
        """
        s_a, s_b = self.pos_arrivee()
        s_a_x = self.__graphe.attributsSommet(s_a).getX()
        s_a_y = self.__graphe.attributsSommet(s_a).getY()
        s_b_x = self.__graphe.attributsSommet(s_b).getX()
        s_b_y = self.__graphe.attributsSommet(s_b).getY()

        return (s_a_x / 2.0 + s_b_x / 2.0, s_a_y / 2.0 + s_b_y / 2.0)

    def liste_sommets(self):
        """
        Renvoie la liste ordonnee des sommets.
        retourne (List) -- la liste [0:nbSommet-1]
        - depuis - 1.0
        - auteur - Julien Burdy
        """
        return self.__sommets

    def nb_sommets(self):
        """
        Renvoie le nombre de sommets parcourus par le chemin.
        retourne (Int) -- le nombre de sommets
        - depuis - 1.0
        - auteur - Julien Burdy
        """
        return len(self.__sommets)

    def nb_arcs(self):
        """
        Renvoie le nombre d'arcs parcourus par le chemin.
        retourne (Int) -- le nombre d'arcs
        - depuis - 1.0
        - auteur - Julien Burdy
        """
        return self.nb_sommets()-1

    def dist_total_sommets(self):
        """
        Renvoie la distance totale entre le 1er sommet et le dernier.
        retourne (Float) -- la distance
        - depuis - 1.0
        - auteur - Lionel Guelat
        """
        return self.__distances[-1]

    def dist_total_pos(self):
        """
        Renvoie la distance totale entre la 1ere position et la derniere.
        retourne (Float) -- la distance
        - depuis - 1.0
        - auteur - Lionel Guelat
        """
        return self.__distances[-1] \
            - (self.__distances[-1] - self.__distances[-2]) / 2.0 \
            - (self.__distances[1] - self.__distances[0]) / 2.0

    def dist_entre_sommets(self, a, b):
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
        while d < 0 and index < self.nb_sommets():
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

    def dist_entre_pos(self, a, b):
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
        while (d < 0) and (index+1 < self.nb_sommets()):
            if (self.__sommets[index] == a[0]) and (self.__sommets[index+1] == a[1]):
                d = self.__distances[index] \
                    + (self.__distances[index+1] - self.__distances[index]) / 2.0
                # trouve = self.__sommets[index]
            index += 1
        # cherche le deuxi§me depuis la fin
        index = self.nb_sommets()-1
        while index > 0:
            if (self.__sommets[index-1] == b[0]) and (self.__sommets[index] == b[1]):
                return self.__distances[index] \
                    - (self.__distances[index] - self.__distances[index-1]) / 2.0 \
                    - d
            index -= 1
        raise Exception("un arc au moins n'est pas dans le chemin")

    def __repr__(self):

        return str(self.nb_arcs())+' arcs'


# seulement pour tester cette classe
if __name__ == '__main__':
    from os import pardir, sep

    from .GrapheXY import GrapheXY

    graphe = GrapheXY(pardir+sep+'graphe'+sep+'graphe.gr')

    l = [1, 2, 3, 4, 5, 6]
    c = Chemin(l, [0.0, 1.0, 2.0, 4.0, 7.0, 10.0])
    assert c.pos_depart() == (1, 2)
    assert c.pos_arrivee() == (5, 6)
    print(c.pos_depart_xy())
    assert c.nb_sommets() == 6
    assert c.nb_arcs() == 5
    assert c.dist_total_sommets() == 10.0
    assert c.dist_total_pos() == 8.0
    assert c.dist_entre_sommets(2, 5) == 6.0
    assert c.dist_entre_pos((2, 3), (3, 4)) == 1.5
    assert c.dist_entre_pos((l[0], l[1]), (l[-2], l[-1])) == c.dist_total_pos()

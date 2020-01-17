#!/usr/bin/env python
"""
Module contenant la classe Point.

$Id: Point.py,v 1.3 2002/12/23 00:03:26 jaquemet Exp $
"""
__version__ = '$Revision: 1.3 $'
__author__ = 'EI5a, eivd, SimTaxi (Groupe Burdy)'
__date__ = '2002-11-10'

class Point:
    """
    Pour la gestion de points en coordonnees X et Y.
    """


    def __init__(self, x=0.0, y=0.0):
        """
        Cette methode sert a creer un Point.

        Par defaut, on cree le point zero.

        x (Float) -- La coordonnee en X

        y (Float) -- La coordonnee en Y

        retourne -- Graphe : Un objet Point

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        # les coordonnees
        self.__x = x
        self.__y = y


    def copy(self):
        """
        Cette methode fait une copie du point.

        retourne (Point) -- La copie du point

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        # retourner une copie
        return Point(self.__x, self.__y)


    def setX(self, x):
        """
        Cette methode change la coordonnee en X du point.

        x (Float) -- La nouvelle coordonnee en X

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        # mettre la nouvelle coordonnee en X
        self.__x = x


    def setY(self, y):
        """
        Cette methode change la coordonnee en Y du point.

        y (Float) -- La nouvelle coordonnee en Y

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        # mettre la nouvelle coordonnee en Y
        self.__y = y


    def setXY(self, x, y):
        """
        Cette methode change les coordonnees du point.

        x (Float) -- La nouvelle coordonnee en X

        y (Float) -- La nouvelle coordonnee en Y

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        # mettre les nouvelles coordonnees
        self.__x = x
        self.__y = y


    def getX(self):
        """
        Cette methode retourne la coordonnee en X du point.

        retourne (Float) -- La coordonnee en X

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        # retourner la coordonnee en X
        return self.__x


    def getY(self):
        """
        Cette methode retourne la coordonnee en Y du point.

        retourne (Float) -- La coordonnee en Y

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        # retourner la coordonnee en Y
        return self.__y

    
    def distance(self, point):
        """
        Cette methode retourne la distance entre le point et le point donne.

        point (Point) -- Le point donné

        retourne (Float) -- La distance entre les 2 points

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        # retourner la coordonnee en Y
        return ((point.getX() - self.getX())**2 +
                (point.getY() - self.getY())**2)**0.5
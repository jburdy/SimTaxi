#!/usr/bin/python2
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.5 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-11-23"
    
from ObjetGraph import *

class Texte(ObjetGraph) :
    """
    Classe permettant de dessiner du texte en opengl.
    
    Classe derivant de ObjetGraph et permettant
    de dessiner du texte en opengl.
    de police.
    
    :version: $Revision 1.0 $
    :author: Gregory Burri    
    """
    
    def __init__(self, couche = 0, couleur =  (1.0, 1.0, 1.0)) :
        """
        Initialisation d'un texte.
        
        Initialise differentes donnees membres.

        @param int couche : la couche sur laquelle se trouve l'objet
        @param (float, float, float) couleur : la couleur du texte
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        ObjetGraph.__init__(self, couche, couleur) #initialise le parent
        
    def dessiner(self, position, texte) :
        """
        Dessiner un texte.
        
        Dessine un texte sur le canevas OpenGL courant.
         
        @param string texte : Le texte
        @param (float, float) position : Position du texte
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """

        #definit sa couleur
        glColor3f(self.couleur[0], self.couleur[1], self.couleur[2])
        
        glRasterPos3i(int(position[0]), int(position[1]), self.getHauteur())   
        
        for i in texte :
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(i))
        

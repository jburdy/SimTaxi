#!/usr/bin/python3
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.7 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-11-23"

from .ObjetGraph import *

from math import *

class Carrefour(ObjetGraph) :
    """
    Classe dessinant un carrefour.
    
    Classe derivant de ObjetGraph et permettant
    de dessiner des carrefours en OpenGL.
    """   
    
    
    def __init__(self, couche = 0, couleur = (0.8, 0.0, 0.0)) :
        """
        Initialisation d'un carrefour.
        
        couche (int) -- couche sur laquelle se trouve le carrefour
        
        couleur (tuple(float, float, float)) -- couleur RGB
        
        - depuis - 1.0
        
        - auteur - Gr§gory Burri
        """
        
        ObjetGraph.__init__(self, couche, couleur) #initialise le paren
        
        Carrefour.taille = 10.0 #taille du carrefour

        
    def dessiner(self, position) :
        """
        Dessine un carrefour sur le canvas OpenGL courant.
        
        position (tuple(float, float)) -- position
        
        - depuis - 1.0
        
        - auteur - Gr§gory Burri
        """
        
        #d§finit la couleur du carrefour
        glColor3f(self.couleur[0], self.couleur[1], self.couleur[2])
        
        glPushMatrix() #sauvegarde la matrice de transformation
        
        #se deplace a l'endroit ou le carrefour doit se trouver
        glTranslatef(position[0], position[1], 0.0);
        
        #dessine le taxi (2 triangles)
        glBegin(GL_QUADS)
        glVertex3f(-1.0 * Carrefour.taille, 0.0, self.getHauteur())
        glVertex3f(0.0, -1.0 * Carrefour.taille, self.getHauteur())
        glVertex3f(1.0 * Carrefour.taille, 0.0, self.getHauteur())
        glVertex3f(0.0, 1 * Carrefour.taille, self.getHauteur())
        glEnd()
        
        glPopMatrix() #restore la matrice de transformation    

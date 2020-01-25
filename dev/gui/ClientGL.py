#!/usr/bin/python3
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.4 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-11-23"

from .ObjetGraph import *

from math import *

class Client(ObjetGraph) :
    """
    Classe dessinant un client.
    
    Classe derivant de ObjetGraph et permettant
    de dessiner des clients en OpenGL.
    """
    
    
    def __init__(self, couche = 0, couleur = (0.4, 0.4, 1.0)) :
        """
        Initialisation d'un client.
        
        couche (int) -- couche sur laquelle se trouve le client
        
        couleur (tuple(float, float, float)) -- couleur RGB
        
        - depuis - 1.0
        
        - auteur - Gr§gory Burri
        """
        
        ObjetGraph.__init__(self, couche, couleur) #initialise le parent
        
        Client.taille = 20.0 #taille d'un client

        
    def dessiner(self, position) :
        """
        Dessine un client.
        
        position (tuple(float, float)) -- position
        
        - depuis - 1.0
        
        - auteur - Gr§gory Burri
        """
        
        glPushMatrix() #sauvegarde la matrice de transformation

        #se d§place a l'endroit ou le taxi doit se trouver
        glTranslatef(position[0], position[1], 0.0)

        #dessine le client
        glBegin(GL_QUADS)
        glVertex3f(1.0*Client.taille, 1.0*Client.taille, self.getHauteur())
        glVertex3f(-1.0*Client.taille, 1.0*Client.taille, self.getHauteur())
        glVertex3f(-1.0*Client.taille, -1.0*Client.taille, self.getHauteur())
        glVertex3f(1.0*Client.taille, -1.0*Client.taille, self.getHauteur())
        glEnd()
        
        glPopMatrix() #restore la matrice de transformation    

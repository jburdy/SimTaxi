#!/usr/bin/python3
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.1 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-11-23"
    
from .TexteGL import *

class TexteAbsolu(Texte) :
    """
    Classe permettant de dessiner du texte en opengl.
    
    Classe derivant de ObjetGraph et permettant
    de dessiner du texte en opengl.
    de police.
    
    :version: $Revision 1.0 $
    :author: Gregory Burri    
    """
    
    def __init__(self, couleur = (1.0, 1.0, 1.0)) :
        """
        Initialisation d'un texte.
        
        Initialise differentes donnees membres.

        @param int couche : la couche sur laquelle se trouve l'objet
        @param (float, float, float) couleur : la couleur du texte
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        Texte.__init__(self, 0, couleur) #initialise le parent
        
    def dessiner(self, position, texte) :
        """
        Dessiner un texte.
        
        Dessine un texte sur le canevas OpenGL courant.
         
        @param string texte : Le texte
        @param (float, float) position : Position du texte
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        glDisable(GL_DEPTH_TEST);
        
        glMatrixMode(GL_PROJECTION)  
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, 100, 0, 100, -1, 1)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        Texte.dessiner(self, position, texte)
        
        glMatrixMode(GL_PROJECTION)

        glPopMatrix() #sauvegarde la matrice de transformation
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glEnable(GL_DEPTH_TEST);
        

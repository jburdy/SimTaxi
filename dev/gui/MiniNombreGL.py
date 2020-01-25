#!/usr/bin/python2
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.2 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-11-23"
    
from ObjetGraph import *

class MiniNombre(ObjetGraph) :
    """
    Classe permettant de dessiner du texte en opengl.
    
    Classe derivant de ObjetGraph et permettant
    de dessiner du texte en opengl.
    Il est possible de choisir entre 2 tailles
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

        self.initGL() #initialise diff§rents param§tre li§s § openGL
              
    def initGL(self) :              
              
        #les bitmap pour les petits chiffres
        self.petit_numerique = (
            (0xe0, 0xa0, 0xa0, 0xa0, 0xe0), #0
            (0xe0, 0x40, 0x40, 0x40, 0xc0), #1
            (0xe0, 0x80, 0xe0, 0x20, 0xe0), #2
            (0xe0, 0x20, 0x60, 0x20, 0xe0), #3
            (0x20, 0x20, 0xe0, 0xa0, 0x80), #4
            (0xe0, 0x20, 0xe0, 0x80, 0xe0), #5
            (0xe0, 0xa0, 0xe0, 0x80, 0xe0), #6
            (0x20, 0x20, 0x20, 0x20, 0xe0), #7
            (0xe0, 0xa0, 0xe0, 0xa0, 0xe0), #8
            (0xe0, 0x20, 0xe0, 0xa0, 0xe0), #9
            (0x80, 0x80, 0x40, 0x20, 0x20)) #/
            
        self.listes_numerique = []
            
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        decalage = glGenLists(11)
        for i in range(11) :
            self.listes_numerique.append(decalage + i)
            glNewList(decalage + i, GL_COMPILE)
            glBitmap(3, 5, 0.0, 0.0, 4.0, 0.0, self.petit_numerique[i])
            glEndList()
        
    def dessiner(self, texte, position) :
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
        
        for i in range(len(texte)) :
            if texte[i] == '/' :
                glCallList(self.listes_numerique[10])
            else :
                glCallList(self.listes_numerique[int(texte[i])])
        

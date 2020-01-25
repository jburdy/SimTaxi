#!/usr/bin/python2
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.2 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2003-2-11"
    
from ObjetGraph import *

class Etat(ObjetGraph) :
    """
    Classe permettant de dessiner les �tats des taxis.
    
    Classe derivant de ObjetGraph et permettant
    de dessiner les symboles d�crivant l'�tat d'un taxi.
    Il est possible de choisir entre 2 tailles
    de police.
    
    :version: $Revision 1.0 $
    :author: Gregory Burri    
    """
    
    def __init__(self, couche = 0, couleur =  (1.0, 1.0, 1.0),
                 etat = 'arrete') :
        """
        Initialisation d'un texte.
        
        Initialise differentes donnees membres.

        @param int couche : la couche sur laquelle se trouve l'objet
        @param (float, float, float) couleur : la couleur du texte
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        ObjetGraph.__init__(self, couche, couleur) #initialise le parent

        #cr�e la liste d'affichage du symbole souhait�
        self.initGL(etat)
              
    def initGL(self, etat) :              
              
        #les symboles des �tats du taxi
        Etat.symboles = {
            #Arret�
            'arrete' :
            (0x00, 0xf0, 0x40, 0x2f, 0xf4, 0x02, 0x0f, 0x00),
            #Cherche un client
            'chercheClient' :
            (0x08, 0x0c, 0x7e, 0x7f, 0x7e, 0x0c, 0x08, 0x00),
            #Conduit un client (occup�)
            'conduitClient' :
            (0x00, 0x3e, 0x3e, 0x3e, 0x3e, 0x1c, 0x00, 0x00),
            #Retourne � une station
            'retourStation' :
            (0x08, 0x0c, 0x7e, 0x7f, 0x7e, 0x0c, 0x08, 0x00)}

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        self.liste = glGenLists(1)
        glNewList(self.liste, GL_COMPILE)
        glBitmap(8, 8, 10.0, 0.0, 0.0, 0.0, Etat.symboles[etat])
        glEndList()
        
    def dessiner(self, position) :
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

        glCallList(self.liste)
        

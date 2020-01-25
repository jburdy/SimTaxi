#!/usr/bin/python3
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.5 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-11-23"

from .importGL import * #module d'importation de OpenGL

class ObjetGraph :
    """
    Classe de base pour tout objet graphique.
    
    Base dont tout objet graphique doit deriver.
    
    :version: $Revision 1.0 $
    :author: Gregory Burri    
    """
    
    def __init__(self, couche = 0, couleur = (0.0, 0.0, 0.0)) :
        """
        Initialisation d'un objet graphique.
        
        Initialise differentes donnees membres.
         
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """

        #couleur de l'objet
        self.couleur = couleur
        
        #couche sur laquelle se trouve l'objet (1 en dessous de 2)
        self.couche = couche
        
    #>-----------------------------------------------------------------------
        
    def setCouleur(self, couleur) :
        """
        Definir la couleur d'un objet.
        
        Definit la couleur d'un objet graphique.

        @param (float, float, float) couleur : la couleur de l'objet
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        self.couleur = couleur
        
    
        
    def setCouche(self, couche) :
        """
        Definir la couche d'un objet.
        
        Definit la couche d'un objet graphique.

        @param float couche : la couche de l'objet
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        self.couche = couche
        
    
        
    def getHauteur(self) :
        """
        Retourner la hauteur d'un objet.
        
        Retourne la hauteur z reel (par rapport a OpenGL)
        d'un objet graphique.

        @return float : La hauteur reel
        @author Gregory Burri
        """
        
        return -self.couche/10.0
        
    
        
    def dessiner() :
        """
        Dessiner un objet (methode vituelle).
        
        Dessine un objet a l'aide de commandes OpenGL.
        
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        pass #methode vituelle


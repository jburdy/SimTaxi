#!/usr/bin/python2
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.2 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-11-23"

from ClientGL import *

from math import *

class ClientDepose(Client) :
    """
    Classe dessinant un client.
    
    Classe derivant de ObjetGraph et permettant
    de dessiner des clients venant d'§tre d§pos§s
    par un taxi en OpenGL.  
    """
    
    
    def __init__(self, couche = 0, couleur = (0.4, 0.4, 1.0)) :
        """
        Initialisation d'un client venant d'§tre d§pos§.
        
        couche (int) -- couche sur laquelle se trouve le client
        
        couleur (tuple(float, float, float)) -- couleur RGB
        
        - depuis - 1.0
        
        - auteur - Gr§gory Burri
        """
        
        Client.__init__(self, couche, couleur) #initialise le parent
        
        self.tempsAffiche = 100.0 #Le temps d'affichage
                
        glEnable(GL_BLEND) #active la transparence

        
    def dessiner(self, position, tempsLargage, temps) :
        """
        Dessine un client qui § §t§ d§pos§ par un taxi.
        
        position (tuple(float, float)) -- position
        
        tempsLargage (float) -- temps au moment ou le client § §t§ d§pos§
        
        temps (float) -- temps de la simulation
        
        - depuis - 1.0
        
        - auteur - Gr§gory Burri
        """
                
        #calcul la transparence, elle est comprise entre 0.0 et 1.0
        transparence = 1.0 - (temps - tempsLargage) / self.tempsAffiche
        
        #d§finit les fonctions de blending
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        #definit sa couleur
        glColor4f(self.couleur[0], self.couleur[1], self.couleur[2], transparence)

        #dessine le client
        Client.dessiner(self, position)
        
        #revient § la fonction de blending initiale
        glBlendFunc(GL_ONE, GL_ZERO)
        
        #si le client ne de doit plus §tre affich§
        if (temps - tempsLargage) >= self.tempsAffiche :
            return False
        else :
            return True
        

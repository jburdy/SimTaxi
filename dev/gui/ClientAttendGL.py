#!/usr/bin/python2
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.2 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-11-23"

from ClientGL import *

from math import *

class ClientAttend(Client) :
    """
    Classe dessinant un client qui attends un taxi.
    
    Classe derivant de ObjetGraph et permettant
    de dessiner des clients attendant un taxi en OpenGL.
    """
    
    
    def __init__(self, couche = 0, couleur = (0.4, 0.4, 1.0)) :
        """
        Initialisation d'un client qui attends.
        
        couche (int) -- couche sur laquelle se trouve le client
        
        couleur (tuple(float, float, float)) -- couleur RGB
        
        - depuis - 1.0
        
        - auteur - Gr§gory Burri
        """
        
        Client.__init__(self, couche, couleur) #initialise le parent
        
        self.vitessePulse = 0.5 #vitesse de pulsation des clients
                
        glEnable(GL_BLEND) #active la transparence
        

    def dessiner(self, position, temps) :
        """
        Dessine un client qui attends.
        
        position (tuple(float, float)) -- position
        
        temps (float) -- temps de la simulation
        
        - depuis - 1.0
        
        - auteur - Gr§gory Burri
        """
        
        #calcul de la transparence en fonction du temps
        #elle est comprise entre 0.5 et 1.0
        transparence = (sin(temps * self.vitessePulse) + 1.0)/4.0 + 0.5
        
        #d§finit les fonctions de blending
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        #definit sa couleur
        glColor4f(self.couleur[0], self.couleur[1], self.couleur[2], transparence)

        #dessine le client
        Client.dessiner(self, position)

        #revient § la fonction de blending initiale
        glBlendFunc(GL_ONE, GL_ZERO)
        

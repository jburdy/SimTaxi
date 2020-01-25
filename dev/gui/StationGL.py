#!/usr/bin/python2
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.9 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-11-23"
    
from ObjetGraph import *
from MiniNombreGL import *

from math import *

class Station(ObjetGraph) :
    """
    Classe dessinant une station.
    
    Classe derivant de ObjetGraph et permettant
    de dessiner des Stations en OpenGL.
    
    :version: $Revision 1.0 $
    :author: Gregory Burri    
    """
    
    def __init__(self, couche = 0, couleur =  (1.0, 0.67, 0.15)) :
        """
        Initialisation d'une station.
        
        Initialise differentes donnees membres.
         
        @param int couche : la couche sur laquelle se trouve l'objet
        @param (float, float, float) couleur : la couleur de la station
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        ObjetGraph.__init__(self, couche, couleur) #initialise le parent
        
        #pour son occupation
        self.texte = MiniNombre(11)
        
        Station.taille = 12.0 #la taille des stations
        Station.eloignement = 14.0 #eloignement de la route
    
    def dessiner(self, position, vecteurDirection, capacite, nombreTaxi) :
        """
        Dessiner un taxi.
        
        Dessine un taxi sur le canevas OpenGL courant.
         
        @param (float, float) position : Position du taxi
        @param (float, float) vecteurDirection : Vecteur de direction
        @param float tauxOccupation : taux d'occupation de la station [0, 1]
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        self.texte.dessiner(str(nombreTaxi) + '/' + str(capacite),
                (position[0]+20, position[1]+20))      
        
        facteurCouleur = (float(nombreTaxi)/float(capacite) + 0.4)
        
        #definit sa couleur
        glColor3f(self.couleur[0]/facteurCouleur,
                  self.couleur[1]/facteurCouleur,
                  self.couleur[2]/facteurCouleur)
        
        glPushMatrix() #sauvegarde la matrice de transformation
        
        #se deplace a l'endroit ou la station doit se trouver
        glTranslatef(position[0], position[1], 0.0)
       
        #calcul l'angle de rotation et applique la rotation
        alpha = atan2(vecteurDirection[1], vecteurDirection[0])
        glRotatef(alpha * 180.0 / pi, 0.0, 0.0, 1.0) 
                
        #deplace la station a cote de la route
        glTranslatef(0.0, Station.eloignement, 0.0)

        #dessine la station
        glBegin(GL_QUADS)
        glVertex3f(-4.0*Station.taille, -1.0*Station.taille, self.getHauteur())
        glVertex3f(4.0*Station.taille, -1.0*Station.taille, self.getHauteur())
        glVertex3f(4.0*Station.taille, 1.0*Station.taille, self.getHauteur())
        glVertex3f(-4.0*Station.taille, 1.0*Station.taille, self.getHauteur())
        glEnd()
        glBegin(GL_TRIANGLES)
        glVertex3f(-4.5*Station.taille, 0.0, self.getHauteur())
        glVertex3f(-4.0*Station.taille, -1.0*Station.taille, self.getHauteur())
        glVertex3f(-4.0*Station.taille, 1.0*Station.taille, self.getHauteur())
        glEnd()
        glBegin(GL_TRIANGLES)
        glVertex3f(4.5*Station.taille, 0.0, self.getHauteur())
        glVertex3f(4.0*Station.taille, 1.0*Station.taille, self.getHauteur())
        glVertex3f(4.0*Station.taille, -1.0*Station.taille, self.getHauteur())
        glEnd()
        
        glPopMatrix() #restore la matrice de transformation    
        

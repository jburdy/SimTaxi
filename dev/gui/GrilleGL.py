#!/usr/bin/python2
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.5 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-11-23"

from ObjetGraph import *

class Grille(ObjetGraph) :
    """
    Classe dessinant une grille.
    
    Classe derivant de ObjetGraph et permettant
    de dessiner une grille.
    
    :version: $Revision 1.0 $
    :author: Gregory Burri    
    """   
    
    def __init__(self, couche = 0, couleur = (0.2, 0.2, 0.2), pas = 10.0) :
        """
        Initialisation d'une grille.
        
        Initialise differentes donnees membres.
         
        @param int couche : la couche sur laquelle se trouve l'objet
        @param (float, float, float) couleur : la couleur de la grille
        @param float pas : pas de la grille
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        ObjetGraph.__init__(self, couche, couleur) #initalise le parent
        self.pas = pas #definit le pas
    

    def setPas(self, pas) :
        """
        Definir le pas.
        
        Definit le pas de la grille.
        
        @param float pas : pas de la grille
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        #definit le pas si il est plus grand que 1
        if pas >= 1.0 : self.pas = pas 
        
    
    
    def dessiner(self, point1, point2) :
        """
        Dessiner une grille.
        
        Dessine une grille sur le canevas OpenGL courant.
         
        @param (float, float) point1 : Coin superieur gauche
        @param (float, float) point2 : Coin inferieur droite
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        #definit la couleur de la grille
        glColor3f(self.couleur[0], self.couleur[1], self.couleur[2]);
                
        glLineWidth(1.0) #epaisseur du trait
        
        glPushMatrix() #sauvegarde la matrice de transformation
       
        #ajuste les coins sur un valeur discrete
        #correspondant au pas de la grille
        point1 = (int((point1[0] - self.pas) / self.pas) * self.pas,
                  int((point1[1] - self.pas) / self.pas) * self.pas) 
        point2 = (int((point2[0] + self.pas) / self.pas) * self.pas,
                  int((point2[1] + self.pas) / self.pas) * self.pas) 

   
        x = point1[0] #valeur courante de x
        #parcours les valeurs de x
        while x <= point2[0] :
            #dessine une ligne
            glBegin(GL_LINES)
            glVertex3f(x, point1[1],  self.getHauteur())
            glVertex3f(x, point2[1],  self.getHauteur())
            glEnd()
            x += self.pas
            
        y = point1[1] #valeur courante de y
        #parcours les valeurs de y
        while y <= point2[1] :
            #dessine une ligne
            glBegin(GL_LINES)
            glVertex3f(point1[0], y,  self.getHauteur())
            glVertex3f(point2[0], y,  self.getHauteur())
            glEnd()
            y += self.pas
            
        glPopMatrix() #restore la matrice de transformation   

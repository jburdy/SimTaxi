#!/usr/bin/python
__version__ = "$Revision: 1.5 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-11-23"

from ObjetGraph import *

class Limite(ObjetGraph) :
    """
    Classe dessinant la limite de deplacement.
    
    Dessine la limite de deplacement
    (lors du deplacement de la souris par exemple).
    
    :version: $Revision 1.0 $
    :author: Gregory Burri    
    """
    
    def __init__(self, couche = 0, couleur = (1.0, 1.0, 1.0)) :
        """
        Initialisation d'un limite.
        
        Initialise differentes donnees membres.
         
        @param int couche : la couche sur laquelle se trouve l'objet
        @param (float, float, float) couleur : la couleur de la limite
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        ObjetGraph.__init__(self, couche, couleur) #initialise le parent
        
    #>-----------------------------------------------------------------------

    def dessiner(self, point1, point2) :
        """
        Dessiner une limite.
        
        Dessine une limite sur le canevas OpenGL courant.
         
        @param (float, float) point1 : Coin superieur gauche
        @param (float, float) point2 : Coin inferieur droite
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        #definit la couleur
        glColor3f(self.couleur[0], self.couleur[1], self.couleur[2])
        
        glLineWidth(2.0) #epaisseur des traits
        
        glPushMatrix() #sauvegarde la matrice de transformation
        
        #dessine la limite
        glBegin(GL_LINE_LOOP)
        glVertex3f(point1[0], point1[1],  self.getHauteur())
        glVertex3f(point1[0], point2[1],  self.getHauteur())
        glVertex3f(point2[0], point2[1],  self.getHauteur())
        glVertex3f(point2[0], point1[1],  self.getHauteur())        
        glEnd()       
        
        glPopMatrix() #restore la matrice de transformation

#!/usr/bin/python
__version__ = "$Revision: 1.8 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-12-7"

from ObjetGraph import * #super classe

from math import *

class Route(ObjetGraph) :
    """
    Classe dessinant une route.
    
    Classe derivant de ObjetGraph et permettant
    de dessiner des routes en OpenGL.
    
    :version: $Revision 1.0 $
    :author: Gregory Burri    
    """
    
    def __init__(self, couche = 0, couleur = (0.6, 0.6, 0.6), couleur2 = (0.1, 0.1, 0.1)) :
        """
        Initialisation d'une route.
        
        Initialise differentes donnees membres.
         
        @param int couche : la couche sur laquelle se trouve l'objet
        @param (float, float, float) couleur : la couleur de la route
        @param (float, float, float) couleur2 : la couleur2 de la route
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        ObjetGraph.__init__(self, couche, couleur) #initialise le parent
        self.couleur2 = couleur2 #definit la couleur 2
        
        Route.taille = 4.0 #largeur de la route

    def dessiner(self, debut, fin, est_sens_unique) :
        """
        Dessiner une route.
        
        Dessine une route sur le canevas OpenGL courant.
         
        @param (float, float) debut : Point de depart de la route
        @param (float, float) fin : Point d'arrive de la route
        @param Boolean est_sens_unique : est-ce un sens unique ?
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """

        #definit sa couleur
        #glColor3f(self.couleur[0], self.couleur[1], self.couleur[2]);
        
        glPushMatrix() #sauvegarde la matrice de transformation
        
        glLineWidth(1.0) #definit l'epaisseur des lignes        
        
        #dessine une ligne entre le debut et la fin de la route
        glBegin(GL_LINES)
        glColor3f(self.couleur[0], self.couleur[1], self.couleur[2])
        glVertex3f(debut[0], debut[1], self.getHauteur())  
        if est_sens_unique :
            glColor3f(self.couleur2[0], self.couleur2[1], self.couleur2[2])
        glVertex3f(fin[0], fin[1], self.getHauteur())
        glEnd()
        
        #calcul le centre de la route (point de gravite)
        centre = (debut[0] + (fin[0] - debut[0]) / 2.0,
                  debut[1] + (fin[1] - debut[1]) / 2.0)
        
        #calcul la longueur de la route (pythagore)
        longueur = sqrt(pow(debut[0] - fin[0], 2) \
                      + pow(debut[1] - fin[1], 2))
       
        #positionne la route
        glTranslatef(centre[0], centre[1], 0.0);
        
        #calcul l'angle de rotation
        alpha = atan2((debut[1]-fin[1]), (debut[0]-fin[0]))
        glRotatef(alpha*180/pi, 0, 0, 1) #tourne la route

        #dessine la route (un rectangle)
        glBegin(GL_QUADS)
        glColor3f(self.couleur[0], self.couleur[1], self.couleur[2])
        glVertex3f(longueur/2, -Route.taille, self.getHauteur())
        glVertex3f(longueur/2, Route.taille, self.getHauteur())
        if est_sens_unique :
            glColor3f(self.couleur2[0], self.couleur2[1], self.couleur2[2])
        glVertex3f(-longueur/2, Route.taille, self.getHauteur())
        glVertex3f(-longueur/2, -Route.taille, self.getHauteur())
        glEnd()       
        
        glPopMatrix() #restore la matrice de transformation

#!/usr/bin/python
__version__ = "$Revision: 1.10 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-11-23"
    
from ObjetGraph import *
from EtatGL import *
from MiniNombreGL import *

from math import *

class Taxi(ObjetGraph) :
    """
    Classe dessinant un taxi.
    
    Classe derivant de ObjetGraph et permettant
    de dessiner des taxis en OpenGL.
    
    :version: $Revision 1.0 $
    :author: Gregory Burri    
    """
    
    def __init__(self, couche = 0, couleur=  (1.0, 1.0, 0.0)) :
        """
        Initialisation d'un taxi.
        
        Initialise differentes donnees membres.
         
        @param int couche : la couche sur laquelle se trouve l'objet
        @param (float, float, float) couleur : la couleur du taxi
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        ObjetGraph.__init__(self, couche, couleur) #initialise le parent
        
        Taxi.taille = 20 #taille des taxis
        
        #pour afficher son numéro
        self.texte = MiniNombre(11)
        
        #les différents symboles d'état
        Taxi.arrete = Etat(11, (1.0, 1.0, 1.0), 'arrete')
        Taxi.chercheClient = Etat(11, (0.4, 0.4, 1.0), 'chercheClient')
        Taxi.conduitClient = Etat(11, (1.0, 0.0, 0.0), 'conduitClient')
        Taxi.retourStation = Etat(11, (1.0, 0.67, 0.15), 'retourStation')        
       
    def dessiner(self, position, vecteurDirection,
                 etat, numero = 0) :
        """
        Dessiner un taxi.
        
        Dessine un taxi sur le canevas OpenGL courant.
         
        @param (float, float) position : Position du taxi
        @param (float, float) vecteurDirection : Vecteur de direction
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        #dessine son état
        if etat == 'arrete' :
           Taxi.arrete.dessiner((position[0]+20, position[1]+20))
        elif etat == 'chercheClient' :
           Taxi.chercheClient.dessiner((position[0]+20, position[1]+20))
        elif etat == 'conduitClient' :
           Taxi.conduitClient.dessiner((position[0]+20, position[1]+20))
        elif etat == 'retourStation' :
           Taxi.retourStation.dessiner((position[0]+20, position[1]+20))
        
        #si le taxi n'est pas en station alors affiche son numéro
        if etat != 'arrete' :
            self.texte.dessiner(str(numero),
                (position[0]+20, position[1]+20))
           
        #definit sa couleur
        glColor3f(self.couleur[0], self.couleur[1], self.couleur[2])
        
        glPushMatrix() #sauvegarde la matrice de transformation
        
        #se deplace a l'endroit ou le taxi doit se trouver
        glTranslatef(position[0], position[1], 0.0)

        #calcul l'angle de rotation et applique la rotation
        alpha = atan2(vecteurDirection[1], vecteurDirection[0])
        glRotatef(alpha * 180.0 / pi, 0.0, 0.0, 1.0) 

        #dessine le taxi (un triangle)
        glBegin(GL_TRIANGLES)
        glVertex3f(1.0*Taxi.taille, 0.0, self.getHauteur())
        glVertex3f(-0.5*Taxi.taille, 0.866*Taxi.taille, self.getHauteur())
        glVertex3f(-0.5*Taxi.taille, -0.866*Taxi.taille, self.getHauteur())
        glEnd()      
        
        glPopMatrix() #restore la matrice de transformation    
        

#!/usr/bin/python3
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.17 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-12-7"

from .AffichageOpenGL import *

#modules de dessins
from .GrilleGL import *
from .LimiteGL import *

from GestionnaireTaxis import *
        
class Vue(AffichageOpenGL) :
    """
    Gestion de la vue de l'affichage OpenGL.
    
    Cette classe sert a positionner la vue a un endroit precis dans
    le graphe. Elle permet egalement de zoomer.
    
    :version: $Revision: 1.17 $
    :author: Gregory Burri
    """
    def __init__(self, attache) :
        """
        Initialisation de la classe vue.
        
        Definit les donnees membres et les initialises comme par exemple
        les limites de zoom et de positionnement.
         
        @param wxFrame attache : La frame a laquelle accrocher le canevas
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        #initialise le parent
        AffichageOpenGL.__init__(self, attache)
        
        self.zoomMax = 100.0 #le zoom maximum
        self.zoomMin = 0.03   #le zoom minimum
        
        self.positionMax = (10000.0, 10000.0) #la position max (x, y)
        self.positionMin = (0.0, 0.0) #la position min (x, y)
        
        self.zoom = 0.04 #le zoom de depart
        self.position = (4100.0, 4100.0) #la position de depart
        
        #les differentes grilles
        self.grille1 = Grille(1, (0.2, 0.2, 0.2), 10.0) #apas de 10m
        self.grille2 = Grille(2, (0.3, 0.3, 0.08), 100.0) #pas de 100m
        self.grille3 = Grille(3, (0.05, 0.05, 0.4), 1000.0) #pas de 1000m     
        
        self.taxis = GestionnaireTaxis() #les taxis
        self.suivreTaxi = 0 #indique le taxi § suivre (0 si aucun)
        self.vitesseSuivi = 0.058 #vitesse § laquelle la vue suit un taxi
        
        #la limite (trait epais entourant la zone de liberte)
        #self.limite = Limite(4)
        
    def set_position(self, nouvelle_position) :
        self.position = nouvelle_position
        
    def set_zoom(self, nouveau_zoom) :
        self.zoom = nouveau_zoom
    
    def evRedessiner(self) :
        """
        Evenement qui redessine le canevas.
        
        Redessine les grilles et la limte puis appel la methode
        du parent pour dessiner tous les autres objets.
         
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        #efface le tampon de couleur et de profonfeur
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
              
        taille = self.GetClientSize() #taille du canevas 
        
        #calcul le point superieur gauche du canevas
        self.point1 = (-taille.width / 2.0 / self.zoom + self.position[0],
                  -taille.height / 2.0 / self.zoom + self.position[1])
                  
        #calcul le point inferieur droite du canevas
        self.point2 = (taille.width / 2.0 / self.zoom + self.position[0],
                  taille.height / 2.0 / self.zoom + self.position[1])  
        
        #si le zoom est plus grand que 0.8 alors dessine la grille n§1
        if self.zoom > 0.8 :
            self.grille1.dessiner(self.point1, self.point2)     
            
        #si le zoom est plus grand que 0.2 alors dessine la grille n§2
        if self.zoom > 0.2 :                           
            self.grille2.dessiner(self.point1, self.point2)
            
        self.grille3.dessiner(self.point1, self.point2) #dessine la grille n§3
                          
        #dessine la limite
        #self.limite.dessiner(self.positionMax, self.positionMin)

               
        #redessine la scene
        AffichageOpenGL.evRedessiner(self)    
    
    def setPosition(self, position) : 
        """
        Change la vue de position.
        
        Change la position de la vue actuelle.
         
        @param (float, float) position : Nouvelle position
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        #si la nouvelle vue en x en valide (dans les limites)
        #alors change la position
        if position[0] <= self.positionMax[0] and \
           position[0] >= self.positionMin[0] :
            self.position = (position[0], self.position[1])
        else : #sinon la veleur x est invalide
            #si la nouvelle valeur de x est superieur a la limite
            if position[0] > self.positionMax[0] :
                #tronque la valeur de x
                self.position = (self.positionMax[0], self.position[1])
            #si la nouvelle valeur de x est inferieur a la limite
            elif position[0] < self.positionMin[0] :
                #tronque la valeur de x
                self.position = (self.positionMin[0], self.position[1])
                
        #si la nouvelle vue en y en valide (dans les limites)
        #alors change la position
        if position[1] <= self.positionMax[1] and \
           position[1] >= self.positionMin[1] : 
            self.position = (self.position[0], position[1])
        else : #sinon la veleur y est invalide
            #si la nouvelle valeur de y est superieur a la limite
            if position[1] > self.positionMax[1] :
                #tronque la valeur de y
                self.position = (self.position[0], self.positionMax[1])
            #si la nouvelle valeur de y est inferieur a la limite
            elif position[1] < self.positionMin[1] :
                #tronque la valeur de y
                self.position = (self.position[0], self.positionMin[1])
                
    
                
    def setZoom(self, zoom) :
        """
        Change le zoom de la vue.
        
        Change le zoom en controlant sa validite.
        
        @param float zoom : Nouveau zoom
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        #si le zoom est compris dans les limites => valide
        if zoom <= self.zoomMax and zoom >= self.zoomMin :
            self.zoom = zoom #change le zoom
        else : 
            #si le zoom est trop grand alors le tronque a la valeur max
            if zoom > self.zoomMax :
                self.zoom = self.zoomMax
            #si le zoom est trop petit alors le tronque a la valeur min
            elif zoom < self.zoomMin :
                self.zoom = self.zoomMin               

    
        
    def repositionner(self) :
        """
        Repositionne la vue.
        
        Repositionne la vue en fonction du zoom et de sa position,
        tient egalement compte de la taille du canevas.
        
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        self.SetCurrent()
        taille = self.GetClientSize() #taille du canevas de dessin
        
        #adapte le cadrage a la taille du canevas
        glViewport(0, 0, taille.width, taille.height)  
        
        #change la matrice de transformation courante
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity() #charge la matrice identite
        #si la taille du canevas est une valeur superieur a 0
        if taille.width > 0.0 and taille.height > 0.0 :
            #change le volume de visualisation
            glOrtho(0, taille.width/self.zoom, 0,
                    taille.height/self.zoom, 100.0, -100.0)
        
        #change la matrice de transformation courante
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity() #charge la matrice identite
        
        #si il faut suivre un taxi
        if self.suivreTaxi :
            positionTaxi = self.taxis.getTaxi(self.suivreTaxi). \
                getPosition(self.rafraichissement.getTemps())[0]
            self.position = ((self.position[0] + self.vitesseSuivi *
                             (positionTaxi[0] - self.position[0])),
                             (self.position[1] + self.vitesseSuivi *
                             (positionTaxi[1] - self.position[1])))
            
        #deplace la vue
        glTranslatef(taille.width / (self.zoom * 2.0) - self.position[0],
                     taille.height / (self.zoom * 2.0) - self.position[1],
                     0.0)
                     
    def visible(self, position, tolerance = 0) :
        return (position[0] > self.point1[0]-tolerance and
                position[0] < self.point2[0]+tolerance and
                position[1] > self.point1[1]-tolerance and
                position[1] < self.point2[1]+tolerance)
                     
    def suivreTaxi(self, numeroTaxi) :
        self.suivreTaxi = numeroTaxi
        
    def annulerSuivre(self) :
        self.suivreTaxi = 0

        

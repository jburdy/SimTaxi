#!/usr/bin/python2
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.9 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-12-7"

from Vue import *
from ThreadTortue import * #pour le deplacement a l'aide de la souris
from ThreadZoom import * #pour le zoom a l'aide de la souris

from Evenement_rafraichir_affichage import *

class EvenementsGlCanvas(Vue) :
    """
    Gestion des evenements sur le canevas OpenGL.
    
    Cette classe gere les evenements provoque par la souris sur
    le canevas OpenGL afin de pouvoir changer la vue en consequence
    comme le zoom et le deplacement.
    
    :version: $Revision: 1.9 $
    :author: Gregory Burri
    """
    
    def __init__(self, attache) :
        """
        Initialisation de la classe EvenementsGlCanvas.
        
        Bind les evenements sur les methodes et cree le deux thread
        (deplacement et zoom).
         
        @param wxFrame attache : La frame a laquelle accrocher le canevas
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """        
        
        #pour memoriser la position du click
        self.xDebut, self.yDebut = 0, 0
        
        Vue.__init__(self, attache) #initialise le parent
        
        #cree les deux thread (deplacement et zoom)
        self.threadTortue = ThreadTortue(self)        
        self.threadZoom = ThreadZoom(self)      
        
        #evenement declanche par le thread tortue
        #pour mettre a jour la position
        EVT_METTRE_A_JOUR_POSITION(self, self.evChangePosition)
        
        #evenement declanche par le thread zoom pour mettre a jour le zoom
        EVT_METTRE_A_JOUR_ZOOM(self, self.evChangeZoom)
        
        #evenement pour mettre � jour l'affichage (redessine la sc�ne openGL)
        EVT_METTRE_A_JOUR_AFFICHAGE(self, self.evRafraichir)
        
        #bind les evenements sur les methodes associees
        EVT_SIZE(self, self.OnSize) #redimensionnement du canevas
        
        #pression du bouton gauche de la souris
        EVT_LEFT_DOWN(self, self.OnMouseDown)        
        #relachement du bouton gauche de la souris
        EVT_LEFT_UP(self, self.OnMouseUp) #
        #pression du bouton droite de la souris
        EVT_RIGHT_DOWN(self, self.OnMouseDown)
        #relachement du bouton droite de la souris
        EVT_RIGHT_UP(self, self.OnMouseUp)        
        #deplacement de la souris
        EVT_MOTION(self, self.OnMouseMotion)
        
        #Vitesses lors du changement de la vue � l'aide de la souris
        self.vitesse_deplacement_x = 0.1
        self.vitesse_deplacement_y = 0.1
        self.vitesse_zoom = 1.0

    def evRafraichir(self, evt) :
        #si il faut suivre un taxi alors rafraichit aussi
        #la position de la vue
        if self.suivreTaxi :
            self.repositionner()
        self.Refresh(false) #rafraichit le canevas
        
    def evChangePosition(self, evt) :
        """
        Evenement s'actionnant lors du changement de position de la vue.
        
        Lorsque le thread tortue desire deplacer la vue il declanche
        l'evenement EVT_METTRE_A_JOUR_POSITION se qui va appeller cette
        methode.
         
        @param MettreAJourPosition evt : L'evenement
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """       
        
        #change la position en fonction du vecteur de deplacement
        self.setPosition ((self.position[0] + self.vitesse_deplacement_x * evt.vecteur[0] /
                           self.zoom,
                           self.position[1] +  self.vitesse_deplacement_y * evt.vecteur[1] /
                           self.zoom))
        self.repositionner() #repositionne la vue
        self.Refresh(false) #rafraichit le canevas
    
        
    def evChangeZoom(self, evt) :
        """
        Evenement s'actionnant lors du changement du zoom de la vue.
        
        Lorsque le thread zoom desire changer le zoom de la vue il declanche
        l'evenement EVT_METTRE_A_JOUR_ZOOM se qui va appeller cette
        methode.
         
        @param MettreAJourZoom evt : L'evenement
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """   
        #change le zoom en fonction de celle presente dans l'evenement evt
        self.setZoom(self.zoom + evt.deltaY * log(self.zoom + self.vitesse_zoom ) * 0.001)
        self.repositionner() #repositionne la vue      
        self.Refresh(false) #rafraichit le canevas
        
    
        
    def OnSize(self, evt) :
        """
        Evenement s'actionnant lors du changement de taille du canevas.
        
        Lorsque la taille du canevas OpenGL est modifie
        cette methode est appellee
         
        @param wxPyEvent evt : L'evenement
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """  
        self.repositionner() #repositionne la vue  
    
    
            
    def OnMouseDown(self, evt) :
        """
        Evenement s'actionnant lors de la pression d'un bouton de la souris.
        
        Lorsque un des bouton de la souris est presse
        cette methode est appellee
         
        @param wxMouseEvent evt : L'evenement souris
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        #if not self.HasCapture() :
        #redirige tout les evenements souris dans ce canevas
        self.CaptureMouse()
        #enregistre la position de click
        self.xDebut, self.yDebut = evt.GetPosition()
        if evt.LeftIsDown() : #si le bouton gauche est presse
            self.threadTortue.start() #enclenche le thread tortue
        if evt.RightIsDown() : #si le bouton droite est presse
            self.threadZoom.start() #enclenche le thread zoom
                
    

    def OnMouseUp(self, evt) :
        """
        Evenement s'actionnant lors du relachement d'un bouton de la souris.
        
        Lorsque un des bouton de la souris est relache
        cette methode est appellee
         
        @param wxMouseEvent evt : L'evenement souris
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        #si le canevas a une capture
        #(entrain de zoomer ou de deplacer)
        if self.HasCapture() :
            self.ReleaseMouse() #enleve la capture
            if evt.LeftUp() :
                self.threadTortue.stop() #arrete les thread
            if evt.RightUp() :
                self.threadZoom.stop()
            
    

    def OnMouseMotion(self, evt):
        """
        Evenement s'actionnant lors du deplacement de la souris.
        
        Lorsque un des bouton de la souris est relache
        cette methode est appellee
         
        @param wxMouseEvent evt : L'evenement souris
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        #si un ou plusieurs boutons de la souris son presses lors
        #du deplacement alors
        if evt.Dragging():
            #prends la position de la souris                  
            self.x, self.y = evt.GetPosition()
            if evt.LeftIsDown() : #si le bouton de gauche est presse
                #defini un vecteur de deplacement
                self.threadTortue.setVecteur(((self.x-self.xDebut), (self.yDebut-self.y)))
            if evt.RightIsDown() :
                #defini un delta
                self.threadZoom.setDeltaY(self.yDebut-self.y)

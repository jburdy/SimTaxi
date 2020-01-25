#!/usr/bin/python3
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.5 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-12-7"

from wxPython.wx import *
import _thread
import time

#un nouveau type d'evenement
wxEVT_METTRE_A_JOUR_POSITION = wxNewEventType()
def EVT_METTRE_A_JOUR_POSITION(win, func) :
    """
    Bind de l'evenement de mise a jour de la position.
    
    Procedure permettant de binder l'evenement
    wxEVT_METTRE_A_JOUR_POSITION sur une methode.
     
    @param wxWindow win : la fen§tre sur laquelle intervient l'evenement
    @param func : la methode a appeller
    @return Rien : Ne retourne rien
    @author Gregory Burri
    """
    
    #bind l'evenement sur la fonction
    win.Connect(-1, -1, wxEVT_METTRE_A_JOUR_POSITION, func)

class MettreAJourPosition(wxPyEvent) :
    """
    Evenement de mise a jour de la position.
    
    Une instance de cet evenement est transmis a la methode
    qui a ete binde a l'aide de EVT_METTRE_A_JOUR_POSITION (voir ci dessu).
    Cet instance contient le vecteur de deplacement.
    
    :version: $Revision 1.0 $
    :author: Gregory Burri    
    """
    
    def __init__(self, vecteur) :
        """
        Initialisation d'un evenement de mise a jour de la position.
        
        Initialise le vecteur.
         
        @param (float, float) vecteur : vecteur de deplacement de la vue
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        wxPyEvent.__init__(self) #initialise le parent
        #definit le type d'evenement
        self.SetEventType(wxEVT_METTRE_A_JOUR_POSITION)
        self.vecteur = vecteur #initialise le vecteur

class ThreadTortue :
    """
    Thread pour le deplacement de la vue.
    
    Ce thread declenche periodiquement, lorsqu'il est actif, un evenement de
    mise a jour de la position de la vue.
    
    :version: $Revision 1.0 $
    :author: Gregory Burri    
    """
    
    def __init__(self, Obj) :
        """
        Initialisation du thread tortue.
        
        Initialise differentes donnees membres.
         
        @param wxObject Obj : objet qui a initialise le thread
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        #objet qui a cree le thread pour pouvoir lui declencher l'evenement
        #de mise a jour de la position
        self.Obj = Obj
        self.vecteur = (0.0, 0.0) #le vecteur de deplacemet
        
        #le taux de rafraichissement, une valeur plus basse permet
        #d'avoir plus d'image/seconde
        self.tauxRafraichissement = 0.03
        
        self.keepGoing = self.running = False
        
    
    
    def setVecteur(self, vecteur) :
        """
        Definir le vecteur.
        
        Definit le vecteur de deplacement.
         
        @param (float, float) vecteur : vecteur de deplacement
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        self.vecteur = vecteur
        
    
    
    def start(self) :
        """
        Demarrer le thread.
        
        Demarre le thread.

        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        #ne permet pas de cree plusieurs thread
        if self.running : return
        
        self.vecteur = (0.0, 0.0) #met a 0 le vecteur de deplacement
        self.keepGoing = self.running = True
        _thread.start_new_thread(self.run, ()) #start le thread
        
    
    
    def stop(self) :
        """
        Arreter le thread.
        
        Arrete le thread.

        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        self.keepGoing = False

            
        
    def run(self) :
        """
        Corps du thread.
        
        Partie qui s'execute lors de l'enclenchement du thread.

        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        #tant que le thread est enclenche
        while self.keepGoing:
            #cree un evenement de mise a jour de la position
            evt = MettreAJourPosition(self.vecteur)
            wxPostEvent(self.Obj, evt) #declanche l'evenement
            time.sleep(self.tauxRafraichissement) #attends un moment
            
        #lorsque le thread a fini sont execution il 'indique
        self.running = false

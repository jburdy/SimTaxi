#!/usr/bin/python
__version__ = "$Revision: 1.5 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-12-7"

from wxPython.wx import *
import thread
import time

#un nouveau type d'evenement
wxEVT_METTRE_A_JOUR_ZOOM = wxNewEventType()
def EVT_METTRE_A_JOUR_ZOOM(win, func) :
    """
    Bind de l'evenement de mise a jour du zoom.
    
    Procedure permettant de binder l'evenement
    wxEVT_METTRE_A_JOUR_ZOOM sur une methode.
     
    @param wxWindow win : la fenêtre sur laquelle intervient l'evenement
    @param func : la methode a appeller
    @return Rien : Ne retourne rien
    @author Gregory Burri
    """
    
    #bind l'evenement sur la fonction
    win.Connect(-1, -1, wxEVT_METTRE_A_JOUR_ZOOM, func)
        
class MettreAJourZoom(wxPyEvent) :
    """
    Evenement de mise a jour du zoom.
    
    Une instance de cet evenement est transmis a la methode
    qui a ete binde a l'aide de EVT_METTRE_A_JOUR_ZOOM (voir ci dessu).
    Cet instance contient le delta de changement du zoom.
    
    :version: $Revision 1.0 $
    :author: Gregory Burri    
    """
    def __init__(self, deltaY) :
        """
        Initialisation d'un evenement de mise a jour du zoom.
        
        Initialise le delta.
         
        @param float deltaY : delta de changement du zoom
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        wxPyEvent.__init__(self) #initialise le parent
        self.SetEventType(wxEVT_METTRE_A_JOUR_ZOOM)
        self.deltaY = deltaY #initialise le vecteur
        
class ThreadZoom :
    """
    Thread pour le changement du zoom.
    
    Ce thread declenche periodiquement, lorsqu'il est actif, un evenement de
    mise a jour du zoom.
    
    :version: $Revision 1.0 $
    :author: Gregory Burri    
    """
    
    def __init__(self, Obj) :
        """
        Initialisation du thread zoom.
        
        Initialise differentes donnees membres.
         
        @param wxObject Obj : objet qui a initialise le thread
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        #objet qui a cree le thread pour pouvoir lui declencher l'evenement
        #de mise a jour du zoom
        self.Obj = Obj
        self.posY = 0.0
        
        #le taux de rafraichissement, une valeur plus basse permet
        #d'avoir plus d'image/seconde
        self.tauxRafraichissement = 0.03

        self.keepGoing = self.running = False        

    
        
    def setDeltaY(self, deltaY) :
        """
        Definir le delta.
        
        Definit le delta de changement du zoom.
         
        @param float deltaY : delta
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        self.deltaY = deltaY
        
    
    
    def start(self) :
        """
        Demarrer le thread.
        
        Demarre le thread.

        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        #ne permet pas de cree plusieurs thread
        if self.running : return
        
        self.deltaY = 0.0 #met a 0 le delta de deplacement
        self.keepGoing = self.running = True
        thread.start_new_thread(self.run, ())  #start le thread
        
    

    def stop(self) :
        """
        Arreter le thread.
        
        Arrete le thread.

        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        self.keepGoing = false
        
    

    def run(self) :
        """
        Corps du thread.
        
        Partie qui s'execute lors de l'enclenchement du thread.

        @return Rien : Ne retourne rien
        @author Gregory Burri
        """

        #tant que le thread est enclenches
        while self.keepGoing :
            #cree un evenement de mise a jour du zoom
            evt = MettreAJourZoom(self.deltaY)
            wxPostEvent(self.Obj, evt) #declanche l'evenement
            time.sleep(self.tauxRafraichissement) #attends un moment
            
        #lorsque le thread a fini sont execution il 'indique
        self.running = False 

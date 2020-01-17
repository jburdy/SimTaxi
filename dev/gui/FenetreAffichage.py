#!/usr/bin/python
__version__ = "$Revision: 1.5 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-11-23"

from wxPython.wx import *
from EvenementsGlCanvas import *

class FenetreAffichage(wxFrame) :
    """
    Fenetre d'affichage.
    
    Fenetre graphique qui affiche les taxis, les routes etc...
    
    :version: $Revision 1.0 $
    :author: Gregory Burri 
    """
    
    def __init__(self) :
        """
        Initialisation de la fenêtre d'affichage.
        
        Initialise la fenêtre d'affichage dans laquel est 
        affiche le graphe en PpenGL.

        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        #initialise le parent
        wxFrame.__init__(self, None, -1, "Simtaxi - Affichage",
            wxDefaultPosition, wxSize(400, 400),
             wxRESIZE_BORDER | wxCAPTION | wxFRAME_NO_TASKBAR | wxMAXIMIZE_BOX | wxSYSTEM_MENU)
        
        #attache a la frame un canevas de dessin
        self.OpenglCanvas = EvenementsGlCanvas(self)


        #evenement lors de la fermeture de la fenêtre
        EVT_CLOSE(self, self.invisible)

    
    
    def invisible(self, event) :
        """
        Initialisation de la fenêtre d'affichage.
        
        Initialise la fenêtre d'affichage dans laquel est 
        affiche le graphe en PpenGL.

        @param wxCloseEvent event : L'evenement de fermeture
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        self.Show(False) #rends invisible la fenêtre

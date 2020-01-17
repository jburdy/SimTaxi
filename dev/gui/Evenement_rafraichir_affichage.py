#!/usr/bin/python
__version__ = "$Revision: 1.1 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-12-7"

from wxPython.wx import *

#un nouveau type d'evenement
wxEVT_METTRE_A_JOUR_AFFICHAGE = wxNewEventType()
def EVT_METTRE_A_JOUR_AFFICHAGE(win, func) :
    #bind l'evenement sur la fonction
    win.Connect(-1, -1, wxEVT_METTRE_A_JOUR_AFFICHAGE, func)

class MettreAJourAffichage(wxPyEvent) :
    def __init__(self) :      
        wxPyEvent.__init__(self) #initialise le parent
        #definit le type d'evenement
        self.SetEventType(wxEVT_METTRE_A_JOUR_AFFICHAGE)

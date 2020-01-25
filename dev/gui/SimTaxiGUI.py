#!/usr/bin/python3
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.11 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-11-23"

from wxPython.wx import *
from .FenetreControl import *

class SimTaxiGUI(wxApp) :
    """
    Interface graphique de SimTaxi.
    
    Cette classe est la racine de l'interface graphique, elle
    contient la fenetre de control.
    
    :version: $Revision 1.0 $
    :author: Gregory Burri    
    """

    def OnInit(self) :
        """
        Initialisation de l'environement graphique.
        
        Cree la fen§tre principal (de control)
         
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        #la fen§tre principal
        laFenetreControl = FenetreControl()
        laFenetreControl.Show(True)
        
        #la module de rafraichissement pour pouvoir mettre § jour
        #la position des taxis sur l'affichage
        self.rafraichissement = Rafraichissement()

        return True        

    def start(self) :
        self.MainLoop()

    def rafraichir(self, temps, evenement) :
        self.rafraichissement.rafraichir(temps, evenement)
        

#test de la classe
if __name__ == '__main__' :
    graphe = GrapheXY("../graphe/graphe.gr")
    gui = SimTaxiGUI(0) #cree l'interface
    gui.start()


#!/usr/bin/python2
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.9 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-11-23"

###############!!!!!!!! TODO !!!!!!!!###############

from wxPython.wx import *
from wxPython.xrc import *
import os

from FenetreAffichage import *
    

"""
lblTemps = 10000
lblTempsAffiche = 10001
gauTemps = 10002
sepLine = 10003
lblVitesse = 10004
lblVitesseAffiche = 10005
sliVitesse = 10006

def MyDialogFunc( parent, call_fit = true, set_sizer = true ):
    item0 = wxBoxSizer( wxVERTICAL )    
    item1 = wxBoxSizer( wxVERTICAL )    
    item2 = wxBoxSizer( wxHORIZONTAL )
    
    item3 = wxStaticText( parent, lblTemps, "Temps", wxDefaultPosition, wxDefaultSize, 0 )
    item2.AddWindow( item3, 0, wxALIGN_CENTRE|wxALL, 5 )

    item4 = wxStaticText( parent, lblTempsAffiche, "12:34", wxDefaultPosition, wxDefaultSize, 0 )
    item4.SetFont( wxFont( 8, wxSWISS, wxNORMAL, wxBOLD ) )
    item2.AddWindow( item4, 0, wxALIGN_CENTRE|wxALL, 5 )

    item1.AddSizer( item2, 0, wxALIGN_CENTER_VERTICAL|wxALL, 0 )

    item5 = wxGauge( parent, gauTemps, 100, wxDefaultPosition, wxSize(100,10), 0 )
    item1.AddWindow( item5, 0, wxALIGN_CENTER_VERTICAL|wxALL, 0 )

    item0.AddSizer( item1, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item6 = wxStaticLine( parent, sepLine, wxDefaultPosition, wxSize(100,-1), wxLI_HORIZONTAL )
    item0.AddWindow( item6, 0, wxALIGN_CENTRE|wxALL, 5 )

    item7 = wxBoxSizer( wxVERTICAL )
    
    item8 = wxBoxSizer( wxHORIZONTAL )
    
    item9 = wxStaticText( parent, lblVitesse, "Vitesse", wxDefaultPosition, wxDefaultSize, 0 )
    item8.AddWindow( item9, 0, wxALIGN_CENTRE|wxALL, 5 )

    item10 = wxStaticText( parent, lblVitesseAffiche, "x4", wxDefaultPosition, wxDefaultSize, 0 )
    item10.SetFont( wxFont( 8, wxSWISS, wxNORMAL, wxBOLD ) )
    item8.AddWindow( item10, 0, wxALIGN_CENTRE|wxALL, 5 )

    item7.AddSizer( item8, 0, wxALIGN_CENTER_VERTICAL|wxALL, 0 )

    item11 = wxSlider( parent, sliVitesse, 0, 0, 10, wxDefaultPosition, wxSize(100,-1), wxSL_HORIZONTAL )
    item7.AddWindow( item11, 0, wxALIGN_CENTER_VERTICAL|wxALL, 0 )

    item0.AddSizer( item7, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    if set_sizer == true:
        parent.SetAutoLayout( true )
        parent.SetSizer( item0 )
        if call_fit == true:
            item0.Fit( parent )
            item0.SetSizeHints( parent )

    return item0
    
ID_A_PROPOS = 101 #identificateur du menu "a propos"
ID_SORTIR  = 102  #identificateur du menu "sortir"
"""


#identificateur du menu pour afficher la fen�tre d'affichage
ID_VOIR_FENETRE_AFFICHAGE = 103

class FenetreControl(wxFrame):
    """
    Fenetre principale.
    
    Fenetre principale gerant les autres fen�tres et contenant les
    contr�les principaux.
    
    :version: $Revision 1.0 $
    :author: Gregory Burri
    """
    
    def __init__(self):
        """
        Initialisation de la fen�tre principale 
        
        @author Gregory Burri
        """
        #initialise la fen�tre
        wxFrame.__init__(self, None, -1,"SimTaxi - Fenetre de controle",
            wxDefaultPosition, wxSize(120, 200), 
            wxMINIMIZE_BOX | wxCAPTION | wxSYSTEM_MENU)
        
        #cree la fen�tre d'affichage
        self.laFenetreAffichage = FenetreAffichage()
        self.laFenetreAffichage.Show(True)
        """
        self.sizer = wxBoxSizer(wxVERTICAL)
        self.sizer.Add(wxStaticText(self, 100, "Vitesse", wxDefaultPosition, wxDefaultSize), 0, wxEXPAND)
        self.sizer.Fit(self)
        """


        #self.lblTemps = xmlPanelControl.Load("lblTemps")
        #self.lblTemps.SetLabel("sjdflkj")
        #sizer = wxBoxSizer(wxVERTICAL)
        #panelControl.Append(self)
        #self.SetSizer
        #BARRE D'ETAT ET MENU (pas encore utilise)
        """
        #cree la barre d'etat
        self.CreateStatusBar()
        self.SetStatusText("barre d'etat")
        """
        #le menu fichier qui va �tre racrocher a la barre de menu qui
        #elle m�me va �tre raccorche a laframe
        menuFichier = wxMenu()
        """
        menuFichier.Append(ID_A_PROPOS, "&About",
            "More information about this fucking progz")
        menuFichier.AppendSeparator()
        menuFichier.Append(ID_SORTIR, "E&xit",
            "Terminate this program")
        """
        #le menu fichier de gestion des fen�tres
        menuFenetre = wxMenu()
        menuFenetre.Append(ID_VOIR_FENETRE_AFFICHAGE,
            "Afficher fenetre OpenGL", "Affiche la fen�tre Opengl")
        
        menuBar = wxMenuBar() #la barre de menu
        
        #accroche le menu fichier a la barre
        #menuBar.Append(menuFichier, "&File");
        
        #on accroche la barre a la fen�tre
        menuBar.Append(menuFenetre, "&Window");
            
        self.SetMenuBar(menuBar) #accroche le menu a la frame
        

        ###EVENEMENTS###
        ##menu
        #EVT_MENU(self, ID_A_PROPOS, self.evAPropos)
        #EVT_MENU(self, ID_SORTIR, self.evMenuQuit)
        EVT_MENU(self, ID_VOIR_FENETRE_AFFICHAGE,
        self.evVoirFenetreAffichage)
        ##
            
        #EVT_COMMAND_SCROLL(self, XMLID("sliVitesse"), self.changeVitesse)
        EVT_CLOSE(self, self.evSortir) #lorsque la fen�tre est ferme
        ###FIN EVENEMENTS###

    
    def changeVitesse(self, evt) :
        vitesse = evt.GetPosition()/10.0
        self.lblVitesseAffiche.SetLabel("%.1f"%(vitesse))
               
    def evAPropos(self, event):
        #test de boite de dialogue
        dlg = wxMessageDialog(self, "ce ceci n'est qu'un test", "about me",
            wxOK | wxICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
    
    def evVoirFenetreAffichage(self, event):
        self.laFenetreAffichage.Show(True)
    
    def evSortir(self, event):
        self.laFenetreAffichage.Destroy() #ferme la frame (fen�tre)
        self.Destroy() #ferme la frame (fen�tre)
    
    def evMenuQuit(self, event):
        self.Close(True) #ferme la frame (fen�tre)
        


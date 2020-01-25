#!/usr/bin/python3
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.7 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-12-7"

from wxPython.wx import *

#essais d'importer le glcanevas (il faut que se composant soit installe)
try:
    from wxPython.glcanvas import *
    haveGLCanvas = True
except ImportError:
    haveGLCanvas = False

from .importGL import *
    
class OpenGLCanvas(wxGLCanvas) :
    """
    Canevas OpenGL personnalise.
    
    Zone de dessin OpengGL.
    
    :version: $Revision: 1.7 $
    :author: Gregory Burri
    """
    
    def __init__(self, parent) :
        """
        Initialisation de la classe OpenGLCanvas.
        
        Bind certains evenements.
         
        @param wxFrame parent : La frame a laquelle accrocher le canevas
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        wxGLCanvas.__init__(self, parent, -1) #initialise le parent
        
        #savoir si opengl § §t§ initialis§
        self.iniGL = False

        #evenement lorsque la zone a besoin d'§tre repeinte
        EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)

        #evenement lorsque la zone doit §tre repeinte
        EVT_PAINT(self, self.OnPaint)
        
    def OnEraseBackground(self, evt) :
        """
        Appele lorsque la zone a besoin d'§tre repeinte.
        
        -.
         
        @param wxEraseEvent evt : l'evenement
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        pass #ne fait rien pour eviter des scintillements sous MSW.
        
    
    def OnPaint(self, evt):
        """
        Appele lorsque la zone doit §tre repeinte.
        
        -.
         
        @param wxPaintEvent evt : l'evenement
        @return Rien : Ne retourne rien
        @author Gregory Burri
        """
        
        if not self.iniGL :
            self.iniGL = True
            self.initGL()
        
        #doit §tre construit lors de l'evenement onPaint...
        dc = wxPaintDC(self)
        

        self.evRedessiner() #redessine la scene


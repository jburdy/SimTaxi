#!/usr/bin/python3
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.18 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-11-23"

from wxPython.wx import *

from .OpenglCanvas import *
from .TexteAbsoluGL import *

#contient les listes d'affichage OpenGL
from .Rafraichissement import *

class AffichageOpenGL(OpenGLCanvas):
    """
    Classe dessinant dans le canevas opengl.
    
    Gestion de l'affichage OpenGL, cette classe va se charger
    de redessiner toute la sc§ne. Elle ne fournit pas les outils
    pour la gestion de la vue, elle est donc quasiment inutilisable
    toute seule.
    """
    
    
    def __init__(self, attache) :
        """
        Initialisation de l'affichage.
        
        attache (wxWindow) -- Conteneur dans lequel mettre l'affichage
        
        - depuis - 1.0
        
        - auteur - Gr§gory Burri
        """
        OpenGLCanvas.__init__(self, attache)
        self.texte = TexteAbsolu() #l'affichage du temps  
    
    
    def initGL(self) :
        """
        Initialisation de diff§rents param§tre OpenGL.
        
        Le canvas OpenGL doit §tre cr§e pour pouvoir effectu§ des
        commandes OpenGL c'est pour cela qu'on ne peut pas mettre le
        contenu de cette m§thode dans le '__init__'
        
        - depuis - 1.0
        
        - auteur - Gr§gory Burri
        """
        #definit ce canevas comme celui de dessin courant
        self.SetCurrent()

        glEnable(GL_CULL_FACE) #active l'effacement des faces cach§es
        glFrontFace(GL_CW) #d§finit la face visible
        glCullFace(GL_FRONT) #on cache certaines faces (les faces devants)
        
        glEnable(GL_DEPTH_TEST) #active le Z-Buffer
        
        #l'objet permettant de rafraichir la sc§ne,
        #il fait la liaison avec les autres partie de SimTaxi
        self.rafraichissement = Rafraichissement()
        
        #passe une r§f§rence de l'affichage au rafraichissement
        #(ceci pour qu'il puisse g§n§rer un événement destin§ au canvas)
        self.rafraichissement.set_obj_evt(self)
        self.repositionner()
        self.evRedessiner()
        
        
    def evRedessiner(self) :
        """
        Redessine la sene.
        
        - depuis - 1.0
        
        - auteur - Gr§gory Burri
        """

        #Affiche les diff§rents composants
        self.rafraichissement.afficherGraphe()
        self.rafraichissement.afficherTaxis()
        self.rafraichissement.afficherStations()
        self.rafraichissement.afficherClients()
        
        #affiche le temps
        t = int(self.rafraichissement.getTemps())
        self.texte.dessiner((2, 2), str(t/3600) + "h " + str(t/60 % 60) +
                                    "min " + str(t % 60) + "s" )
        
        self.SwapBuffers() #permute les tampons d'affichage

#!/usr/bin/python3
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.17 $"
__author__ = "EI5a, eivd, SimTaxi (Groupe Burdy)"
__date__ = "2002-12-7"

from Singleton import *

from GrapheXY import *
from GestionnaireStations import *
from GestionnaireTaxis import *

#modules de dessin
from .TaxiGL import *
from .RouteGL import *
from .CarrefourGL import *
from .StationGL import *
from .ClientAttendGL import *
from .ClientDeposeGL import *

#evenement pour rafraichir l'affichage
from .Evenement_rafraichir_affichage import *

class Rafraichissement(Singleton) :

    def init(self) :
        
        self.obj_evt = None
        
        #cree une instance de dessin route sur la couche 7               
        self.route = Route(7)
        
        #cree une instance de dessin carrefour sur la couche 8    
        self.carrefour = Carrefour(8)
        
        #cree une instance de dessin taxi sur la couche 9
        self.taxi = Taxi(9)
        
        #cree une instance de dessin station sur la couche 8
        self.station = Station(8)
        
        #cree une instance de dessin clientAttend 
        #et de clientDepose sur la couche 10
        self.client = ClientAttend(10)
        self.clientD = ClientDepose(10)
        
        #les liste d'affichage pour le graphe et les stations
        self.listeAffichageGraphe = glGenLists(1)
        #self.listeAffichageStations = glGenLists(1)
     
        self.graphe = GrapheXY() #le graphe
        self.taxis = GestionnaireTaxis() #les taxis
        self.stations = GestionnaireStations() #les stations
        self.clients = [] #liste des clients § afficher
        self.clientsDepose = [] #liste des clients d§pos§s
        
        #le temps du dernier rafraichissement
        self.temps = 0;
        
        #Met § jour la liste d'affichage pour le graphe
        self.maj_liste_graphe()
        #self.maj_liste_stations()
      
    def set_obj_evt(self, obj) :
        self.obj_evt = obj
        
    def getTemps(self) :
        return self.temps;
                    
    def rafraichir(self, temps, evenement) :
           
        #si l'evenement est une demande de taxi d'un client
        if evenement.__class__.__name__ == 'EvClient' :
            #ajoute le client § la liste des clients § afficher
            self.clients.append(evenement)
            
        #si l'evenement est le chargement d'un client 
        elif evenement.__class__.__name__ == 'EvChargerClient' :
            #enl§ve le client de la liste des clients § afficher
            #if evenement.client() in self.clients :
            self.clients.remove(evenement.client())
            
        #si l'evenement est un largage de client
        elif evenement.__class__.__name__ == 'EvPoserClient' :
            #l'ajoute § la liste des clients d§pos§s
            self.clientsDepose.append((evenement, temps))        
            
        if self.obj_evt != None :
            self.temps = temps #m§morise le temps
            #cr§e et declanche l'evenement de rafraichissement
            evt = MettreAJourAffichage()
            wxPostEvent(self.obj_evt, evt)
                
    def maj_liste_graphe(self) :
        liste_routes = [] #la liste des routes § affichers
        
        #commence la liste
        glNewList(self.listeAffichageGraphe, GL_COMPILE)
        for arc in self.graphe.listeArcs(True) : #pour chaque arc
            #sommet de debut et de fin de la route
            debut = (self.graphe.attributsSommet(arc[0]).getX(),
                self.graphe.attributsSommet(arc[0]).getY())
            fin = (self.graphe.attributsSommet(arc[1]).getX(),
                self.graphe.attributsSommet(arc[1]).getY())

            #si une route dans allant dans l'autre sens
            #exite deja dans la liste alors
            if (fin, debut, True) in liste_routes : 
                #notifie cette route comme n'§tant pas sens-unique
                liste_routes[liste_routes.index((fin, debut, True))] = \
                    (fin, debut, False)
            else :
                #sinon ajoute cette route § la liste
                liste_routes.append((debut, fin, True))
         
        #affiche chaque route de la liste
        for route in liste_routes :          
            self.route.dessiner(route[0], route[1], route[2])
            
        #pour chaques sommets
        for sommet in self.graphe.listeSommets(True) :
            #le dessine
            self.carrefour.dessiner((sommet[1].getX(), sommet[1].getY()))
                    
        glEndList() #fin de la liste
        
    def maj_liste_stations(self) :
        #commence la liste
        glNewList(self.listeAffichageStations, GL_COMPILE)
        #pour chaque taxis (du gestionnaire de taxis)
        for station_obj in self.stations.getListeStations() :
            position = station_obj.getPosition()
            self.station.dessiner(position[0], position[1])
        glEndList() #fin de la liste
        
    def afficherStations(self) :
        for station_obj in self.stations.getListeStations() :
            position = station_obj.getPosition()
            if self.obj_evt.visible(position[0], 50) :
                self.station.dessiner(position[0], position[1],
                   station_obj.getNbPlacesTot(),
                   station_obj.getNbPlacesTot() -
                   station_obj.getNbPlacesLibres())
        
    def afficherTaxis(self) :
        for taxi_obj in self.taxis.getListe() :
            position = taxi_obj.getPosition(self.temps)
            
            #si le taxi se trouve § l'§cran alors l'affiche
            if self.obj_evt.visible(position[0], 20) :                    
                self.taxi.dessiner(position[0], position[1],
                    taxi_obj.getEtat(), taxi_obj.getNo())
            
    def afficherClients(self) :
        for client_obj in self.clients :
            position = client_obj.chemin().posDepartXY();
            
            #si le client se trouve § l'§cran alors l'affiche
            if self.obj_evt.visible(position, 10) :
                self.client.dessiner(position, self.temps)
                    
        for client_obj in self.clientsDepose :
            position = client_obj[0].cheminStation().posDepartXY();
            
            #si le client se trouve § l'§cran alors l'affiche
            if self.obj_evt.visible(position, 10) :
                afficher = self.clientD.dessiner(
                    position, client_obj[1], self.temps)
                if not afficher : self.clientsDepose.remove(client_obj)
               
    def afficherGraphe(self) :
        glCallList(self.listeAffichageGraphe)


#!/usr/bin/python2
# -*- coding: utf-8 -*-
"""
Module contenant les classes �v�nements.

$Id: Evenement.py,v 1.19 2003/02/09 12:17:38 vega01 Exp $
"""
__version__ = '$Revision: 1.19 $'
__author__ = 'EI5a, eivd, SimTaxi (Groupe Burdy)'
__date__ = '2002-12-01'

from Taxi import *
import GrapheXY
import Central

class ErreurTraiter(Exception):
    """
    Exception lors du traitement d'un evenement.
    """
    pass



class Evenement:
    """
    Classe racine de tout les evenements pour SimTaxi.
    """


    def __init__(self, temps, traiter = None):
        """
        Constructeur

        temps (Int) -- Le moment ou l'evenement aura lieu

        traiter (Function) -- Le code a executer lorsque l'evenement a lieu

        retourne (Evenement) -- Un objet evenement

        - depuis - 1.0

        - auteur - Vincent Decorges
        """
        self._temps = temps
        self._traiter = traiter


    def traiter(self):
        """
        Traitement associe � l'evenement.

        Par d�faut aucun traitement associe. Peut d�clencher l'exception
        Erreur_Traiter.

        - depuis - 1.0

        - auteur - Vincent Decorges
        """
        self._traiter()


    def temps(self):
        """
        Donne le temps auquel l'evenement doit avoir lieu.

        - depuis - 1.0

        - auteur - Vincent Decorges
        """
        return self._temps
        
    def __repr__(self):
        """
        Donne des infos sur l'�v�nement

        - depuis - 1.0

        - auteur - Vincent Decorges
        """
        return self.__class__.__name__ + "\ntemps : " + str(self._temps)



class EvClient(Evenement):
    """
    Evenement client.

    Permet de savoir qu'un client a appelle un taxi est � quel moment.
    """


    def __init__(self, temps, positions):
        """
        Constructeur

        temps (Int) -- Le moment ou l'evenement aura lieu

        positions (Tuple) -- Tuple contenant la position + la destination

        retourne (EvClient) -- Un objet EvClient

        - depuis - 1.0

        - auteur - Vincent Decorges
        """
        Evenement.__init__(self, temps, self.__traitementClient)
        self.__positions = positions
        self.__chemin = None
        self.__cheminClient = None


    def chemin(self):
        """
        Selecteur.

        retourne (Chemin) -- Chemin pour aller de la position intial a
                                  la destination.

        - depuis - 1.1

        - auteur - Vincent Decorges
        """
        return self.__chemin


    def cheminClient(self):
        """
        Selecteur.

        retourne (Chemin) -- Chemin que le taxi doit faire pour aller
                                  chercher le client.

        - depuis - 1.3

        - auteur - Vincent Decorges
        """
        return self.__cheminClient
        
    def positions(self):
        """
        Selecteur.

        retourne (Tuple arcs) -- Position du client et destination
 

        - depuis - 1.3

        - auteur - Vincent Decorges
        """
        return self.__positions



    def __traitementClient(self):
        """
        Appeler par traiter.

        Choisi un taxi d'apr�s la politique.

        - depuis - 1.0

        - auteur - Vincent Decorges
        """
        
        graphe = GrapheXY.GrapheXY()
        #Calcul du chemin � parcourir utiliser par le taxi
        self.__chemin = graphe.cheminPlusCourt(self.__positions[0], self.__positions[1])
        
        #On recupere la politique courante
        politique = Central.Central().politique()
        taxi, self.__cheminClient = politique.choisirTaxi(self)

        if taxi == None:
            raise ErreurTraiter
        
        taxi.traiterEvenement(self)

    def __repr__(self):
        """
        Donne des infos sur l'�v�nement

        - depuis - 1.0

        - auteur - Vincent Decorges
        """
        return Evenement.__repr__(self) + "\nchemin : " + str(self.__chemin) \
        + "\nchemin client : " + str(self.__cheminClient)

class EvTaxi(Evenement):
    """
    Evenement Taxi.

    Classe racine des evenements que peut lancer un taxi.
    """


    def __init__(self, temps, taxi, traiter = None):
        """
        Constructeur

        temps (Int) -- Le moment ou l'evenement aura lieu

        taxi (Taxi) -- Le taxi qui cree l'evenement

        traitement (Function) -- Traitement a effectue

        retourne (EvTaxi) -- Un objet EvTaxi

        - depuis - 1.0

        - auteur - Vincent Decorges
        """
        Evenement.__init__(self, temps, traiter)
        self._taxi = taxi


    def taxi(self):
        """
        Retourne le taxi qui a cree l'evenement

        retourne (Taxi) -- Un objet Taxi

        - depuis - 1.0

        - auteur - Vincent Decorges
        """
        return self._taxi

    def __repr__(self):
        """
        Donne des infos sur l'�v�nement

        - depuis - 1.0

        - auteur - Vincent Decorges
        """
        return Evenement.__repr__(self) + "\ntaxi : " + str(self._taxi.getNo())


class EvChargerClient(EvTaxi):
    """
    Lancer par le taxi quand il charge un client.
    """


    def __init__(self, temps, taxi, client):
        """
        Constructeur.

        temps (Int) -- Le moment ou l'evenement aura lieu

        taxi (Taxi) -- Le taxi qui cree l'evenement

        client (EvClient) -- Le client que le taxi charge

        retourne (EvChargerClient) -- Un objet EvChargerClient

        - depuis - 1.0

        - auteur - Vincent Decorges
        """
        EvTaxi.__init__(self, temps, taxi, self.__traitementCharger)
        self._client = client


    def client(self):
        """
        Retourne l'evenement client.

        retourne (EvClient) -- Un objet EvClient

        - depuis - 1.0

        - auteur - Vincent Decorges
        """
        return self._client


    def __traitementCharger(self):
        """
        Appeler par traiter.

        S'envoye au taxi.

        - depuis - 1.3

        - auteur - Vincent Decorges
        """
        self._taxi.traiterEvenement(self)

    def __repr__(self):
        """
        Donne des infos sur l'�v�nement

        - depuis - 1.0

        - auteur - Vincent Decorges
        """
        return EvTaxi.__repr__(self) + "\nclient : " + self._client.__repr__()

class EvPoserClient(EvChargerClient):
    """
    Lancer par le taxi quand il pose un client.
    """


    def __init__(self, temps, taxi, client):
        """
        Constructeur.

        temps (Int) -- Le moment ou l'evenement aura lieu

        taxi (Taxi) -- Le taxi qui cree l'evenement

        retourne (EvTaxi) -- Un objet EvTaxi

        - depuis - 1.3

        - auteur - Vincent Decorges
        """
        EvTaxi.__init__(self, temps, taxi, self.__traitementStation)
        self._client = client
        self.__cheminStation = None


    def cheminStation(self):
        """
        Selecteur.

        retourne (Chemin) -- Chemin que le taxi doit faire pour aller
                         chercher le client.
        - depuis - 1.3

        - auteur - Vincent Decorges
        """
        return self.__cheminStation


    def station(self):
        """
        la station ou est le taxi.

        retourne (Station) -- Un objet Station

        - depuis - 1.6

        - auteur - Vincent Decorges
        """
        return self._station


    def __traitementStation(self):
        """
        Appeler par traiter.

        D'apres la politique redonne une station.

        - depuis - 1.4

        - auteur - Vincent Decorges
        """
        #On recupere la central pour avoir la politique
        politique = Central.Central().politique()


        self._station, self.__cheminStation = politique.choisirStation(self)

        if self._station == None:
            raise ErreurTraiter

        self._taxi.traiterEvenement(self)

    def __repr__(self):
        """
        Donne des infos sur l'�v�nement

        - depuis - 1.0

        - auteur - Vincent Decorges
        """
        return EvChargerClient.__repr__(self) + "\nclient : " + self._client.__repr__() \
        + "\nchemin station : " + str(self.__cheminStation) + "\nstation : " + str(self._station.getNo())

class EvArriverStation(EvTaxi):
    """
    A lieu quand un taxi arrive � une station.
    """


    def __init__(self, temps, taxi, station):
        """
        Constructeur.

        temps (Int) -- Le moment ou l'evenement aura lieu

        taxi (Taxi) -- Le taxi qui cree l'evenement

        station (Station) -- La station ou le taxi arrive

        retourne (EvArriverStation) -- EvArriverStation

        - depuis - 1.0

        - auteur - Vincent Decorges
        """
        EvTaxi.__init__(self, temps, taxi, self.__traitementStation)
        self._station = station


    def __traitementStation(self):
        """
        Appeler par traiter.

        Doit transmettre des infos � la station.

        - depuis - 1.0

        - auteur - Vincent Decorges
        """
        self._taxi.traiterEvenement(self)

    def __repr__(self):
        """
        Donne des infos sur l'�v�nement

        - depuis - 1.0

        - auteur - Vincent Decorges
        """
        return EvTaxi.__repr__(self) + "\nstation : " + str(self._station.getNo())


# seulement pour tester cette classe
if __name__ == '__main__':

    def traiter():
        print "OK"

    unEvenement = Evenement(10, traiter)

    print "Evenement :"
    print "Temps : " + str(unEvenement.temps())
    unEvenement.traiter()
    print "-------------------------------------"


    print "Client :"
    unClient = EvClient(19, ['D', 1, 2, 3, 4, 5, 6, 'A'])

    unClient.temps()
    print "Chemin : " + str(unClient.chemin())
    print "Temps : " + str(unClient.temps())
    print "-------------------------------------"

    temps = EvClient(1, ['2', ['c']]).temps()
    print temps

    unTaxi = Taxi(1, 1)



    unEvPoserClient = EvPoserClient(3, unTaxi, unClient)

    EvPoserClient.traiter()



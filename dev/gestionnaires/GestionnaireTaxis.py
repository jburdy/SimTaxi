#!/usr/bin/env python
"""
Module du gestionnaire des taxis.

$Id: GestionnaireTaxis.py,v 1.28 2003/02/13 19:23:48 lulutchab Exp $
"""
__version__ = '$Revision: 1.28 $'
__author__ = 'EI5a, eivd, SimTaxi (Groupe Burdy)'
__date__ = '2002-11-20'

from Singleton import Singleton
import Taxi
from Gestionnaire import Gestionnaire
from GestionnaireStations import GestionnaireStations
from GrapheXY import GrapheXY



class ErreurAucunTaxi(Exception):
    """
    Exception levée quand on cherche le taxi le plus proche et
    qu'il n'y a aucun taxi dans la liste.

    """
    pass


class ErreurAucunTaxiLibre(Exception):
    """
    Exception levée quand on demande quel est le taxi le plus
    proche et qu'il n'en reste plus aucun de libre
    """
    pass


class GestionnaireTaxis(Singleton):
    """
    Implemente un gestionnaire de Taxis.

    Cette classe fournit un gestionnaire de taxis.
    """


    def init(self):
        """
        Constructeur.

        Permet de creer un objet de la classe.

        - depuis - 1.0

        - auteur - Lucien Chaboudez
        """
        # Creation du gestionnaire
        self.__gestionnaire = Gestionnaire()



    def addTaxi(self, noStation):
        """
        Ajouter un Taxi.

        Permet d'ajouter un taxi au gestionnaire.

        noStation (int) -- Le no de la station dans laquelle le taxi se trouve.

        - depuis - 1.0

        - auteur - Lucien Chaboudez
        """
        lesStations = GestionnaireStations()

        # Recherche du no du nouveau taxi
        no = self.getNbTaxis() + 1

        # Creation du nouveau taxi
        newTaxi = Taxi.Taxi(no, noStation)

        # Ajout du taxi dans le gestionnaire
        self.__gestionnaire.addElement(no,newTaxi)

        # Ajout du taxi dans la station
        lesStations.affecterTaxi(noStation,no)


    def getNbTaxis(self):
        """
        Nombre de taxis qui sont dans le gestionnaire.

        Renvoie le nombre de taxis du gestionnaire.

        retourne (int) -- Le nombre de taxis du gestionnaire.

        - depuis - 1.0

        - auteur -
        """
        # Renvoie le nombre d'elements
        return self.__gestionnaire.nbElements





    def plusProcheDe(self, client):
        """
        (TODO : add description)

         client (EvClient) -- un evenement client.

         retourne tuple(Taxi, Chemin) -- retourne le taxi le plus
         proche ainsi que le chemin pour aller jusqu'au client.

        - depuis - 1.0

        - auteur -
        """
        #Reference sur le graphe.
        graphe = GrapheXY()

        #Récupération des stations
        listeStations = GestionnaireStations().getListeStations()

        #recherche de la position du client en prenant les 2 premiers sommets
        #du chemin qu'il faudra prendre pour le conduire a destination
        posClient = client.chemin().posDepart()

        indexStation = -1

        #Recherche d'une station contenant un taxi
        for stationCour in listeStations :

            # si il y a un taxi de libre dans la station,
            if stationCour.getNbTaxis() > 0 :

                #arc de la 1ere station
                posStation = stationCour.arc()
                #récupération du no du taxi
                taxiPlusProche = stationCour.getTaxiSuivant()
                #recherche du chemin le plus court jusqu'au taxi
                cheminLePlusCourt =  graphe.cheminPlusCourt(posStation,posClient)
                #calcul de la taille du chemin
                distancePlusCourte = cheminLePlusCourt.distTotalPos()

                #recherche de la position de la station dans la liste
                indexStation = listeStations.index(stationCour)
                break

        #Si on ne trouve pas de taxi,
        if indexStation == -1 :
            raise ErreurAucunTaxiLibre

        #suppression des stations qu'on a déjà visité,
        listeStations = listeStations[indexStation:]


        #Recherche d'une station contenant un taxi
        for stationCour in listeStations :

            # si il y a un taxi de libre dans la station,
            if stationCour.getNbTaxis() > 0 :

                #arc de la 1ere station
                posStation = stationCour.arc()

                #recherche du chemin le plus court jusqu'au taxi
                cheminCourant =  graphe.cheminPlusCourt(posStation,posClient)
                distanceCourante = cheminCourant.distTotalPos()

                # Si on trouve un chemin plus court,
                if distanceCourante < distancePlusCourte :

                    #récupération du no du taxi
                    taxiPlusProche = stationCour.getTaxiSuivant()
                    #mise à jour du chemin
                    cheminLePlusCourt = cheminCourant
                    #mise à jour de la distance
                    distancePlusCourte = distanceCourante


        #Recuperation du taxi en fonction de son numero
        taxiPlusProche = self.getTaxi(taxiPlusProche)

        return (taxiPlusProche,cheminLePlusCourt)


    def delContenu(self):
        """
        Efface les taxis.

        Vide le gestionnaire contenant les taxis.

        - depuis - 1.3

        - auteur - Lucien Chaboudez
        """

        self.__gestionnaire.delContenu()


    def getListe(self):
        """
        Renvoie une liste des taxis.

        Permet de mettre les taxis dans une liste et de la renvoyer.

        retourne (List) -- Une liste de taxis

        - depuis - 1.9

        - auteur - Lucien Chaboudez
        """

        # retour de la liste
        return self.__gestionnaire.values()


    def getTaxi(self, noTaxi):
        """
        Renvoie le taxi correspondant au no.

        Permet de renvoyer le taxi qui correspond au numero passé.

        noTaxi int -- le no du taxi
        retourne Taxi -- Le taxi

        - depuis - 1.24

        - auteur - Lucien Chaboudez
        """
        return self.__gestionnaire[str(noTaxi)]


if __name__ == '__main__' :


    from os import sep, pardir
    from GestionnairePreferences import GestionnairePreferences

    gs = GestionnaireStations()
    gt = GestionnaireTaxis()

    gp = GestionnairePreferences(pardir+sep+'config.txt')

    gs.addStation(5,('s1','s1'),('s2','s2'))

    gt.addTaxi(1)

    print gt.getTaxi(1)

    print 'Nombre de stations : ' + str(gs.getNbStations())
    print 'Nombre de taxis    : ' + str(gt.getNbTaxis())

    print 'LE TEST S\'EST DEROULE AVEC SUCCES'
#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Module du gestionnaire des stations.

$Id: GestionnaireStations.py,v 1.19 2003/01/29 16:15:17 lulutchab Exp $
"""
__version__ = '$Revision: 1.19 $'
__author__ = 'EI5a, eivd, SimTaxi (Groupe Burdy)'
__date__ = '2002-11-20'

from GrapheXY import GrapheXY
from Singleton import Singleton
from Station import Station


class ErreurEvenementIncorrect(Exception):
    """
    Exception quand on passe un §venement incorrect
    § la m§thode plusProcheDe()
    """
    pass


class ErreurAucuneStation(Exception):
    """
    Exception quand on cherche la station la + proche
    et qu'aucune station n'existe
    """
    pass


class ErreurAucuneStationAvecPlaceLibre(Exception):
    """
    Exception quand on demande la station la + proche et qu'il n'en
    reste aucune avec une place de libre
    """
    pass


class GestionnaireStations(Singleton):
    """
    Implemente un gestionnaire de stations.
    Cette classe fournit un gestionnaire de stations.
    """

    def init(self):
        """
        Constructeur.
        Permet de creer un objet de la classe.
        - depuis - 1.0
        - auteur -  Lucien Chaboudez
        """
        # Creation du gestionnaire
        self.__gestionnaire = {}

    def addStation(self, nbPlaces, sommet1, sommet2):
        """
        Ajouter une station.
        Permet d'ajouter une station dans le gestionnaire.
        nbPlaces (int) -- le nombre de places de la station
        sommet1,sommet2(tuple(nomSommet, Point)) -- les sommets entre lesquels se trouve la station
        retourne (int) -- le no de la station ajoutee
        - depuis - 1.0
        - auteur - Lucien Chaboudez
        """
        # Recherche du no de la nouvelle station
        no = self.getNbStations() + 1

        # Creation de la nouvelle station
        newStation = Station(nbPlaces, no, sommet1, sommet2)

        # Ajout de la station dans le gestionnaire
        self.__gestionnaire[no] = newStation
        return no

    def getNbStations(self):
        """
        Nombre de stations qui sont dans le gestionnaire.
        Renvoie le nombre de stations du gestionnaire.
        retourne (int) -- Le nombre de stations du gestionnaire.
        - depuis - 1.0
        - auteur - Lucien Chaboudez
        """
        # Renvoie le nombre d'elements
        return len(self.__gestionnaire)

    def plusProcheDe(self, evPoserClient):
        """
        Renvois la station la plus proche de la position.
        position (EvPoserClient) -- un §venement poser client
        retourne (tuple(Station,Chemin)) -- la station la plus proche et
        le chemin pour s'y rendre.
        - depuis - 1.0
        - auteur - Lucien Chaboudez
        """

        # Si ce n'est pas le bon §venement,
        if evPoserClient.__class__.__name__ != 'EvPoserClient':
            raise ErreurEvenementIncorrect

        # Creation d'une liste de taxis.
        listeStations = list(self.__gestionnaire.values())

        # si il n'y pas de stations,
        if len(listeStations) == 0:

            raise ErreurAucuneStation

        # Reference sur le graphe
        graphe = GrapheXY()

        # recherche de la position du taxi
        position = evPoserClient.taxi().arc()
        position = position[0]

        posStation = -1

        for stationPlusProche in listeStations:

            # si il reste des places dans la station,
            if stationPlusProche.getNbPlacesLibres() > 0:
                # enregistrement de la position de la station dans la liste
                posStation = listeStations.index(stationPlusProche)
                break

        # Si il n'y a plus de place dans aucune des stations,
        if posStation == -1:
            # on propage une exception
            raise ErreurAucuneStationAvecPlaceLibre

        # recherche de l'arc sur lequel la station se trouve
        arc = stationPlusProche.arc()

        # Recherche du chemin le plus court jusqu'a la 1ere station
        cheminLePlusCourt = graphe.cheminPlusCourt(position, arc)

        # Recherche de la taille du chemin
        distancePlusCourte = cheminLePlusCourt.dist_total_pos()

        # Suppression de la station
        listeStations = listeStations[posStation:]

        # parcour des autres taxis
        for stationCourante in listeStations:

            # si il reste des places de libre dans la station,
            if stationCourante.getNbPlacesLibres() > 0:

                # recherche de l'arc sur lequel la station se trouve
                arc = stationCourante.arc()

                # recherche du chemin le + court jusqu'a la station courante.
                cheminCourant = graphe.cheminPlusCourt(position, arc)
                distanceCourante = cheminCourant.dist_total_pos()

                # Si le chemin courant est plus court,
                if distanceCourante < distancePlusCourte:

                    # mise a jour des infos
                    distancePlusCourte = distanceCourante
                    cheminLePlusCourt = cheminCourant
                    stationPlusProche = stationCourante

        # retour de l'optimal
        return (stationPlusProche, cheminLePlusCourt)

    def getListeStations(self):
        """
        Renvoie une liste des stations.
        Permet de mettre les stations dans une liste et de la renvoyer.
        retourne (List) -- Une liste de stations
        - depuis - 1.2
        - auteur - Lucien Chaboudez
        """
        # retour de la liste
        return list(self.__gestionnaire.values())

    def affecterTaxi(self, noStation, noTaxi):
        """
        Affecte un taxi a la station dont le no est passe.
        Permet d'affecter un taxi a la station dont le no est passe. Sera
        appelee a l'initialisation du programme.
        noStation (int) -- le no de la station a laquelle le taxi est affecte.
        noTaxi (int) -- Le no du taxi a ajouter
        - depuis - 1.2
        - auteur - Lucien Chaboudez
        """
        # Ajout du taxi a la station
        self.__gestionnaire[noStation].affecterTaxi(noTaxi)

    def delContenu(self):
        """
        Efface les stations.
        Vide le gestionnaire contenant les stations.
        - depuis - 1.3
        - auteur - Lucien Chaboudez
        """
        self.__gestionnaire.delContenu()

    def getPosition(self, noStation):
        """
        Donne la position d'une station.
        Permet de connaitre la position de la station, dont le no est passe,
        sur le graphe en fonction des informations contenues dans les sommets.
        noStation (int) : le no de la station dont on desire la position.
        retourne (Tuple(Tuple(float,float),Tuple(float,float)) --
        un tuple contenant 2 tuples.
        1 avec la position (x,y) et le 2e avec vecteur d'orientation.
        - depuis - 1.4
        - auteur - Lucien Chaboudez
        """
        # appelle de la fonction getPosition de la station correspondante.
        return self.__gestionnaire[str(noStation)].getPosition()

    def arc(self, noStation):
        """
        renvoie l'arc sur lequel la station se trouve.
        Permet de connaitre l'arc sur laquelle la station se trouve.
        noStation (int) -- le no de la station dont on veut l'arc
        retourne (Tuple(Sommet, Sommet)) -- un tuple contenant les sommets
        entre lesquels la station se trouve.
        - depuis - 1.4
        - auteur - Lucien Chaboudez
        """

        # appel de la fonction arc de la station correspondante
        return self.__gestionnaire[str(noStation)].arc()

    def getNbPlacesLibres(self, noStation):
        """
        renvoie le nb de places libres dans la station.
        Permet de connaitre le nombre de places qui sont libres dans la station
        dont le no est pass§.
        noStation (int) -- le no de la station dont on veut le nombre de places libres.
        retourne (int) -- le nombre de places libres.
        - depuis - 1.7
        - auteur - Lucien Chaboudez
        """

        # appel de la fonction getNbPlacesLibres de la station correspondante
        return self.__gestionnaire[noStation].getNbPlacesLibres()

    def getStation(self, noStation):
        """
        renvoie la station correspondant au no.
        Permet d'avoir acc§s § la station dont le no est pass§ en param§tre.
        noStation (int) -- le no de la station.
        retourne (int) -- la station.
        - depuis - 1.17
        - auteur - Lucien Chaboudez
        """
        # retour de la station
        return self.__gestionnaire[noStation]


if __name__ == '__main__':

    gs = GestionnaireStations()

    gs.addStation(10, 's1', 's2')
    gs.addStation(5, 's5', 's21')
    gs.affecterTaxi(1, 5)

    l = gs.getListeStations()

    for s in l:

        print(s.getNbPlacesLibres())

    print('LE TEST S\'EST DEROULE AVEC SUCCES')

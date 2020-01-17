#!/usr/bin/env python
"""
Module contenant le classe Station.

$Id: Station.py,v 1.15 2003/02/13 16:17:44 lulutchab Exp $
"""
__version__ = '$Revision: 1.15 $'
__author__ = 'EI5A, eivd, SimTaxi (Groupe Burdy)'
__date__ = '2002-11-20'


class ErreurReservation(Exception):
    """
    Exception quand on veut réserver une place qui n'existe pas.

    """
    pass


class ErreurTaxisInconnu(Exception):
    """
    Exception quand un taxi désire quitter une station dans laquelle
    il ne se trouve pas.
    """

    pass

class ErreurSommetsIdentiques(Exception):
    """
    Exception quand on crée une station avec 2 sommets identiques
    """

    pass


class ErreurStationVide(Exception):
    """
    Exception quand on demande le 1er taxi de la liste que celle-ci
    est vide
    """
    pass


class Station :
    """
    Implemente une station.

    Cette classe fournit une station de taxis et des methodes permettant
    de la gerer.
    """


    def __init__(self, nbPlaces, no, sommet1, sommet2):
        """
        Constructeur.

        Permet de creer un objet de la classe.

        nbPlaces (int) -- Le nombre de places de la station

        no (int) -- Le no de la station

        sommet1, sommet2 (tuple(nomSommet, Point)) -- Les sommets entre lesquels est la station

        - depuis - 1.0

        - auteur - Lucien Chaboudez
        """

        # Si les 2 sommets sont identiques
        if sommet1[0] == sommet2[0] :
            raise ErreurSommetsIdentiques

        # Initialisations
        self.__no = no
        self.__nbPlacesTot = nbPlaces
        self.__nbPlacesLibres = nbPlaces
        self.__nbPlacesReservees = 0
        self.__listeTaxis = []
        self.__sommetAvant = sommet1
        self.__sommetApres = sommet2


    def reserverPlace(self):
        """
        Reserver une place dans la station.

        Permet de reserver une place dans la station. Si il ne reste plus de
        places, on propage une Exception.

        - depuis - 1.0

        - auteur - Lucien Chaboudez
        """
        # Si il n'y a plus de places,
        if self.__nbPlacesLibres == 0 :
            # On propage une exception
            raise ErreurReservation

        # Une reservation de plus
        self.__nbPlacesReservees += 1
        self.__nbPlacesLibres -= 1


    def quitterPlace(self, noTaxi):
        """
        Quitter une place.

        Permet de liberer une place dans la station. Le no du taxi qui part
        est passe en parametre. Si le taxi n'est pas dans la station, une
        Exception est propagee.

        noTaxi (int) -- le no du taxi qui quitte la station

        - depuis - 1.0

        - auteur - Lucien Chaboudez
        """
        # Si le taxi n'est pas dans la liste,
        if self.__listeTaxis.count(noTaxi) == 0 :

            # On propage une exception
            raise ErreurTaxisInconnu

        # Suppression dans la liste de taxis
        self.__listeTaxis.remove(noTaxi)

        #Une place de libre en plus
        self.__nbPlacesLibres += 1


    def annulerReservation(self):
        """
        Annuler une reservation anterieure.

        Permet d'annuler une reservation faite plus tôt. Si aucune reservation
        n'existe, une exception est propagee.

        - depuis - 1.0

        - auteur - Lucien Chaboudez
        """
        # Si aucune reservation
        if self.__nbPlacesReservees == 0 :

            # On propage une exception
            raise erreurAnnulationReservation


        # Une reservation de moins
        self.__nbPlacesReservees -= 1
        self.__nbPlacesLibres += 1


    def getNbPlacesTot(self):
        """
        Renvoie le nombre de places de la station.

        Permet de connaitre le nombre de places totales de la station.

        retourne (int) -- le nombre de places

        - depuis - 1.0

        - auteur - Lucien Chaboudez
        """
        return self.__nbPlacesTot


    def getNbPlacesLibres(self):
        """
        Renvoie le nombre de places libres de la station.

        Permet de connaitre le nombre de places libres de la station.

        retourne (int) -- le nombre de places libres

        - depuis - 1.0

        - auteur - Lucien Chaboudez
        """
        return self.__nbPlacesLibres


    def getPosition(self):
        """
        Renvoie la position de la station.

        Permet de connaitre la position de la station sur le graphe en
        fonction des informations contenues dans les sommets.

        retourne (tuple(tuple(float,float),tuple(float,float))) -- un tuple contenant 2 tuples.
                        1 avec la position (x,y)  et le 2e avec
                        vecteur d'orientation.

        - depuis - 1.0

        - auteur - Lucien Chaboudez
        """

        # Calcul des positions x et y de la station
        x = self.__sommetAvant[1].getX() + \
           (self.__sommetApres[1].getX() - self.__sommetAvant[1].getX()) / 2.0
        y = self.__sommetAvant[1].getY() + \
           (self.__sommetApres[1].getY() - self.__sommetAvant[1].getY()) / 2.0

        # Calcul du vecteur d'orientation
        vectX = self.__sommetApres[1].getX() - self.__sommetAvant[1].getX()
        vectY = self.__sommetApres[1].getY() - self.__sommetAvant[1].getY()

        # retour de la position
        return ( (x, y), (vectX, vectY) )


    def prendPlace(self, noTaxi):
        """
        Pour dire qu'un taxi prend place dans la station.

        Est appelee quand un taxi prend place dans la station. Si aucune place
        n'a ete reservee, une exception est levee.

        noTaxi (int) -- Le no du taxi qui prend place dans la station

        - depuis - 1.0

        - auteur - Lucien Chaboudez
        """
        # Si aucune place n'est reservee,
        if self.__nbPlacesReservees == 0 :

            # On propage une exception
            raise erreurReservationManquante

        # Une place de moins dans la station
        self.__nbPlacesReservees -= 1
        self.__listeTaxis.append(noTaxi)


    def getNo(self):
        """
        Renvoie le no de la station.

        Permet de connaitre le no qui a ete attribue a la station.

        retourne (int) -- Le no attribué

        - depuis - 1.2

        - auteur - Lucien Chaboudez
        """
        # Retour du no
        return self.__no


    def affecterTaxi(self, noTaxi):
        """
        affecte un taxi a la station.

        Permet d'affecter un taxi a la station. Sera appelee a
        l'initialisation du programme.

        noTaxi (int) -- Le no du taxi a ajouter

        - depuis - 1.2

        - auteur - Lucien Chaboudez
        """
        # Si il n'y a plus de place libre,
        if self.__nbPlacesLibres == 0 :

            raise erreurAffectationImpossible

        # Modification de l'etat
        self.__nbPlacesLibres -=1
        self.__listeTaxis.append(noTaxi)


    def arc(self):
        """
        renvoie l'arc sur lequel la station se trouve.

        Permet de connaitre l'arc sur laquelle la station se trouve.

        retourne (tuple(NomSommet,NomSommet)) -- un tuple contenant les sommets entre lesquels la
                               station se trouve.
        - depuis - 1.3

        - auteur - Lucien Chaboudez
        """
        return (self.__sommetAvant[0],self.__sommetApres[0])


    def getNbTaxis(self):
        """
        renvoie le nombre de taxi.

        Permet de connaitre le nombre de taxis qui sont dans la station.

        retourne (int) -- le nombre de taxis.
        - depuis - 1.14

        - auteur - Lucien Chaboudez
        """

        return len(self.__listeTaxis)


    def getTaxiSuivant(self):
        """
        renvoie le no du 1er taxi de la liste.

        Permet de connaitre le no du taxi qui est en tête de la liste.

        retourne (int) -- le no du taxi.
        - depuis - 1.14

        - auteur - Lucien Chaboudez
        """
        # Si il n'y a pas de taxis,
        if len(self.__listeTaxis) == 0:
            raise ErreurStationVide

        #retour du taxi
        return self.__listeTaxis[0]


if __name__ == '__main__' :

    S = Station(10,1,'s1','s2')

    print 'Nb places libres : ' + str(S.getNbPlacesLibres())
    print 'Nb Places Tot    : ' + str(S.getNbPlacesTot())

    print '\nReservation de 1 place '
    S.reserverPlace()

    print '\nNb places libres : ' + str(S.getNbPlacesLibres())
    print 'Nb Places Tot    : ' + str(S.getNbPlacesTot() )

    print '\nAnnulation de la reservation'
    S.annulerReservation()

    print '\nNb places libres : ' + str(S.getNbPlacesLibres())
    print 'Nb Places Tot    : ' + str(S.getNbPlacesTot() )

    print '\nNo de station : ' + str(S.getNo())

    print '\nLE TEST S\'EST DEROULE AVEC SUCCES'
#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Module contenant la classe du central.

$Id: Central.py,v 1.17 2003/01/26 10:30:53 vega01 Exp $
"""
__version__ = '$Revision: 1.17 $'
__author__ = 'EI5A, eivd, SimTaxi (Groupe Burdy)'
__date__ = '2002-12-01'


# pour les tests

from Echeancier import Echeancier
from Evenement import EvArriverStation, Evenement
from GestionnaireStations import GestionnaireStations
from GestionnaireTaxis import GestionnaireTaxis
from PolitiquePlusPres import PolitiquePlusPres
from Singleton import Singleton


def fonc_comp(evenement1, evenement2):
    """
    Fonction de comparaison des evenements pour l'echeancier.
    evenement1, evenement2 (Evenement) -- les evenements a comparer
    retourne (Integer) --  0 si les evenements ont lieu en meme temps egaux
                           1 si le premier evenement a lieu apres le deuxieme
                           -1 sinon
    - depuis - 1.0
    - auteur - Alexandre D'Amico
    """

    return evenement1.temps() < evenement2.temps()


class Central(Singleton):
    """
    Implemente le central.
    Cette classe fournit un central qui traite les evenements de l'echeancier.
    """

    def init(self, politique=PolitiquePlusPres()):
        """
        Constructeur.
        Permet de cr§er un objet de la classe Central.
        - depuis - 1.0
        - auteur - Alexandre D'Amico
        """
        # INITIALISATIONS

        # initialisation de l'echeancier avec sa fonction de comparaison
        self._echeancier = Echeancier(fonc_comp)

        # creation des gestionnaires
        self._gestionnaireTaxis = GestionnaireTaxis()
        self._gestionnaireStations = GestionnaireStations()

        # creation de la politique
        self._politique = politique

    def initEv(self, liste_ev):
        """
        Initialise l'echeancier avec des evenements.
        listeEv (Liste) -- les evenements pour initialiser l'echeancier
        - depuis - 1.0
        - auteur - Alexandre D'Amico
        """
        self._echeancier.initEcheancier(liste_ev)

    def ajouterEvenement(self, evenement):
        """
        Ajoute un evenement dans l'echeancier du Central.
        evenement (Evenement) -- l'evenement a inserer dans l'echeancier
        - depuis - 1.0
        - auteur - Alexandre D'Amico
        """
        self._echeancier.deposer(evenement)

    def traiterProchainEvenement(self):
        """
        Supprimer le premier element de l'echeancier et le traiter en
        fonction de son type. Puis le retourne.
        retourne (Evenement) -- L'événement qui a §t§ trait§.
        - depuis - 1.0
        - auteur - Alexandre D'Amico
        """
        # utiliser la methode traiter propre a chaque evenement
        ev = self._echeancier.prelever()
        ev.traiter()
        return ev

    def modifierPolitique(self, politique):
        """
        Modifie la politique de traitement des evenements.
        Modifie la politique pour le choix du taxi en fonction de la 
        position d'un client et le choix d'une station en fonction de la
        position du taxi.
        politique (Politique) -- la nouvelle politique de traitement des
                                 evenements
        - depuis - 1.1
        - auteur - Alexandre D'Amico
        """
        self._politique = politique

    def politique(self):
        """
        Retourne la politique actuelle de traitement des evenements.
        retourne (Politique) -- la politique actuelle
        - depuis - 1.5
        - auteur - Alexandre D'Amico
        """
        return self._politique

    def supprimerEvArriverStation(self, taxi):
        """
        Supprime l'evenement de l'arrivee d'un taxi en station.
        taxi (Taxi) : le taxi qui devait arriver en station
        - depuis - 1.5
        - auteur - Alexandre D'Amico
        """
        for i in self._echeancier:
            # recherche de l'evenement a supprimer
            if (i.__self__.__class__ == EvArriverStation and i.taxi() == taxi):
                # c'est un evenemet d'arrivee en station et il concerne ce taxi
                self._echeancier.remove(i)  # supression de l'evenement
                # annulation de la reservation du taxi
                i.station().annulerReservation()
                break

    def evenement(self):
        """
        Permet de savoir s'il y a encore au moins un evenement.
        retourne (Bool) -- Vrai s'il y a au moins un element
        - depuis - 1.1
        - auteur - Alexandre D'Amico
        """
        return not self._echeancier.vide()

    def intervalleProchainEvement(self, mnt=0):
        """
        Retourne le temps auquel aura lieu le prochain evenement.
        mnt (Temps) -- Le temps actuel.
        retourne (Temps) -- L'intervalle de temps entre mnt et le prochain evenement.
        - depuis - 1.16
        - auteur - Julien Burdy
        """
        return self._echeancier.tempsProchainEv() - mnt


if __name__ == '__main__':

    a = 0

    central = Central()
    central.init()

    def traiter():
        global a
        a = a + 1
        print(a)

    unEvenement1 = Evenement(10, traiter)
    unEvenement2 = Evenement(20, traiter)
    unEvenement3 = Evenement(15, traiter)

    central.ajouterEvenement(unEvenement1)
    central.ajouterEvenement(unEvenement2)
    central.ajouterEvenement(unEvenement3)

    central.traiterProchainEvenement()
    central.traiterProchainEvenement()
    central.traiterProchainEvenement()
    central.traiterProchainEvenement()

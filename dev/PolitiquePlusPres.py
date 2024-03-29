#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Module contenant la politique du plus pr§s.

$Id: PolitiquePlusPres.py,v 1.5 2003/01/26 10:37:55 vega01 Exp $
"""
__version__ = '$Revision: 1.5 $'
__author__ = 'EI5a, eivd, SimTaxi (Groupe Burdy)'
__date__ = '2002-12-22'

from GestionnaireStations import GestionnaireStations
from GestionnaireTaxis import GestionnaireTaxis
from Politique import Politique


class PolitiquePlusPres (Politique):
    """
    Implémante la politique du taxi le plus près et de
    la station la plus proche.
    """

    def choisirTaxi(self, client):
        """
        Retourne un taxi pour prendre en charge un client d'après la politique courante.
        client (EvClient) -- Le client qui veut faire la course
        retourne (Tuple(Taxi, Chemin)) -- Le taxi qui va prendre en charge la course
        - depuis - 1.0
        - auteur - Vincent Decorges
        """
        return GestionnaireTaxis().plusProcheDe(client)

    def choisirStation(self, taxi):
        """
        Retourne une station d'après la politique courante.
        taxi (EvTaxi) -- Le taxi qui va § une station
        retourne (Tuple(Station, Chemin)) -- La station et
        - depuis - 1.0
        - auteur - Vincent Decorges
        """
        return GestionnaireStations().plusProcheDe(taxi)

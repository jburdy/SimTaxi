#!/usr/bin/env python
"""
Module contenant la classe abstraite des politiques.

$Id: Politique.py,v 1.3 2003/01/11 11:32:00 vega01 Exp $
"""
__version__ = '$Revision: 1.3 $'
__author__ = 'EI5A, eivd, SimTaxi (Groupe Burdy)'
__date__ = '2002-12-22'



class ErreurAbstraite(Exception):
    """
    Exception pour les classes abstraites.
    """
    pass

    

class Politique:

    """
    Classe abstraite pour l'implémentation des politiques.
    """
    

    def choisirTaxi(self, client):
        """
        Retourne un taxi pour prendre en charge un client 
        d'après la politique courante.

        client (EvClient) -- Le client qui veut faire la course

        retourne (Tuple(Taxi, Chemin)) -- Le taxi qui va prendre en charge la course

        - depuis - 1.0

        - auteur - Vincent Decorges
        """
        raise ErreurAbstraite


    def choisirStation(self, taxi):
        """
        Retourne une station d'après la politique courante.

        taxi (EvTaxi) -- Le taxi qui va à une station

        retourne (Station, Chemin) -- La station

        - depuis - 1.0

        - auteur - Vincent Decorges
        """
        raise ErreurAbstraite
        
    




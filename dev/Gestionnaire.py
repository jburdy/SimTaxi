#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Module de base des gestionnaires.

$Id: Gestionnaire.py,v 1.7 2003/01/07 19:31:28 lulutchab Exp $
"""
__version__ = '$Revision: 1.7 $'
__author__ = 'EI5A, eivd, SimTaxi (Groupe Burdy)'
__date__ = '2002-11-20'


class Gestionnaire(dict):
    """
    Implemente un gestionnaire.

    Cette classe derive de dictionnaire et fournit un gestionnaire
    d'elements.
    """

    def __init__(self):
        """
        Constructeur.

        Permet de creer un objet de la classe.

        - depuis - 1.0

        - auteur - Lucien Chaboudez
        """
        self.nbElements = 0
        self = {}

    def addElement(self, no, element):
        """
        Ajoute un element au gestionnaire.

        Permet d'ajouter a un element dans le gestionnaire.

        no (int) -- Le no de l'element

        element -- L'element a ajouter

        retourne (int) -- le no de l'§l§ment qui a §t§ ajout§

        - depuis - 1.0

        - auteur - Lucien Chaboudez
        """
        self.nbElements += 1
        # Ajout de l'element
        self.update({str(no): element})

        return no

    def delContenu(self):
        """
        Efface le contenu du gestionnaire.

        Vide le gestionnaire et reinitialise les donnees membres.

        - depuis - 1.3

        - auteur - Lucien Chaboudez
        """
        self = {}
        self.nbElements = 0


if __name__ == "__main__":

    gest = Gestionnaire()
    dic = {}

    gest.addElement(1, 'salut')

    for i in gest:

        print(i + ' - ' + gest.get(i))

    print(gest)

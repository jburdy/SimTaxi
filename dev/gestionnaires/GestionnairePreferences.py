#!/usr/bin/python2
# -*- coding: utf-8 -*-
""" 
Module du gestionnaire de pr§f§rences. 

$Id: GestionnairePreferences.py,v 1.5 2003/01/11 12:22:46 erreur Exp $
"""
__version__ = '$Revision: 1.5 $'
__author__ = 'EI5a, eivd, SimTaxi (Groupe Burdy)'
__date__ = '2002-12-09'

import Singleton
from os import sep, curdir



class GestionnairePreferences(Singleton.Singleton):
    """
    Gestionnaire de preferences.

    Ce gestionnaire contient les valeurs de configuration importees
    d'un fichier. Une option se distinge par son nom et sa valeur.

    Le format du fichier doit etre::

      ==============================
      # ceci est un commentaire
      nbMax : 500
      nomDuFichierY : 'fichier.y' # un autre commentaire
      ==============================
    """
    

    def init(self, nomFichier=''):
        """
        Creation du gestionnaire (Singleton).

        nomFichier (String) -- Le nom du fichier de config

        retourne (GestionnairePreferences) -- le gestionnaire

        - depuis - 1.0

        - auteur - Julien Burdy
        """
        self.__dico = {}
        # importation du fichier
        if nomFichier != '': self.importer(nomFichier)


    def importer(self, nomFichier):
        """
        Importe les preferences depuis le fichier.

        La suppression des valeurs superflue est automatique (tab, espaces,...)

        nomFichier (String) -- Le nom du fichier d'importation

        - depuis - 1.0

        - auteur - Julien Burdy
        """
        # recuperation des lignes du fichier
        try: contenu = file(nomFichier).readlines()
        except: raise nomFichier

        # suppression des commentaires
        contenu = map(lambda x: x.split('#')[0], contenu)
        # suppression des tab, des fin de lignes et des espaces
        contenu = map(lambda x: x.replace('\n', '').replace('\t', '')\
                                                   .replace(' ', ''), contenu)
        # suppression des lignes vides
        contenu = filter(lambda x: len(x)>0, contenu)
        # separation du nom des options de leurs valeurs
        contenu = map(lambda x: x.split(':'), contenu)
        # ajout des options dans le dictionnaire
        map(lambda x: self.__dico.update({x[0]:eval(x[1])}), contenu)


    
    def valeurDe(self, option):
        """
        Revois la valeur d'une option.

        option (String) -- l'option dont on veut la valeur

        returne -- la valeur (exception si elle n'existe pas)

        - depuis - 1.0

        - auteur - Julien Burdy
        """
        try: return self.__dico[option]
        except: raise "option non definie"
        

    
    def optionDefinie(self, option):
        """
        Revois si une option est definie ou non.

        option (String) -- l'option en question

        returne -- 0 si elle ne l'est pas

        - depuis - 1.0

        - auteur - Julien Burdy
        """
        return self.__dico.has_key(option)


    
    def mettreAJour(self, option, nouvelValeur):
        """
        Mise a jour de la valeur d'une option.

        Creation de l'option si elle n'existe pas.

        option (String) -- l'option a mettre a jour

        nouvelValeur -- la valeur a mettre a jour

        - depuis - 1.0

        - auteur - Julien Burdy
        """
        self.__dico.update({option:nouvelValeur})
        

    
    def ajouterOption(self, option, valeur):
        """
        Ajoute une option au gestionnaire.

        Actuelement ceci est un alias de mettreAJour()

        option (String) -- l'option a ajouter

        valeur -- sa valeur

        - depuis - 1.0

        - auteur - Julien Burdy
        """
        self.mettreAJour(option, valeur)
        


    def listeOptions(self):
        """
        Retourne la liste des options presente dans le gestionnaire.

        returne (List) -- La liste des options

        - depuis - 1.0

        - auteur - Julien Burdy
        """
        return self.__dico.keys()



# seulement pour tester cette classe
if __name__ == '__main__':
    
    print "Creation importation fichier"
    maConf = GestionnairePreferences('../config.txt')
    print "Listing du fichier"
    for i in maConf.listeOptions():
        t = maConf.valeurDe(i)
        print i
        print type(t), '\t' , t
        print

    try: maConf.valeurDe('rien')
    except: print 'test exception "option non definie" OK'
    print "Ajout d'une nouvelle option"
    maConf.ajouterOption('newOption', 999)
    print "Consultation de cette option"
    assert maConf.valeurDe('newOption')==999, 'erreur ajout/consult'
    print "Mise a jour de cette option"
    maConf.mettreAJour('newOption', 777)
    print "Consultation de cette option"
    assert maConf.valeurDe('newOption')==777, 'erreur mise a jour/consult'
    print "Tout est OK..."



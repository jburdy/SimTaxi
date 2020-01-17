#!/usr/bin/env python
"""
Lancement de SimTaxi (multiOS) après divers contrôles.

- contrôle des dépendances

- création de l'environement approprié

$Id: startSimTaxi.pyw,v 1.9 2003/02/06 16:33:31 erreur Exp $
"""


# disctionnaire des lib dont nous sommes dépendant
dependance = {'OpenGL':'http://pyopengl.sourceforge.net',
              #'Numeric':'http://www.pfdubois.com/numpy',
              'wxPython':'http://www.wxpython.org'}


# msg d'avertissement pour les librairies manquantes.
avertissement = """************************
Attention: impossible de lancer l'execution.
SimTaxi ne peut pas acceder aux librairies Python suivantes:"""


def fixerPYTHONPATH():
    """
    Fixe la varibable d'environement.

    Cette variable d'environement est obligatoire pour pouvoir accèder à nos
    module contenu dans les paquetage de SimTaxi.

    - depuis - 1.1

    - auteur - Julien Burdy
    """
    from os import listdir,curdir #, sep, pathsep, , putenv, getenv
    from os.path import abspath, isdir
    from sys import path
    map( lambda x: path.insert(0, abspath(x)), filter(lambda x: isdir(x), listdir(curdir)))


def dependanceOK(dicoDep, avertissement):
    """
    Contrôle que les librairies dont nous avons besoin sont disponnible.

    Si au moins une librairie est absente, un message d'avertissement s'affiche
    puis les librairies manquantes sont listée, avec leurs URL.

    dicoDep (dict) -- le dico contenant les librairies et leurs URL

    avertissement (string) -- le msg d'avertissement
    
    retourne (bool) -- faux s'il manque au moins une librairie

    - depuis - 1.4

    - auteur - Julien Burdy
    """
    depOK = True

    for i in dicoDep:
        try: exec('import ' + i) # essaye d'importer la lib
        except:
            # affiche ce qu'il manque
            if depOK: print avertissement
            print i, dicoDep[i]
            depOK = False
    return depOK


# main
if dependanceOK(dependance, avertissement):
    fixerPYTHONPATH()
    #import SimTaxiGUI # provisoire, lancement de l'ancien affichage
    import SimTaxi
    SimTaxi.main()
else: raw_input()





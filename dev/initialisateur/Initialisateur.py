#!/usr/bin/env python
"""
Module d'initialisation.

$Id: Initialisateur.py,v 1.15 2003/02/09 10:05:04 erreur Exp $
"""
__version__ = '$Revision: 1.15 $'
__author__ = 'EI5a, eivd, SimTaxi (Groupe Burdy)'
__date__ = '2002-12-04'

from GrapheXY import *
from GestionnaireTaxis import *
from Evenement import EvClient
from Chemin import *
from random import *

class Initialisateur:
    """
    Initialisations de SimTaxi.

    Cette classe permet de generer les courses des clients et d'initialiser
    les taxis en les positionnant dans une station.
    """


    def __init__(self):
        """
        Constructeur.

        Permet de créer un objet de la classe.

        - depuis - 1.0

        - auteur - Patrice Ferrot
        """
        # Les courses qui vont etre generees, sous forme de
        # liste d'evenements clients.
        self.__courses = []
        # Le graphe de travail.
        #self.__graphe = GrapheXY('graphe.gr')
        self.__graphe = GrapheXY()

    def genererCourses(self, nbCourses, heurePremiereCourse,
                       heureDerniereCourse, distanceMoyenne = 0, germe = None):
        """
        Generateur de courses.

        Genere la totalite des courses qui seront effectuees.

        nbCourses -- le nombre de courses a generer

        heurePremiereCourse -- l'heure du premier appel d'un client

        heureDerniereCourse -- l'heure du dernier appel d'un client

        distanceMoyenne -- la distance moyenne des courses, 0 pour
                           des distances quelconques

        germe -- le germe utilise pour les generations aleatoires. Si pas
                 de germe specifie, se base sur l'heure actuelle.

        retourne (List) -- les courses generees, liste d'evenements clients.

        - depuis - 1.0

        - auteur - Patrice Ferrot
        """
        # Si pas de course a generer.
        if (nbCourses <= 0):
            return self.__courses

        # Le generateur de nombre aleatoires.
        generateur = Random()
        # La distance moyenne des courses.
        moyenneTemp = 0
        # Avoir tous les sommets du graphe.
        listeSommets = self.__graphe.listeSommets()
        # Le nombre de sommets du graphe.
        nbSommets =  len(listeSommets)
        # Les courses.
        coursesTemp = []

        # Utiliser le germe desire.
        generateur.seed(germe)

        # Le nombre de courses crees.
        i = 0
        # Le nombre de passage dans la boucle.
        j = 0
        # Pour generer le bon nombre de courses.
        #for i in range(nbCourses):
        while i < nbCourses:
            # Choisir le premier sommet de depart aleatoirement.
            #print listeSommets
            sommetDepart1 = listeSommets[int(self.__nbAleatoire(generateur) *
                            nbSommets)]
            # Choisir l'autre sommet de depart aleatoirement dans la
            # liste des sommets voisins.
            listeSommetsVus = self.__graphe.sommetsVus(sommetDepart1)
            sommetDepart2 = listeSommetsVus[int(self.__nbAleatoire(generateur) *
                            len(listeSommetsVus))]

            # Pour ne pas faire un trajet nul, supprimer les deux sommets
            # de depart.
            listeSommets.remove(sommetDepart1)
            listeSommets.remove(sommetDepart2)
            nbSommets = nbSommets - 2
            # Choisir le premier sommet d'arrivee aleatoirement.
            sommetArrivee1 = listeSommets[int(self.__nbAleatoire(generateur) *
                             nbSommets)]
            # Choisir l'autre sommet d'arrivee aleatoirement dans la liste des
            # sommets voisins.
            listeSommetsVus = self.__graphe.sommetsVus(sommetArrivee1)
            sommetArrivee2 = listeSommetsVus[int(
                             self.__nbAleatoire(generateur)*
                             len(listeSommetsVus))]
            # Remettre les sommets qui avaient ete ecartes.
            listeSommets.append(sommetDepart1)
            listeSommets.append(sommetDepart2)
            nbSommets = nbSommets + 2

            # Trajet pour effectuer la course.
            cheminCourse = self.__graphe.cheminPlusCourt(
                           (sommetDepart1, sommetDepart2),
                           (sommetArrivee1, sommetArrivee2))
            coursesTemp.append((cheminCourse,))
            distanceCourse = coursesTemp[i][0].distTotalPos()

            # S'il faut supprimer cette derniere course pour adapter
            # la moyenne.
            if not (distanceMoyenne == 0) and (
               (i > (nbCourses/3) and j < (10*nbCourses)) and (
               ((moyenneTemp > distanceMoyenne) and
                (distanceCourse > distanceMoyenne)) or
               ((moyenneTemp < distanceMoyenne) and
                (distanceCourse < distanceMoyenne))
               )) :
                # La supprimer.
                coursesTemp.remove(coursesTemp[i])
            # Sinon, on garde cette course.
            else:
                # Mise a jour de la moyenne.
                moyenneTemp = ((moyenneTemp*(i)) + distanceCourse) / (i+1)
                # Generation des heures des courses.
                if (i == 0):
                    coursesTemp[i] = (heurePremiereCourse,) + coursesTemp[i]
                elif (i == 1):
                    coursesTemp[i] = (heureDerniereCourse,) + coursesTemp[i]
                else:
                    heure = (int(self.__nbAleatoire(generateur) *
                            (heureDerniereCourse-heurePremiereCourse)) +
                            heurePremiereCourse)
                    coursesTemp[i] = (heure,) + coursesTemp[i]

                # Une course de plus.
                i = i + 1

            # Un passage de plus dans la boucle.
            j = j + 1

        # Trier les courese selon leur ordre chronologique.
        coursesTemp.sort()

        # Affiche la moyenne des distances des courses et les courses.
        #print coursesTemp
        #print "Moyenne des distances des courses : ", moyenneTemp

        # Creer une liste d'evenements clients.
        while len(coursesTemp) > 0:
            pseudoChemin = (coursesTemp[0][1].posDepart(),coursesTemp[0][1].posArrivee())
            self.__courses.append(EvClient(coursesTemp[0][0],
                                  pseudoChemin))
            coursesTemp.remove(coursesTemp[0])

        # Retourner la liste d'evenements clients.
        return self.__courses


    def genererStations(self, nbStations, nbPlaces, germe = None):
        """
        Initialise les stations.

        Place le nombre voulu de stations dans le graphe.

        nbStations -- le nombre de taxis a placer.

        nbPlaces -- liste indiquant le nombre de place que doivent contenir
                    les stations. Si moins d'elements dans la liste que de
                    stations, utilise le dernier pour toutes les suivantes,
                    si plus d'elements dans la liste, ne tient pas compte
                    des supplementaires.

        germe -- le germe utilise pour les generations aleatoires. Si pas
                 de germe specifie, se base sur l'heure actuelle.

        - depuis - 1.5
        - auteur - Patrice Ferrot
        """
        # Si pas de station a creer.
        if nbStations < 1:
            return

        # Le generateur de nombre aleatoires.
        generateur = Random()
        # Utiliser le germe desire.
        generateur.seed(germe)

        # Avoir tous les sommets du graphe.
        listeSommets = self.__graphe.listeSommets()
        # Le nombre de sommets du graphe.
        nbSommets =  len(listeSommets)
        # Le gestionnaire de stations.
        gestStations = GestionnaireStations()
        # La liste des sommets supprimes.
        listeSommetsSupprimes = []

        # Creer le nombre de stations voulues.
        for i in range(nbStations):
            # Le bon nombre de places pour cette station.
            if i < len(nbPlaces):
                places = nbPlaces[i]
            # Choisir le premier sommet de la station.
            sommet1 = listeSommets[int(self.__nbAleatoire(generateur) *
                      nbSommets)]

            """
            print "Liste sommets :  ", listeSommets
            print "Liste sommets supprimes : ", listeSommetsSupprimes
            """

            # La liste des sommets voisins.
            listeSommetsVus = self.__graphe.sommetsVus(sommet1)

            """
            print "Liste sommets vus avant : ", listeSommetsVus
            """

            # Supprimer les sommets deja utilises pour une
            # station, si possible.
            for j in range(len(listeSommetsSupprimes)):
                if len(listeSommetsVus) > 1:
                    try:
                        listeSommetsVus.remove(listeSommetsSupprimes[j])
                    except:
                        pass

            """
            print "Liste sommets vus apres : ", listeSommetsVus
            """

            # Choisir le deuxieme sommet de la station.
            sommet2 = listeSommetsVus[int(self.__nbAleatoire(generateur) *
                      len(listeSommetsVus))]

            """
            print "Sommet1 : ", sommet1
            print "Sommet2 : ", sommet2
            print
            """

            # Pour ne pas placer deux stations au meme endroit.
            # Les tests assurent qu'il n'y aie pas d'erreur, mais possibilité
            # de plusieurs stations au meme endroit...
            if len(listeSommets) > 1:
                listeSommets.remove(sommet1)
                nbSommets = nbSommets - 1
                listeSommetsSupprimes.append(sommet1)
            if len(listeSommets) > 1:
                try:
                    listeSommets.remove(sommet2)
                    nbSommets = nbSommets - 1
                    listeSommetsSupprimes.append(sommet2)
                except:
                    pass

            # Ajouter la station.
            gestStations.addStation(places, \
             (sommet1,self.__graphe.attributsSommet(sommet1)), \
             (sommet2,self.__graphe.attributsSommet(sommet2)) )


    def initialiserTaxis(self, nbTaxis, germe = None):
        """
        Initialise les taxis.

        Place le nombre voulu de taxis dans les stations.

        nbTaxis -- le nombre de taxis a placer.

        germe -- le germe utilise pour les generations aleatoires. Si pas
                 de germe specifie, se base sur l'heure actuelle.

        - depuis - 1.0
        - auteur - Patrice Ferrot
        """

        # Si pas de taxi a placer.
        if nbTaxis < 1:
            return

        # Le generateur de nombre aleatoires.
        generateur = Random()
        # Utiliser le germe desire.
        generateur.seed(germe)

        # Le gestionnaire utilise.
        gestStations = GestionnaireStations()
        # Les taxis
        gestTaxis = GestionnaireTaxis()

        # Le nombre de stations et leur liste.
        nbStations = gestStations.getNbStations()
        listeStations = range(1, nbStations + 1)

        # Pour tous les taxis demandes.
        for i in range(nbTaxis):
            # Si plus de place, sortir.
            if nbStations == 0:
                break
            # Choisir la station ou placer le taxi.
            noStation =  listeStations[int(self.__nbAleatoire(generateur) *
                         nbStations)]
            # Placer le taxi.
            #gestStations.affecterTaxi(noStation, i)
            gestTaxis.addTaxi(noStation)
            # Si la station est pleine, la supprimer des stations possibles.
            if gestStations.getNbPlacesLibres(noStation) == 0:
                listeStations.remove(noStation)
                nbStations = nbStations - 1


    def __nbAleatoire(self, gene):
        """
        Generateur aleatoire.

        Retourne un nombre aleatoire de l'intervalle [0,1[.

        gene -- le generateur utilise.

        retourne (Float) -- le nombre aleatoire genere.

        - depuis - 1.0

        - auteur - Patrice Ferrot
        """

        nb = gene.random()
        if nb == 1.0:
           nb = nb - 0.01
        return nb

if __name__ == "__main__" :
    #from os import sep, pardir
    #graphe = GrapheXY('graphe.gr')

    test = Initialisateur()

    test.genererCourses(20, 0, 60, 8000)

    test.genererStations(3, [20, 10, 5])

    test.initialiserTaxis(20)


#!/usr/bin/python2
# -*- coding: utf-8 -*-
"""
Module contenant la classe GrapheXY.

$Id: GrapheXY.py,v 1.24 2003/02/20 02:00:40 leyonel Exp $
"""
__version__ = '$Revision: 1.24 $'
__author__ = 'EI5a, eivd, SimTaxi (Groupe Burdy)'
__date__ = '2002-11-10'


from Graphe import *
from Point import *
from QueuePriorite import *
from Chemin import *
from random import *

# les exceptions
erreurTypePoint = "l'attribut du sommet n'est pas un objet Point"
fichierChemins = 'dumpChemins'

class GrapheXY(Graphe):
    """
    Graphe oriente et pondere (pondere par des attributs).

    Les sommets et les arcs ont des attributs de n'importe quel type.
    """

    def init(self, fichierImport = None):
        """
        Cette methode sert a creer un graphe.

        On peut importer un graphe a partir d'un fichier donne.

        fichierImport (String) -- Le nom du fichier a importer

        retourne (Graphe) -- Un objet Graphe

        - depuis - 1.0

        - auteur - Lionel Gu§lat
        """
        # constructeur parent
        Graphe.init(self, fichierImport)
        
        import pickle
        try:
            print 'Chargement des chemins d§j§ calcul§s...'
            self.__chemins = pickle.load(file(fichierChemins))
            self.__nbCheminsLoad = len(self.__chemins)
            print self.__nbCheminsLoad, 'arbres existants.'
        except : 
            self.__nbCheminsLoad = 0
            self.__chemins = {} # pour stoquer les chemins calcul§s de chaque sommet


    def dump(self):
        """
        Dump (sauvegarde apr§s transformation) de la structure contenant
        les arbres de chemins les plus courts. Le dump est fait uniquement
        s'il y a de nouveaux arbres.

        Le fichier (%s) est sous forme binaire.

        - depuis - 1.20

        - auteur - Julien Burdy
        """ % fichierChemins
        import pickle
        if self.__nbCheminsLoad < len(self.__chemins):
            print 'Dump des chemins (%d nouveaux arbres)' % (len(self.__chemins) - self.__nbCheminsLoad)
            pickle.dump(self.__chemins, file(fichierChemins,'w'), True)
            self.__nbCheminsLoad = len(self.__chemins)
            print 'Dump OK'


    def insererSommet(self, nomSommet, point):
        """
        Cette methode permet d'inserer un sommet avec son point.

        Exception levee si le point n'est pas un objet Point.

        nomSommet -- Le nom du sommet

        Point point -- Le point du sommet

        - depuis - 1.2

        - auteur - Joel Jaquemet
        """
        # controle du type Point
        try: point.getX()
        except: raise erreurTypePoint

        # inserer le sommet avec son point
        Graphe.insererSommet(self, nomSommet, point.copy())


    def insererArc(self, sommetDep, sommetArr):
        """
        Cette methode permet d'inserer un arc dont on calcule sa longueur.

        Exception levee si les sommets ne sont pas definis dans le graphe ou
        si l'arc est deja defini.

        sommetDep -- Le nom du sommet de depart de l'arc

        sommetArr -- Le nom du sommet d'arrivee de l'arc

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        # insertion de l'arc avec sa longueur calculee
        Graphe.insererArc(self, sommetDep, sommetArr,
                          self.attributsSommet(sommetDep).
                          distance(self.attributsSommet(sommetArr)))


    
    def remplacerAttributsSommet(self, sommet, point):
        """
        Cette methode permet de modifier le point d'un sommet.

        On recalcule la logueur des arcs relies au sommet.
        Exception levee si le point n'est pas un objet Point.

        sommet -- Le nom du sommet

        point (Point) -- Le nouveau point du sommet

        - depuis - 1.2

        - auteur - Joel Jaquemet
        """
        # controle du type Point
        try: point.getX()
        except: raise erreurTypePoint

        # modifier le point du sommet
        Graphe.remplacerAttributsSommet(self, sommet, point.copy())
        # mettre a jour les nouvelles longueurs des arcs sortants
        for s in self.sommetsVus(sommet):
            self.remplacerAttributsArc(sommet, s,
                                       self.attributsSommet(sommet).
                                       distance(self.attributsSommet(s)))
        # mettre a jour les nouvelles longueurs des arcs entrants
        for s in self.sommetsVoyants(sommet):
            self.remplacerAttributsArc(s, sommet,
                                       self.attributsSommet(sommet).
                                       distance(self.attributsSommet(s)))



    def cheminPlusCourt(self, arcDepart, arcFin):
        """
        Algo du chemin le plus court

        arcDepart -- Arc de d§part (tuple de sommets)

        arcFin -- Arc de fin (tuple de sommets)

        retourne (Chemin) -- Le chemin le plus court

        - depuis - 1.5

        - auteur - Lionel Guelat
        """
        infini = 999999999999999

        # retourne le chemin le plus court
        # sans tenir compte des arc bidirectionnels pour le depart et la fin
        def CPC(arcDepart, arcFin):

            # cas trivial
            if arcDepart[1] == arcFin[0]:
              return Chemin([arcDepart[0], arcDepart[1], arcFin[1]] \
                     , [0, self.attributsArc(arcDepart[0], arcDepart[1]) \
                       , self.attributsArc(arcDepart[1], arcFin[1])])

            # les deux sommets § relier
            depart = arcDepart[1]
            fin = arcFin[0]

            # ATTENTION si des arcs ont §t§ supprim§s du graphe!!

            # voir si ce sommet de d§part a d§j§ §t§ demand§
            if depart in self.__chemins.keys():

                # r§cup§rer les §l§ments calcul§s pr§c§demment
                parents = self.__chemins[depart][0]
                priorites = self.__chemins[depart][1]

            # sinon chercher le chemin demand§
            else:

                # liste des sommets visit§s
                visites = {}

                # liste des priorit§s
                priorites = {}

                for sommet in self.listeSommets():
                    # marquer tous les sommets comme non visites
                    visites[sommet] = False;
                    # initialiser les priorit§s
                    priorites[sommet] = infini

                # liste des sommets parents
                parents = {}
                parents[depart] = arcDepart[0]

                # pour le tri de la liste (compare les distances)
                def comp(a, b):
                    return priorites[a] < priorites[b]

                # la liste des sommets tri§s par priorit§
                liste = QueuePriorite(comp)

                # recherche le chemin depuis la fin
                priorites[depart] = self.attributsArc(arcDepart[0], arcDepart[1])
                liste.deposer(depart)
                # tant que la liste contient des sommets
                while not liste.vide():
                    # retirer le sommet prioritaire
                    extrait = liste.prelever()
                    # marquer le sommet comme visite
                    visites[extrait] = True
                    # pour tous les voisins non visites
                    for voisin in self.sommetsVus(extrait):
                        if not visites[voisin]:
                            # voir s'il est mieux de passer par extrait
                            if self.attributsArc(extrait, voisin) + priorites[extrait] < priorites[voisin]:
                                # modifier la priorit§
                                priorites[voisin] = self.attributsArc(extrait, voisin) + priorites[extrait]
                                # enregistrer le sommet qui permet de l'atteindre
                                parents[voisin] = extrait
                                # ajouter § la liste
                                liste.deposer(voisin)

                # stoquer l'arbre des chemins de ce sommet
                self.__chemins[depart] = (parents, priorites)

            # verifier si le chemin d§sir§ existe
            if not fin in parents.keys():
               raise Exception, 'Pas de chemin entre ces deux sommets'

            # construire le chemin
            sommetsChemin = []
            distancesChemin = []
            sommet = fin
            sommetsChemin.insert(0, sommet)
            distancesChemin.insert(0, priorites[sommet])
            while not parents[sommet] == depart:
                  sommet = parents[sommet]
                  sommetsChemin.insert(0, sommet)
                  distancesChemin.insert(0, priorites[sommet])
            sommetsChemin.insert(0, depart)
            distancesChemin.insert(0, priorites[depart])

            # ajouter les deux sommets des extremites
            sommetsChemin.insert(0, arcDepart[0])
            distancesChemin.insert(0, 0)
            sommetsChemin.append(arcFin[1])
            distancesChemin.append(priorites[fin] \
                + self.attributsArc(arcFin[0], arcFin[1]) )

            return Chemin(sommetsChemin, distancesChemin)



        ##################################################
        # recherche la meilleure des quatre possibilit§s

        a = CPC((arcDepart[0], arcDepart[1]), (arcFin[0], arcFin[1]))
        d = a.distTotalSommets()

        if self.arcDefini(arcDepart[1], arcDepart[0]):
            b = CPC((arcDepart[1], arcDepart[0]), (arcFin[0], arcFin[1]))
            if b.distTotalSommets() < d:
                a = b
                d = a.distTotalSommets()

        if self.arcDefini(arcFin[1], arcFin[0]):
            b = CPC((arcDepart[0], arcDepart[1]), (arcFin[1], arcFin[0]))
            if b.distTotalSommets() < d:
               a = b
               d = a.distTotalSommets()

            if self.arcDefini(arcDepart[1], arcDepart[0]):
                b = CPC((arcDepart[1], arcDepart[0]), (arcFin[1], arcFin[0]))
                if b.distTotalSommets() < d:
                     a = b

        return a


    def genererGraphe(self, nbSommets, nbArcs, distanceMax, germe = None):
        """
        Cette methode permet de generer un graphe.

        Exception levee si le graphe ne peut pas etre connexe.

        nbSommets (Int) -- Le nombre de sommets

        nbArcs (Int) -- Le nombre d'arcs

        distanceMax (Float) -- La distance maximale entre 2 sommets

        germe (Int) -- Le germe de la fonction aleatoire

        - depuis - 1.8

        - auteur - Joel Jaquemet
        """
        # controle des parametres
        if nbSommets < 8: raise Exception, 'Nombre de sommets trop petit: ' + `nbSommets`
        if distanceMax <= 0: raise Exception, 'Distance max. invalide: ' + `distanceMax`

        # calculer le nb de lignes (et de colonnes)
        nbLignes = int(nbSommets**0.5)
        if nbLignes**2 < nbSommets: nbLignes = nbLignes + 1

        # controle du nombre d'arcs donn§
        if 2 * (nbSommets - 1) > nbArcs:
            raise Exception, "Nombre d'arcs trop petit: " + `nbArcs`
        if nbArcs > -4 * (nbLignes**2 + nbLignes -  2 * nbSommets):
            raise Exception, "Nombre d'arcs trop grand: " + `nbArcs`

        # initialisation de la fonction aleatoire
        rand = Random(germe)

        # vider le graphe
        Graphe.initialiser(self)

        # palcement des sommets de maniere optimale dans l'espace disponible

        # calculer la longueur des cotes du graphe
        longCote = (2**0.5 * distanceMax) / 2.0

        # calculer l'espace minimum entre les sommets
        distanceMin = (longCote / (nbLignes - 1)) / 20.0

        # calculer l'espace dans lequelle peut se trouver un sommet
        espaceSommet = (longCote - (nbLignes - 1) * distanceMin) / nbLignes

        # placement des sommets
        sommetCourant = 1  # numero du sommet courant
        coord = Point() # coordonnees du sommets courant

        yTemp = 0
        while yTemp < longCote:
            xTemp = 0
            while xTemp < longCote:
                coord.setXY(xTemp + rand.randrange(int(espaceSommet) + 1),\
                            yTemp + rand.randrange(int(espaceSommet) + 1))
                self.insererSommet(sommetCourant, coord)
                sommetCourant = sommetCourant + 1
                xTemp = xTemp + espaceSommet + distanceMin
            yTemp = yTemp + espaceSommet + distanceMin

        # pour connaitre les sommets qui peuvent etre lies avec celui donne
        def liaisonsPossibles(sommet):
            # liste des liaisons possibles
            sommetsProches = []
            sommetsProches.append(sommetCourant - nbLignes)
            sommetsProches.append(sommetCourant + nbLignes)
            if sommetCourant % nbLignes != 1:
                sommetsProches.append(sommetCourant - 1)
            if sommetCourant % nbLignes != 0:
                sommetsProches.append(sommetCourant + 1)

            # retirer les arcs impossibles
            sommetsProchesTemp = []
            # copie de la liste
            for sommetArr in sommetsProches:
                sommetsProchesTemp.append(sommetArr)

            # enlever les sommets inexistants ou deja lies
            for sommetArr in sommetsProchesTemp:
                if not self.sommetDefini(sommetArr):
                    sommetsProches.remove(sommetArr)
                elif self.arcDefini(sommetCourant, sommetArr):
                    sommetsProches.remove(sommetArr)

            return sommetsProches

        # generer la connexite du graphe
        sommetsNonRelies = self.listeSommets()
        chemin = []

        # choisir un sommet de depart
        sommetCourant = sommetsNonRelies[rand.randrange(len(sommetsNonRelies))]
        # le sommet courant va etre relie
        sommetsNonRelies.remove(sommetCourant)
        chemin.append(sommetCourant)

        while len(sommetsNonRelies) > 0:
            # liste des liaisons possibles
            listeSommets = liaisonsPossibles(sommetCourant)

            # retirer les sommets deja visites
            listeSommetsTemp = []
            for sommetSuivant in listeSommets: # copie de la liste
                listeSommetsTemp.append(sommetSuivant)

            for sommetSuivant in listeSommetsTemp:
                if not sommetSuivant in sommetsNonRelies:
                    listeSommets.remove(sommetSuivant)

            if len(listeSommets) > 0:
            # on peut continuer => choisir le sommet suivant
                sommetSuivant = listeSommets[rand.randrange(len(listeSommets))]
                # insertion des 2 arcs
                self.insererArc(sommetCourant, sommetSuivant)
                self.insererArc(sommetSuivant, sommetCourant)
                # le sommet suivant a ete relie
                sommetsNonRelies.remove(sommetSuivant)
                chemin.append(sommetSuivant)
                # passer au sommet suivant
                sommetCourant = sommetSuivant

            else:
            # cul de sac => revenire en arriere
                chemin.remove(sommetCourant)
                sommetCourant = chemin[len(chemin) - 1]

        # reduction du nombre de sommets
        while self.nbSommets() > nbSommets:
            # choisir un sommet a supprimer
            sommetCourant = self.listeSommets()[rand.randrange(len(self.listeSommets()))]

            # pour conserver les liaisons des sommets
            for voyant in self.sommetsVoyants(sommetCourant):
                for vu in self.sommetsVus(sommetCourant):
                    if voyant != vu:
                        if not self.arcDefini(voyant, vu):
                            self.insererArc(voyant, vu)

            # suppression du sommet
            self.supprimerSommet(sommetCourant)

        # augmentation du nombre d'arcs
        while self.nbArcs() < nbArcs:
            # choisir un sommet de depart de l'arc
            sommetCourant = self.listeSommets()[rand.randrange(len(self.listeSommets()))]

            # liste des liaisons possibles
            listeSommets = liaisonsPossibles(sommetCourant)

            # garde fou pour eviter d'essayer d'ajouter un arc alors qu'on ne peu plus
            if len(listeSommets) > 0:
                # insertion d'un arc
                self.insererArc(sommetCourant, listeSommets[rand.randrange(len(listeSommets))])



# seulement pour tester cette classe
if __name__ == '__main__':

    a = GrapheXY()
    p = Point(15)
    try: a.insererSommet('a')
    except: print 'OK'
    try: a.insererSommet('a', (15.0,16))
    except: print erreurTypePoint
    a.insererSommet('a', p)
    p.setXY(2, -3)
    a.insererSommet('b', p)
    p.setXY(5, 4)
    a.insererSommet('c', p)
    a.insererArc('a', 'c')
    a.insererArc('b', 'c')
    print a.listeArcs(1)

    a.inverserTousArcs()
    print a.listeArcs(1)
    print a.attributsArc('b', 'c')
    p.setXY(3.21, 12.4)
    a.remplacerAttributsSommet('a', p)
    print a.listeArcs(1)
    print a.attributsSommet('a').getX()
    a.remplacerAttributsArc('a', 'c', 6)
    print a.attributsArc('a', 'c')
    print a.attributsArc('c', 'a')

    print 'OK'

    print ''
    print 'CHEMINS:'

    a.init()
    p = Point(0.0, 0.0)

    p.setXY(-6.0, 0.0)
    a.insererSommet('<', p)
    p.setXY(-3.0, 0.0)
    a.insererSommet('s', p)
    p.setXY(0.0, 0.0)
    a.insererSommet('a', p)
    p.setXY(0.0, 2.0)
    a.insererSommet('b', p)
    p.setXY(0.0, 4.0)
    a.insererSommet('c', p)
    p.setXY(0.0, 6.0)
    a.insererSommet('d', p)
    p.setXY(3.0, 3.0)
    a.insererSommet('z', p)
    p.setXY(6.0, 3.0)
    a.insererSommet('>', p)
    a.insererArc('<', 's')
    a.insererArc('s', 'a')
    a.insererArc('s', 'b')
    a.insererArc('s', 'c')
    a.insererArc('s', 'd')
    a.insererArc('a', 'z')
    a.insererArc('b', 'z')
    a.insererArc('c', 'z')
    a.insererArc('d', 'z')
    a.insererArc('z', '>')
    print a.listeArcs()

    chemin = a.cheminPlusCourt(('<', 's'), ('z', '>'))
    print chemin.listeSommets()
    print chemin.distTotalSommets()
    print chemin.distTotalPos()
    try:
        a.cheminPlusCourt(('a', 's'), ('<', 'a'))
    except Exception:
        print 'pas de chemin: OK\n'

    # generation du graphe
    a.genererGraphe(15, 35, 12000, 59)
    a.exporter('graphe_test.gr')

    print 'Generation OK\n'

    # recuperation du graphe
    a.importer('graphe_test.gr')
    a.afficher()

    print 'nb sommets: '
    print a.nbSommets()
    print a.nbArcs()

    print 'Recuperation OK\n'

    # constructeur
    c = GrapheXY('graphe_text.gr')
    c.afficher()

    print 'nb sommets: '
    print c.nbSommets()
    print c.nbArcs()

    print 'Constructeur OK\n'



#!/usr/bin/python2
# -*- coding: utf-8 -*-
"""
Module contenant la classe Graphe.

$Id: Graphe.py,v 1.11 2003/01/25 19:01:28 erreur Exp $
"""
__version__ = '$Revision: 1.11 $'
__author__ = 'EI5a, eivd, SimTaxi (Groupe Burdy)'
__date__ = '2002-11-01'

from Singleton import *



class Graphe(Singleton):
    """
    Graphe oriente et pondere (pondere par des attributs).
    
    Les sommets et les arcs ont des attributs de n'importe quel type.
    Attentio, cette classe est un singleton, c'est-a-dire qu'un seule objet
    peut etre cree. Les suivants pointent sur le premier.
    """


    def init(self, fichierImport = None):
        """
        Cette methode sert a creer un graphe.

        On peut importer un graphe a partir d'un fichier donne.

        fichierImport (String) -- Le nom du fichier a importer

        retourne (Graphe) -- Un objet Graphe

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        # le dico representant le graphe
        self.__dico = {}
        # importation du fichier s'il y en a un
        if fichierImport != None: self.importer(fichierImport)


    def initialiser(self):
        """
        Cette methode permet d'initialiser le graphe.

        - depuis - 1.9

        - auteur - Joel Jaquemet
        """
        # effacer le graphe
        self.__dico.clear()

            
    
    def importer(self, fichierImport):
        """
        Cette methode permet d'importer un graphe depuis un fichier.

        Le fichier a du etre cree avec la methode "exporter" auparavant pour
        que le type soit compatible. De plus, le graphe actuel sera ecrase.

        fichierImport (String) -- Le nom du fichier d'importation

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        import pickle
        
        try:
            fichier = open(fichierImport, 'r') # ouvrir le fichier
        except:
            # le fichier n'a pas pu etre ouvert
            raise Exception, fichierImport
        else:
            self.initialiser() # pour effacer le graphe actuel
            # mettre a jour le graphe avec celui du fichier
            self.__dico.update(pickle.load(fichier))
            fichier.close()


    
    def exporter(self, fichierExport):
        """
        Cette methode permet d'exporter un graphe vers un fichier.

        fichierExport (String) -- Le nom du fichier d'exportation

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        import pickle
        
        try:
            fichier = open(fichierExport, 'w') # creer le fichier
        except:
            # le fichier n'a pas pu etre creer
            raise Exception, fichierExport
        else:
            # enregistrer le graphe dans le fichier
            pickle.dump(self.__dico, fichier)
            fichier.close()


    
    def insererSommet(self, nomSommet, attributsSommet = None):
        """
        Cette methode permet d'inserer un sommet avec ses attributs.

        Exception levee si le sommet est deja defini dans le graphe.

        nomSommet -- Le nom du sommet

        attributsSommet -- Les attributs du sommet

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        # controle du sommet donne
        if self.sommetDefini(nomSommet):
            raise Exception, 'sommet deja defini : ' + `nomSommet`

        # inserer le sommet (on met a jour le dico qui represente le graphe)
        self.__dico.update({nomSommet: [attributsSommet, {}]})


    
    def insererArc(self, sommetDep, sommetArr, attributsArc = None):
        """
        Cette methode permet d'inserer un arc avec ses attributs.

        Exception levee si les sommets ne sont pas definis dans le graphe ou
        si l'arc est deja defini.

        sommetDep -- Le nom du sommet de depart de l'arc

        sommetArr -- Le nom du sommet d'arrivee de l'arc

        attributsArc -- Les attributs de l'arc

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        # controle que l'arc ne soit pas deja defini
        if self.arcDefini(sommetDep, sommetArr):
            raise Exception, 'arc deja defini'

        # inserer l'arc (on met a jour le dico du sommet de depart)
        self.__dico[sommetDep][1].update({sommetArr: attributsArc})


    
    def supprimerSommet(self, sommet):
        """
        Cette methode permet de supprimer un sommet.

        Les arcs relies au sommet sont aussi supprimes.
        Exception levee si le sommet n'est pas defini dans le graphe.

        sommet -- Le nom du sommet

        - depuis - 1.3

        - auteur - Joel Jaquemet
        """
        # controle du sommet donne
        if not self.sommetDefini(sommet):
            raise Exception, 'sommet indefini : ' + `sommet`

        # supprimer les arcs arrivant au sommet
        for arc in self.listeArcs():
            if arc[1] == sommet: self.supprimerArc(arc[0], arc[1])
        # supprimer les arcs partant du sommet et le sommet
        del self.__dico[sommet]


    
    def supprimerArc(self, sommetDep, sommetArr):
        """
        Cette methode permet de supprimer un arc.

        Exception levee si les sommets ou l'arc ne sont pas definis dans le
        graphe.

        sommetDep -- Le nom du sommet de depart de l'arc

        sommetArr -- Le nom du sommet d'arrivee de l'arc

        - depuis - 1.3

        - auteur - Joel Jaquemet
        """
        # controle que l'arc soit deja defini
        if not self.arcDefini(sommetDep, sommetArr):
            raise Exception, 'arc indefini'

        # supprimer l'arc (on met a jour le dico du sommet de depart)
        del self.__dico[sommetDep][1][sommetArr]


    
    def remplacerAttributsSommet(self, sommet, attributsSommet):
        """
        Cette methode permet de modifier les attributs d'un sommet.

        Exception levee si le sommet n'est pas defini dans le graphe.

        sommet -- Le nom du sommet

        attributsSommet -- Les nouveaux attributs du sommet

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        # controle du sommet donne
        if not self.sommetDefini(sommet):
            raise Exception, 'sommet indefini : ' + `sommet`

        # mettre les nouveaux attributs du sommet
        self.__dico[sommet][0] = attributsSommet


    
    def remplacerAttributsArc(self, sommetDep, sommetArr, attributsArc):
        """
        Cette methode permet de modifier les attributs d'un arc.

        Exception levee si les sommets ou l'arc ne sont pas definis dans le
        graphe.

        sommetDep -- Le nom du sommet de depart de l'arc

        sommetArr -- Le nom du sommet d'arrivee de l'arc

        attributsArc -- Les nouveaux attributs de l'arc

        - depuis - 1.2

        - auteur - Joel Jaquemet
        """
        # controle que l'arc soit deja defini
        if not self.arcDefini(sommetDep, sommetArr):
            raise Exception, 'arc indefini'

        # mettre les nouveaux attributs de l'arc
        self.__dico[sommetDep][1][sommetArr] = attributsArc


    
    def inverserTousArcs(self):
        """
        Cette methode permet d'ajouter tous les arcs de sens contraire a ceux
        deja definis dans le graphe.

        Les nouveaux arcs ont les memes attributs que ceux de sens oppose.
        Exception levee si un arcs a deja un semblable de sens contraire.

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        sauve = self.__dico.copy() # pour restituer le graphe en cas d'erreur
        
        # parcourir chaque arc et inserer celui de sens contraire
        try:
            for a in self.listeArcs(1): self.insererArc(a[1], a[0], a[2])

        except TypeError: # erreur => essayer avec la methode de la classe
            self.__dico.clear()
            self.__dico.update(sauve)
            for a in self.listeArcs(1):
                Graphe.insererArc(self, a[1], a[0], a[2])
            
        except: # erreur => restituer le graphe
            self.__dico.clear()
            self.__dico.update(sauve)
            raise


    
    def attributsSommet(self, sommet):
        """
        Cette methode permet de connaitre les attributs d'un sommet.

        Exception levee si le sommet n'est pas defini dans le graphe.

        sommet -- Le nom du sommet

        retourne -- Les attributs du sommet donne

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        # controle du sommet donne
#        if not self.sommetDefini(sommet):
#            raise Exception, 'sommet indefini : ' + `sommet`
        
        # retourner les attributs du sommet donne
        return self.__dico[sommet][0]


    
    def attributsArc(self, sommetDep, sommetArr):
        """
        Cette methode permet de connaitre les attributs d'un arc.

        Exception levee si les sommets ou l'arc ne sont pas definis dans le
        graphe.

        sommetDep -- Le nom du sommet de depart de l'arc

        sommetArr -- Le nom du sommet d'arrivee de l'arc

        retourne -- : Les attributs de l'arc donne

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        # controle de l'arc donne
#        if not self.arcDefini(sommetDep, sommetArr):
#            raise Exception, 'arc indefini'

        # retourner les attributs de l'arc donne
        return self.__dico[sommetDep][1][sommetArr]


    
    def nbSommets(self):
        """
        Cette methode donne le nombre de sommets du graphe.

        retourne (Int) -- Le nombre de sommets du graphe

        - depuis - 1.2

        - auteur - Joel Jaquemet
        """
        # retourner le nombre d'entrees du dico
        return len(self.__dico)

    
    
    def nbArcs(self):
        """
        Cette methode donne le nombre d'arcs du graphe.

        retourne (Int) -- Le nombre d'arcs du graphe

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        nbArcs = 0
        # parcourir et compter chaque arc
        for i in self.__dico: nbArcs += len(self.__dico[i][1])
        return nbArcs


    
    def listeSommets(self, attributs = 0):
        """
        Cette methode donne la liste contenant tous les sommets du graphe
        avec leurs attributs si on le souhaite.

        Par defaut (attributs = faux), la liste contient uniquement le nom
        des sommets et pas leurs attributs.
        Si attributs = vrai, la liste contiendra des tuples (1 par sommet)
        qui contiendront (dans l'ordre) le nom du sommet et ses attributs.
        L'ordre des sommets est identique a celui de l'insertion de ces
        derniers.

        attributs (Boolean) -- Les sommets avec leurs attributs ou pas

        retourne (List) -- La liste des sommets du graphe

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        if attributs: # retourner la liste des sommets avec attributs
            liste = []
            # parcourir chaque sommet et l'ajouter a la liste
            for sommet in self.__dico:
                liste.append((sommet, self.__dico[sommet][0]))
            return liste
        
        else: # retourner la liste des sommets sans attributs
            return self.__dico.keys()


    
    def listeArcs(self, attributs = 0):
        """
        Cette methode donne la liste contenant tous les arcs du graphe.

        La liste contient des tuples (1 par arc) qui contiennent (dans
        l'ordre) les noms de ces sommets de depart et d'arrivee et ses
        attributs.
        Par defaut, les attributs ne sont pas mis dans les tuples des arcs.

        attributs (Boolean) -- Les arcs avec leurs attributs ou pas

        retourne (List) -- La liste des arcs du graphe

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        liste = []
        # parcourir chaque arc et l'ajouter a la liste
        for sommetDep in self.__dico:
            for sommetArr in self.__dico[sommetDep][1]:
                if attributs: # liste des arcs avec attributs
                    liste.append((sommetDep, sommetArr,
                                  self.__dico[sommetDep][1][sommetArr]))
                else: # liste des arcs sans attributs
                    liste.append((sommetDep, sommetArr))
        return liste


    
    def sommetsVus(self, sommet):
        """
        Cette methode donne une liste des sommets vus par le sommet donne.

        Exception levee si le sommet n'est pas defini dans le graphe.

        sommet -- Le nom du sommet

        retourne -- Liste : Liste des sommets vus par le sommet donne

        - depuis - 1.5

        - auteur - Joel Jaquemet
        """
        # controle du sommet donne
        if not self.sommetDefini(sommet):
            raise Exception, 'sommet indefini : ' + `sommet`

        # la liste des voisins vus depuis le sommet
        return self.__dico[sommet][1].keys()


    
    def sommetsVoyants(self, sommet):
        """
        Cette methode donne une liste des sommets qui voient le sommet donne.

        Exception levee si le sommet n'est pas defini dans le graphe.

        sommet -- Le nom du sommet

        retourne (List) -- Liste des sommets qui voient le sommet donne

        - depuis - 1.5

        - auteur - Joel Jaquemet
        """
        # controle du sommet donne
        if not self.sommetDefini(sommet):
            raise Exception, 'sommet indefini : ' + `sommet`

        # la liste des sommets qui voient le sommet donne
        voyants = []
        for arc in self.listeArcs():
            if arc[1] == sommet: voyants.append(arc[0])
        return voyants


    
    def sommetDefini(self, sommet):
        """
        Cette methode permet de savoir si un sommet est defini ou pas.

        sommet -- Le nom du sommet

        retourne (Boolean) -- Indique si le sommet est defini ou pas

        - depuis - 1.2

        - auteur - Joel Jaquemet
        """
        # retourner si le sommet est defini ou pas
        return self.__dico.has_key(sommet)

        
    
    def arcDefini(self, sommetDep, sommetArr):
        """
        Cette methode permet de savoir si un arc est defini ou pas.

        Exception levee si les sommets ne sont pas definis dans le graphe.

        sommetDep -- Le nom du sommet de depart de l'arc

        sommetArr -- Le nom du sommet d'arrivee de l'arc

        retourne (Boolean) -- Indique si l'arc est defini ou pas

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        # controle des sommets donnes
        if not self.sommetDefini(sommetDep):
            raise Exception, 'sommet indefini : ' + `sommetDep`
        if not self.sommetDefini(sommetArr):
            raise Exception, 'sommet indefini : ' + `sommetArr`

        # retourner si l'arc est defini ou pas
        return self.__dico[sommetDep][1].has_key(sommetArr)

        
    
    def afficher(self):
        """
        Cette methode permet d'afficher un graphe (en String).

        Cette methode est utile uniquement pour le deboguage.

        - depuis - 1.0

        - auteur - Joel Jaquemet
        """
        # parcourir et afficher chaque structure des sommets du graphe
        liste = self.__dico.items()
        liste.sort()
        for i in liste: print i


# seulement pour tester cette classe
if __name__ == '__main__':

    g = Graphe()
    g.insererSommet('a', 'Test')
    g.insererSommet('t')
    g.insererSommet('c',(32,3))
    g.insererSommet('b',(2,5.5))
    g.insererArc('c', 'a', 15.3)
    g.insererArc('b', 'c', 13)
    g.inverserTousArcs()
    g.afficher()
    print g.attributsArc('a','c')
    print g.nbArcs()
    print g.nbSommets()
    print g.listeSommets(4)
    print g.listeArcs()
    print g.sommetDefini('k');
    g.exporter('test.txt')
    print g.sommetsVus('a')
    print g.sommetsVoyants('c')
    g.supprimerSommet('a')
    g.afficher()
    print 'OK'

    a = Graphe('test.txt')
    a.afficher()
    try: a.remplacerAttributsSommet('a', ('er',15))
    except Exception: print 'OK'
    print a.attributsSommet('b')
    print a.attributsSommet('t')
    a.remplacerAttributsArc('c', 'b', 'Salut')
    print a.attributsArc('c', 'b')
    print 'OK'

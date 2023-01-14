#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Module contenant le classe Taxi.

$Id: Taxi.py,v 1.34 2003/02/28 10:53:55 lulutchab Exp $
"""
__version__ = '$Revision: 1.34 $'
__author__ = 'EI5A, eivd, SimTaxi (Groupe Burdy)'
__date__ = '2002-11-20'


from GestionnairePreferences import GestionnairePreferences
from GestionnaireStations import GestionnaireStations
from GrapheXY import GrapheXY

D = 0  # Debug


class ErreurEvenementIncorrect(Exception):
    """
    Exception pour les §venements incorrects
    """
    pass


class ErreurHeureIncorrecte(Exception):
    """
    Exception quand une heure incorrecte est pass§e
    """
    pass


class Taxi:
    """
    Implemente un taxi

    Cette classe fournit un taxi et des methodes permettant
    de le gerer.
    """

    def __init__(self, noTaxi, noStation):
        """
        Constructeur.

        Permet de creer un objet de la classe.

        noTaxi (int)-- le no du taxi

        noStation (int)-- le no de la station ou le taxi se trouve

        - depuis - 1.0

        - auteur - Lucien Chaboudez
        """
        # reference sur le graphe
        self.__graphe = GrapheXY()

        # le gestionnaire de preferences.
        gestPref = GestionnairePreferences()

        # Initialisations
        self.__vitesse = gestPref.valeurDe('vitesseTaxiKMH')
        self.__evenementCourant = None
        self.__no = noTaxi
        self.__noStation = noStation
        self.__cheminCourant = None
        self.__heureFinEvenement = None
        self.__etat = 'arrete'
        self.__mParcourus = 0.0
        self.__nbCoursesEffectuees = 0
        self.__distTrajet = 0.0

    def getPosition(self, heure):
        """
        Renvoie la position du taxi.

        Permet de connaitre la position (x,y) du taxi et son vecteur de
        direction.

        heure (int) -- l'heure courante

        retourne (tuple(tuple(float,float),tuple(float,float))) --
        un tuple contenant 2 tuples. Le 1er donne la position
        (x,y) du taxi et le 2e le vecteur de direction.

        - depuis - 1.0

        - auteur - Lucien Chaboudez
        """
        # si le taxi roule,
        if self.estEnDeplacement():

            # Si l'heure passee est incorrecte,
            if self.__heureFinEvenement != None and \
                    heure > self.__heureFinEvenement:
                # on propage une exception
                raise Exception(ErreurHeureIncorrecte)

            # recherche de l'arc sur lequel le taxi se trouve
            ((sommet1, sommet2), distanceParcourueSurArc) = self.arc(heure)

            if D:
                if distanceParcourueSurArc > self.__cheminCourant.distEntreSommets(sommet1, sommet2):
                    print("Sommets : ", sommet1, sommet2)
                    print("Dist entre sommets : ", self.__cheminCourant.distEntreSommets(sommet1, sommet2))
                    print("Dist parcourue sur arc : ", distanceParcourueSurArc)
                    raise "Erreur Distance Incorrecte"

            # Enregistrement des coordonn§es des sommets
            som1X = self.__graphe.attributsSommet(sommet1).getX()
            som1Y = self.__graphe.attributsSommet(sommet1).getY()
            som2X = self.__graphe.attributsSommet(sommet2).getX()
            som2Y = self.__graphe.attributsSommet(sommet2).getY()

            # vecteur de direction
            vectX = som2X - som1X
            vectY = som2Y - som1Y

            # longueur de l'arc sur lequel le taxi se trouve.
            longArc = self.__cheminCourant.distEntreSommets(sommet1, sommet2)
            # longArc = sqrt( pow(vectX,2) + pow(vectY,2))

            # calcul du vecteur de direction unitaire.
            vectX = vectX * (1.0 / longArc)
            vectY = vectY * (1.0 / longArc)

            # calcul de la position sur l'arc.
            posX = som1X + (distanceParcourueSurArc * vectX)
            posY = som1Y + (distanceParcourueSurArc * vectY)

            if D:

                if ((posX < som1X) and (posX < som2X)) or \
                   ((posX > som1X) and (posX > som2X)) or \
                   ((posY < som1Y) and (posY < som2Y)) or \
                   ((posY > som1Y) and (posY > som2Y)):

                    print("PosX : ", posX)
                    print("s1X : ", som1X, " s2X : ", som2X)
                    print("vectX : ", vectX)

                    print("PosY : ", posY)
                    print("s1Y : ", som1Y, " s2Y : ", som2Y)
                    print("vectY : ", vectY)

                    print("Dist : ", distanceParcourueSurArc)
                    print("Long arc : ", longArc)
                    raise "Erreur Coordonnees Incorrect"

            # retour de la position
            return ((posX, posY), (vectX, vectY))

        else:  # le taxi est dans une station

            # Reference sur le gestionnaire de stations
            lesStations = GestionnaireStations()

            # retour de la position
            return lesStations.getPosition(self.__noStation)

    def estEnDeplacement(self):
        """
        Savoir si un taxi roule ou non.

        Permet de savoir si un taxi est en train de rouler ou si il
        est en station.

        retourne (int) -- 1 = taxi en deplacement, 0 = a l'arret

        - depuis - 1.0

        - auteur - Lucien Chaboudez
        """
        if self.__evenementCourant == None:

            return 0
        else:
            return 1

    def traiterEvenement(self, evenement):
        """
        Traiter l'evenement passe.

        Traite l'evenement passe en parametre et renvoie un autre
        evenement.

        evenement (Evenement) -- l'evenement qu'il faut traiter

        - depuis - 1.0

        - auteur - Lucien Chaboudez
        """
        from Central import Central  # FIX2023 Circular Imports

        # Reference sur la centrale
        leCentral = Central()

        # Reference sur les stations
        lesStations = GestionnaireStations()

        # Recuperation de l'heure
        heure = evenement.temps()

        # ----- CHERCHER UN CLIENT -----

        if evenement.__class__.__name__ == 'EvClient':

            # Recuperation du chemin pour aller chercher le client
            self.__cheminCourant = evenement.cheminClient()

            # Recherche de la distance pour aller chercher le client
            self.__distTrajet = self.__cheminCourant.distTotalPos()

            # Calcul de l'heure a laquelle le client sera charge
            self.__heureFinEvenement = heure + ((self.__distTrajet * 3.6) / self.__vitesse)

            # Creation du nouvel evenement
            from Evenement import EvChargerClient  # FIX2023 Circular
            newEvenement = EvChargerClient(self.__heureFinEvenement, self, evenement)

            if D:
                print('Charger client au temps : ', self.__heureFinEvenement)
            # Ajout de l'evenement dans la centrale
            leCentral.ajouterEvenement(newEvenement)

            # si le taxi est dans une station,
            if self.estEnDeplacement() == 0:
                # on dit § la station qu'on la quitte.
                lesStations.getStation(self.__noStation).quitterPlace(self.__no)

            # Enregistrement de l'evenement
            self.__evenementCourant = evenement

            self.__etat = 'chercheClient'

            # Le taxi n'est plus dans une station
            self.__noStation = None

        # -----  CHARGER UN CLIENT -----

        elif evenement.__class__.__name__ == 'EvChargerClient':

            # Si l'evenement courant (EvClient) n'existe pas,
            if self.__evenementCourant == None:
                raise ErreurEvenementIncorrect

            # mise § jour de la distance totale parcourue
            self.__mParcourus += self.__distTrajet

            # Recuperation du chemin pour conduire le client
            self.__cheminCourant = self.__evenementCourant.chemin()

            # Recherche de la distance pour conduire le client
            self.__distTrajet = self.__cheminCourant.distTotalPos()

            # Calcul de l'heure a laquelle le client sera depose
            self.__heureFinEvenement = heure + ((self.__distTrajet * 3.6) / self.__vitesse)

            # creation du nouvel evenement
            from Evenement import EvPoserClient  # FIX2023
            newEvenement = EvPoserClient(self.__heureFinEvenement, self, evenement)

            if D:
                print('Poser client au temps : ', self.__heureFinEvenement)

            # Ajout de l'evenement dans la centrale
            leCentral.ajouterEvenement(newEvenement)

            # Enregistrement de l'evenement
            self.__evenementCourant = evenement

            self.__etat = 'conduitClient'

        # ----- POSER UN CLIENT -----

        elif evenement.__class__.__name__ == 'EvPoserClient':

            # Si l'evenement courant (EvChargerClient) n'existe pas,
            if self.__evenementCourant == None:
                raise ErreurEvenementIncorrect

            # mise § jour de la distance totale parcourue
            self.__mParcourus += self.__distTrajet

            # Recuperation du chemin pour aller a la station
            self.__cheminCourant = evenement.cheminStation()

            # Recherche de la distance pour aller a la station
            self.__distTrajet = self.__cheminCourant.distTotalPos()

            # Calcul de l'heure a laquelle le client sera depose
            self.__heureFinEvenement = heure + ((self.__distTrajet * 3.6) / self.__vitesse)

            # Creation de l'evenement pour signaler l'arrivee en station
            from Evenement import EvArriverStation  # FIX2023
            newEvenement = EvArriverStation(self.__heureFinEvenement,
                                            self, evenement.station())

            # Ajout de l'evenement dans la centrale
            leCentral.ajouterEvenement(newEvenement)

            # Enregistrement de l'evenement
            self.__evenementCourant = evenement

            # on r§serve une place dans la station ou on va.
            self.__evenementCourant.station().reserverPlace()

            self.__etat = 'retourStation'

            # Une course de plus pour le taxi
            self.__nbCoursesEffectuees += 1

        # ----- ARRIVER A LA STATION -----

        elif evenement.__class__.__name__ == 'EvArriverStation':

            # Si l'evenement courant (EvArriverStation) n'existe pas,
            if self.__evenementCourant == None:
                raise ErreurEvenementIncorrect

            # mise § jour de la distance totale parcourue
            self.__mParcourus += self.__distTrajet

            # enregistrement du no de la nouvelle station dans laquelle
            # on se trouve.
            self.__noStation = self.__evenementCourant.station().getNo()

            # on informe la station qu'on prend place dedans
            self.__evenementCourant.station().prendPlace(self.__no)

            # Reset des valeurs
            self.__evenementCourant = None
            self.__heureFinEvenement = 0

            self.__etat = 'arrete'

        # Si c'est autre chose, c'est un erreur
        else:

            raise ErreurEvenementIncorrect
        pass

    def getNoStation(self):
        """
        Renvoie le no de la station.

        Permet de connaitre le no de la station dans laquelle se trouve
        le taxi.

        retourne (int) -- noStation : le no de la station

        - depuis - 1.2

        - auteur - Lucien Chaboudez
        """
        return self.__noStation

    def arc(self, heure=0):
        """
        renvoie l'arc sur lequel le taxi se trouve.

        Permet de connaitre l'arc sur laquelle le taxi se trouve.

        heure (int) -- l'heure courante

        retourne (tuple(tuple(NomSommet,NomSommet), float))
        -- un tuple contenant 1 tuple et la distance parcourue
           sur l'arc . Le tuple contient les sommets entre lesquels
           le taxi se trouve.

        - depuis - 1.4

        - auteur - Lucien Chaboudez
        """

        if self.estEnDeplacement():

            # si il n'y a pas d'heure,
            if heure == 0:
                # on retourne le dernier arc du chemin courant.
                return (self.__cheminCourant.posArrivee(), 0)

            distanceParcourue = (heure - self.__evenementCourant.temps()) \
                * (self.__vitesse / 3.6)

            # recherche de la liste des sommets composants le chemin
            listeSommetsChemin = self.__cheminCourant.listeSommets()

            # Si il y a eu une erreur dans l'heure pass§e, qu'elle est
            # trop grande
            if self.__heureFinEvenement != None and \
                    heure > self.__heureFinEvenement:
                raise Exception(ErreurHeureIncorrecte)

            # calcul de la distance du 1er demi-arc
            distanceCumulee = \
                self.__cheminCourant.distEntreSommets(listeSommetsChemin[0],
                                                      listeSommetsChemin[1]) / 2.0

            # Si on n'est pas sur le 1er demi-arc,
            if distanceCumulee < distanceParcourue:

                posDansListe = 1

                # Initialisation
                sommet2 = listeSommetsChemin[1]

                # tant qu'on n'a pas d§pass§ la distance max autoris§e,
                while distanceCumulee < self.__distTrajet:

                    # passage au sommet suivant
                    sommet1 = sommet2

                    # Passage au sommet suivant
                    posDansListe += 1

                    if D:
                        if posDansListe > len(listeSommetsChemin)-1:
                            print("Taxi no : ", self.__no)
                            print("Pos dans liste ", posDansListe)
                            print("Sommet1 cour : ", sommet1)
                            print("Sommet2 cour : ", sommet2)
                            print("Dist cum : ", distanceCumulee)
                            print("Dist parcourue : ", distanceParcourue)
                            print("dist chemin : ", self.__cheminCourant.distTotalPos())
                            raise "Erreur position incorrecte"

                    # passage au sommet suivant
                    sommet2 = listeSommetsChemin[posDansListe]

                    # distance de l'arc courant
                    distArc = self.__cheminCourant.distEntreSommets(sommet1, sommet2)

                    # si le taxi se trouve sur ce arc,
                    if distanceCumulee + distArc >= distanceParcourue:

                        # on sort de la boucle
                        break

                    # mise a jour de la distance cumulee
                    distanceCumulee += distArc

                # si la distance max a §t§  d§pass§e,
                if distanceCumulee > self.__distTrajet:

                    distParcourueSurArc = distArc

                else:
                    # Calcul de la distance parcourue sur l'arc.
                    distParcourueSurArc = distanceParcourue - distanceCumulee

            else:  # Le taxi se trouve sur le 1er demi-arc

                sommet1 = listeSommetsChemin[0]
                sommet2 = listeSommetsChemin[1]
                distParcourueSurArc = distanceParcourue + distanceCumulee

            if D:
                if distParcourueSurArc > self.__cheminCourant.distEntreSommets(sommet1, sommet2):
                    print("Sommets : ", sommet1, sommet2)
                    print("Dist entre sommets : ", self.__cheminCourant.distEntreSommets(sommet1, sommet2))
                    print("Dist parcourue sur arc : ", distParcourueSurArc)
                    raise "Erreur Distance Incorrecte"

            # retour de la position
            return ((sommet1, sommet2), distParcourueSurArc)

        else:  # le taxi est dans une station

            # Reference sur le gestionnaire de stations
            lesStations = GestionnaireStations()

            # retour de la position de la station
            return (lesStations.arc(self.__noStation), 0)

    def getNo(self):
        """
        renvoie le no du taxi.

        Permet de connaitre le no que porte le taxi.

        retourne int  -- le no du taxi.

        - depuis - 1.24

        - auteur - Lucien Chaboudez
        """
        return self.__no

    def getEtat(self):
        """
        renvoie l'etat du taxi sous forme de string.

        Permet de connaitre l'§tat du taxi.

        retourne string  -- l'§tat du taxi
            Etats possibles : 'arrete', 'chercheClient', 'conduitClient',
                              'retourStation'.

        - depuis - 1.27

        - auteur - Lucien Chaboudez
        """
        return self.__etat

    def getNbCoursesEffectuees(self):
        """
        renvoie le nombre de courses effectuees par le taxi.

        Permet de connaitre le nombre de courses que le taxi a effectu§es.
        C'est-§-dire le nombre de client qu'il a charg§ et qu'il a amen§ § destination.

        retourne int -- le nombre de courses

        - depuis - 1.33

        - auteur - Lucien Chaboudez
        """
        return self.__nbCoursesEffectuees

    def getNbmParcourus(self):
        """
        renvoie le nombre de m§tres parcourus par le taxi.

        Permet de connaitre le nombre de m§tres que le taxi a parcouru.

        retourne float -- le nombre de m§tres parcourus

        - depuis - 1.33

        - auteur - Lucien Chaboudez
        """
        return self.__mParcourus


if __name__ == '__main__':

    gestPref = GestionnairePreferences()

    gestPref.ajouterOption('vitesseTaxiKMH', 50)

    T = Taxi(1, 0)

    if T.estEnDeplacement == 1:

        print('Se deplace')

    else:

        print('Est a l\'arret')

    print('LE TEST S\'EST DEROULE AVEC SUCCES')

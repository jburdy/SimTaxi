#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programme principal.

$Id: SimTaxi.py,v 1.26 2003/03/03 10:10:18 erreur Exp $
"""
import sys
from threading import Thread
from time import sleep

from Central import Central
from GestionnairePreferences import GestionnairePreferences
from GrapheXY import GrapheXY
from Initialisateur import Initialisateur

ID = "$Id: SimTaxi.py,v 1.26 2003/03/03 10:10:18 erreur Exp $"


sys.stderr = open('ERREURS.log', 'a')  # .write('\n'*5+ID)

fichierClients = 'dumpClients'

print('\n'*3+ID+'\n')


def dumpClients(liste):
    """
    Dump (sauvegarde après transformation) de la demande (liste d'év. clients).
    Le fichier (%s) est sous forme texte.
    liste -- la liste d'événements clients.
    - depuis - 1.21
    - auteur - Julien Burdy
    """
    f = open(fichierClients, 'w')
    for i in liste:
        f.write(str(i.temps())+';'+str(i.positions())+'\n')
    f.close()


def loadClients():
    """
    Chargement du dump de la demande (liste d'év. clients).
    Le fichier (%s) est sous forme texte.
    retourne (list) -- liste d'événements clients.
    - depuis - 1.21
    - auteur - Julien Burdy
    """
    from string import split

    from Evenement import EvClient
    clients = []
    liste = open(fichierClients).readlines()
    for i in liste:
        spl = split(i, ';')
        clients.append(EvClient(eval(spl[0]), eval(spl[1])))
    return clients


class T(Thread):
    def run(self):
        # tant qu'il y a des evenements
        print('==== Début de la simulation')
        while cntrl.evenement():
            evenement = cntrl.traiterProchainEvenement()  # renvois l'evenement traite (pour le gui)
            # if D: print str(evenement) + "\n"
            temps = evenement.temps()  # saisie du temps de l'evenement
            #print((temps/(3600.0*24.0))*100.0, '%')
            # if D: print '=== temps :', temps
            # if gp.valeurDe('gui'): gui.rafraichir(temps, evenement) # le gui raffraichi et renvois vrai s'il veut stopper

            # si le prochain evenement est trop loin dans le temps, on continue de raffraichir avant
            # de traiter ce prochain evenement
            while gp.valeurDe('gui') and \
                    cntrl.evenement() and \
                    cntrl.intervalleProchainEvement(temps) > 1 and \
                    gp.valeurDe('pseudoContinu'):
                temps += 1
                # if D: print '=== tempsInter :', temps
                # if gp.valeurDe('gui'): gui.rafraichir(temps, None)
                sleep(gp.valeurDe('dureeSec'))
        print('==== FIN')
        grph.dump()


if __name__ == '__main__':

    D = 1  # 1 = DEBUG
    # recuperation des préférences (param§tres + configuration)
    gp = GestionnairePreferences('config.txt')

    # initialisation de l'interface utilisateur, permettant § l'utilisateur
    # de changer certain param§tre avant les initialisations suivantes (donc bloquant)
    # création des objets
    grph = GrapheXY()
    grph.init()
    grph.initialiser()
    grph.genererGraphe(15, 35, 12000, 59)
    cntrl = Central()

    intlst = Initialisateur()

    # mise ne place des taxis/stations
    print('Initialisation stations...')
    intlst.genererStations(gp.valeurDe('ndStation'), gp.valeurDe('tailleStation'))
    print('Initialisation taxis...')
    intlst.initialiserTaxis(gp.valeurDe('nbTaxi'))

    # generation des courses et initialisation du central
    try:
        print('Recup de la demande...')
        clients = loadClients()
        if len(clients) != gp.valeurDe('nbCoursesJour'):
            raise
        print(len(clients), 'clients')
        # for i in clients: graphe.cheminPlusCourt(i.positions()[0],i.positions()[1])
    except:
        print('Génération de la demande (long la 1ère fois)...')
        clients = intlst.genererCourses(gp.valeurDe('nbCoursesJour'),
                                        gp.valeurDe('hPremiereCourse'),
                                        gp.valeurDe('hDerniereCourse'),
                                        gp.valeurDe('moyenneCourseKM'))
        dumpClients(clients)

    cntrl.initEv(clients)

    # if gp.valeurDe('gui'):
    #     from SimTaxiGUI import SimTaxiGUI
    #     gui = SimTaxiGUI(0)

    # def main():
    t = T()
    if gp.valeurDe('gui'):
        t.setDaemon(True)
    t.start()
    # if gp.valeurDe('gui'): gui.start()
    grph.dump()

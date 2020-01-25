#!/usr/bin/python2
# -*- coding: utf-8 -*-
"""
Programme principal.

$Id: SimTaxi.py,v 1.26 2003/03/03 10:10:18 erreur Exp $
"""
ID = "$Id: SimTaxi.py,v 1.26 2003/03/03 10:10:18 erreur Exp $"

from threading import Thread
from Central import Central
from GestionnairePreferences import GestionnairePreferences
from GrapheXY import GrapheXY
from Initialisateur import Initialisateur
from time import sleep
import sys
sys.stderr = file('ERREURS.log', 'a')#.write('\n'*5+ID)

fichierClients = 'dumpClients'

print '\n'*3+ID+'\n'


def dumpClients(liste):
    """
    Dump (sauvegarde apr§s transformation) de la demande (liste d'§v clients).

    Le fichier (%s) est sous forme texte.

    liste -- la liste d'§v§nements clients.

    - depuis - 1.21

    - auteur - Julien Burdy
    """ % fichierClients
    f = file(fichierClients,'w')
    for i in liste: f.write(str(i.temps())+';'+str(i.positions())+'\n')
    f.close()


def loadClients():
    """
    Chargement du dump de la demande (liste d'§v clients).

    Le fichier (%s) est sous forme texte.
    
    retourne (list) -- liste d'§v§nements clients.

    - depuis - 1.21

    - auteur - Julien Burdy
    """ % fichierClients
    from Evenement import EvClient
    from string import split
    clients = []
    liste = file(fichierClients).readlines()
    for i in liste:
        spl = split(i, ';')
        clients.append(EvClient(eval(spl[0]), eval(spl[1])))
    return clients



if __name__ == '__main__':
    print """Utilisez startSimTaxi.pyw pour lancer le programme 
(a lancer depuis la console pour voir le log)"""
    raw_input()
else:

    D = 1 # 1 = DEBUG

    # recuperation des pr§f§rences (param§tres + configuration)
    gp = GestionnairePreferences('config.txt')

    ##### initialisation de l'interface utilisateur, permettant § l'utilisateur
    ##### de changer certain param§tre avant les initialisations suivantes (donc bloquant)

    # cr§ation des objets
    graphe = GrapheXY(gp.valeurDe('fichierGraphe'))
    central = Central()

    initialisateur = Initialisateur()

    # mise ne place des taxis/stations
    print 'Initialisation stations...'
    initialisateur.genererStations(gp.valeurDe('ndStation'),gp.valeurDe('tailleStation'))
    print 'Initialisation taxis...'
    initialisateur.initialiserTaxis(gp.valeurDe('nbTaxi'))


    # generation des courses et initialisation du central
    try: 
        print 'Recup de la demande...'
        clients = loadClients()
        if len(clients) != gp.valeurDe('nbCoursesJour'): raise
        print len(clients), 'clients'
        #for i in clients: graphe.cheminPlusCourt(i.positions()[0],i.positions()[1])
    except:
        print 'G§n§ration de la demande (long la 1§re fois)...'
        clients = initialisateur.genererCourses(gp.valeurDe('nbCoursesJour'),
                                                gp.valeurDe('hPremiereCourse'),
                                                gp.valeurDe('hDerniereCourse'),
                                                gp.valeurDe('moyenneCourseKM'))
        dumpClients(clients)

    central.initEv(clients)

    if gp.valeurDe('gui'):  
        from SimTaxiGUI import SimTaxiGUI
        gui = SimTaxiGUI(0)

class T(Thread):
    def run(self):
        # tant qu'il y a des evenements
        print '==== D§but de la simulation'
        while central.evenement():
            evenement = central.traiterProchainEvenement() # renvois l'evenement traite (pour le gui)
            #if D: print str(evenement) + "\n"
            temps = evenement.temps() # saisie du temps de l'evenement
            print (temps/(3600.0*24.0))*100.0, '%'
            #if D: print '=== temps :', temps
            if gp.valeurDe('gui'): gui.rafraichir(temps, evenement) # le gui raffraichi et renvois vrai s'il veut stopper

            # si le prochain evenement est trop loin dans le temps, on continue de raffraichir avant
            # de traiter ce prochain evenement
            while gp.valeurDe('pseudoContinu') and central.evenement() and central.intervalleProchainEvement(temps) > 1 \
                  and gp.valeurDe('gui'):
                temps += 1
                #if D: print '=== tempsInter :', temps
                if gp.valeurDe('gui'): gui.rafraichir(temps, None)
                sleep(gp.valeurDe('dureeSec'))
        print '==== FIN'
        graphe.dump()

def main():
    t = T()
    if gp.valeurDe('gui'): t.setDaemon(True)
    t.start()
    if gp.valeurDe('gui'): gui.start()
    graphe.dump()





#!/usr/bin/env python
#$Id: test_taxi.py,v 1.14 2003/01/22 17:18:11 erreur Exp $

import Central, GestionnairePreferences, GrapheXY, GestionnaireTaxis, GestionnaireStations, Taxi, Evenement, random, PolitiquePlusPres
import SimTaxiGUI
import Initialisateur
from time import sleep
from threading import Thread
from os import curdir, sep, pardir

False = 0
True = not False

if __name__ == '__main__': PATH = pardir+sep
else: PATH = curdir+sep

# recuperation de la config
conf = GestionnairePreferences.GestionnairePreferences(PATH+'config.txt')

central = Central.Central()

graphe = GrapheXY.GrapheXY(PATH+'graphe'+sep+'graphe.gr')

taxis = GestionnaireTaxis.GestionnaireTaxis()
stations = GestionnaireStations.GestionnaireStations()

politique = PolitiquePlusPres.PolitiquePlusPres()

central.modifierPolitique(politique)

nbTax = 180

arcs = graphe.listeArcs()
rand = random.Random()

# renvois un chemin quelconque
def unChemin():
    for i in xrange(100):
        try :
            return graphe.cheminPlusCourt(arcs[rand.randrange(len(arcs))],
                                          arcs[rand.randrange(len(arcs))])
        except:
            print "erreur: recherche d'un autre chemin", i



print "Creation des stations ..."
# création de stations
stations.addStation(nbTax,graphe.listeSommets(1)[0], graphe.listeSommets(1)[1])


print "Creation des %d taxis ..." % nbTax
#création des taxis, remplissage des stations
for i in range(nbTax): taxis.addTaxi(1)




print "Creation des %d evenements ..." % nbTax
lesEvCli = []
#création des évenements
for i in range(nbTax):
    lesEvCli.append(Evenement.EvClient(0, unChemin()))
    if (i)%10 == 0: print int(float(i)/nbTax*100), '%'


print "Traitement des %d evenements ..." % nbTax
i = 0
for ev in lesEvCli :
    ev.traiter()
    if i%10 == 0: print int(float(i)/nbTax*100), '%'
    i += 1


print "Demarrage de l'interface ..."
gui = SimTaxiGUI.SimTaxiGUI(0)

class T(Thread):
    def run(self):
        i = 1
        while(go):
            gui.rafraichir((i)%20, None)
            i = i + 1
            sleep(.5)

go = True
T().start()

gui.start()
go = False


#   $Log: test_taxi.py,v $
#   Revision 1.14  2003/01/22 17:18:11  erreur
#   180taxis + divers
#
#   Revision 1.13  2003/01/22 11:38:27  erreur
#   *** empty log message ***
#
#   Revision 1.12  2003/01/21 21:34:48  erreur
#   modif du path
#
#   Revision 1.11  2003/01/15 14:11:09  erreur
#   200 taxis, ok pour le PCC
#
#   Revision 1.10  2003/01/13 16:02:54  erreur
#   val pour nos essais
#





"""Compare les strategies automatiques sur les terrains du depot.

Lancer depuis la racine du projet :  python comparer_strategies.py
Le tableau affiche peut etre recopie dans le rapport.
"""
from Terrain import Terrain
from Reseau import Reseau
from StrategieReseau import StrategieReseauAuto, StrategieReseauOptimisee

TERRAINS = ["terrains/t1.txt", "terrains/t2.txt"]
STRATEGIES = [("Auto (BFS)", StrategieReseauAuto), ("Optimisee (Dijkstra)", StrategieReseauOptimisee)]

if __name__ == "__main__":
    print("{:<18} {:<22} {:>7} {:>6} {:>10} {:>7}".format(
        "Terrain", "Strategie", "Noeuds", "Arcs", "Cout (ME)", "Valide"))
    for fichier in TERRAINS:
        t = Terrain()
        t.charger(fichier)
        for nom, Strategie in STRATEGIES:
            r = Reseau()
            r.set_strategie(Strategie())
            r.configurer(t)
            valide = r.valider_reseau() and r.valider_distribution(t)
            print("{:<18} {:<22} {:>7} {:>6} {:>10} {:>7}".format(
                fichier, nom, len(r.noeuds), len(r.arcs), r.calculer_cout(t), "oui" if valide else "non"))

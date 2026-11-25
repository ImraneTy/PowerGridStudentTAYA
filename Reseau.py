
from Terrain import Terrain, Case
from StrategieReseau import StrategieReseau, StrategieReseauAuto

class Reseau:
    def __init__(self):
        self.strat = StrategieReseauAuto()
        self.noeuds = {}
        self.arcs = []

        self.noeud_entree = -1

    def definir_entree(self, n: int) -> None:
        if n in self.noeuds.keys():
            self.noeud_entree = n
        else:
            self.noeud_entree = -1

    def ajouter_noeud(self, n: int, coords: tuple[int, int]):
        if isinstance(n, int) and not isinstance(n, bool):
            if n >= 0 and n not in self.noeuds:
                self.noeuds[n] = coords

    def ajouter_arc(self, n1: int, n2: int) -> None:
        if n1 > n2:
            tmp = n2
            n2 = n1
            n1 = tmp
        if n1 not in self.noeuds.keys() or n2 not in self.noeuds.keys():
            return
        if (n1, n2) not in self.arcs:
            self.arcs.append((n1, n2))

    def set_strategie(self, strat: StrategieReseau):
        self.strat = strat

    def valider_reseau(self) -> bool:

        # Check that the entry node exists
        if self.noeud_entree not in self.noeuds:
            return False

        # Start exploring from the entry node
        visites = set()
        a_visiter = [self.noeud_entree]

        while a_visiter:
            noeud = a_visiter.pop()

            if noeud in visites:
                continue

            visites.add(noeud)

            # Find all nodes connected to this node
            for a, b in self.arcs:
                if a == noeud and b not in visites:
                    a_visiter.append(b)

                elif b == noeud and a not in visites:
                    a_visiter.append(a)

        # All nodes must be connected to the entry
        return len(visites) == len(self.noeuds)

    def valider_distribution(self, t: Terrain) -> bool:

        # Check that the electrical network is valid
        if not self.valider_reseau():
            return False

        # Get the positions of all clients
        clients = t.get_clients()

        # Get the positions of all network nodes
        positions_noeuds = set(self.noeuds.values())

        # Check that every client has a network node
        for client in clients:
            if client not in positions_noeuds:
                return False

        return True

    def configurer(self, t: Terrain):
        self.noeud_entree, self.noeuds, self.arcs  = self.strat.configurer(t)

    def afficher(self) -> None:
        print("Noeud d'entree : {}".format(self.noeud_entree))
        print("Noeuds ({}) : {}".format(len(self.noeuds), self.noeuds))
        print("Arcs ({}) : {}".format(len(self.arcs), self.arcs))
        if not self.noeuds:
            return
        # Dessin du reseau : une case du terrain = 2 caracteres de large et 2 de haut,
        # pour avoir la place de dessiner les arcs ("-" horizontal, "|" vertical)
        hauteur = max(l for l, _ in self.noeuds.values()) + 1
        largeur = max(c for _, c in self.noeuds.values()) + 1
        grille = [[" "] * (2 * largeur - 1) for _ in range(2 * hauteur - 1)]
        for n, (l, c) in self.noeuds.items():
            grille[2 * l][2 * c] = "E" if n == self.noeud_entree else "o"
        for n1, n2 in self.arcs:
            if n1 not in self.noeuds or n2 not in self.noeuds:
                continue
            (l1, c1), (l2, c2) = self.noeuds[n1], self.noeuds[n2]
            if l1 == l2 and abs(c1 - c2) == 1:
                grille[2 * l1][c1 + c2] = "-"
            elif c1 == c2 and abs(l1 - l2) == 1:
                grille[l1 + l2][2 * c1] = "|"
        for ligne in grille:
            print("".join(ligne).rstrip())

    def afficher_avec_terrain(self, t: Terrain) -> None:
        # Correction : "elif" au lieu de plusieurs "if" (sinon un espace en trop par case)
        for ligne, l in enumerate(t.cases):
            for colonne, c in enumerate(l):
                if (ligne, colonne) not in self.noeuds.values():
                    if c == Case.OBSTACLE:
                        print("X", end="")
                    elif c == Case.CLIENT:
                        print("C", end="")
                    elif c == Case.VIDE:
                        print("~", end="")
                    elif c == Case.ENTREE:
                        print("E", end="")
                    else:
                        print(" ", end="")
                else:
                    if c == Case.OBSTACLE:
                        print("T", end="")
                    elif c == Case.CLIENT:
                        print("C", end="")
                    elif c == Case.VIDE:
                        print("+", end="")
                    elif c == Case.ENTREE:
                        print("E", end="")
                    else:
                        print(" ", end="")
            print()

    def calculer_cout(self, t: Terrain) -> float:
        cout = 0
        for _ in self.arcs:
            cout += 1.5
        for n in self.noeuds.values():
            if t[n[0]][n[1]] == Case.OBSTACLE:
                cout += 2
            else:
                cout += 1
        return cout



from Terrain import Terrain, Case
from collections import deque

class StrategieReseau:
    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:
        return -1, {}, []

class StrategieReseauManuelle(StrategieReseau):

    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:

        noeuds = {}
        arcs = []
        noeud_entree = -1

        entree = t.get_entree()

        while True:
            print("\n===== CONFIGURATION MANUELLE =====")
            print("1. Ajouter un noeud")
            print("2. Ajouter un arc")
            print("3. Definir le noeud d'entree")
            print("4. Afficher le reseau")
            print("5. Terminer")

            choix = input("Votre choix : ").strip()

            if choix == "1":
                try:
                    n = int(input("Identifiant du noeud : "))
                    x = int(input("Ligne : "))
                    y = int(input("Colonne : "))
                except ValueError:
                    print("Erreur : entrez des entiers.")
                    continue

                if n < 0 or n in noeuds:
                    print("Identifiant invalide ou deja utilise.")
                elif not (0 <= x < len(t.cases) and
                          0 <= y < len(t.cases[x])):
                    print("Position hors du terrain.")
                elif (x, y) in noeuds.values():
                    print("Cette position est deja occupee.")
                else:
                    noeuds[n] = (x, y)
                    print("Noeud ajoute.")

            elif choix == "2":
                try:
                    n1 = int(input("Premier noeud : "))
                    n2 = int(input("Deuxieme noeud : "))
                except ValueError:
                    print("Erreur : entrez des entiers.")
                    continue

                if n1 not in noeuds or n2 not in noeuds:
                    print("Un des noeuds n'existe pas.")
                    continue

                if n1 == n2:
                    print("Impossible de relier un noeud a lui-meme.")
                    continue

                x1, y1 = noeuds[n1]
                x2, y2 = noeuds[n2]

                if abs(x1 - x2) + abs(y1 - y2) != 1:
                    print("Les noeuds doivent etre voisins.")
                    continue

                arc = (min(n1, n2), max(n1, n2))

                if arc in arcs:
                    print("Cet arc existe deja.")
                else:
                    arcs.append(arc)
                    print("Arc ajoute.")

            elif choix == "3":
                try:
                    n = int(input("Identifiant du noeud d'entree : "))
                except ValueError:
                    print("Identifiant invalide.")
                    continue

                if n in noeuds and noeuds[n] == entree:
                    noeud_entree = n
                    print("Entree definie.")
                else:
                    print("Le noeud doit etre sur la case d'entree.")

            elif choix == "4":
                print("\nNoeuds :", noeuds)
                print("Arcs :", arcs)
                print("Noeud d'entree :", noeud_entree)

            elif choix == "5":
                if noeud_entree == -1:
                    print("Attention : entree non definie.")

                return noeud_entree, noeuds, arcs

            else:
                print("Choix invalide.")
class StrategieReseauAuto(StrategieReseau):

    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:

        entree = t.get_entree()
        clients = t.get_clients()

        if entree == (-1, -1):
            return -1, {}, []

        noeuds = {0: entree}
        arcs = []
        positions = {entree: 0}
        prochain_id = 1

        # Directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for client in clients:

            file = deque([entree])
            parents = {entree: None}

            while file:
                position = file.popleft()

                if position == client:
                    break

                for dx, dy in directions:
                    x = position[0] + dx
                    y = position[1] + dy
                    voisin = (x, y)

                    if 0 <= x < len(t.cases) and 0 <= y < len(t.cases[x]):
                        if voisin not in parents:
                            if t.cases[x][y] != Case.OBSTACLE:
                                parents[voisin] = position
                                file.append(voisin)

            # Reconstruct the path to the client
            if client not in parents:
                continue

            chemin = []
            position = client

            while position is not None:
                chemin.append(position)
                position = parents[position]

            chemin.reverse()

            # Add nodes and connections
            for i, position in enumerate(chemin):

                if position not in positions:
                    positions[position] = prochain_id
                    noeuds[prochain_id] = position
                    prochain_id += 1

                if i > 0:
                    a = positions[chemin[i - 1]]
                    b = positions[position]

                    arc = (min(a, b), max(a, b))

                    if arc not in arcs:
                        arcs.append(arc)

        return 0, noeuds, arcs


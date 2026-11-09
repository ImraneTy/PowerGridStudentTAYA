
from Terrain import Terrain, Case
from collections import deque

class StrategieReseau:
    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:
        return -1, {}, []

class StrategieReseauManuelle(StrategieReseau):
    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:
        # TODO
        return -1, {}, []

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


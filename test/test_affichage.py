import io
import unittest
from contextlib import redirect_stdout

import xmlrunner

from Terrain import Terrain, Case
from Reseau import Reseau


def capturer(fonction, *args):
    """Execute fonction(*args) et renvoie tout ce qu'elle a affiche avec print()."""
    sortie = io.StringIO()
    with redirect_stdout(sortie):
        fonction(*args)
    return sortie.getvalue()


class TestAffichage(unittest.TestCase):

    def setUp(self):
        self.t = Terrain()
        self.t.cases = [[Case.ENTREE, Case.VIDE, Case.CLIENT, Case.OBSTACLE]]
        self.t.hauteur, self.t.largeur = 1, 4

    def test_afficher_terrain(self):
        # Avant la correction (if au lieu de elif), un espace en trop s'affichait
        # apres chaque case sauf l'entree : "E~ C X " au lieu de "E~CX"
        self.assertEqual(capturer(self.t.afficher), "E~CX\n")

    def test_afficher_avec_terrain(self):
        r = Reseau()
        r.ajouter_noeud(0, (0, 0))
        r.ajouter_noeud(1, (0, 1))
        r.ajouter_noeud(2, (0, 2))
        r.definir_entree(0)
        r.ajouter_arc(0, 1)
        r.ajouter_arc(1, 2)
        self.assertEqual(capturer(r.afficher_avec_terrain, self.t), "E+CX\n")

    def test_afficher_reseau(self):
        r = Reseau()
        r.ajouter_noeud(0, (0, 0))
        r.ajouter_noeud(1, (0, 1))
        r.ajouter_noeud(2, (1, 1))
        r.definir_entree(0)
        r.ajouter_arc(0, 1)
        r.ajouter_arc(1, 2)
        lignes = capturer(r.afficher).splitlines()
        # les 3 premieres lignes resument le reseau, puis vient le dessin
        self.assertEqual(lignes[0], "Noeud d'entree : 0")
        self.assertEqual(lignes[3:], ["E-o", "  |", "  o"])

    def test_afficher_reseau_vide(self):
        r = Reseau()
        lignes = capturer(r.afficher).splitlines()
        self.assertEqual(len(lignes), 3)          # juste le resume, pas de dessin

if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-reports"))

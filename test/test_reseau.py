
import unittest
import xmlrunner

from Reseau import Reseau
from Terrain import Terrain, Case

class TestReseau(unittest.TestCase):

    def test_definition_entree(self):
        r = Reseau()

        r.ajouter_noeud(0, (0, 0))
        r.ajouter_noeud(1, (0, 1))

        r.definir_entree(0)

        self.assertEqual(r.noeud_entree, 0)

        # An unknown node cannot be the entry
        r.definir_entree(5)

        self.assertEqual(r.noeud_entree, -1)

    def test_ajout_noeud(self):
        r = Reseau()

        r.ajouter_noeud(0, (0, 0))
        r.ajouter_noeud(1, (1, 2))

        self.assertEqual(r.noeuds[0], (0, 0))
        self.assertEqual(r.noeuds[1], (1, 2))

        # Negative identifiers must be rejected
        r.ajouter_noeud(-1, (2, 2))

        self.assertNotIn(-1, r.noeuds)
        # Try to add an existing node with different coordinates
        r.ajouter_noeud(0, (5, 5))

        # Original coordinates must remain unchanged
        self.assertEqual(r.noeuds[0], (0, 0))

    def test_ajout_arc(self):
        r = Reseau()

        r.ajouter_noeud(0, (0, 0))
        r.ajouter_noeud(1, (0, 1))

        r.ajouter_arc(0, 1)

        self.assertIn((0, 1), r.arcs)

        # A duplicate arc should not be added
        r.ajouter_arc(1, 0)

        self.assertEqual(len(r.arcs), 1)

        # Cannot connect a nonexistent node
        r.ajouter_arc(0, 5)

        self.assertEqual(len(r.arcs), 1)

    def test_validation_correcte(self):
        r = Reseau()
        r.noeuds[0] = (0, 0)
        r.noeud_entree = 0

        r.noeuds[1] = (1, 0)
        r.arcs.append((0, 1))

        r.noeuds[2] = (0, 1)
        r.arcs.append((0, 2))

        r.noeuds[3] = (0, 2)
        r.arcs.append((2, 3))

        r.noeuds[4] = (1, 2)
        r.arcs.append((3, 4))

        self.assertTrue(r.valider_reseau())

    def test_validation_incorrecte(self):
        r = Reseau()
        r.noeuds[0] = (0, 0)
        r.noeud_entree = 0

        r.noeuds[1] = (1, 0)
        r.arcs.append((0, 1))

        r.noeuds[2] = (0, 1)
        r.arcs.append((0, 2))

        r.noeuds[3] = (0, 2)
        r.arcs.append((2, 3))

        r.noeuds[4] = (1, 2)

        self.assertFalse(r.valider_reseau())

    def test_distribution_correcte(self):
        r = Reseau()
        r.noeuds[0] = (0, 0)
        r.noeud_entree = 0

        r.noeuds[1] = (1, 0)
        r.arcs.append((0, 1))

        r.noeuds[2] = (0, 1)
        r.arcs.append((0, 2))

        r.noeuds[3] = (0, 2)
        r.arcs.append((2, 3))

        r.noeuds[4] = (1, 2)
        r.arcs.append((3, 4))

        t = Terrain()
        t.cases = [
                [Case.ENTREE, Case.VIDE, Case.VIDE],
                [Case.CLIENT, Case.VIDE, Case.CLIENT],
        ]

        self.assertTrue(r.valider_distribution(t))

    def test_distribution_incorrecte(self):
        r = Reseau()
        r.noeuds[0] = (0, 0)
        r.noeud_entree = 0

        r.noeuds[1] = (1, 0)
        r.arcs.append((0, 1))

        r.noeuds[2] = (0, 1)
        r.arcs.append((0, 2))

        r.noeuds[3] = (0, 2)
        r.arcs.append((2, 3))

        r.noeuds[4] = (1, 2)
        r.arcs.append((3, 4))

        t = Terrain()
        t.cases = [
                [Case.ENTREE, Case.VIDE, Case.VIDE],
                [Case.CLIENT, Case.CLIENT, Case.CLIENT],
        ]

        self.assertFalse(r.valider_distribution(t))

if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-reports"))



import unittest
import xmlrunner

from Terrain import Terrain, Case

class TestTerrain(unittest.TestCase):

    def test_chargement(self):
        import tempfile
        import os

        # Create a temporary terrain file
        contenu = "E~~\n~C~\n~~C\n"

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as fichier:
            fichier.write(contenu)
            chemin = fichier.name

        try:
            # Load the terrain
            t = Terrain()
            t.charger(chemin)

            # Verify dimensions
            self.assertEqual(t.largeur, 3)
            self.assertEqual(t.hauteur, 3)

            # Verify terrain contents
            self.assertEqual(t.cases[0][0], Case.ENTREE)
            self.assertEqual(t.cases[0][1], Case.VIDE)
            self.assertEqual(t.cases[1][1], Case.CLIENT)
            self.assertEqual(t.cases[2][2], Case.CLIENT)

            # Verify entry and clients
            self.assertEqual(t.get_entree(), (0, 0))
            self.assertEqual(t.get_clients(), [(1, 1), (2, 2)])

        finally:
            os.unlink(chemin)

    def test_get_entree(self):
        t = Terrain()
        t.cases = [
                [Case.VIDE, Case.VIDE, Case.ENTREE],
                [Case.CLIENT, Case.CLIENT, Case.CLIENT],
        ]
        entree = t.get_entree()
        self.assertIsNotNone(entree)
        self.assertEqual(entree[0], 0)
        self.assertEqual(entree[1], 2)

    def test_accesseur(self):
        t = Terrain()
        t.cases = [
                [Case.ENTREE, Case.VIDE, Case.VIDE],
                [Case.CLIENT, Case.CLIENT, Case.CLIENT],
        ]
        self.assertEqual(t[0][0], Case.ENTREE)
        self.assertEqual(t[0][1], Case.VIDE)
        self.assertEqual(t[1][2], Case.CLIENT)

if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-reports"))


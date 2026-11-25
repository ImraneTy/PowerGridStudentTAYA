import unittest
from unittest.mock import patch

import xmlrunner

from Terrain import Terrain, Case
from Reseau import Reseau
from StrategieReseau import StrategieReseauAuto, StrategieReseauManuelle, StrategieReseauOptimisee


class TestStrategiesReseau(unittest.TestCase):

    def test_config_auto(self):
        r = Reseau()
        r.set_strategie(StrategieReseauAuto())

        t = Terrain()
        t.charger("terrains/t1.txt")
        r.configurer(t)

        self.assertTrue(r.valider_reseau())
        self.assertTrue(r.valider_distribution(t))

        t.charger("terrains/t2.txt")
        r.configurer(t)

        self.assertTrue(r.valider_reseau())
        self.assertTrue(r.valider_distribution(t))

    # ---------- Strategie optimisee ----------

    def test_config_optimisee(self):
        r = Reseau()
        r.set_strategie(StrategieReseauOptimisee())
        t = Terrain()

        t.charger("terrains/t1.txt")
        r.configurer(t)
        self.assertTrue(r.valider_reseau())
        self.assertTrue(r.valider_distribution(t))
        self.assertAlmostEqual(r.calculer_cout(t), 58.5)

        t.charger("terrains/t2.txt")
        r.configurer(t)
        self.assertTrue(r.valider_reseau())
        self.assertTrue(r.valider_distribution(t))
        self.assertAlmostEqual(r.calculer_cout(t), 103.5)

    def test_config_optimisee_traverse_obstacle_si_moins_cher(self):
        # Traverser l'obstacle : 3 noeuds (1 + 2 + 1) + 2 arcs (3)  = 7 M EUR
        # Le contourner par le bas : 5 noeuds (5) + 4 arcs (6)     = 11 M EUR
        t = Terrain()
        t.cases = [
            [Case.ENTREE, Case.OBSTACLE, Case.CLIENT],
            [Case.VIDE,   Case.VIDE,     Case.VIDE],
        ]
        t.hauteur, t.largeur = 2, 3
        r = Reseau()
        r.set_strategie(StrategieReseauOptimisee())
        r.configurer(t)
        self.assertTrue(r.valider_reseau())
        self.assertTrue(r.valider_distribution(t))
        self.assertAlmostEqual(r.calculer_cout(t), 7.0)

    def test_config_optimisee_sans_entree(self):
        t = Terrain()
        t.cases = [[Case.VIDE, Case.CLIENT]]
        t.hauteur, t.largeur = 1, 2
        r = Reseau()
        r.set_strategie(StrategieReseauOptimisee())
        r.configurer(t)
        self.assertEqual(r.noeud_entree, -1)
        self.assertFalse(r.valider_reseau())

    # ---------- Strategie manuelle (menu d'Imrane) ----------
    # patch remplace input() par une liste de reponses preparees a l'avance,
    # et print() par une fonction muette : le test tourne sans clavier (Jenkins).

    def test_config_manuelle(self):
        t = Terrain()
        t.cases = [
            [Case.ENTREE, Case.VIDE, Case.VIDE],
            [Case.CLIENT, Case.VIDE, Case.CLIENT],
        ]
        reponses = [
            "1", "0", "0", "0",     # noeud 0 en (0,0)
            "1", "1", "1", "0",     # noeud 1 en (1,0)
            "1", "2", "0", "1",     # noeud 2 en (0,1)
            "1", "3", "0", "2",     # noeud 3 en (0,2)
            "1", "4", "1", "2",     # noeud 4 en (1,2)
            "2", "0", "1",          # arc 0-1
            "2", "0", "2",          # arc 0-2
            "2", "2", "3",          # arc 2-3
            "2", "3", "4",          # arc 3-4
            "3", "0",               # le noeud 0 est l'entree
            "5",                    # terminer
        ]
        r = Reseau()
        r.set_strategie(StrategieReseauManuelle())
        with patch("builtins.input", side_effect=reponses), patch("builtins.print"):
            r.configurer(t)

        self.assertEqual(r.noeud_entree, 0)
        self.assertEqual(len(r.noeuds), 5)
        self.assertEqual(len(r.arcs), 4)
        self.assertTrue(r.valider_reseau())
        self.assertTrue(r.valider_distribution(t))

    def test_config_manuelle_saisies_invalides(self):
        t = Terrain()
        t.cases = [[Case.ENTREE, Case.CLIENT, Case.VIDE]]
        reponses = [
            "1", "a",               # identifiant qui n'est pas un nombre : refuse
            "3", "0",               # entree sur un noeud qui n'existe pas : refuse
            "9",                    # choix de menu invalide
            "1", "0", "0", "0",     # noeud 0 en (0,0) : accepte
            "1", "1", "5", "5",     # hors du terrain : refuse
            "1", "1", "0", "0",     # case deja occupee : refuse
            "1", "0", "0", "2",     # identifiant deja utilise : refuse
            "1", "1", "0", "1",     # noeud 1 en (0,1) : accepte
            "2", "0", "0",          # arc d'un noeud vers lui-meme : refuse
            "2", "0", "7",          # noeud 7 inexistant : refuse
            "3", "1",               # le noeud 1 n'est pas sur l'entree : refuse
            "3", "0",               # entree : accepte
            "2", "0", "1",          # arc 0-1 : accepte
            "2", "1", "0",          # meme arc dans l'autre sens : refuse
            "5",
        ]
        r = Reseau()
        r.set_strategie(StrategieReseauManuelle())
        with patch("builtins.input", side_effect=reponses), patch("builtins.print"):
            r.configurer(t)

        self.assertEqual(r.noeuds, {0: (0, 0), 1: (0, 1)})
        self.assertEqual(r.arcs, [(0, 1)])
        self.assertEqual(r.noeud_entree, 0)
        self.assertTrue(r.valider_distribution(t))

    def test_config_manuelle_terminer_tout_de_suite(self):
        t = Terrain()
        t.cases = [[Case.ENTREE, Case.CLIENT]]
        r = Reseau()
        r.set_strategie(StrategieReseauManuelle())
        with patch("builtins.input", side_effect=["5"]), patch("builtins.print"):
            r.configurer(t)
        self.assertEqual(r.noeud_entree, -1)
        self.assertFalse(r.valider_reseau())

if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-reports"))

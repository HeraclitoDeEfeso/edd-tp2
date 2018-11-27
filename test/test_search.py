import unittest
from buscador.search import Buscador
from buscador.inverted_index import Control


class TestBuscador(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.control = Control()
        cls.buscador = Buscador(cls.control)
        cls.control.procesar_documento("doc1", "cantor trotar")
        cls.control.procesar_documento("doc2", "chatarra cancion")
        cls.control.procesar_documento("doc3", "ocación")

    def test_un_patron_no_acepta_un_caracter_especial_distinto_al_asterisco(self):
        self.assertRaises(ValueError, self.buscador.buscar, "lla.da")

    def test_un_patron_vacio_no_es_valido(self):
        self.assertRaises(ValueError, self.buscador.buscar, "")

    def test_un_patron_con_solo_un_asterisco_no_es_valido(self):
        self.assertRaises(ValueError, self.buscador.buscar, "*")

    def test_un_patron_con_solo_asteriscos_no_es_valido(self):
        self.assertRaises(ValueError, self.buscador.buscar, "***")

    def test_un_patron_con_un_asterisco_al_inicio_es_valido(self):
        self.assertIsInstance(self.buscador.buscar("*los"), set)

    def test_un_patron_con_un_asterisco_al_medio_es_valido(self):
        self.assertIsInstance(self.buscador.buscar("en*los"), set)

    def test_un_patron_con_un_asterisco_al_final_es_valido(self):
        self.assertIsInstance(self.buscador.buscar("en*"), set)

    def test_un_patron_sin_asterisco_es_valido(self):
        self.assertIsInstance(self.buscador.buscar("entre"), set)

    def test_una_busqueda_literal(self):
        self.assertEqual(self.buscador.buscar("cantor"), {0})

    def test_una_busqueda_con_prefijo(self):
        self.assertEqual(self.buscador.buscar("c*"), {0, 1})

    def test_una_busqueda_con_sufijo(self):
        self.assertEqual(self.buscador.buscar("*cion"), {1, 2})

    def test_una_busqueda_con_prefijo_y_sufijo(self):
        self.assertEqual(self.buscador.buscar("o*on"), {2})


if __name__ == '__main__':
    unittest.main()

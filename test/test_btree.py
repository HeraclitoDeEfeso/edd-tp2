# -*- coding: utf-8 -*-
"""Test unitarios para la clase jugador."""

import unittest
from buscador.btree import BTree


class BTree_test(unittest.TestCase):

    def setUp(self):
        # Se crea un arbol de orden 3 para realizar las pruebas
        self.arbol = BTree(3)
        self.b = BTree(3)
        self.b.add(2, "A"), self.b.add(2, "b"), self.b.add(2, "c"), self.b.add(2, "d")
        self.b.add(12, 48), self.b.add(4, 46), self.b.add(3, 22220), self.b.add(123, 13213)
        self.b.add(13, 1321321), self.b.add(1, 446), self.b.add(12, "dfgdg"), self.b.add(12, "dfgdg")
        self.b.add(5, 4646), self.b.add(6, 498412), self.b.add(9, 465464), self.b.add(17, 45461)
        self.b.add(18, "J"), self.b.add(13, 22220), self.b.add(1123, 13213), self.b.add(113, 1321321)
        self.b.add(11, 446), self.b.add(112, "dfgdg"), self.b.add(20, "dfgdg"), self.b.add(15, 4646)
        self.b.add(16, 498412), self.b.add(19, 465464), self.b.add(17, 45461), self.b.add(18, "J")

    def test_se_puede_crear_un_arbol_de_cualquier_orden_mayor_a_uno(self):
        self.arbol = BTree(3)
        self.arbol = BTree(4)
        self.arbol = BTree(5)
        self.arbol = BTree(10)
        self.arbol = BTree(994464)
        self.arbol = BTree(466131)

    def test_no_se_puede_crear_un_arbol_de_orden_menor_a_dos(self):
        with self.assertRaises(ValueError):
            BTree(1)

    def test_verificando_add_y_get(self):
        self.arbol.add("alfonso", 46)
        self.arbol.add("alfonso", 6)
        self.arbol.add("alfonso", 4)
        self.arbol.add("alfonso", 64)
        self.assertEqual([46, 6, 4, 64], self.arbol.get("alfonso"))

    """los arboles de oprden 3 splitean al llegar a 5 keys(2*3-1)"""

    def test_verificando_que_el_arbol_splitea_correctamente(self):
        self.arbol.add(1, 5)
        self.arbol.add(2, 5)
        self.arbol.add(3, 4)
        self.arbol.add(4, 5)
        self.arbol.add(5, 5)
        self.arbol.add(6, 5)
        self.assertEqual([3], self.arbol.raiz.keys)
        self.assertEqual([[1, 2], [3, 4, 5, 6]], self.arbol.get_hojas())

    def test_verificando_que_el_arbol_resista_una_gran_cantidad_de_datos(self):
        self.assertEqual([[1, 2, 3], [4, 5, 6, 9, 11], [12, 13, 15, 16], [17, 18], [19, 20, 112], [113, 123, 1123]],
                         self.b.get_hojas())

    def test_verificando_que_el_arbol_matenga_las_correspondientes_listas_en_arboles_extensos(self):
        self.assertEqual([46], self.b.get(4))
        self.assertEqual(['A', 'b', 'c', 'd'], self.b.get(2))
        self.assertEqual(["dfgdg"], self.b.get(112))

    def test_verificando_que_no_aparezca_dos_veces_el_mismo_documento_en_la_lista(self):
        self.arbol.add(1, "1 sola vez")
        self.arbol.add(1, "otro")
        self.arbol.add(1, "1 sola vez")
        self.assertEqual(["1 sola vez", "otro"], self.arbol.get(1))

    def test_verificando_que_el_Get_de_una_palabra_que_no_esta_en_el_arbol_imprime_un_aviso(self):
        self.assertEqual("'hola' is not in list", str(self.arbol.get("hola")))

    def test_verificando_que_el_get_slice_devuelva_los_elementos_en_el_rango_debido(self):
        self.assertEqual([1,2,3,4], self.b.get_Slice(1,5))
        self.assertEqual([1, 2, 3, 4, 5, 6, 9, 11, 12, 13, 15, 16, 17, 18, 19, 20, 112, 113], self.b.get_Slice(1,120))
        self.assertEqual([17, 18, 19, 20, 112, 113], self.b.get_Slice(17, 120))
        self.assertEqual([3, 4], self.b.get_Slice(3, 5))
        self.assertEqual([6, 9, 11, 12, 13, 15, 16], self.b.get_Slice(6, 17))
        self.assertEqual([12, 13, 15, 16, 17, 18], self.b.get_Slice(12, 19))
        self.assertEqual([17, 18, 19, 20], self.b.get_Slice(17, 112))

    def test_al_pedir_un_slice_con_un_inicio_mayor_al_final_devuelve_un_valueError(self):
        with self.assertRaises(ValueError):
            self.b.get_Slice(5, 1)

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], verbosity=2, exit=False)

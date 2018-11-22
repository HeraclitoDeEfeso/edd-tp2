import unittest
import os
from multiprocessing import Process
from datetime import datetime, timedelta
from buscador.crawler import Crawler, es_direccion_relativa
from buscador.inverted_index import Control
from test.server import run


class TestCrawlerDetenido(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Desde el directorio raiz del proyecto avanzar hasta el directorio con las páginas
        os.chdir(os.path.join(os.getcwd(),"test", "pages"))
        # Correr un web server en un proceso para no bloquear los test
        cls.proceso = Process(target=run)
        cls.proceso.start()
        # Correr el crawler
        cls.crawler = Crawler(Control(), ["http://localhost:8000"], "bitacora.log", 1000)
        cls.crawler.iniciar()
        # Parsear cada entrada al log como lista de listas ['Crawler','iniciado','[00-00-0000 00:00:00,000]']
        with open(cls.crawler.archivo_log, "r") as log:
            cls.log = [palabras[:-2] + [" ".join(palabras[-2:])]
                       for palabras in [linea.split() for linea in log]]
        # Obtener las páginas completas, las visitadas y sus tiempos para los test
        cls.paginas_completas = []
        cls.paginas_visitadas = []
        cls.tiempos = []
        for entrada in cls.log:
            if len(entrada) == 2:
                cls.paginas_visitadas.append(entrada[0])
                cls.tiempos.append(datetime.strptime(entrada[1], "[%Y-%m-%d %H:%M:%S,%f]"))
            elif entrada[1] == "completa":
                cls.paginas_completas.append(entrada[0])
        # Estructura de links esperada segun las paginas del test
        cls.paginas = {
            "http://localhost:8000": ["http://localhost:8000/ala-bueno.html",
                                      "http://localhost:8000/cabra-mar.html",
                                      "http://localhost:8000/nube-tierra.html",
                                      "http://localhost:8000/uva-zinc.html"],
            "http://localhost:8000/ala-bueno.html": [],
            "http://localhost:8000/cabra-mar.html": ["http://localhost:8000/cabra-foca.html",
                                                     "http://localhost:8000/gato-mar.html"],
            "http://localhost:8000/nube-tierra.html": ["http://localhost:8000/nube-puerta.html",
                                                       "http://localhost:8000/queso-tierra.html"],
            "http://localhost:8000/uva-zinc.html": [],
            "http://localhost:8000/cabra-foca.html": [],
            "http://localhost:8000/gato-mar.html": [],
            "http://localhost:8000/nube-puerta.html": [],
            "http://localhost:8000/queso-tierra.html": []}

    @classmethod
    def tearDownClass(cls):
        cls.proceso.terminate()

    def test_completada_una_pagina_se_han_recorrido_todos_sus_enlaces(self):
        paginas_completas = {entrada[0] for entrada in self.log if entrada[1] == "completa"}
        self.assertTrue(paginas_completas.issuperset(sum(map(self.paginas.get, paginas_completas), [])))

    def test_solo_se_visitan_enlaces_dentro_de_la_frontera(self):
        self.assertTrue(all(es_direccion_relativa("http://localhost:8000", pagina)
                            for pagina in self.paginas_visitadas))

    def test_los_enlaces_se_visitan_solo_una_vez(self):
        self.assertEqual(len(self.paginas_visitadas), len(set(self.paginas_visitadas)))

    def test_entre_visita_y_visita_se_respeta_el_tiempo_minimo(self):
        duracion = timedelta(0, 0, 0, self.crawler.tmin)
        self.assertTrue(all(self.tiempos[posicion + 1] - tiempo > duracion
                            for posicion, tiempo in enumerate(self.tiempos[:-1])))

    def test_se_han_visitado_todos_los_sitios_de_la_frontera(self):
        self.assertTrue(set(self.crawler.dominios).issubset(self.paginas_visitadas))


if __name__ == '__main__':
    unittest.main()

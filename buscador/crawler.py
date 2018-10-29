from buscador.inverted_index import Control
class Crawler(object):
    """
    La clase `Crawler` representa el robot que busca los
    encales en las páginas del dominio asignado de manera
    recursiva
    """
    def __init__(self, control, dominios):
        self.controlador = control
        self.dominios = dominios
        self.direcciones_procesadas = []
        self.direcciones_sin_procesar = dominios[:]

    def detener(self):
        """
        Detiene el proceso recursivo de recorrer los enlaces
        de una pagina y obtener aquellas a las que apuntan
        """
        pass
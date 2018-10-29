class Direccion(object):
    """
    La clase `Direccion` sirve para representar las
        direcciones de los documentos encontrados al
        recorrer las páginas.
    """
    def __init__(self, url):
        self.url = url

    def es_relativa(self, direccion):
        """
        El método indica si la dirección es relativa
        con respecto de otra que se pasa por parámetro
        :param direccion: otra `Direccion` que se espera sea relativa
        :return: el `bool` `True` si la dirección es relativa
        """
        pass

class Documento(object):
    """
    La clase `Documento` sirve para representar los
    documentos encontrados al recorrer los enlaces de
    las páginas
    """
    def __init__(self, direccion, contenido):
        self.direccion = direccion
        self.contenido = contenido
from urllib.parse import urlsplit, urlunsplit
class Documento(object):
    """
    La clase `Documento` sirve para representar los
    documentos encontrados al recorrer los enlaces de
    las páginas
    """

    def __init__(self, direccion, contenido):
        self.direccion = direccion
        self.contenido = contenido


def es_direccion_relativa(dominio, direccion):
    """
    La función indica si la `dirección` es relativa
    con respecto de un `dominio`
    :param dominio: una cadena de caracteres
    :param direccion: una cadena de caracteres
    :return: bool `True` si `direccion` es relativa al `dominio`
    """
    return urlsplit(dominio)[:2] == urlsplit(direccion)[:2]


def limpiar_direccion(direccion):
    """
    La función elimina parámetros (query strings) y enlaces internos
    (fragment identifiers) de `direccion`
    :param direccion: una cadena de caracteres
    :return: una cadena de caracteres que representa la dirección limpia
    """
    return urlunsplit(urlsplit(direccion)[:3] + ('',''))

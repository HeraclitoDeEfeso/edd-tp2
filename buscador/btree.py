class BTree(object):
    """
    Esta es una mala implementación de un Árbol-B utilizando
    un diccionario
    """
    def __init__(self):
        self.datos = {}

    def add(self, palabra, documento):
        """
        Agrega la `palabra` al árbol con una referencia al
        `documento` que la contenía. Si ya existía la palabra
        en el árbol, agrega sola la referencia al `documento`.
        :param palabra: una cadena de caracteres
        :param documento: un `Documento`
        """
        if palabra in self.datos:
            self.datos[palabra].add(documento)
        else:
            self.datos[palabra] = {documento,}

    def get(self, palabra):
        """
        Obtiene las referencias a los documentos que contenían
        la `palabra` buscada. En caso de no existir la palabra
        devuelve un set vacío.
        :param palabra: una cadena de carcateres
        :return: un set de `Documento`
        """
        if palabra in self.datos:
            return self.datos[palabra]
        else:
            return set()
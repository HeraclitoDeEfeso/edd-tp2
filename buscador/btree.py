class BTree(object):
    """
    Esta es una mala implementación de un Árbol-B utilizando un diccionario
    """
    #TODO: Un verdadero Árbol B+
    def __init__(self):
        self.datos = {}

    def add(self, palabra, documento):
        """
        Agrega la `palabra` al árbol con una referencia al `documento` que la contenía.
        Si ya existía la palabra en el árbol, agrega solo la referencia al `documento`.
        :param palabra: una cadena de caracteres
        :param documento: un número como referencia al documento
        """
        if palabra in self.datos:
            self.datos[palabra].add(documento)
        else:
            self.datos[palabra] = {documento,}

    def get(self, palabra):
        """
        Obtiene las referencias a los documentos que contenían la `palabra` buscada.
        En caso de no existir la palabra devuelve un set vacío.
        :param palabra: una cadena de carcateres
        :return: un set de números como referencias a documentos
        """
        if palabra in self.datos:
            return self.datos[palabra]
        else:
            return set()
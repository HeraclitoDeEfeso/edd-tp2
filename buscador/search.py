class Buscador(object):
    """
    Esta clase recoge todas las funciones de búsqueda
    sobre los índices invertidos `Indexer` sobre los que
    particiona las palabras el `Control`
    """
    def __init__(self, controlador):
        """
        Constructor de un `Buscador`
        :param controlador: un `Control` que particiona las palabras sobre diverson índices
        """
        self.controlador = controlador

    def buscar(self, patron_palabra):
        """
        Este método busca los documentos que contienen una palabra que se ajusta
        al `patron_palabra`.
        Un patrón de palabra admite una sola ocurrencia de entre cualquiera de los
        siguientes wildcards:
            * indica una cantidad indeterminada de cualesquiera caracteres (incluyendo cero)
            . indica una sola y necesaria presencia de un caracter cualquiera
        :param patron_palabra: cadena de caracteres que representa un patron de palabras
        :return: un set de `Documento`
        """
        # Se debe implementar el parseo de un patrón:
        #   - comprobar que exista un sólo wildcard
        #   - buscar en el índice normal el prefijo hasta el wildcard
        #   - buscar en el índice reverso el sufijo desde el wildcard
        #   - filtrar de las palabras recuperadas aquellas que cumplan con el tamaño
        #     según el wildcard: para el punto es el largo del sufijo más el prefijo
        #     más uno, y para el asterisco al menos el largo del prefijo más el sufijo
        # Mientras tanto devolvemos los documentos que tienen la palabra exacta
        return self.controlador.obtener_indice(patron_palabra).obtener_documentos(patron_palabra)

    def busqueda_conjuntiva(self, patron_palabra, documentos):
        """
        Agrega al conjunto de `documentos` aquellos que también estén
        en el índice y contengan el `patron_palabra`
        :param patron_palabra: una cadena de caracteres
        :param documentos: un `set` de `Documento`
        :return: un `set` de `Documento`
        """
        return documentos.union(self.buscar(patron_palabra))

    def busqueda_disjuntiva(self, patron_palabra, documentos):
        """
        Elimina del conjunto de `documentos` aquellos que no contengan
        el `patron_palabra`
        :param patron_palabra: una cadena de caracteres
        :param documentos: un `set` de `Documento`
        :return: un `set` de `Documento`
        """
        return documentos.intersection(self.buscar(patron_palabra))

    def busqueda_negativa(self, patron_palabra, documentos):
        """
        Elimina del conjunto de `documentos` aquellos que contengan
        el `patron_palabra`
        :param patron_palabra: una cadena de caracteres
        :param documentos: un `set` de `Documento`
        :return: un `set` de `Documento`
        """
        return documentos.difference(self.buscar(patron_palabra))

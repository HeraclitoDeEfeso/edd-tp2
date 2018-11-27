import re


class Buscador(object):
    """
    Esta clase recoge todas las funciones de búsqueda
    sobre los índices invertidos `Indexer` sobre los que
    particiona las palabras el `Control`
    """
    max_caracter = chr(ord("z") + 1)

    def __init__(self, controlador):
        """
        Constructor de un `Buscador`
        :param controlador: un `Control` que particiona las palabras sobre diverson índices
        """
        self.controlador = controlador

    def buscar(self, patron_palabra):
        """
        Este método busca los documentos que contienen una palabra que se ajusta al `patron_palabra`.
        Un patrón de palabra admite una sola ocurrencia de entre cualquiera de los siguientes comodines:
            * indica una cantidad indeterminada (incluyendo cero) de cualesquiera caracteres
        :param patron_palabra: cadena de caracteres que representa un patron de palabras
        :return: un set de enteros que corresponden a los identificadores de documentos
        """
        return set().union(*map(self.buscar_documentos,
                                self.buscar_por_patron(self.interpreta_patron(patron_palabra))))

    def interpreta_patron(self, patron):
        """
        Este método es el encargado de interpretar un `patron` y devolver una tupla que el
        método `buscar_claves` sea capáz de utilizar. Utiliza la excepción `ValueError` en
        caso que el patrón sea inválido.
        :param patron: una cadena de caracteres
        :return: una tupla
        """
        match = re.match(r"^(\w*)(\*?)(\w*)$", patron)
        if match and (match.group(1) or match.group(3)):
            # El patrón es válido
            return match.groups()
        else:
            # El patrón es inválido
            raise ValueError("El patrón de búsqueda '%s' no es válido." % patron)

    def buscar_por_patron(self, tupla):
        """
        Éste método interpreta una estructura de tupla que representa un patrón y devuelve las
        palabras encontradas en los documentos que cumplen con el patrón representado
        :param tupla: una tupla como estructura que expresa un patrón
        :return: una lista de cadena de caracteres que representan palabras
        """
        if tupla[1]:
            # Existe comodín
            prefijos = [] if not tupla[0] else self.buscar_palabras(tupla[0], tupla[0] + self.max_caracter)
            sufijos = [] if not tupla[2] else self.buscar_palabras_reversas(tupla[2], self.max_caracter + tupla[2])
            if tupla[0] and tupla[2]:
                # Si consultó por prefijo y sufijo, devolver las palabras coincidentes
                return [palabra for palabra in prefijos if palabra in sufijos]
            else:
                # Si consultó sólo por prefijos o sólo por sufijos, devolver todas la palabras
                return prefijos + sufijos
        else:
            # El primer elemento de la tupla contiene la palabra literal por la que buscar
            return [tupla[0]]

    def buscar_palabras(self, inicio, fin, indices=None):
        """
        El método devuelve todas las palabras que han sido claves de los `indices` y que están
        en orden alfanumérico igual o mayor a la palabra `inicio` y menor extricto a la palabra `fin`.
        :param inicio: una cadena de caracteres
        :param fin: una cadena de caracteres
        :param indices: una lista de `Indexer`
        :return: una lista de cadenas de caracteres
        """
        # Por defecto, los índices son los de palabras sin revertir
        if not indices:
            indices = self.controlador.obtener_indices(inicio, fin)
        return [palabra for indice in indices for palabra in indice.buscar_palabras(inicio, fin)]

    def buscar_palabras_reversas(self, inicio, fin):
        """
        El método devuelve todas las palabras que han sido claves de los indices reversos y que están
        en orden alfanumérico igual o mayor a la palabra `inicio` y menor extricto a la palabra `fin`
        :param inicio: una cadena de caracteres
        :param fin: una cadena de caracteres
        :return: una lista de cadenas de caracteres
        """
        inicio = inicio[::-1]
        fin = fin[::-1]
        return [palabra[::-1] for palabra
                in self.buscar_palabras(inicio, fin, self.controlador.obtener_indices_reversos(inicio, fin))]

    def buscar_documentos(self, palabra):
        return self.controlador.obtener_indice(palabra).obtener_documentos(palabra)

    def busqueda_conjuntiva(self, patron_palabra, documentos):
        """
        Agrega al conjunto de `documentos` aquellos que también estén
        en el índice y contengan el `patron_palabra`
        :param patron_palabra: una cadena de caracteres
        :param documentos: un `set` de enteros. Representan identificadores de documentos
        :return: un `set` de enteros. Representan identificadores de documentos
        """
        return documentos.union(self.buscar(patron_palabra))

    def busqueda_disjuntiva(self, patron_palabra, documentos):
        """
        Elimina de la lista de `documentos` aquellos que no contengan el `patron_palabra`
        :param patron_palabra: una cadena de caracteres
        :param documentos: un `set` de enteros. Representan identificadores de documentos
        :return: un `set` de enteros. Representan identificadores de documentos
        """
        return documentos.intersection(self.buscar(patron_palabra))

    def busqueda_negativa(self, patron_palabra, documentos):
        """
        Elimina del conjunto de `documentos` aquellos que contengan el `patron_palabra`
        :param patron_palabra: una cadena de caracteres
        :param documentos: un `set` de enteros. Representan identificadores de documentos
        :return: un `set` de enteros. Representan identificadores de documentos
        """
        return documentos.difference(self.buscar(patron_palabra))

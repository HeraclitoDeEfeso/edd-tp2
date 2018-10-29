from buscador.btree import BTree
class Control(object):
    """
    La clase `Control` sirve para representar el objeto que
    distribuye el trabajo entre los documentos que obtiene
    el `Crawler` los que son distribuidos a los `Tokenizer`
    para obtener las palabras que luegos serán indexadas por
    los `Indexer`
    """
    def __init__(self, separadores=None, indexadores=None):
        # Mientras no implementemos las particiones
        # utilizamos un solo tokenizer y un solo índice
        self.map = separadores if separadores != None else Tokenizer()
        self.reduce = indexadores if indexadores != None else Indexer()
        self.documentos = []
        self.documentos_sin_procesar = []

    def procesar_documento(self, documento):
        """
        Este es el método que llama el `Crawler` para que
        el `Control` distribuya el trabajo que debe
        realizarse sobre un documento recuperado
        :param documento: `Documento` con la página recuperada
        """
        pass

    def obtener_indice(self, palabra):
        """
        Este método es utilizado por el `Buscador` para
        obtener el `Indexer` que debiera mantener el
        índice invertido que contiene la `palabra`
        :param palabra: un string con la palabra indexada
        :return: el `Indexer` que mantiene el índice invertido
        """
        # Mientras no tengamos implementadas las particiones
        # usamos un único índice
        return self.reduce

class Tokenizer(object):
    """
    Esta clase es la encargada de obtener las palabras de los
    documentos recuperados por el `Crawler`
    """
    def obtener_palabras(self, documento):
        """
        Este método devuelve una lista de palabras recuperadas
        del `documento`
        :param documento: un `Documento` ya recuperado por el `Crawler`
        :return: una lista de cadenas de caracteres representando las palabras
        """
        # Falta implementar el stemming y el filtro de palabras básicas
        return documento.contenido.split(r'\W')

class Indexer(object):
    """
    Esta es la clase encargado de mantener el índice invertido con
    las palabras encontradas en los documentos recuperados por el
    `Crawler`
    """
    def __init__(self):
        self.indice = BTree()

    def agregar_palabra(self, palabra, documento):
        """
        Agrega la `palabra` al índice invertido con una referencia
        al `documento`
        :param palabra: una cadena de caracteres que representa una palabra
        :param documento: una referencia al `Documento` que contenía la palabra
        """
        self.indice.add(palabra, documento)

    def obtener_documentos(self, palabra):
        """
        Método que devuelve las referencias a los documentos que
        contenienen la `palabra`
        :param palabra: una cadena de caracteres que representa la palabara
        :return: una lista de referencias de `Documento` que contienen la palabra
        """
        return self.indice.get(palabra)

    def palabras_mayores(self, palabra):
        """
        Este método devuelde todas las palabras que se encuentran en el índice
        y que proceden a `palabra` en orden alfabético
        :param palabra: una cadena de caracteres
        :return: una lista con cadenas de caracters que representan cada palabra
        """
        pass

    def palabras_menores(self, palabra):
        """
        Este método devuelde todas las palabras que se encuentran en el índice
        y que preceden a `palabra` en orden alfabético
        :param palabra: una cadena de caracteres
        :return: una lista con cadenas de caracters que representan cada palabra
        """
        pass

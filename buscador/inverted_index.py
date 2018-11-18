import re
from nltk.stem.snowball import SpanishStemmer
from nltk.corpus import stopwords
from buscador.btree import BTree


class Tokenizer(object):
    """
    Esta clase es la encargada de obtener las palabras de los
    documentos recuperados por el `Crawler`
    """
    def __init__(self):
        self.stemmer = SpanishStemmer()

    def obtener_palabras(self, contenido, min_long=5):
        """
        Este método devuelve una lista de palabras recuperadas del `contenido`
        :param documento: una cadena con el contenido de texto del documento
        :return: una lista de cadenas de caracteres representando las palabras
        """
        #Realizo el stemming en todo el contenido. Eliminando acentos mayusculas y dejando las raices.
        cont_stemed = self.stemmer.stem(contenido)
        #Divido el texto por palabras eliminando las repetidas
        conjunto_palabras = set(re.split(r'\W+', cont_stemed))
        #Elimino Stopwords, palabras menores a min_long y retorno lista
        return [palabra for palabra in conjunto_palabras if palabra not in stopwords.words('spanish') && not len(palabra) < min_long]

                        

        return sorted(set(re.split(r'\W+', contenido)))


class Indexer(object):
    """
    Esta es la clase encargado de mantener el índice invertido con
    las palabras encontradas en los documentos recuperados por el
    `Crawler`
    """

    def __init__(self):
        self.indice = BTree()

    def agregar_palabras(self, palabras, documento):
        """
        Agrega las `palabras` al índice invertido con una referencia al `documento`
        :param palabras: una lista de cadenas de caracteres que representan palabras
        :param documento: un número que referencia al documento que contenía las palabras
        """
        for palabra in palabras:
            self.indice.add(palabra, documento)

    def obtener_documentos(self, palabra):
        """
        Método que devuelve las referencias a los documentos que contenienen la `palabra`
        :param palabra: una cadena de caracteres que representa la palabra
        :return: una lista de números como referencias a documentos
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


class Control(object):
    """
    La clase `Control` sirve para representar el objeto que
    distribuye el trabajo entre los documentos que obtiene
    el `Crawler` los que son distribuidos a los `Tokenizer`
    para obtener las palabras que luegos serán indexadas por
    los `Indexer`
    """

    def __init__(self, separadores=None, indexadores=None):
        # TODO: Particiones
        # Mientras no implementemos las particiones utilizamos un tokenizer y un índice
        self.map = separadores if separadores else Tokenizer()
        self.reduce = indexadores if indexadores else Indexer()
        self.documentos = []

    def procesar_documento(self, direccion, contenido):
        """
        Este es el método que llama el `Crawler` para que el `Control`
        distribuya el trabajo que debe realizarse sobre un documento
        recuperado de la `direccion` y con el `contenido` de texto
        :param direccion: una cadena de caracteres
        :param contenido: una cadena de caracteres
        """
        self.documentos.append(direccion)
        self.reduce.agregar_palabras(self.map.obtener_palabras(contenido), len(self.documentos) - 1)

    def obtener_indice(self, palabra):
        """
        Este método es utilizado por el `Buscador` para
        obtener el `Indexer` que debiera mantener el
        índice invertido que contiene la `palabra`
        :param palabra: un string con la palabra indexada
        :return: el `Indexer` que mantiene el índice invertido
        """
        # Mientras no tengamos implementadas las particiones usamos un único índice
        return self.reduce

import re
from nltk.stem.snowball import SpanishStemmer
from nltk.corpus import stopwords
from buscador.btree import BTree


class Tokenizer(object):
    """
    Esta clase es la encargada de obtener las palabras de los
    documentos recuperados por el `Crawler`
    """

    def __init__(self, min_long=5):
        """
        Para inicializar un `Tokenizer` es necesario saber el tamaño mínimo de caracteres
        `min_long`. que constituyen una palabra válidad
        :param min_long: un entero. Por defecto igual a cinco (5)
        """
        self.stemmer = SpanishStemmer()
        self.min_long = min_long

    def obtener_palabras(self, contenido):
        """
        Este método devuelve una lista de palabras recuperadas del `contenido`
        :param contenido: una cadena con el contenido de texto del documento
        :return: una lista de cadenas de caracteres representando las palabras
        """
        # Realizo el stemming en todo el contenido. Eliminando acentos mayusculas y dejando las raices.
        cont_stemed = self.stemmer.stem(contenido)
        # Divido el texto por palabras eliminando las repetidas
        conjunto_palabras = set(re.split(r'\W+', cont_stemed))
        # Elimino Stopwords, palabras menores a min_long y retorno lista
        return [palabra for palabra in conjunto_palabras if
                palabra not in stopwords.words('spanish') and not len(palabra) < self.min_long]


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
        :return: un lista de números como referencias a documentos
        """
        resultado = self.indice.get(palabra)
        # TODO: El árbol B debería arrojar una excepción con `raice` no devolver el objeto excepción
        if isinstance(resultado, ValueError):
            return []
        return resultado

    def buscar_palabras(self, inicio, fin):
        return self.indice.get_Slice(inicio, fin)


class Control(object):
    """
    La clase `Control` sirve para representar el objeto que
    distribuye el trabajo entre los documentos que obtiene
    el `Crawler` los que son distribuidos a los `Tokenizer`
    para obtener las palabras que luegos serán indexadas por
    los `Indexer`
    """

    def __init__(self, separadores=None, indexadores=None, indices_reversos=None):
        self.map = separadores if separadores else Tokenizer()
        self.reduce = indexadores if indexadores else Indexer()
        self.indices_reversos = indices_reversos if indices_reversos else Indexer()
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
        documento = len(self.documentos) - 1
        palabras = self.map.obtener_palabras(contenido)
        self.reduce.agregar_palabras(palabras, documento)
        self.indices_reversos.agregar_palabras([palabra[::-1] for palabra in palabras], documento)

    def obtener_indice(self, palabra):
        """
        Éste método devuelve el indices que deberían contener la `palabra` según como se haya
        particionado el conjunto de índices
        :param palabra: una cadena de caracteres
        :return: un `Indexer`
        """
        # TODO: mientras no se implementen las particiones trabajamos con índices únicos
        return self.reduce

    def obtener_indices(self, inicio, final):
        """
        Éste método devuelve todos los indices en que se deberían haber particionado las palabras
        en la palabra `inicio` y la palabra `final` en orden alfabético.
        :param inicio: una cadena de caracteres
        :param final: una cadena de caracteres
        :return: una lista de `Indexer`
        """
        # TODO: mientras no se implementen las particiones trabajamos con índices únicos
        return [self.reduce]

    def obtener_indices_reversos(self, inicio, final):
        """
        Éste método devuelve todos los indices en que se deberían haber particionado las palabras
        invertidas entre la palabra `inicio` y la palabra `final` en orden alfabético.
        :param inicio: una cadena de caracteres
        :param final: una cadena de caracteres
        :return: una lista de `Indexer`
        """
        # TODO: mientras no se implementen las particiones trabajamos con índices únicos
        return [self.indices_reversos]

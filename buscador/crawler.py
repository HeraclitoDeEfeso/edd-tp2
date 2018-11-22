from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
from urllib.parse import urlsplit, urlunsplit
import logging
import signal
import time


class LinkParser(HTMLParser):
    """
    Esta clase modela un parser de una página HTML.
    Se reutiliza y modifica la implementación ofrecida
    en el enunciado del TP.
    """

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newURL = parse.urljoin(self.baseURL, value)
                    self.links.append(newURL)

    def handle_data(self, data):
        # No se toman en cuenta los nodos Texto de los elementos `script` o `style`
        if self.lasttag != 'style' and self.lasttag != 'script':
            self.string_content += " " + data

    def fetch_page(self, url):
        """
        Método por el que se accede a una página cuya dirección es `url`
        y se la procesa con el parser HTML obtiendo sus enlaces y la
        concatenación de los nodos texto ('DOM Node.textContent').
        :param url: una cadena de caracteres que representa la dirección
        :return: una tupla con una cadena de caracteres (textContent) \
        y una lista de cadenas de caracteres representando los enlaces
        """
        self.string_content = ""
        self.links = []
        self.baseURL = url
        response = urlopen(url)
        contentType = response.getheader('Content-type')
        if 'text/html' in contentType:
            encoding = response.headers.get_param('charset')
            data = response.read()
            htmlString = data.decode(encoding) if encoding else data.decode()
            self.feed(htmlString)
        return self.string_content, self.links


class Crawler(object):
    """
    La clase `Crawler` representa el robot que busca recursivamente
    los enlaces en las páginas dentro de la frontera de dominios asignada
    """

    def __init__(self, control, dominios, log="log.txt", tmin=500):
        """
        Para crear un `Cawler` es necesario un lista de `dominios` que
        compongan su frontera y un `control` al que le pase la páginas
        que deben ser procesadas, un nombre del archivo de `log` donde
        persistirá sus actividades y un tiempo mínimo `tmin` de milisegundos
        entre peticiones de página a un mismo servidor web.
        :param control: un `Control`
        :param dominios: una lista de cadenas de caracteres que representen las direcciones
        :param log: una cadena de caracteres con el nombre del archivo de logging
        :param tmin: un entero que representa milisegundos
        """
        self.controlador = control
        self.dominios = dominios
        self.archivo_log = log
        self.tmin = tmin
        self.direcciones_procesadas = set()
        self.direcciones_sin_procesar = dominios
        self.direcciones_recorridas = []
        self.archivo_modo = "w"

    def iniciar(self):
        """
        El método que inicia la labor del `Crawler` o la
        continúa después de haber sido detenido
        """
        # Instanciar un parser
        parser = LinkParser()
        # Instanciar un logger
        logger = logging.getLogger("crawler")
        logger.setLevel(logging.INFO)
        log_handler = logging.FileHandler(self.archivo_log, self.archivo_modo)
        log_handler.setLevel(logging.INFO)
        log_handler.setFormatter(logging.Formatter('%(message)s [%(asctime)s]'))
        logger.addHandler(log_handler)
        logger.info("Crawler iniciado")
        # Instanciar un handler de CONTROL-C
        salir_original = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, lambda x, y: self.__salir__())
        # Inicializar un tiempo de referencia y una bandera de salida
        tiempo = time.monotonic()
        self.salir = False
        while self.direcciones_sin_procesar and not self.salir:
            direccion = self.direcciones_sin_procesar[-1]
            if not self.direcciones_recorridas \
                    or self.direcciones_recorridas[-1] != direccion:
                tiempo_restante = self.tmin / 1000 - (time.monotonic() - tiempo)
                if tiempo_restante > 0:
                    time.sleep(tiempo_restante)
                contenido, enlaces = parser.fetch_page(direccion)
                logger.info(direccion)
                self.controlador.procesar_documento(direccion, contenido)
                self.direcciones_procesadas.add(direccion)
                self.direcciones_recorridas.append(direccion)
                self.direcciones_sin_procesar.extend(
                    filter(self.direccion_no_procesada,
                           filter(self.direccion_en_frontera,
                                  map(limpiar_direccion, enlaces))))
            else:
                self.direcciones_sin_procesar.pop()
                self.direcciones_recorridas.pop()
                logger.info(direccion + " completa")
        logger.info("Crawler finalizado")
        self.archivo_modo = "a"
        signal.signal(signal.SIGINT, salir_original)

    def __getstate__(self):
        """
        Este método es parte del protocolo Pickle
        :return: un `dict` con los atributos a persistir
        """
        # Copy the object's state from self.__dict__
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['direcciones_procesadas'], state['direcciones_recorridas']
        return state

    def __setstate__(self, state):
        """
        Éste método es parte del protocolo Pickle
        :param state: un `dict` con los atributos que han persistido
        """
        # Restore instance attributes.
        self.__dict__.update(state)
        self.direcciones_procesadas = set()
        self.direcciones_recorridas = []
        # Restore the previously state.
        try:
            with open(self.archivo_log, "r") as log:
                for linea in log:
                    palabras = linea.split()
                    if len(palabras) == 3:
                        self.direcciones_procesadas.add(palabras[0])
                        self.direcciones_recorridas.append(palabras[0])
                    elif len(palabras) == 4 and palabras[1] == "completa":
                        if self.direcciones_recorridas[-1] == palabras[0]:
                            self.direcciones_recorridas.pop()
                        else:
                            raise ValueError("Archivo de log %s corrupto" % self.archivo_log)
        except FileNotFoundError:
            pass

    def direccion_en_frontera(self, direccion):
        """
        Éste método informa si `direccion` está en la frontera asignada al `Crawler`
        :param direccion: una `Direccion`
        :return: bool
        """
        return any(map(lambda x: es_direccion_relativa(x, direccion), self.dominios))

    def direccion_no_procesada(self, direccion):
        """
        Éste método informa si la `direccion` ya ha sido
        procesada por el `Crawler`
        :param direccion: una `Direccion`
        :return: bool
        """
        return direccion not in self.direcciones_procesadas

    def __salir__(self):
        """
        Manejador de la señal de CTRL-C. Simplemente setea un bool.
        """
        self.salir = True


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
    return urlunsplit(urlsplit(direccion)[:3] + ('', ''))

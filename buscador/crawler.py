from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
import logging
from buscador import limpiar_direccion, es_direccion_relativa


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

    def __init__(self, control, dominios, log):
        """
        Para crear un `Cawler` es necesario un lista de `dominios` que
        compongan su frontera y un `control` al que le pase la páginas
        que deben ser procesadas
        :param control: un `Control`
        :param dominios: una lista de cadenas de caracteres que representen las direcciones
        :param log: una cadena de caracteres con el nombre del archivo de logging
        """
        self.controlador = control
        self.dominios = dominios
        self.archivo_log = log
        self.recuperar()

    def iniciar(self):
        """
        El método que inicia la labor del `Crawler` o la
        continúa después de haber sido detenido
        """
        self.registrar()
        logging.info("Crawler iniciado")
        while self.direcciones_sin_procesar:
            direccion = self.direcciones_sin_procesar[-1]
            if not self.direcciones_recorridas \
                    or self.direcciones_recorridas[-1] != direccion:
                logging.info(direccion)
                contenido, enlaces = LinkParser().fetch_page(direccion)
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
                logging.info(direccion + " completa")
        self.detener()

    def detener(self):
        """
        El método que detiene la labor del `Crawler` y lo
        deja en un estado conocido para que pueda ser reiniciado
        """
        logging.info("Crawler finalizado")
        self.almacenar()
        self.desregistrar()

    def recuperar(self):
        """
        El método que recupera los datos almacenados al detener el `Crawler`
        """
        # TODO: recuperación desde el logging
        # Mientras tanto el Crawler comienza siempre desde cero
        self.direcciones_procesadas = set()
        self.direcciones_sin_procesar = []
        self.direcciones_recorridas = []
        self.direcciones_sin_procesar = self.dominios[:]
        # TODO: formatear el loggin
        logging.basicConfig(filename=self.archivo_log, level=logging.INFO)

    def almacenar(self):
        """
        El método que almacena los datos del estado del `Crawler` para poder
        reiniciar el proceso donde se detuvo
        :return:
        """
        # TODO: Persistencia del Crawler
        pass

    def registrar(self):
        """
        El método que registra un manejador para la señal de sistema CTRL-C
        """
        # TODO: Captura de la interrupción por teclado
        pass

    def desregistrar(self):
        """
        El método que elimina el manejador para la señal de sistema CTRL-C
        """
        pass

    def direccion_en_frontera(self, direccion):
        """
        Éste método informa si `direccion` está en la
        frontera asignada al `Crawler`
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
        return not direccion in self.direcciones_procesadas

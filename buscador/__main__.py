from configparser import ConfigParser
from functools import reduce
from sys import stdout
from logging import StreamHandler, getLogger, INFO, Formatter
from pickle import load, dump
from buscador.crawler import Crawler
from buscador.inverted_index import Control, Tokenizer
from buscador.search import Buscador

# Leo el archivo de configuración
# TODO: agregar la opción del nombre del archivo a la línea de comandos
config = ConfigParser()
config.read("config.ini")

# Se crean los objetos de acuerdo a los valores de configuración
# TODO: está pendiente el manejo de los índices invertidos de palabras reversas
try:
    archivo = open("crawler.bin", "rb")
    crawler = load(archivo)
    control = crawler.controlador
    archivo.close()
except OSError:
    control = Control(separadores=Tokenizer(int(config["INVERTED_INDEX"]["min_long"])))
    crawler = Crawler(control,
                      [direccion.encode('utf-8').decode('unicode_escape')
                       for direccion in config["CRAWLER"]["URLs"].split(";")],
                      config["CRAWLER"]["Log"],
                      int(config["CRAWLER"]["Tmin"]))
buscador = Buscador(control)

# Se agrega un manejador del logger del crawler para que se emita la actividad por consola
logger = getLogger("crawler")
log_handler = StreamHandler(stdout)
log_handler.setLevel(INFO)
log_handler.setFormatter(Formatter('%(message)s'))
logger.addHandler(log_handler)

# Ciclo principal
while True:
    crawler.iniciar()
    while True:
        if input("\nDesea realizar una búsqueda [S/N] ?  ").lower() == "s":
            patrones = input(
                "\nIngrese una lista palabras que la página debe contener, separadas por espacio.\n").split()
            documentos = reduce(lambda docs, patron: buscador.busqueda_disjuntiva(patron, docs),
                                patrones[:-1],
                                buscador.buscar(patrones[-1]))
            if documentos:
                print("", *[control.documentos[doc] for doc in documentos], sep="\n")
            else:
                print("\nNo se encontraron documentos con esa palabra")
        else:
            break
    if input("\nDesea salir de la aplicación [S/N] ?  ").lower() == "s":
        with open("crawler.bin", "wb") as archivo:
            dump(crawler, archivo)
        break

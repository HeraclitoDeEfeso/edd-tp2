# edd-tp2
Buscador Web en Python

## Diagrama de Clases
![UML](doc/diagrama.png)

## Requisitos
Para correr la aplicación es necesario instalar la librería
[`nltk`](http://www.nltk.org/) de python. Correr como administrador:

    pip install nltk

En modo consola de Python, correr:

    import nltk
    nltk.download()

Luego de esto se abrirá una ventana, ir a Packages e instalar 
el paquete `stopwords`.

## Ejecucion
El paquete trae una consola básica de ejecución. Lo mismo que 
un archivo de configuración en el directorio raiz del proyecto 
(`config.ini`). Para correrla, ejecutar desde el directorio 
raiz del proyecto:

    python -m buscador
    
## Pruebas
Para correr los test unitarios que vienen con la aplicación debe 
ubicarse en el directorio raiz del proyecto y ejecutar en la línea 
de comandos:

    python -m unittest discover
    
## Implementación

### Módulo `btree`
Éste es el módulo que contiene la implementación del Árbol B. Sus 
detalles se encuentran en la Jupiter notebook [`btree.ipynb`](doc/btree.ipynb)

### Módulo `crawler`
Éste es el módulo que contiene la implementación del robot encargado de recorrer
las páginas. Se ha tomado como base la clase `LinkParser` dada como ejemplo en el 
enunciado del trabajo. Sus detalles se encuentran en la Jupiter notebook
[`crawler.ipynb`](doc/crawler.ipynb)

### Módulo `search`
Éste módulo contiene la implementación de una clase `Buscador` encargada de
exponer una interfaz de alto nivel para las tareas de búsqueda. Sus detalles 
se encuentran en la Jupiter notebook [`search.ipynb`](doc/search.ipynb)

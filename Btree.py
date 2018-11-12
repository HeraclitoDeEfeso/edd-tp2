class BTree(object):
    """BTree de Orden t"""

    class Nodo(object):

        def __init__(self, t):
            self.keys = []  # elementos del nodo
            self.hijo = []  # hijos(otros nodos internos o el contenido de la hoja en caso de serlo)
            self.hoja = True  # me permite saber si sus hijos son otros nodos o datos
            self._t = t  # t = orden

        def split(self, padre, nueva_key):
            """divide el nodo y reasigna keys e hijos,devuelve el nodo que contendra a la nueva key"""
            nuevo_nodo = self.__class__(self._t)
            mitad = self.size // 2
            key_medio = self.keys[mitad]
            padre.agregar_key(key_medio)

            # Agrega las keys y los hijos al nodo correcto,el nuevo nodo siempre contendra las keys mas altas
            nuevo_nodo.hijo = self.hijo[mitad + 1:]
            self.hijo = self.hijo[:mitad + 1]
            nuevo_nodo.keys = self.keys[mitad + 1:]
            self.keys = self.keys[:mitad]

            # Si el nuevo_nodo tiene hijo, es un nodo interno
            if len(nuevo_nodo.hijo) > 0:
                nuevo_nodo.hoja = False

            # Agrega al padre el nuevo nodo con las keys de mayor valor y devuelve el nodo que contendra la nueva key
            padre.hijo = padre.insertar_hijo(nuevo_nodo)
            if nueva_key < key_medio:
                return self
            else:
                return nuevo_nodo

        @property
        def _is_full(self):
            return self.size == 2 * self._t - 1

        @property
        def size(self):
            return len(self.keys)

        def agregar_key(self, valor):
            self.keys.append(valor)
            self.keys.sort()

        def insertar_hijo(self, nuevo_nodo):
            """agrega un hijo al nodo y ordena a todos los hijos.Devuelve una lista ordenada de los nodos hijos"""
            i = len(self.hijo) - 1
            while i >= 0 and self.hijo[i].keys[0] > nuevo_nodo.keys[0]:
                i -= 1
            return self.hijo[:i + 1] + [nuevo_nodo] + self.hijo[i + 1:]

    def __init__(self, t):
        """Crea un arbolb de orden t sin keys.Actualmente permite keys duplicadas"""
        self._t = t
        if self._t <= 1:
            raise ValueError("El orden del arbol debe ser 2 o superior")
        self.raiz = self.Nodo(t)

    def insertar(self, nueva_key):
        """Inserta un key con un valor determinado"""
        nodo = self.raiz
        # El split de la raiz es manejada de forma particular(nuestro metodo split necesita un padre)
        if nodo._is_full:
            new_raiz = self.Nodo(self._t)
            new_raiz.hijo.append(self.raiz)
            new_raiz.hoja = False
            # nodo sera el nodo que contendra la nueva key agregada y redefine la raiz
            nodo = nodo.split(new_raiz, nueva_key)
            self.raiz = new_raiz

        while not nodo.hoja:
            i = nodo.size - 1  # ultima key
            while i > 0 and nueva_key < nodo.keys[i]:
                i -= 1  # posicion de la nueva key o la mas grande de las que son menores a la nueva key
            if nueva_key > nodo.keys[i]:
                i += 1
                # si keys[i] es la mas grande de las menores a nueva_key, la convierto en la menor de las mayores

            # proximo sera el nodo que sigue en el camino hasta ser la hoja que contendra la nueva key
            proximo = nodo.hijo[i]
            if proximo._is_full:
                nodo = proximo.split(nodo, nueva_key)
            else:
                nodo = proximo
        # Como spliteamos todos los nodos completos en el camino a la hoja indicada podemos simplemente agregar la key.
        nodo.agregar_key(nueva_key)

    def buscar(self, valor, nodo=None):
        """Devuelve True el valor esta en el arbol"""
        if nodo is None:
            nodo = self.raiz
        if valor in nodo.keys:
            return True
        elif nodo.hoja:  # no hay mas hijos que chequear.
            return False
        else:
            i = 0
            while i < nodo.size and valor > nodo.keys[i]:
                i += 1
                # hasta que i la pos del nodo hijo que podria contener el valor
            return self.buscar(valor, nodo.hijo[i])

    def imprimir_arbol(self):
        """imprime una representacion por nivel"""
        este_nivel = [self.raiz]
        while este_nivel:
            prox_nivel = []
            output = ""
            for nodo in este_nivel:
                if nodo.hijo:
                    prox_nivel.extend(nodo.hijo)
                output += str(nodo.keys) + " "
            print(output)
            este_nivel = prox_nivel

class BTree(object):
    """BTree de Orden t: permite 2 * orden - 1 keys"""

    class Nodo(object):

        def __init__(self, t, hoja=True):
            self.keys = []  # elementos del nodo
            self.hijo = []  # hijos(otros nodos internos o el contenido de la hoja en caso de serlo)
            self.hoja = hoja  # me permite saber si sus hijos son otros nodos o datos
            self._t = t  # t = orden

        def split(self, padre, nueva_key):
            """divide el nodo y reasigna keys e hijos,devuelve el nodo que contendra a la nueva key"""
            nuevo_nodo = self.__class__(self._t, self.hoja)
            mitad = self.size // 2
            key_medio = self.keys[mitad]
            padre.keys.append(key_medio)
            padre.keys.sort()

            # Agrega las keys y los hijos al nodo correcto,el nuevo nodo siempre contendra las keys mas altas
            nuevo_nodo.hijo = self.hijo[mitad :]
            self.hijo = self.hijo[:mitad ]
            nuevo_nodo.keys = self.keys[mitad :]
            self.keys = self.keys[:mitad]

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

        def agregar_key(self, valor,documento):
            self.keys.append(valor)
            self.hijo.append([documento])
            i = len(self.keys)-1
            while i >= 1 and self.keys[i] < self.keys[i-1]:
                self.swap(self.keys,i)
                self.swap(self.hijo,i)
                i-=1

        def swap(self, lista, indice):
            aux = lista[indice]
            lista[indice] = lista[indice-1]
            lista[indice-1] = aux

        def insertar_hijo(self, nuevo_nodo):
            """agrega un hijo al nodo y ordena a todos los hijos.Devuelve una lista ordenada de los nodos hijos"""
            i = len(self.hijo) - 1 #ultimo hijo
            while i >= 0 and self.hijo[i].keys[0] > nuevo_nodo.keys[0]:
                i -= 1
            return self.hijo[:i + 1] + [nuevo_nodo] + self.hijo[i + 1:]

    def __init__(self, t):
        """Crea un arbolb de orden t sin keys.Actualmente permite keys duplicadas"""
        self._t = t
        if self._t <= 1:
            raise ValueError("El orden del arbol debe ser 2 o superior")
        self.raiz = self.Nodo(t)

    def insertar(self, nueva_key, documento):
        """Inserta un key con un valor determinado"""
        nodo = self.raiz
        # El split de la raiz es manejada de forma particular(nuestro metodo split necesita un padre)
        if nodo._is_full:
            new_raiz = self.Nodo(self._t, False)
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
                i += 1  # ahora i sera la posicion mayor mas proxima a la nueva key
            # proximo sera el nodo que sigue en el camino hasta ser la hoja que contendra la nueva key
            proximo = nodo.hijo[i]
            if proximo._is_full:
                nodo = proximo.split(nodo, nueva_key)
            else:
                nodo = proximo
        if not self.buscar(nueva_key):
            # Como spliteamos todos los nodos completos podemos simplemente agregar la key.
            nodo.agregar_key(nueva_key,documento)#aca agrega la key y el documento a la lista de aparicion.
        else:
            nodo.hijo[nodo.keys.index(nueva_key)].append(documento)

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
                i += 1  # hasta que i la pos del nodo hijo que podria contener el valor
            return self.buscar(valor, nodo.hijo[i])

    def imprimir_arbol(self):
        """imprime una representacion por nivel"""
        este_nivel = [self.raiz]
        while este_nivel:
            prox_nivel = []
            output = ""
            for nodo in este_nivel:
                if not nodo.hoja:
                    prox_nivel.extend(nodo.hijo)
                output += str(nodo.keys) + " "
            print(output)
            este_nivel = prox_nivel



def prueba():
    """ expected = [4, 6, 12]
    [1, 2, 3] [4, 5] [6, 7, 8, 9] [12, 13, 123]
    el numero dos aparece en los documentos :A, b, c, d"""
    b = BTree(3)
    b.insertar(2,"A")
    b.insertar(2,"b")
    b.insertar(2,"c")
    b.insertar(2,"d")
    b.insertar(12, 1)
    b.insertar(4, 1)
    b.insertar(3, 1)
    b.insertar(123,1)
    b.insertar(13,1)
    b.insertar(1,1)
    b.insertar(5,1)
    b.insertar(6,1)
    b.insertar(9,1)
    b.insertar(7,1)
    b.insertar(8,1)
    b.imprimir_arbol()

    print("el numero 2 aparece en los documentos :" + ", ".join(b.raiz.hijo[0].hijo[1]))

if __name__ == "__main__":
    prueba()


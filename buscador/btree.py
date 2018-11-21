class BTree(object):
    """BTree de Orden t: permite 2 * orden - 1 keys"""

    class Nodo(object):

        def __init__(self, t, hoja=True):
            self.keys = []  # elementos del nodo
            self.hijo = []  # hijos(otros nodos internos o el contenido de la hoja en caso de serlo)
            self.hoja = hoja  # me permite saber si sus hijos son otros nodos o datos
            self._t = t  # t = orden

        def split(self, padre, palabra):
            """divide el nodo y reasigna keys e hijos,devuelve el nodo que contendra a la nueva key"""
            nuevo_nodo = self.__class__(self._t, self.hoja)

            mitad = self.size // 2
            key_medio = self.keys[mitad]
            padre.keys.append(key_medio)
            padre.keys.sort()
            if not self.hoja:
                self.keys.remove(key_medio)
                # Agrega las keys y los hijos al nodo correcto,el nuevo nodo siempre contendra las keys mas altas
                nuevo_nodo.hijo = self.hijo[mitad+1:]
                self.hijo = self.hijo[:mitad+1]
            else:
                nuevo_nodo.hijo = self.hijo[mitad:]
                self.hijo = self.hijo[:mitad ]
            nuevo_nodo.keys = self.keys[mitad:]
            self.keys = self.keys[:mitad]

            # Agrega al padre el nuevo nodo con las keys de mayor valor y devuelve el nodo que contendra la nueva key
            padre.hijo = padre.add_hijo(nuevo_nodo)
            if palabra < key_medio:
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

        def add_hijo(self, nuevo_nodo):
            """agrega un hijo al nodo y ordena a todos los hijos.Devuelve una lista ordenada de los nodos hijos"""
            i = len(self.hijo) - 1 #ultimo hijo
            while i >= 0 and self.hijo[i].keys[0] > nuevo_nodo.keys[0]:
                i -= 1
            return self.hijo[:i + 1] + [nuevo_nodo] + self.hijo[i + 1:]

    def __init__(self, t=5):
        """Crea un arbolb de orden t sin keys. Actualmente permite keys duplicadas. Por defecto el orden es 5"""
        self._t = t
        if self._t <= 1:
            raise ValueError("El orden del arbol debe ser 2 o superior")
        self.raiz = self.Nodo(t,True)

    def add(self, palabra, documento):
        """Inserta un key con un valor determinado"""
        nodo = self.raiz
        # El split de la raiz es manejada de forma particular(nuestro metodo split necesita un padre)
        if nodo._is_full:
            new_raiz = self.Nodo(self._t, False)
            new_raiz.hijo.append(self.raiz)
            # nodo sera el nodo que contendra la nueva key agregada y redefine la raiz
            nodo = nodo.split(new_raiz, palabra)
            self.raiz = new_raiz
        while not nodo.hoja:
            i = nodo.size - 1  # ultima key
            while i > 0 and palabra < nodo.keys[i]:
                i -= 1  # posicion de la nueva key o la mas grande de las que son menores a la nueva key
            if palabra >= nodo.keys[i]:
                i += 1  # ahora i sera la posicion mayor mas proxima a la nueva key
            # proximo sera el nodo que sigue en el camino hasta ser la hoja que contendra la nueva key
            proximo = nodo.hijo[i]
            if proximo._is_full:
                nodo = proximo.split(nodo, palabra)
            else:
                nodo = proximo
        if palabra not in nodo.keys:
            # Como spliteamos todos los nodos completos podemos simplemente agregar la key.
            nodo.agregar_key(palabra,documento)#aca agrega la key y el documento a la lista de aparicion.

        elif documento not in self.get(palabra):
               nodo.hijo[nodo.keys.index(palabra)].append(documento)

    def get(self, palabra):
        nodo = self.raiz
        while not nodo.hoja:
            i = nodo.size - 1  # ultima key
            while i > 0 and palabra < nodo.keys[i]:
                i -= 1  # posicion de la nueva key o la mas grande de las que son menores a la nueva key
            if palabra >= nodo.keys[i]:
                i += 1  # ahora i sera la posicion mayor mas proxima a la nueva key
            nodo = nodo.hijo[i]# proximo sera el nodo que sigue en la rama que lleva a la palabra
        try: #si es una de las keys devuelvo su lista
            posicion = nodo.keys.index(palabra)
            return(nodo.hijo[posicion])
        except ValueError as e: #si no es una key digo que no esta
            return(e) #key is not in list

    def get_hojas(self):
        hojas = []
        este_nivel = [self.raiz]
        while este_nivel:
            prox_nivel = []
            for nodo in este_nivel:
                if not nodo.hoja:
                    prox_nivel.extend(nodo.hijo)
                else:
                    hojas.append(nodo.keys)
            este_nivel = prox_nivel
        return hojas



    def _imprimir_arbol(self):
        """imprime una representacion visual por nivel unicamente util para cuequear arbol a simple vista"""
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
            
            
            
    def get_Slice(self, inicio, fin, por_revisar=[]):
        if fin <= inicio:
            raise ValueError("el inicio debe ser menor al fin")
        resultado = []
        nuevos_hijos = []
        if len(por_revisar) == 0:
            nuevos_hijos = self._buscar_hijos_compatibles(inicio, fin, self.raiz,resultado)
            if len(nuevos_hijos) > 0:
                for nv in nuevos_hijos:
                    por_revisar.append(nv)
        while len(por_revisar) > 0:
            nuevos_hijos = self._buscar_hijos_compatibles(inicio, fin, por_revisar[0],resultado)
            por_revisar.pop(0)
            if len(nuevos_hijos) > 0:
                for nv in nuevos_hijos:
                        por_revisar.append(nv)
        return resultado

    def _buscar_hijos_compatibles(self,inicio, fin, nodo, resultado):
        nueva_lista = []
        if not nodo.hoja:
            i = 0
            while i < nodo.size and inicio > nodo.keys[i]:
                i += 1  # posicion de la nueva key o la mas grande de las que son menores a la nueva key
            for posicion in range(i, nodo.size+1):
                    nueva_lista.append(nodo.hijo[posicion])
        else:
            for key in nodo.keys:
                if inicio <= key < fin:
                    resultado.append(key)
        return nueva_lista

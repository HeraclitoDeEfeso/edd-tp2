class Nodo(object):
    
    def __init__(self, hoja=False):
        self.hoja = hoja
        self.hijos = []
        self.indices = []
		
    """Busca un indice y devuelve true y su posicion si este esta en la lista de indices,
    si este no es encontrado devolvera false y 0 como posicion"""
    def consultar(self, indice):
            for i in self.indices:
                if i == indice:
                    return (True, self.indices.index(indice))
                return (False, 0)

import simpy
from Nodo import *
from Canales.CanalRecorridos import *

''' Práctica 2
-- Romo Olea Fhernanda
-- Jardínes Mendoza César (el vaquero)
'''

# La unidad de tiempo
TICK = 1

class NodoDFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de DFS.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo DFS. '''
        self.id_nodo=id_nodo
        self.vecinos=vecinos
        self.canal_entrada=canal_entrada
        self.canal_salida=canal_salida
        #Atributos propios de la clase
        self.padre = None
        self.hijos = list()

    # Aquí sucede la magia (el rerrido)
    def dfs(self, env):
        # Código que sólo ejecuta el nodo distinguido
        if self.id_nodo is 0:
            self.padre=self.get_id()
            # tomamos el mínimo de la lista
            k = min(self.vecinos)
            self.canal_salida.envia(("Go",{self.get_id()}, self.get_id()), [k])
            self.hijos.append(k)
            # +++ print("el proceso %d agrega como hijo a %d"%(self.id_nodo,k))
            # +++ print("La raíz envía un GO a %d en la ronda %d"%(k,env.now))

        while True:
            yield env.timeout(TICK)
            mensaje = yield self.canal_entrada.get()
            # +++ print("%d recibe un %s en la ronda %d del proceso %d, mensaje: %s"%(self.get_id(),mensaje[0],env.now,mensaje[2],str(mensaje[1])))
            # label se refiere a "Go" o "Back"
            label=mensaje[0]
            visited=mensaje[1]

            #Si recibimos un "Go" realizamos lo siguiente:
            if label is "Go":
                self.padre=mensaje[2]
                if set(self.vecinos).issubset(visited):
                    yield env.timeout(TICK)
                    self.canal_salida.envia(("Back",visited.union({self.get_id()}),
                    self.get_id()),[self.padre])
                else:
                    k=min(list(set(self.vecinos).difference(visited)))
                    yield env.timeout(TICK)
                    self.hijos.append(k)
                    # +++ print("el proceso %d agrega como hijo a %d"%(self.id_nodo,k))
                    self.canal_salida.envia(("Go",visited.union({self.id_nodo}),
                    self.get_id()),[k])

            # En caso que la etiqueta sea un "Back":
            else:
                if(set(self.vecinos).issubset(visited)):
                    if self.padre == self.id_nodo:
                        break
                    else:
                        yield env.timeout(TICK)
                        self.canal_salida.envia(("Back",visited,self.get_id()),
                        [self.padre])
                else:
                    k = min(list(set(self.vecinos).difference(visited)))
                    yield env.timeout(TICK)
                    self.hijos.append(k)
                    # +++ print("el proceso %d agrega como hijo a %d"%(self.id_nodo,k))
                    self.canal_salida.envia(("Go",visited,self.id_nodo),[k])

# Implementación del método get_id, regresa el id del nodo actual
    def get_id(self):
        return self.id_nodo

''' Main que implementamos para ir haciendo pruebas
    * Descomentar las lineas que comienzan con +++ para obtener información en
    * consola al momento de ejecutar el programa.

if __name__ == "__main__":

    envi = simpy.Environment()
    pipe = CanalRecorridos(envi)
    grafica = []
    adyacencias = [[1, 3, 4, 6], [0, 3, 5, 7], [3, 5, 6], [0, 1, 2], [0], [1, 2], [0, 2], [1]]

    for i in range(0, len(adyacencias)):
        grafica.append(NodoDFS(i, adyacencias[i], pipe.crea_canal_de_entrada(), pipe))
    for i in grafica:
        envi.process(i.dfs(envi))
'''

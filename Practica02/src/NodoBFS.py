import simpy
from Nodo import *
from Canales.CanalRecorridos import *

''' Práctica 2
-- Romo Olea Fhernanda
-- Jardínes Mendoza César (el vaquero)
'''

# La unidad de tiempo
TICK = 1

class NodoBFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de BFS que no detecta terminación.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo BFS. '''
        self.id_nodo=id_nodo
        self.vecinos=vecinos
        self.canal_entrada=canal_entrada
        self.canal_salida=canal_salida
        #Atributos de la clase NodoBFS
        self.distancia = float('inf')
        self.padre = self.id_nodo if self.id_nodo is 0 else None

# Algoritmo para realizar un recorrido bfs en la gráfica
    def bfs(self, env):
        ''' Algoritmo BFS. '''
        # El nodo raíz comienza con el recorrido
        if self.padre == self.id_nodo:
            self.distancia= 0
            self.canal_salida.envia((self.get_id(), self.distancia), self.vecinos)
            # +++ print("El proceso distinguido %d envía su distancia a sus vecinos"%self.get_id())
            # +++ print(".......")
            yield env.timeout(TICK)

        while True:
            mensaje = yield self.canal_entrada.get()
            d = mensaje[1]
            # +++ print("El procedo %d recibe un mensaje de %d en la ronda %d"%(self.get_id(),mensaje[0],env.now))
            if d+1 < self.distancia:
                self.distancia = d+1
                self.padre = mensaje[0]
                # +++ print("El padre de %d es %d"%(self.get_id(),self.padre))
                self.canal_salida.envia((self.get_id(),self.distancia),self.vecinos)
                yield env.timeout(TICK)

#Método que devuelve el id del proceso actual
    def get_id(self):
        return self.id_nodo

''' Main que implementamos para probar nuestras soluciones
    * Descomentar las lineas que comienzan con +++ para obtener información en
    * consola al momento de ejecutar el programa.

if __name__ == "__main__":

    envi = simpy.Environment()
    pipe = CanalRecorridos(envi)
    grafica = []
    adyacencias = [[1,2,3],[0,2,3],[0,1,4,5],[0,1,4],[2,3],[2]]

    for i in range(0, len(adyacencias)):
        grafica.append(NodoBFS(i, adyacencias[i], pipe.crea_canal_de_entrada(), pipe))
    for i in range(0, len(adyacencias)):
        envi.process(grafica[i].bfs(envi))
'''

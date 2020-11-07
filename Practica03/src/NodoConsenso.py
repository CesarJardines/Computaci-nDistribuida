import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoConsenso(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Consenso.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo de consenso. '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        # Atributos extra
        self.V = [None] * (len(vecinos) + 1) # Llenamos la lista de None
        self.V[id_nodo] = id_nodo
        self.New = set([id_nodo])
        self.rec_from = [None] * (len(vecinos) + 1)
        self.fallare = False      # Colocaremos esta en True si el nodo fallará
        self.lider = None         # La elección del lider.

    def consenso(self, env, f):
        '''El algoritmo de consenso.'''
        if self.id_nodo < f:
            self.fallare=True
        while env.now<f+1:
            if not self.fallare:
                if self.New != set():
                    self.canal_salida.envia((self.New,self.id_nodo), self.vecinos)
                yield env.timeout(TICK)
                i=0
                while True:
                    mensaje = yield self.canal_entrada.get()
                    self.rec_from[mensaje[1]]=mensaje[0]
                    i += 1
                    if(i==len(self.vecinos)-f):
                        break
                # print(str(self.id_nodo)+" recibe a "+str(self.rec_from))
                for cjto in self.rec_from:
                    if cjto is not None and len(cjto)>0:
                        for elem in cjto:
                            if self.V[elem]==None:
                                self.V[elem] = elem
                                self.New.update(cjto)
                # print(str(self.V))
            else:
                break
        for elem in self.V:
            if elem is not None:
                self.lider = elem
                #print(self.lider)
                break


if __name__ == "__main__":

    envi = simpy.Environment()
    pipe = CanalRecorridos(envi)
    grafica = []
    adyacencias = [[1,2,3,4,5],[0,2,3,4,5],[0,1,3,4,5],[0,1,2,4,5],[0,1,2,3,5],[0,1,2,3,4]]

    for i in range(0, len(adyacencias)):
        grafica.append(NodoConsenso(i, adyacencias[i], pipe.crea_canal_de_entrada(), pipe))
    for i in range(0, len(adyacencias)):
        envi.process(grafica[i].consenso(envi,1))

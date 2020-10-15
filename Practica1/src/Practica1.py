import simpy
import Canales.CanalVecinos
from Nodo import *
#Algoritmo para conocer los vecinos de los vecinos
class NodoVecinos(Nodo):
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        #Atributos de todo nodo
        self.id_nodo=id_nodo
        self.vecinos=vecinos
        self.canal_entrada=canal_entrada
        self.canal_salida=canal_salida
        #Propio de la clase será una lista conformada de parejas de la forma: (id_nodo, [vecinos_nodo])
        self.identificadores=list()

    def conocerVecinos(self, envi):
        # Esperamos una ronda para comenzar a enviar nuestros mensajes
        yield envi.timeout(1)
        self.canal_salida.envia([self.id_nodo,self.vecinos], self.vecinos)
        #Código que sólo imprime en bonito la lista de vecinos xD
        s = "{"
        for i in range(0, len(self.vecinos)-1):
            s = s+str(self.vecinos[i])+", "
        s = s + str(self.vecinos[-1])+"}"
        #Aquí acaba la impresión bonita
        print("El proceso %d manda mensaje a %s en la roda %d" %(self.id_nodo, s, envi.now))

        while True:
            yield envi.timeout(1)
            mensaje = yield self.canal_entrada.get()
        ###
            self.identificadores.append(mensaje)
            print("-----------------")
            for i in self.identificadores:
                for v in i[1]:
                    print("El proceso %d conoce que su vecino %d es vecino de %d en la ronda %d" %(self.id_nodo, i[0], v, envi.now))
            break


#Problema 2. Generar el árbol generador de una gráfica

class NodoArbol(Nodo):

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        #Atributos de todo nodo
        self.id_nodo=id_nodo
        self.vecinos=vecinos
        self.canal_entrada=canal_entrada
        self.canal_salida=canal_salida
        #Atibutos propios de esta clase:
        self.padre=None
        self.hijos={}
        self.exp_msgs=-1

    def generaArbol(self, envi):
        if self.id_nodo is 0:
            self.padre=self.id_nodo
            self.exp_msgs=len(self.vecinos)
            yield envi.timeout(1)
            self.canal_salida.envia(("go",self.id_nodo),self.vecinos)
            print("El proceso distinguido %d, envía su id a sus vecinos %s, sabe que %d es su Padre" %(self.id_nodo,str(self.vecinos),self.padre))
            print("--------------")

        mensaje = yield self.canal_entrada.get()
        print("El proceso %d recibe un mensaje en la ronda %d" %(self.id_nodo,envi.now))
        if mensaje[0] is "go":
            yield envi.timeout(1)
            print("El mensaje recibido por %d es un Go, es procesado en la ronda %d"% (self.id_nodo,envi.now))
            if (self.padre == None):
                self.padre = mensaje[1]
                self.exp_msgs = len(self.vecinos)-1
                if (self.exp_msgs == 0):
                    self.canal_salida.envia(("back",self.id_nodo),[self.padre])
                    print("El proceso %d envió un back a su padre %d"%(self.id_nodo,self.padre))
                else:
                    self.vecinos.remove(self.padre)
                    self.canal_salida.envia(("go",self.id_nodo),self.vecinos)
                    print("El proceso %d envía su id a sus vecinos %s, sabe que %d es su padre"%(self.id_nodo,str(self.vecinos),self.padre))

        else:
            yield envi.timeout(1)
            print("El mensaje recibido es un Back, es procesado en la ronda %d"% envi.now)
            self.exp_msgs = self.exp_msgs -1
            self.hijos.update(mensaje[1])
            if self.exp_msgs is 0:
                if not(self.padre is self.padre):
                    self.canal_salida.envia(("back",self.id_nodo),[self.padre])




#Problema 1
## Main para conocer los vecinos de los vecinos ##
'''
if __name__ == "__main__":

    envi = simpy.Environment()
    pipe = Canales.CanalVecinos.CanalVecinos(envi)

    grafica = []
    adyacencias = [[1,2,3],[0,2,3],[0,1,4,5],[0,1,4],[2,3],[2]]
    for i in range(0, len(adyacencias)):
        grafica.append(NodoVecinos(i, adyacencias[i], pipe.crea_canal_de_entrada(), pipe))

    for i in range(0, len(adyacencias)):
        envi.process(grafica[i].conocerVecinos(envi))
'''
#Problema 2
## Main para construir el árbol ##
'''
if __name__ == "__main__":

    envi = simpy.Environment()
    pipe = Canales.CanalVecinos.CanalVecinos(envi)

    grafica = []
    adyacencias = [[1,2,3],[0,2,3],[0,1,4,5],[0,1,4],[2,3],[2]]
    for i in range(0, len(adyacencias)):
        grafica.append(NodoArbol(i, adyacencias[i], pipe.crea_canal_de_entrada(), pipe))

    for i in range(0, len(adyacencias)):
        envi.process(grafica[i].generaArbol(envi))
'''

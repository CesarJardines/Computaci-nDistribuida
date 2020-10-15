import simpy
import CanalVecinos
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
        yield envi.timeout(1)
        mensaje = yield self.canal_entrada.get()
        while True:
            self.identificadores.append(mensaje)
            print(mensaje)
            print("-----------------")
            for i in self.identificadores:
                for v in i[1]:
                    print("El proceso %d conoce que su vecino %d es vecino de %d en la ronda %d" %(self.id_nodo, i[0], v, envi.now))
            break



if __name__ == "__main__":

    envi = simpy.Environment()
    pipe = CanalVecinos.CanalVecinos(envi)

    grafica = []
    adyacencias = [[1,2,3],[0,2,3],[0,1,4,5],[0,1,4],[2,3],[2]]
    for i in range(0, len(adyacencias)):
        grafica.append(NodoVecinos(i, adyacencias[i], pipe.crea_canal_de_entrada(), pipe))

    for i in range(0, len(adyacencias)):
        envi.process(grafica[i].conocerVecinos(envi))

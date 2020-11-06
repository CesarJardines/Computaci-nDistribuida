import simpy
import Canales.CanalVecinos
from Nodo import *

# # # PRÁCTICA 1. Computación distribuída # # #
# Fhernanda Romo Olea
# César Eduardo Jardínes Mendoza (el vaquero)

# Problema 1. Algoritmo para conocer los vecinos de los vecinos
class NodoVecinos(Nodo):
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        #Atributos de todo nodo
        self.id_nodo=id_nodo
        self.vecinos=vecinos
        self.canal_entrada=canal_entrada
        self.canal_salida=canal_salida
        #Propio de la clase será una lista conformada de parejas de la forma: (id_nodo, [vecinos_nodo])
        self.identificadores=list()

# Aquí sucede toda la magia :3
    def conocerVecinos(self, envi):
        # Esperamos una ronda para comenzar a enviar nuestros mensajes
        yield envi.timeout(1)
        #Cada mensaje es una pareja ordenada que contiene el id del nodo que
        #la envía y su lista de vecinos.
        self.canal_salida.envia([self.id_nodo,self.vecinos], self.vecinos)
        #Código que sólo imprime en bonito la lista de vecinos xD
        s = "{"
        for i in range(0, len(self.vecinos)-1):
            s = s+str(self.vecinos[i])+", "
        s = s + str(self.vecinos[-1])+"}"
        #Aquí acaba la impresión bonita
        #Todos los procesos envían sus mensajes al mismo tiempo
        print("El proceso %d manda mensaje a %s en la roda %d" %(self.id_nodo, s, envi.now))
        #Les toma a estos una ronda para recibirlos y empezar a procesarlos
        yield envi.timeout(1)

        while True:
            #Todo lo que esté llegando al Store del nodo se mete en el cto. identificadores
            mensaje = yield self.canal_entrada.get()
            self.identificadores.append(mensaje)
            print("-----------------")
            #Registramos cada que un mensaje llegue al Store
            print("El proceso %d conoce los vecinos del proceso %d en la ronda %d" %(self.id_nodo,mensaje[0], envi.now))
            #Para el while cuando el canal de entrada de un nodo se queda vacío
            if(len(self.canal_entrada.items)==0):
                break
        #Si ya hemos recibido toda la info. de nuestros vecinos imprime la información recabada.
        if len(self.identificadores)==len(self.vecinos):
            print(".......................................................")
            for i in self.identificadores:
                print("El proceso "+str(self.id_nodo)+" sabe que su vecino "+ str(i[0]) +" es vecino de: "+ str(i[1]))
            print(".......................................................")


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
        self.hijos=list()
        self.exp_msgs=len(vecinos)
        self.originalexpectedmsgs=len(vecinos)


    def generaArbol(self, envi):
        #Si el nodo es el nodo distinguido se inicializa y manda a sus vecinos el mensaje,
        #hago diferencia entre Go's y Back's para conocer en qué momento de la ejecución me encuentro.
        if self.id_nodo is 0:
            self.padre=0
            #Esperamos 1 ronda en lo que se recibe el primer mensaje
            yield envi.timeout(1)
            self.canal_salida.envia(("go",self.id_nodo),self.vecinos)
            print("El proceso distinguido %d, envía un Go a sus vecinos %s, sabe que %d es su Padre" %(self.id_nodo,str(self.vecinos),self.padre))
            print("--------------")

        while True:
            #Espero a que algo llegue a mi canal de entrada y verifico si es un back o un go.
            mensaje = yield self.canal_entrada.get()

            if mensaje[0] is "go":
                #Si es un Go hago la parte del pseudocódgo que es para Go's
                yield envi.timeout(1)
                #Si no tenemos padre :( adoptamos al remitente como padre
                if self.padre == None:
                    self.padre = mensaje[1]
                    self.exp_msgs = len(self.vecinos)-1
                    print("El proceso %d recibe un Go, es procesado en la ronda %d, se le asigna a %d como padre"% (self.id_nodo,envi.now,self.padre))
                    if (self.exp_msgs == 0):
                        self.canal_salida.envia(["back",self.id_nodo],[self.padre])
                        print("El proceso %d envía un Back a su padre %d"%(self.id_nodo,self.padre))
                        print("---------------")
                    else:
                        #Se envía a los vecinos menos al padre
                        self.vecinos.remove(self.padre)
                        self.canal_salida.envia(("go",self.id_nodo),self.vecinos)
                        print("El proceso %d envió un Go a %s"%(self.id_nodo,str(self.vecinos)))
                        print("---------------")
                else:
                    self.canal_salida.envia(["back",-1],[self.padre])

            #Hacemos esto si lo recibido es un back
            else:
                if (self.id_nodo==0 and len(self.hijos)==self.originalexpectedmsgs):
                    break
                else:
                    self.exp_msgs = self.exp_msgs-1
                    yield envi.timeout(1)
                    print("El proceso %d recibe un Back, es procesado en la ronda %d"%(self.id_nodo,envi.now))
                    if mensaje[1]!=-1:
                        self.hijos.append(mensaje[1])
                    if self.exp_msgs==0:
                        if self.padre!=self.id_nodo:
                            self.canal_salida.envia(["back",self.id_nodo],[self.padre])





# Problea 3. Algoritmo de Broadcast

class NodoBroadcast(Nodo):
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        #Atributos de todo nodo
        self.id_nodo=id_nodo
        self.vecinos=vecinos
        self.canal_entrada=canal_entrada
        self.canal_salida=canal_salida
        #Atributos de la clase, mensaje es el mensaje que enviaremos
        self.mensaje=None

    #Método broadcast, inunda la gráfica con el mensaje
    def broadcast(self, envi, mensaje):
        #Determinamos a 0 como el nodo distinguido y la fuente del mensaje
        if self.id_nodo is 0:
            self.mensaje = mensaje
            print("El proceso %d es el proceso distinguido, envía el mensaje a sus vecinos"%self.id_nodo)
            self.canal_salida.envia(self.mensaje,self.vecinos)

        #Sus vecinos reciben el mensaje en la siguiente ronda
        msg = yield self.canal_entrada.get()
        yield envi.timeout(1)
        print("El proceso %d ha recibido el mensaje en la ronda %d"%(self.id_nodo,envi.now))
        # El mensaje le llegará nuevamente al proceso distinguido, después de eso entrará
        # al while y saldrá del ciclo.
        while True:
            self.mensaje=msg
            self.canal_salida.envia(msg,self.vecinos)
            print("El proceso %d envió el mensaje \"%s\" a sus vecinos"%(self.id_nodo,msg))
            break

# Problea 4. Punto extra. Algoritmo de Convergecast

class NodoConvergecast(Nodo):
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        #Atributos de todo nodo
        self.id_nodo=id_nodo
        self.vecinos=vecinos
        self.canal_entrada=canal_entrada
        self.canal_salida=canal_salida
        #Atributos de la clase, mensaje es el conjunto de mensajes recolectados
        #por los vértices
        self.mensaje=list()
        self.padre=None
        self.hijos=list()

    # Método convergecast, recolecta todos los mensajes, desde las hojas a la
    # raíz. Lista define quién es el padre y los hijos de un nodo, si el nodo
    # no tiene hijos, entonces es vacía.
    def convergecast(self,envi,lista,mensaje):
        self.padre=lista[0]
        self.hijos=lista[1]
        self.mensaje.append(mensaje)
        if len(self.hijos)==0:
            self.canal_salida.envia(self.mensaje,[self.padre])
            print("Las hoja %d envió el mensaje %s a su padre en la ronda %d"%(self.id_nodo,str(self.mensaje),envi.now))

        yield envi.timeout(1)
        while True:
            msg = yield self.canal_entrada.get()
            print("------------------")
            print("El proceso %d recibe un mensaje de su hijo en la ronda %d"%(self.id_nodo,envi.now))
            # Concatenamos los mensajes que vayamos recibiendo
            self.mensaje = self.mensaje+msg
            # Necesitamos verificar si el nodo ya recolectó todos los mensajes esperados.
            if self.padre != self.id_nodo and len(self.mensaje)==len(self.hijos)+1:
                yield envi.timeout(1)
                self.canal_salida.envia(self.mensaje,[self.padre])
                print("El proceso %d envía el mensaje %s a su padre"%(self.id_nodo,str(self.mensaje)))
            else:
                # Si llegamos a un nodo que es padre de sí mismo, ya estamos
                # en la raíz, unimos los mensajes y los operamos.
                if len(self.mensaje)>len(self.vecinos):
                    print("------------------\nEl proceso raíz acaba de recibir todos los mensajes de la gráfica\n------------------")
                    print("El mensaje es la unión de todos los mensajes de la gráfica:\n"+str(self.mensaje))
                    break



#El main, comentar y descomentar las líneas del cuerpo sgún el algoritmo que quiera probarse, las lineas de código correspondientes a la ejecución de cada algoritmo se encuentran comentadas en órden.

# ** Ocasionalmente al descomentar aparece un error que dice que la identación está mal, en ese caso hay que cortar el bloque de código del algoritmo que se desee ejecutar y pegarlo justo debajo de la línea 210 ** #

if __name__ == "__main__":

    envi = simpy.Environment()
    pipe = Canales.CanalVecinos.CanalVecinos(envi)
    grafica = []
    adyacencias = [[1,2,3],[0,2,3],[0,1,4,5],[0,1,4],[2,3],[2]]

# Problema 1
## Bloque para conocer los vecinos de los vecinos ##
'''
    for i in range(0, len(adyacencias)):
        grafica.append(NodoVecinos(i, adyacencias[i], pipe.crea_canal_de_entrada(), pipe))
    for i in range(0, len(adyacencias)):
        envi.process(grafica[i].conocerVecinos(envi))
'''

# Problema 2
## Bloque para construir el árbol generador de una gráfica##
'''
    for i in range(0, len(adyacencias)):
        grafica.append(NodoArbol(i, adyacencias[i], pipe.crea_canal_de_entrada(), pipe))
    for i in range(0, len(adyacencias)):
        envi.process(grafica[i].generaArbol(envi))
'''
# Problema 3
## Bloque para el algoritomo de broadcast sobre una gráfica ##
'''
    for i in range(0, len(adyacencias)):
        grafica.append(NodoBroadcast(i, adyacencias[i], pipe.crea_canal_de_entrada(), pipe))
    for i in range(0, len(adyacencias)):
        envi.process(grafica[i].broadcast(envi,"hola :)"))
'''
# Problema 4. extra. Algoritmo de convergecast
'''
    for i in range(0, len(adyacencias)):
        grafica.append(NodoConvergecast(i, adyacencias[i], pipe.crea_canal_de_entrada(), pipe))
    envi.process(grafica[0].convergecast(envi,[0,[1,2,3]],"Soy el proceso 0"))
    envi.process(grafica[1].convergecast(envi,[0,[]],"Soy el proceso 1"))
    envi.process(grafica[2].convergecast(envi,[0,[4,5]],"Soy el proceso 2"))
    envi.process(grafica[3].convergecast(envi,[0,[]],"Soy el proceso 3"))
    envi.process(grafica[4].convergecast(envi,[2,[]],"Soy el proceso 4"))
    envi.process(grafica[5].convergecast(envi,[2,[]],"Soy el proceso 5"))
'''

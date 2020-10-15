import simpy

class CanalVecinos(object):
    def __init__(self, envi, capacidad=simpy.core.Infinity):
        self.envi=envi
        self.capacidad=capacidad
        self.canales=[]
        self.canal_salida=None

    def crea_canal_de_entrada(self):
        canal = simpy.Store(self.envi, capacity=self.capacidad)
        self.canales.append(canal)
        self.canal_salida=canal
        return canal

    def envia(self,mensaje, vecinos):
        if not self.canales:
            raise RuntimeError('No hay canales de salida.')
        eventos=list()
        for i in range(len(self.canales)):
            if i in vecinos:
                eventos.append(self.canales[i].put(mensaje))
        return self.envi.all_of(eventos)

    def get_canal_salida(self):
        return self.canal_salida

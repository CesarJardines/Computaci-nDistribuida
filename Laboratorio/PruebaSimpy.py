import simpy

class Carro(object):
	def __init__(self, env):
		self.env = env
		self.accion = env.process(self.run())
		#self.estacion_carga = estacion_carga

	def run(self):
		while True:
			print("Empiezo a estacionarme y cargar el auto %d" %self.env.now)
			duracion_cargada = 5
			yield self.env.process(self.charge(duracion_cargada))

		print("Empece a conducir %d" %self.env.now)
		duracion_viaje = 4
		yield self.env.timeout(duracion_viaje)


	def charge(self, duration):
		yield self.env.timeout(duration)

env = simpy.Environment()
carro = Carro(env)



'''
def car(env):
	while True:
		print("Empece a recargar gasolina %d" %env.now)
		duracion_estacionado = 5
		yield env.timeout(duracion_estacionado)

		print("Empieza a conducir")
		duracion_viaje = 4
		yield env.timeout(duracion_viaje)
		'''
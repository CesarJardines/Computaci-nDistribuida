import simpy

def car(env):
	while True:
		print("Empece a recargar gasolina %d" %env.now)
		duracion_estacionado = 5
		yield env.timeout(duracion_estacionado)

		print("Empieza a conducir")
		duracion_viaje = 4
		yield env.timeout(duracion_viaje)
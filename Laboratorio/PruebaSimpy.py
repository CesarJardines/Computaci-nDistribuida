import simpy

def car(env):
	while true:
		print("Empece a recargar gasolina %d" %env.now)
		duracion_estacionado = 5
		yield
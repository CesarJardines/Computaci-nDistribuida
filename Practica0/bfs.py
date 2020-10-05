#algoritmo bfs para gráficas en representación de lista de listas
def bfs(lista):
    #Suponemos que la raís siempre está es el vértice 0
    visitados = []
    cola = [0]
    while len(cola) != 0:
        #posición es es id de vértice el v1, v2, ..., vn.
        posicion=cola.pop(0)
        #El vértice representado por la lista de adyacencias
        nodo = lista[posicion]
        for vecino in nodo:
            #no me interesa meter a la cola los que ya visité
            if (vecino not in visitados): cola.append(vecino)
        #guardo los id de los vectores ya visitados    
        if posicion not in visitados: visitados.append(posicion)
    return visitados

g = [[1,2], [0,3,2,4], [0,1], [1], [0,1,2,3]]
print(bfs(g))

"""EJERCICIO 1 
    Quitar duplicados conservando el orden Dada 
ciudades = ["Quito","Guayaquil","Quito","Cuenca","Guayaquil"], 
obtén una lista sin repetidos respetando el orden de aparición 
(un set solo no alcanza).
"""

ciudades = ["Quito","Guayaquil","Quito","Cuenca","Guayaquil", "guayaquil"]
set = set()
ciudades_sin_repetidos = []
for ciudad in ciudades:
    if ciudad not in set:
        set.add(ciudad)
        ciudades_sin_repetidos.append(ciudad)
print(ciudades_sin_repetidos)

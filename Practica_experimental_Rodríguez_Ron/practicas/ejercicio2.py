"""EJERCICIO 2 
    Contar con un diccionario
Con la misma lista, arma un diccionario {"Quito": 2, "Guayaquil": 2, "Cuenca": 1}
"""

ciudades = ["Quito","Guayaquil","Quito","Cuenca","Guayaquil", "guayaquil"]
contador = {}
for ciudad in ciudades:
    if ciudad in contador:
        contador[ciudad] += 1
    else:
        contador[ciudad] = 1
print(contador)

mas_repetida = max(contador, key=contador.get)
print(mas_repetida)
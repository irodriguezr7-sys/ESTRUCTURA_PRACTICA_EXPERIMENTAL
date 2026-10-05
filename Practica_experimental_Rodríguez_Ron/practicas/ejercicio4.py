"""EJERCICIO 4 
    De lista de diccionarios a índice
Con clientes = [{"id":1,"nombre":"Ana"},{"id":2,"nombre":"Luis"}], 
crea un diccionario {id: cliente} para acceder por id sin recorrer 
la lista. Luego imprime el nombre del id 2.
"""

clientes = [{"id":1,"nombre":"Ana"},{"id":2,"nombre":"Luis"}]
indice_clientes = {cliente["id"]: cliente for cliente in clientes}
print(indice_clientes[2]["nombre"])

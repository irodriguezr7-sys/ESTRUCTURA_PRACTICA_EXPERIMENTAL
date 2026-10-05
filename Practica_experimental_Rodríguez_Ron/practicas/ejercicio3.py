"""EJERCICIO 3 
    Conjuntos en acción inscritos_matematica = {"Ana","Luis","Sol","Marco"} 
y inscritos_ingles = {"Luis","Marco","Ruth"}. 
Responde con código: ¿quiénes están en las dos?, 
¿quiénes solo en matemática?, ¿cuántos estudiantes distintos hay en total?
"""

alumnos_matematica = {"Ana","Luis","Sol","Marco"}
alumnos_ingles = {"Luis","Marco","Ruth"}

en_ambas = alumnos_matematica & alumnos_ingles
solo_matematica = alumnos_matematica - alumnos_ingles
total_distintos = len(alumnos_matematica | alumnos_ingles)

print("Estudiantes en ambas materias:", en_ambas)
print("Estudiantes solo en matemática:", solo_matematica)
print("Total de estudiantes distintos:", total_distintos)
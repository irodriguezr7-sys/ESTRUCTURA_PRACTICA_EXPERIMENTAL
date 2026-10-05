import json

# TUPLA de campos básicos de un estudiante; la ciudad es opcional.
CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email", "carnet", "ciudad")


class Estudiante:
    """MODELO: representa a un estudiante. Usa las cuatro colecciones."""

    def __init__(
        self, id_estudiante, nombre, apellido, email, carnet,
        notas=None, materias=None, ciudad="",
    ):
        self.id = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet                      # ej: EST2026001
        self.ciudad = ciudad
        # DICCIONARIO DE LISTAS: {"Matemática": [18, 19], "Inglés": [17]}
        self.notas = notas if notas else {}
        # CONJUNTO: materias en las que está inscrito, sin repetidos
        self.materias = set(materias) if materias else set()

    def obtener_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def inscribir_materia(self, materia):
        # add() no duplica: si ya estaba inscrito, no pasa nada
        self.materias.add(materia)

    def agregar_nota(self, materia, nota):
        self.inscribir_materia(materia)
        # setdefault crea la lista vacía la primera vez que aparece la materia
        self.notas.setdefault(materia, []).append(nota)

    def obtener_promedio(self):
        todas = []
        for lista_notas in self.notas.values():
            todas.extend(lista_notas)
        if not todas:
            return 0
        return round(sum(todas) / len(todas), 2)

    def materias_en_comun(self, otro_estudiante):
        # INTERSECCIÓN de conjuntos: qué materias comparten dos estudiantes
        return self.materias & otro_estudiante.materias

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "ciudad": self.ciudad,
            "notas": self.notas,
            # JSON no sabe guardar un set: lo convertimos a lista ordenada
            "materias": sorted(self.materias),
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"], datos["nombre"], datos["apellido"], datos["email"],
            datos["carnet"],
            notas=datos.get("notas", {}),
            # y al leer lo volvemos a convertir en set
            materias=set(datos.get("materias", [])),
            ciudad=datos.get("ciudad", ""),
        )

    def __str__(self):
        return f"[{self.carnet}] {self.obtener_nombre_completo()} - Promedio: {self.obtener_promedio()}"


# Las pruebas se ejecutan solo cuando este archivo se inicia directamente.
if __name__ == "__main__":
    # Añade la raíz del proyecto para reutilizar los mensajes compartidos.
    import sys
    from pathlib import Path

    raiz_proyecto = Path(__file__).resolve().parent.parent
    if str(raiz_proyecto) not in sys.path:
        sys.path.insert(0, str(raiz_proyecto))

    from shared.herramientas import imprimir_error, imprimir_exito, imprimir_info

    print("=== PRUEBAS DEL MODELO DE ESTUDIANTES ===")
    imprimir_info("Se probarán los datos, notas, materias y conversiones JSON.")

    # Crea dos estudiantes con notas y materias diferentes.
    estudiante1 = Estudiante(
        1,
        "Ana",
        "Pérez",
        "ana@unemi.edu.ec",
        "EST2026001",
        notas={"Matemática": [18, 20], "Inglés": [16]},
        materias={"Matemática", "Inglés"},
        ciudad="Guayaquil",
    )
    estudiante2 = Estudiante(
        2,
        "Luis",
        "Gómez",
        "luis@unemi.edu.ec",
        "EST2026002",
        materias={"Matemática", "Historia"},
        ciudad="Quito",
    )
    assert estudiante1.obtener_nombre_completo() == "Ana Pérez"
    assert estudiante1.carnet == "EST2026001"
    assert estudiante1.ciudad == "Guayaquil"
    imprimir_exito("Creación y nombre completo de estudiantes.")

    # Inscribir dos veces la misma materia no debe crear duplicados.
    estudiante1.inscribir_materia("Matemática")
    assert estudiante1.materias == {"Matemática", "Inglés"}

    # Agregar una nota también inscribe la materia y guarda la nota.
    estudiante1.agregar_nota("Ciencias", 19)
    assert "Ciencias" in estudiante1.materias
    assert estudiante1.notas["Ciencias"] == [19]
    imprimir_exito("Inscripción sin duplicados y registro de notas.")

    # El promedio incluye las notas de todas las materias.
    assert estudiante1.obtener_promedio() == 18.25
    estudiante_sin_notas = Estudiante(
        3, "Eva", "Luna", "eva@unemi.edu.ec", "EST2026003"
    )
    assert estudiante_sin_notas.obtener_promedio() == 0
    imprimir_exito("Promedio calculado y caso sin notas.")

    # La intersección devuelve las materias que comparten los dos estudiantes.
    assert estudiante1.materias_en_comun(estudiante2) == {"Matemática"}
    imprimir_exito("Búsqueda de materias en común.")

    # Convierte el objeto a datos JSON y luego reconstruye el estudiante.
    datos = estudiante1.a_diccionario()
    datos_json = json.dumps(datos, ensure_ascii=False)
    estudiante_recuperado = Estudiante.desde_diccionario(json.loads(datos_json))
    assert estudiante_recuperado.id == estudiante1.id
    assert estudiante_recuperado.carnet == estudiante1.carnet
    assert estudiante_recuperado.notas == estudiante1.notas
    assert estudiante_recuperado.materias == estudiante1.materias
    assert estudiante_recuperado.ciudad == estudiante1.ciudad
    assert isinstance(estudiante_recuperado.materias, set)
    imprimir_exito("Conversión a JSON y reconstrucción del estudiante.")

    # Comprueba que el texto del objeto incluye el carnet, el nombre y el promedio.
    texto_estudiante = str(estudiante1)
    assert "EST2026001" in texto_estudiante
    assert "Ana Pérez" in texto_estudiante
    assert "18.25" in texto_estudiante
    imprimir_exito("Representación del estudiante como texto.")

    # Ejemplo visual del mensaje rojo; es una demostración, no una prueba fallida.
    imprimir_error("Ejemplo de mensaje de error (solo demostración visual).")
    imprimir_exito("Todas las pruebas del modelo de estudiantes terminaron correctamente.")

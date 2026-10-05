import json
import os


class GestorJSON:
    """Lee y guarda una lista de diccionarios en un archivo JSON."""

    def __init__(self, ruta):
        self.ruta = ruta
        carpeta = os.path.dirname(ruta)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)

    def leer(self):
        # Devuelve SIEMPRE una lista: vacía si el archivo no existe o está dañado
        if not os.path.exists(self.ruta):
            return []
        try:
            with open(self.ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            return datos if isinstance(datos, list) else []
        except (json.JSONDecodeError, OSError):
            # Capturamos errores concretos, nunca un "except:" pelado
            return []

    def guardar(self, datos):
        try:
            with open(self.ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=2)
            return True
        except (TypeError, OSError):
            # TypeError aparece si intentas guardar un set: JSON no lo conoce
            return False


# Las pruebas se ejecutan solo cuando este archivo se inicia directamente.
if __name__ == "__main__":
    # Imports usados únicamente por esta prueba independiente.
    import sys
    import tempfile
    from pathlib import Path

    # Añade la raíz del proyecto para reutilizar las herramientas compartidas.
    raiz_proyecto = Path(__file__).resolve().parent.parent
    if str(raiz_proyecto) not in sys.path:
        sys.path.insert(0, str(raiz_proyecto))

    # Reutiliza los mismos colores y mensajes que usa el resto de la aplicación.
    from shared.herramientas import (
        imprimir_color,
        imprimir_error,
        imprimir_exito,
        imprimir_info,
    )

    # Datos de ejemplo de estudiantes, usando campos que pueden guardarse en JSON.
    estudiantes = [
        {
            "id": 1,
            "nombre": "Ana",
            "apellido": "Pérez",
            "email": "ana@unemi.edu.ec",
            "carnet": "EST2026001",
            "notas": {
                "Matemática": [18, 19, 20],
                "Inglés": [16, 17],
            },
            "materias": ["Inglés", "Matemática"],
        },
        {
            "id": 2,
            "nombre": "Luis",
            "apellido": "Gómez",
            "email": "luis@unemi.edu.ec",
            "carnet": "EST2026002",
            "notas": {},
            "materias": ["Historia", "Matemática"],
        },
    ]

    # Muestra directamente los tres mensajes compartidos y sus símbolos.
    print("=== EJEMPLOS VISIBLES DE LOS MENSAJES ===")
    imprimir_exito("Estudiantes guardados correctamente")
    imprimir_error("Ejemplo de un error al guardar estudiantes")
    imprimir_info("Prueba de los mensajes de herramientas desde json_manager")

    # Usa una carpeta temporal para no crear ni modificar el JSON real del proyecto.
    with tempfile.TemporaryDirectory() as carpeta_temporal:
        ruta_archivo = Path(carpeta_temporal) / "data" / "estudiantes.json"
        gestor = GestorJSON(str(ruta_archivo))

        # El gestor crea la carpeta, pero el archivo aparece al guardar.
        assert ruta_archivo.parent.is_dir()
        assert not ruta_archivo.exists()
        imprimir_color("AVISO: aún no existe estudiantes.json.", "AMARILLO")

        # Leer un archivo inexistente debe devolver una lista vacía.
        assert gestor.leer() == []
        imprimir_color("AVISO: la lectura inicial devuelve una lista vacía.", "AMARILLO")

        # Guarda los estudiantes y vuelve a leerlos para comprobar la persistencia.
        assert gestor.guardar(estudiantes) is True
        assert ruta_archivo.is_file()
        estudiantes_leidos = gestor.leer()
        assert estudiantes_leidos == estudiantes
        assert estudiantes_leidos[0]["email"] == "ana@unemi.edu.ec"
        assert estudiantes_leidos[0]["materias"] == ["Inglés", "Matemática"]
        imprimir_color("OK: estudiantes guardados y leídos correctamente.", "VERDE")
        for estudiante in estudiantes_leidos:
            imprimir_color(
                f"Correo registrado: {estudiante['email']}",
                "VERDE",
            )

        # Un conjunto no se puede serializar directamente a JSON.
        assert gestor.guardar({"materias": {"Matemática"}}) is False
        imprimir_color(
            "ERROR ESPERADO: JSON no guarda conjuntos directamente.",
            "ROJO",
        )

        # Si el JSON está dañado, leer() devuelve una lista vacía.
        ruta_archivo.write_text("{ JSON dañado", encoding="utf-8")
        assert gestor.leer() == []
        imprimir_color(
            "ERROR ESPERADO: archivo JSON dañado; lectura vacía.",
            "ROJO",
        )

        # Si la raíz del JSON no es una lista, leer() también devuelve una lista vacía.
        ruta_archivo.write_text('{"estudiante": "Ana"}', encoding="utf-8")
        assert gestor.leer() == []
        imprimir_color("AVISO: la raíz JSON debe ser una lista de estudiantes.", "AMARILLO")

        # La herramienta compartida usa blanco como respaldo para un color desconocido.
        imprimir_color("Prueba del color de respaldo.", "COLOR_NO_EXISTE")

    # Confirma que todas las comprobaciones anteriores finalizaron.
    imprimir_color("OK: todas las pruebas del gestor JSON terminaron correctamente.", "VERDE")
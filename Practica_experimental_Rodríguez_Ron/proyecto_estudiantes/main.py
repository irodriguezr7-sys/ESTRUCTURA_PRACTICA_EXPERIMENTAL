import sys
from pathlib import Path

raiz_proyecto = Path(__file__).resolve().parent.parent
if str(raiz_proyecto) not in sys.path:
    sys.path.insert(0, str(raiz_proyecto))

from models import CAMPOS_ESTUDIANTE, Estudiante
from shared.herramientas import (
    confirmar,
    imprimir_error,
    imprimir_exito,
    imprimir_info,
    imprimir_titulo,
)
import views as controlador


def pausa():
    input("\nPresione Enter para continuar...")


def mostrar_tabla(estudiantes):
    print(
        f"{'ID':<5}{'NOMBRE':<28}{'EMAIL':<30}"
        f"{'CARNET':<16}{'CIUDAD':<18}{'PROMEDIO':<10}"
    )
    print("-" * 107)
    for estudiante in estudiantes:
        print(
            f"{estudiante.id:<5}"
            f"{estudiante.obtener_nombre_completo():<28}"
            f"{estudiante.email:<30}"
            f"{estudiante.carnet:<16}"
            f"{estudiante.ciudad or 'Sin ciudad':<18}"
            f"{estudiante.obtener_promedio():<10}"
        )
    print("-" * 107)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


def opcion_crear():
    imprimir_titulo("CREAR ESTUDIANTE")
    datos = {}
    for campo in CAMPOS_ESTUDIANTE:
        etiqueta = "Ciudad (opcional)" if campo == "ciudad" else campo.capitalize()
        datos[campo] = input(f"{etiqueta}: ")
    exito, mensaje = controlador.crear_estudiante(datos)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_ver_todos():
    imprimir_titulo("LISTA DE ESTUDIANTES")
    estudiantes = controlador.obtener_todos()
    if estudiantes:
        mostrar_tabla(estudiantes)
    else:
        imprimir_info("Todavía no hay estudiantes registrados.")
    pausa()


def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, apellido, email o carnet: ")
    encontrados = controlador.buscar_estudiantes(termino)
    if encontrados:
        mostrar_tabla(encontrados)
    else:
        imprimir_info(f"Ningún estudiante coincide con '{termino}'.")
    pausa()


def opcion_ver_por_id():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = controlador.obtener_por_id(id_estudiante)
    if estudiante is None:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
    else:
        for clave, valor in estudiante.a_diccionario().items():
            print(f"  {clave.capitalize():<12}: {valor}")
    pausa()


def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = controlador.obtener_por_id(id_estudiante)
    if estudiante is None:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        return pausa()

    imprimir_info(f"Editando a {estudiante.obtener_nombre_completo()}")
    print("Deje en blanco el campo que no quiera cambiar.\n")
    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        valor_actual = getattr(estudiante, campo)
        valor_nuevo = input(f"{campo.capitalize()} [{valor_actual}]: ").strip()
        if valor_nuevo:
            cambios[campo] = valor_nuevo

    exito, mensaje = controlador.actualizar_estudiante(id_estudiante, cambios)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = controlador.obtener_por_id(id_estudiante)
    if estudiante is None:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        return pausa()

    imprimir_info(f"Se eliminará: {estudiante}")
    if confirmar("¿Confirma la eliminación?"):
        exito, mensaje = controlador.eliminar_estudiante(id_estudiante)
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    else:
        imprimir_info("Operación cancelada")
    pausa()


def opcion_agregar_nota():
    imprimir_titulo("AGREGAR NOTA")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    materia = input("Materia: ")
    nota = input("Nota (0-20): ")
    exito, mensaje = controlador.agregar_nota(id_estudiante, materia, nota)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_ver_promedio():
    imprimir_titulo("VER PROMEDIO")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = controlador.obtener_por_id(id_estudiante)
    if estudiante is None:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
    else:
        imprimir_info(
            f"Promedio de {estudiante.obtener_nombre_completo()}: "
            f"{estudiante.obtener_promedio()}"
        )
    pausa()


def opcion_materias_en_comun():
    imprimir_titulo("MATERIAS EN COMÚN")
    try:
        id_a = int(input("Id del primer estudiante: "))
        id_b = int(input("Id del segundo estudiante: "))
    except ValueError:
        imprimir_error("Los ids deben ser números enteros")
        return pausa()

    exito, resultado = controlador.estudiantes_en_comun(id_a, id_b)
    if not exito:
        imprimir_error(resultado)
    elif resultado:
        imprimir_info(f"Materias compartidas: {', '.join(sorted(resultado))}")
    else:
        imprimir_info("No tienen materias en común.")
    pausa()


def opcion_materias_ofertadas():
    imprimir_titulo("MATERIAS INSCRITAS")
    materias = sorted(controlador.materias_ofertadas())
    if materias:
        for materia in materias:
            print(f"- {materia}")
    else:
        imprimir_info("Todavía no hay materias inscritas.")
    pausa()


def salir():
    imprimir_info("¡Hasta luego!")
    return "salir"


OPCIONES = {
    "1": ("Crear estudiante", opcion_crear),
    "2": ("Ver todos", opcion_ver_todos),
    "3": ("Buscar", opcion_buscar),
    "4": ("Ver por id", opcion_ver_por_id),
    "5": ("Actualizar", opcion_actualizar),
    "6": ("Eliminar", opcion_eliminar),
    "7": ("Agregar nota", opcion_agregar_nota),
    "8": ("Ver promedio", opcion_ver_promedio),
    "9": ("Materias en común", opcion_materias_en_comun),
    "10": ("Materias inscritas", opcion_materias_ofertadas),
    "0": ("Salir", salir),
}


def mostrar_menu():
    imprimir_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTES")
    for tecla, (texto, _funcion) in OPCIONES.items():
        print(f"  {tecla}. {texto}")
    print()


def main():
    while True:
        mostrar_menu()
        tecla = input("Seleccione una opción: ").strip()
        if tecla not in OPCIONES:
            imprimir_error("Opción no válida")
            pausa()
            continue

        _texto, funcion = OPCIONES[tecla]
        if funcion() == "salir":
            break


if __name__ == "__main__":
    print("=== PRUEBA DE ESTUDIANTES ===")
    imprimir_info("Se probarán las dos instancias y sus funciones principales.")

    estudiante1 = Estudiante(
        1,
        "Ana",
        "Pérez",
        "ana@unemi.edu.ec",
        "EST2026001",
        notas={"Matemática": [18, 19, 20], "Inglés": [16, 17]},
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

    print(estudiante1)
    print(estudiante2)
    print("Estudiante en diccionario:", estudiante1.a_diccionario())
    assert estudiante1.obtener_nombre_completo() == "Ana Pérez"
    assert estudiante1.obtener_promedio() == 18
    assert estudiante2.obtener_promedio() == 0
    assert estudiante1.materias_en_comun(estudiante2) == {"Matemática"}

    # Reconstruye un estudiante desde el diccionario compatible con JSON.
    estudiante_recuperado = Estudiante.desde_diccionario(
        estudiante1.a_diccionario()
    )
    assert estudiante_recuperado.email == estudiante1.email
    assert estudiante_recuperado.materias == estudiante1.materias

    estudiante1.agregar_nota("Programación", 20)
    assert estudiante1.notas["Programación"] == [20]
    assert "Programación" in estudiante1.materias
    imprimir_exito("Instancias, notas, promedio, materias y conversión comprobados.")

    imprimir_error("Ejemplo de mensaje de error (solo demostración visual).")
    imprimir_info("La prueba terminó; ahora se inicia el menú.")

    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")

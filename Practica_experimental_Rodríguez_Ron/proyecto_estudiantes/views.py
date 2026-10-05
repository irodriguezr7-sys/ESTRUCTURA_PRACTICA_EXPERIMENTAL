import sys
from pathlib import Path

raiz_proyecto = Path(__file__).resolve().parent.parent
if str(raiz_proyecto) not in sys.path:
    sys.path.insert(0, str(raiz_proyecto))

from models import CAMPOS_ESTUDIANTE, Estudiante
from shared.herramientas import es_email_valido
from shared.json_manager import GestorJSON

RUTA_DATOS = raiz_proyecto / "data" / "estudiantes.json"
gestor = GestorJSON(str(RUTA_DATOS))


# TUPLAS de configuración: campos obligatorios y campos donde se busca.
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = CAMPOS_ESTUDIANTE


# ===================== AYUDAS INTERNAS =====================

def identificadores_registrados(campo, excepto_id=None):
    """Devuelve un conjunto de emails o carnets ya usados."""
    return {
        str(registro.get(campo, "")).strip().casefold()
        for registro in gestor.leer()
        if registro.get("id") != excepto_id
    }


def siguiente_id():
    ids = [registro["id"] for registro in gestor.leer()]
    return max(ids) + 1 if ids else 1


# ===================== C · CREATE =====================

def crear_estudiante(datos):
    """Crea un estudiante y devuelve (exito, mensaje)."""
    valores = {
        campo: str(datos.get(campo, "")).strip()
        for campo in CAMPOS_ESTUDIANTE
    }

    faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if not valores[campo]]
    if faltantes:
        return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

    if not es_email_valido(valores["email"]):
        return False, f"El email '{valores['email']}' no tiene un formato válido"

    if valores["email"].casefold() in identificadores_registrados("email"):
        return False, "Ese email ya está registrado"

    if valores["carnet"].casefold() in identificadores_registrados("carnet"):
        return False, "Ese carnet ya está registrado"

    estudiante = Estudiante(siguiente_id(), **valores)
    registros = gestor.leer()
    registros.append(estudiante.a_diccionario())
    if not gestor.guardar(registros):
        return False, "No se pudo escribir el archivo de estudiantes"

    return True, (
        f"Estudiante {estudiante.obtener_nombre_completo()} "
        f"creado con id {estudiante.id}"
    )


# ===================== R · READ =====================

def obtener_todos():
    """Devuelve la lista de objetos Estudiante registrados."""
    return [Estudiante.desde_diccionario(registro) for registro in gestor.leer()]


def obtener_por_id(id_estudiante):
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante
    return None


# ===================== S · SEARCH =====================

def buscar_estudiantes(termino):
    """Busca estudiantes por nombre, apellido, email o carnet."""
    termino = termino.strip().casefold()
    if not termino:
        return []

    encontrados = []
    for registro in gestor.leer():
        if any(
            termino in str(registro.get(campo, "")).casefold()
            for campo in CAMPOS_BUSCABLES
        ):
            encontrados.append(Estudiante.desde_diccionario(registro))
    return encontrados


# ===================== U · UPDATE =====================

def actualizar_estudiante(id_estudiante, cambios):
    """Actualiza únicamente los campos básicos indicados."""
    desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
    if desconocidos:
        return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"
    if not cambios:
        return False, "No se indicó ningún cambio"

    cambios_limpios = {
        campo: str(valor).strip()
        for campo, valor in cambios.items()
    }
    vacios = [
        campo for campo, valor in cambios_limpios.items()
        if not valor and campo != "ciudad"
    ]
    if vacios:
        return False, f"Los campos no pueden quedar vacíos: {', '.join(vacios)}"

    if "email" in cambios_limpios:
        email = cambios_limpios["email"]
        if not es_email_valido(email):
            return False, "El email no tiene un formato válido"
        if email.casefold() in identificadores_registrados("email", id_estudiante):
            return False, "Ese email ya lo usa otro estudiante"

    if "carnet" in cambios_limpios:
        carnet = cambios_limpios["carnet"]
        if carnet.casefold() in identificadores_registrados("carnet", id_estudiante):
            return False, "Ese carnet ya lo usa otro estudiante"

    registros = gestor.leer()
    for registro in registros:
        if registro.get("id") == id_estudiante:
            registro.update(cambios_limpios)
            if not gestor.guardar(registros):
                return False, "No se pudo guardar la actualización"
            return True, f"Estudiante {id_estudiante} actualizado ({len(cambios_limpios)} campo/s)"

    return False, f"No existe un estudiante con id {id_estudiante}"


# ===================== D · DELETE =====================

def eliminar_estudiante(id_estudiante):
    registros = gestor.leer()
    quedan = [
        registro for registro in registros
        if registro.get("id") != id_estudiante
    ]

    if len(quedan) == len(registros):
        return False, f"No existe un estudiante con id {id_estudiante}"
    if not gestor.guardar(quedan):
        return False, "No se pudo guardar la eliminación"

    return True, f"Estudiante {id_estudiante} eliminado"


# ===================== NOTAS Y MATERIAS =====================

def agregar_nota(id_estudiante, materia, nota):
    """Agrega una nota entera entre 0 y 20 al estudiante indicado."""
    materia = materia.strip()
    if not materia:
        return False, "La materia no puede estar vacía"

    try:
        nota_numerica = int(nota)
    except (TypeError, ValueError):
        return False, "La nota debe ser un número entero entre 0 y 20"

    if not 0 <= nota_numerica <= 20:
        return False, "La nota debe estar entre 0 y 20"

    registros = gestor.leer()
    for indice, registro in enumerate(registros):
        if registro.get("id") == id_estudiante:
            estudiante = Estudiante.desde_diccionario(registro)
            estudiante.agregar_nota(materia, nota_numerica)
            registros[indice] = estudiante.a_diccionario()
            if not gestor.guardar(registros):
                return False, "No se pudo guardar la nota"
            return True, (
                f"Nota {nota_numerica} agregada en {materia} "
                f"para {estudiante.obtener_nombre_completo()}"
            )

    return False, f"No existe un estudiante con id {id_estudiante}"


def estudiantes_en_comun(id_a, id_b):
    """Devuelve el conjunto de materias compartidas por dos estudiantes."""
    estudiante_a = obtener_por_id(id_a)
    if estudiante_a is None:
        return False, f"No existe un estudiante con id {id_a}"

    estudiante_b = obtener_por_id(id_b)
    if estudiante_b is None:
        return False, f"No existe un estudiante con id {id_b}"

    return True, estudiante_a.materias_en_comun(estudiante_b)


def materias_ofertadas():
    """Devuelve el conjunto de materias en las que hay estudiantes inscritos."""
    materias = set()
    for estudiante in obtener_todos():
        materias.update(estudiante.materias)
    return materias


def estudiantes_por_ciudad():
    """Agrupa los nombres de estudiantes por ciudad de residencia."""
    agrupados = {}
    for registro in gestor.leer():
        ciudad = str(registro.get("ciudad", "")).strip().title()
        ciudad = ciudad or "Sin ciudad"
        agrupados.setdefault(ciudad, []).append(registro["nombre"])
    return agrupados


# Las pruebas se ejecutan solo cuando este archivo se inicia directamente.
if __name__ == "__main__":
    import sys
    import tempfile
    from pathlib import Path

    raiz_proyecto = Path(__file__).resolve().parent.parent
    if str(raiz_proyecto) not in sys.path:
        sys.path.insert(0, str(raiz_proyecto))

    from shared.herramientas import imprimir_error, imprimir_exito, imprimir_info

    print("=== PRUEBAS DEL CONTROLADOR DE ESTUDIANTES ===")
    imprimir_info("Se probarán el registro, búsqueda, edición, notas y eliminación.")

    gestor_original = gestor
    with tempfile.TemporaryDirectory() as carpeta_temporal:
        gestor = GestorJSON(
            str(Path(carpeta_temporal) / "estudiantes.json")
        )

        datos_ana = {
            "nombre": "Ana",
            "apellido": "Pérez",
            "email": "ana@unemi.edu.ec",
            "carnet": "EST2026001",
            "ciudad": "Guayaquil",
        }
        datos_luis = {
            "nombre": "Luis",
            "apellido": "Gómez",
            "email": "luis@unemi.edu.ec",
            "carnet": "EST2026002",
            "ciudad": "Quito",
        }

        exito, _ = crear_estudiante(datos_ana)
        assert exito
        exito, _ = crear_estudiante(datos_luis)
        assert exito
        assert crear_estudiante(datos_ana)[0] is False
        assert crear_estudiante({**datos_ana, "email": "no-es-correo"})[0] is False
        assert crear_estudiante({**datos_ana, "email": "otro@unemi.edu.ec"})[0] is False
        imprimir_exito("Registro, validación de datos y detección de duplicados.")

        todos = obtener_todos()
        assert len(todos) == 2
        assert obtener_por_id(1).nombre == "Ana"
        assert obtener_por_id(99) is None
        assert len(buscar_estudiantes("ANA")) == 1
        assert len(buscar_estudiantes("EST2026002")) == 1
        assert buscar_estudiantes("quito")[0].nombre == "Luis"
        assert buscar_estudiantes("   ") == []
        assert estudiantes_por_ciudad() == {
            "Guayaquil": ["Ana"],
            "Quito": ["Luis"],
        }
        assert actualizar_estudiante(2, {"ciudad": ""})[0]
        assert estudiantes_por_ciudad() == {
            "Guayaquil": ["Ana"],
            "Sin ciudad": ["Luis"],
        }
        imprimir_exito("Lectura por lista e id, y búsqueda por campos.")

        assert actualizar_estudiante(1, {"apellido": "López"})[0]
        assert actualizar_estudiante(1, {"email": "correo-invalido"})[0] is False
        assert actualizar_estudiante(1, {"email": "luis@unemi.edu.ec"})[0] is False
        assert actualizar_estudiante(1, {"carnet": "EST2026002"})[0] is False
        assert actualizar_estudiante(1, {"campo": "valor"})[0] is False
        assert actualizar_estudiante(99, {"apellido": "López"})[0] is False
        imprimir_exito("Actualización y validación de campos, email y carnet.")

        assert agregar_nota(1, "Matemática", "18")[0]
        assert agregar_nota(1, "Matemática", "20")[0]
        assert agregar_nota(2, "Historia", "12")[0]
        assert agregar_nota(2, "Matemática", "15")[0]
        assert agregar_nota(1, "Ciencias", "21")[0] is False
        assert agregar_nota(1, "Ciencias", "abc")[0] is False
        assert agregar_nota(99, "Ciencias", "15")[0] is False
        assert obtener_por_id(1).obtener_promedio() == 19
        assert estudiantes_en_comun(1, 2) == (True, {"Matemática"})
        assert materias_ofertadas() == {"Matemática", "Historia"}
        imprimir_exito("Registro de notas, promedio y conjuntos de materias.")

        assert eliminar_estudiante(1)[0]
        assert eliminar_estudiante(1)[0] is False
        assert len(obtener_todos()) == 1
        imprimir_exito("Eliminación y manejo de estudiante inexistente.")

    gestor = gestor_original
    # Deja los estudiantes de ejemplo en el JSON real sin borrar datos existentes.
    if not RUTA_DATOS.exists():
        estudiantes_prueba = [
            {
                "id": 1,
                "nombre": "Ana",
                "apellido": "Pérez",
                "email": "ana@unemi.edu.ec",
                "carnet": "EST2026001",
                "ciudad": "Guayaquil",
                "notas": {
                    "Matemática": [18, 20],
                    "Inglés": [16],
                },
                "materias": ["Inglés", "Matemática"],
            },
            {
                "id": 2,
                "nombre": "Luis",
                "apellido": "Gómez",
                "email": "luis@unemi.edu.ec",
                "carnet": "EST2026002",
                "ciudad": "Quito",
                "notas": {},
                "materias": ["Historia", "Matemática"],
            },
        ]
        assert gestor.guardar(estudiantes_prueba), (
            f"No se pudo crear el archivo {RUTA_DATOS}"
        )
        imprimir_exito(f"Se creó {RUTA_DATOS} con los estudiantes de prueba.")
    else:
        imprimir_info(
            f"Ya existe {RUTA_DATOS}; se conservaron sus datos."
        )

    imprimir_error("Ejemplo de mensaje de error (solo demostración visual).")
    imprimir_exito("Todas las pruebas del controlador terminaron correctamente.")

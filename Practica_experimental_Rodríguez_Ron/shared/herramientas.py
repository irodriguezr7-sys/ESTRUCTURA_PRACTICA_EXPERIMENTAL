import os

# DICCIONARIO: cada nombre de color se relaciona con su código ANSI.
COLORES = {
    "ROJO": "\033[91m",
    "VERDE": "\033[92m",
    "AZUL": "\033[94m",
    "AMARILLO": "\033[93m",
    "CYAN": "\033[96m",
    "BLANCO": "\033[97m",
    "RESET": "\033[0m",
}

# TUPLA: respuestas afirmativas aceptadas por confirmar().
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")


# Limpia la consola usando el comando que corresponde al sistema operativo.
def limpiar_pantalla():
    os.system("clear" if os.name == "posix" else "cls")


# Imprime texto coloreado; si el color no existe, utiliza blanco.
def imprimir_color(texto, color):
    codigo = COLORES.get(color, COLORES["BLANCO"])   # .get evita el error si el color no existe
    print(f"{codigo}{texto}{COLORES['RESET']}")


# Limpia la consola y muestra un título enmarcado en azul.
def imprimir_titulo(texto):
    limpiar_pantalla()
    imprimir_color("=" * 60, "AZUL")
    print(f"  {texto}".center(60))
    imprimir_color("=" * 60, "AZUL")
    print()


# Imprime un mensaje de éxito en verde.
def imprimir_exito(mensaje):
    imprimir_color(f"✓ {mensaje}", "VERDE")


# Imprime un mensaje de error en rojo.
def imprimir_error(mensaje):
    imprimir_color(f"✗ {mensaje}", "ROJO")


# Imprime un mensaje informativo en cian.
def imprimir_info(mensaje):
    imprimir_color(f"ℹ {mensaje}", "CYAN")


# Pregunta al usuario y acepta cualquiera de las respuestas afirmativas de la tupla.
def confirmar(pregunta):
    # Devuelve True si el usuario respondió algo de la tupla RESPUESTAS_SI
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()
    return respuesta in RESPUESTAS_SI


# Comprueba que un correo tenga texto antes y después de @ y un punto en el dominio.
def es_email_valido(texto):
    # Validación mínima: un @, algo antes, algo después y un punto al final
    texto = texto.strip()
    if texto.count("@") != 1:
        return False
    usuario, dominio = texto.split("@")
    return len(usuario) > 0 and "." in dominio and not dominio.endswith(".")


# Las pruebas solo se ejecutan al abrir este archivo directamente.
if __name__ == "__main__":
    # Imports locales: se usan solo para comprobar la salida y simular respuestas.
    from contextlib import redirect_stdout
    from io import StringIO
    from unittest.mock import patch

    # Usa diccionarios para que la prueba no dependa de otros archivos del proyecto.
    estudiante1 = {
        "id": 1,
        "nombre": "Ana",
        "apellido": "Pérez",
        "email": "ana@unemi.edu.ec",
        "carnet": "EST2026001",
        "notas": {"Matemática": [18, 19, 20], "Inglés": [16, 17]},
        "materias": {"Matemática", "Inglés"},
    }
    estudiante2 = {
        "id": 2,
        "nombre": "Luis",
        "apellido": "Gómez",
        "email": "luis@unemi.edu.ec",
        "carnet": "EST2026002",
        "notas": {},
        "materias": {"Matemática", "Historia"},
    }

    # Muestra las instancias de ejemplo que se usarán en las pruebas.
    print("=== PRUEBAS DE HERRAMIENTAS CON ESTUDIANTES ===")
    print("Estudiante 1:", estudiante1)
    print("Estudiante 2:", estudiante2)

    # Comprueba que limpiar_pantalla envía el comando adecuado al sistema operativo.
    with patch.object(os, "system") as comando_sistema:
        limpiar_pantalla()
        comando_esperado = "clear" if os.name == "posix" else "cls"
        comando_sistema.assert_called_once_with(comando_esperado)
    imprimir_color("OK - limpiar_pantalla(): comando correcto.", "VERDE")

    # Comprueba que todos los colores definidos y el respaldo blanco producen ANSI.
    salida = StringIO()
    with redirect_stdout(salida):
        for nombre_color in ("ROJO", "VERDE", "AZUL", "AMARILLO", "CYAN", "BLANCO"):
            imprimir_color(f"Prueba {nombre_color}", nombre_color)
        imprimir_color("Color desconocido", "NO_EXISTE")
    texto_coloreado = salida.getvalue()
    for nombre_color in ("ROJO", "VERDE", "AZUL", "AMARILLO", "CYAN", "BLANCO"):
        assert COLORES[nombre_color] in texto_coloreado
    assert "Color desconocido" in texto_coloreado
    assert COLORES["BLANCO"] in texto_coloreado
    imprimir_color("OK - imprimir_color(): seis colores y respaldo blanco.", "VERDE")

    # Comprueba que imprimir_titulo limpia la consola e imprime el título en azul.
    salida = StringIO()
    with patch.object(os, "system") as comando_sistema:
        with redirect_stdout(salida):
            imprimir_titulo("PRUEBA DE ESTUDIANTES")
    comando_sistema.assert_called_once_with(comando_esperado)
    assert "PRUEBA DE ESTUDIANTES" in salida.getvalue()
    assert COLORES["AZUL"] in salida.getvalue()
    imprimir_color("OK - imprimir_titulo(): texto, limpieza y azul.", "VERDE")

    # Comprueba texto y color de los mensajes de éxito, error e información.
    salida = StringIO()
    with redirect_stdout(salida):
        imprimir_exito("Estudiante registrado")
        imprimir_error("Carnet duplicado")
        imprimir_info("Prueba informativa")
    mensajes = salida.getvalue()
    assert "Estudiante registrado" in mensajes
    assert "Carnet duplicado" in mensajes
    assert "Prueba informativa" in mensajes
    assert COLORES["VERDE"] in mensajes
    assert COLORES["ROJO"] in mensajes
    assert COLORES["CYAN"] in mensajes
    # Llama de nuevo a las tres funciones sin capturar la salida para ver sus símbolos.
    print("\n=== EJEMPLOS VISIBLES DE LOS MENSAJES ===")
    imprimir_exito("Estudiante registrado correctamente")
    imprimir_error("No se pudo registrar el estudiante")
    imprimir_info("El estudiante está inscrito en Matemática")

    # Comprueba todas las respuestas afirmativas definidas en la tupla.
    for respuesta in RESPUESTAS_SI:
        with patch("builtins.input", return_value=respuesta):
            assert confirmar("¿Continuar?") is True

    # Comprueba espacios y mayúsculas en afirmativas: strip() y lower() las normalizan.
    for respuesta in (" SI ", "Sí", " YES ", "Y"):
        with patch("builtins.input", return_value=respuesta):
            assert confirmar("¿Continuar?") is True

    # Comprueba varias respuestas negativas, vacías y no reconocidas.
    for respuesta in ("no", "n", "talvez", "", "  NO  "):
        with patch("builtins.input", return_value=respuesta):
            assert confirmar("¿Continuar?") is False
    imprimir_color("OK - confirmar(): casos afirmativos y negativos.", "VERDE")

    # Define correos válidos de estudiantes UNEMI y casos de formato incorrecto.
    correos_validos = (
        estudiante1["email"],
        estudiante2["email"],
        "ana.perez@facultad.unemi.edu.ec",
        "  ana@unemi.edu.ec  ",
    )
    correos_invalidos = (
        "",
        "ana@@unemi.edu.ec",
        "@unemi.edu.ec",
        "ana@unemi",
        "ana@unemi.",
        "ana.unemi.edu.ec",
    )

    # Comprueba cada correo y presenta el resultado con los colores compartidos.
    for correo in correos_validos:
        assert es_email_valido(correo)
        imprimir_color(f"OK - correo válido y registrado: {correo.strip()}", "VERDE")

    for correo in correos_invalidos:
        assert not es_email_valido(correo)
        imprimir_color(f"ERROR - correo inválido rechazado: {correo or '(vacío)'}", "ROJO")

    # Comprueba además casos básicos de instancias y carnets diferentes.
    assert estudiante1["id"] != estudiante2["id"]
    assert estudiante1["carnet"] != estudiante2["carnet"]

    # Muestra directamente en la terminal cada color disponible.
    print("\n=== MUESTRA DE COLORES EN LA TERMINAL ===")
    for nombre_color in ("ROJO", "VERDE", "AZUL", "AMARILLO", "CYAN", "BLANCO"):
        imprimir_color(f"Este texto debe verse en {nombre_color.lower()}", nombre_color)

    # Informa con el visto verde que todas las comprobaciones terminaron bien.
    imprimir_exito("Todas las pruebas terminaron correctamente.")
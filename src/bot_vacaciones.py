from datetime import datetime


# ------------------------------------------------------------
# Trabajo Practico Integrador - Organizacion Empresarial
# Chatbot para solicitud de vacaciones de empleados
# Empresa ficticia: TecnoGestion S.R.L.
# ------------------------------------------------------------

# El programa funciona como un simulador por consola.
# Lee los empleados desde un archivo CSV y permite realizar
# una solicitud de vacaciones.
#
# Las solicitudes no se guardan de forma permanente.
# Solo se almacenan en una lista mientras el programa esta abierto.
#
# El archivo solicitudes.csv queda como plantilla de estructura,
# pero esta version del simulador no escribe datos en ese archivo.


ARCHIVO_EMPLEADOS = "data/empleados.csv"


# Lista principal de empleados.
# Se carga desde el archivo data/empleados.csv.
empleados = []


# Lista de solicitudes generadas durante la ejecucion.
# Cuando el programa termina, esta informacion se pierde.
solicitudes = []


# ------------------------------------------------------------
# Esta funcion lee el archivo CSV de empleados.
# Cada linea del archivo se transforma en un diccionario.
# Luego cada diccionario se agrega a la lista empleados.
# ------------------------------------------------------------
def cargar_empleados():
    try:
        archivo = open(ARCHIVO_EMPLEADOS, "r", encoding="utf-8")
        lineas = archivo.readlines()
        archivo.close()

        # Se empieza desde la linea 1 para saltear el encabezado.
        for i in range(1, len(lineas)):
            linea = lineas[i].strip()

            # Si la linea no esta vacia, se procesa.
            if linea != "":
                datos = linea.split(",")

                empleado = {
                    "legajo": datos[0],
                    "nombre": datos[1],
                    "sector": datos[2],
                    "saldo": int(datos[3]),
                    "estado": datos[4]
                }

                empleados.append(empleado)

    except FileNotFoundError:
        print("Error: no se encontro el archivo", ARCHIVO_EMPLEADOS)
        print("Verifique que el archivo exista y que este ejecutando el programa desde la carpeta principal.")


# ------------------------------------------------------------
# Esta funcion busca un empleado por numero de legajo.
# Si encuentra el legajo, devuelve el diccionario del empleado.
# Si no lo encuentra, devuelve None.
# ------------------------------------------------------------
def buscar_empleado(legajo):
    for empleado in empleados:
        if empleado["legajo"] == legajo:
            return empleado

    return None


# ------------------------------------------------------------
# Esta funcion convierte una fecha escrita como texto
# al formato de fecha de Python usando datetime.
#
# El formato esperado es DD/MM/AAAA.
# Si el formato es correcto, devuelve la fecha convertida.
# Si el formato es incorrecto, devuelve None.
# ------------------------------------------------------------
def convertir_fecha(texto_fecha):
    try:
        fecha = datetime.strptime(texto_fecha, "%d/%m/%Y")
        return fecha
    except ValueError:
        return None


# ------------------------------------------------------------
# Esta funcion calcula la cantidad de dias solicitados.
# Se suma 1 porque si el empleado pide del 10 al 10,
# corresponde contar 1 dia y no 0.
# ------------------------------------------------------------
def calcular_dias(fecha_inicio, fecha_fin):
    diferencia = fecha_fin - fecha_inicio
    dias = diferencia.days + 1

    return dias


# ------------------------------------------------------------
# Esta funcion genera un ID simple para cada solicitud.
# Ejemplo:
# Primera solicitud  -> S001
# Segunda solicitud  -> S002
# Tercera solicitud  -> S003
# ------------------------------------------------------------
def generar_id_solicitud():
    numero = len(solicitudes) + 1
    id_solicitud = "S" + str(numero).zfill(3)

    return id_solicitud


# ------------------------------------------------------------
# Esta funcion registra una solicitud en la lista solicitudes.
# No guarda la informacion en un archivo permanente.
# Solo deja el registro disponible mientras el programa se ejecuta.
# ------------------------------------------------------------
def registrar_solicitud(legajo, fecha_inicio, fecha_fin, dias, estado, observacion):
    solicitud = {
        "id_solicitud": generar_id_solicitud(),
        "legajo": legajo,
        "fecha_inicio": fecha_inicio.strftime("%d/%m/%Y"),
        "fecha_fin": fecha_fin.strftime("%d/%m/%Y"),
        "dias_solicitados": dias,
        "estado_solicitud": estado,
        "observacion": observacion
    }

    solicitudes.append(solicitud)


# ------------------------------------------------------------
# Esta funcion muestra las solicitudes registradas
# durante la ejecucion actual del programa.
# ------------------------------------------------------------
def mostrar_solicitudes():
    print()
    print("Solicitudes registradas durante esta ejecucion:")

    if len(solicitudes) == 0:
        print("No hay solicitudes registradas.")
    else:
        for solicitud in solicitudes:
            print(solicitud)


# ------------------------------------------------------------
# Esta funcion pide el legajo al usuario.
# Si el usuario escribe cancelar, devuelve None.
# Si el legajo existe, devuelve el empleado.
# Si no existe, vuelve a pedir el dato.
# ------------------------------------------------------------
def pedir_y_validar_legajo():
    legajo = input("Bot: Ingrese su numero de legajo: ")

    if legajo.lower() == "cancelar":
        return None

    empleado = buscar_empleado(legajo)

    while empleado is None:
        print("Bot: El legajo ingresado no existe.")
        legajo = input("Bot: Ingrese nuevamente su numero de legajo: ")

        if legajo.lower() == "cancelar":
            return None

        empleado = buscar_empleado(legajo)

    return empleado


# ------------------------------------------------------------
# Esta funcion pide una fecha al usuario.
# El mensaje cambia segun se pida fecha de inicio o de fin.
# Si la fecha esta mal escrita, vuelve a pedirla.
# Si el usuario escribe cancelar, devuelve None.
# ------------------------------------------------------------
def pedir_fecha(mensaje):
    fecha = None

    while fecha is None:
        texto_fecha = input(mensaje)

        if texto_fecha.lower() == "cancelar":
            return None

        fecha = convertir_fecha(texto_fecha)

        if fecha is None:
            print("Bot: Formato invalido. Use DD/MM/AAAA.")

    return fecha


# ------------------------------------------------------------
# Esta funcion muestra los datos principales del empleado.
# Sirve para que el usuario confirme que el legajo encontrado
# corresponde a su informacion.
# ------------------------------------------------------------
def mostrar_datos_empleado(empleado):
    print("Bot: Legajo encontrado.")
    print("Bot: Empleado:", empleado["nombre"])
    print("Bot: Sector:", empleado["sector"])
    print("Bot: Saldo disponible:", empleado["saldo"], "dias.")
    print()


# ------------------------------------------------------------
# Esta funcion aplica las reglas de negocio del proceso.
#
# Regla 1:
# Si los dias solicitados son mayores al saldo, se rechaza.
#
# Regla 2:
# Si hay saldo suficiente pero la solicitud supera 15 dias,
# se deriva a RRHH.
#
# Regla 3:
# Si hay saldo suficiente y son 15 dias o menos,
# se registra como preaprobada.
# ------------------------------------------------------------
def decidir_resultado(empleado, fecha_inicio, fecha_fin, dias_solicitados):
    legajo = empleado["legajo"]

    if dias_solicitados > empleado["saldo"]:
        print("Bot: Solicitud rechazada por saldo insuficiente.")

        registrar_solicitud(
            legajo,
            fecha_inicio,
            fecha_fin,
            dias_solicitados,
            "Rechazada",
            "Saldo insuficiente"
        )

    elif dias_solicitados > 15:
        print("Bot: La solicitud supera los 15 dias.")
        print("Bot: Sera derivada a RRHH para revision manual.")

        registrar_solicitud(
            legajo,
            fecha_inicio,
            fecha_fin,
            dias_solicitados,
            "Derivada",
            "Solicitud mayor a 15 dias"
        )

    else:
        print("Bot: Solicitud registrada como preaprobada.")

        registrar_solicitud(
            legajo,
            fecha_inicio,
            fecha_fin,
            dias_solicitados,
            "Preaprobada",
            "Saldo suficiente"
        )


# ------------------------------------------------------------
# Esta funcion contiene el flujo principal del chatbot.
# Representa el proceso TO-BE:
# 1. Cargar empleados.
# 2. Pedir legajo.
# 3. Validar empleado.
# 4. Pedir fechas.
# 5. Calcular dias.
# 6. Aplicar reglas de negocio.
# 7. Mostrar el resultado.
# ------------------------------------------------------------
def iniciar_chatbot():
    cargar_empleados()

    if len(empleados) == 0:
        print("No se cargaron empleados. El programa no puede continuar.")
        return

    print("Bot: Bienvenido al sistema de solicitud de vacaciones.")
    print("Bot: Escriba 'cancelar' en cualquier momento para terminar la operacion.")
    print()

    empleado = pedir_y_validar_legajo()

    if empleado is None:
        print("Bot: Operacion cancelada.")
        return

    if empleado["estado"] != "Activo":
        print("Bot: El empleado no se encuentra activo.")
        print("Bot: La solicitud debe ser revisada por RRHH.")
        return

    mostrar_datos_empleado(empleado)

    fecha_inicio = pedir_fecha("Bot: Ingrese fecha de inicio (DD/MM/AAAA): ")

    if fecha_inicio is None:
        print("Bot: Operacion cancelada.")
        return

    fecha_fin = pedir_fecha("Bot: Ingrese fecha de fin (DD/MM/AAAA): ")

    if fecha_fin is None:
        print("Bot: Operacion cancelada.")
        return

    dias_solicitados = calcular_dias(fecha_inicio, fecha_fin)

    if dias_solicitados <= 0:
        print("Bot: La fecha de fin no puede ser anterior a la fecha de inicio.")
        print("Bot: Solicitud cancelada. Inicie nuevamente el tramite.")
        return

    print()
    print("Bot: Usted solicito", dias_solicitados, "dia/s de vacaciones.")

    decidir_resultado(empleado, fecha_inicio, fecha_fin, dias_solicitados)

    mostrar_solicitudes()

    print()
    print("Bot: Fin del proceso.")


# ------------------------------------------------------------
# Llamamos a la funcion principal para iniciar el programa.
# ------------------------------------------------------------
iniciar_chatbot()
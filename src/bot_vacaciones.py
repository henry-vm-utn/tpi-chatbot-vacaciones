# TP Organizacion Empresarial
# Sistema de solicitud de vacaciones
# Fecha de modificacion: 10/06/2026


# Datos iniciales del sistema

empleados = [
    {"legajo": "1001", "nombre": "Ana Lopez", "sector": "Administracion", "saldo": 14, "estado": "Activo"},
    {"legajo": "1002", "nombre": "Bruno Diaz", "sector": "Soporte", "saldo": 5, "estado": "Activo"},
    {"legajo": "1003", "nombre": "Carla Perez", "sector": "Desarrollo", "saldo": 20, "estado": "Activo"},
    {"legajo": "1004", "nombre": "Diego Ruiz", "sector": "Soporte", "saldo": 0, "estado": "Activo"},
    {"legajo": "1005", "nombre": "Elena Gomez", "sector": "Administracion", "saldo": 18, "estado": "Inactivo"}
]

solicitudes = []


# Busca un empleado segun el numero de legajo ingresado

def buscar_empleado(legajo):
    for empleado in empleados:
        if empleado["legajo"] == legajo:
            return empleado
    return None


# Funciones para validar y calcular fechas

def es_bisiesto(anio):
    if anio % 400 == 0:
        return True
    elif anio % 100 == 0:
        return False
    elif anio % 4 == 0:
        return True
    else:
        return False


def obtener_dias_del_mes(mes, anio):
    dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if mes == 2 and es_bisiesto(anio):
        return 29
    else:
        return dias_por_mes[mes - 1]


def convertir_fecha(texto_fecha):
    partes = texto_fecha.split("/")

    if len(partes) != 3:
        return None

    if not partes[0].isdigit() or not partes[1].isdigit() or not partes[2].isdigit():
        return None

    dia = int(partes[0])
    mes = int(partes[1])
    anio = int(partes[2])

    if anio < 1900:
        return None

    if mes < 1 or mes > 12:
        return None

    dias_del_mes = obtener_dias_del_mes(mes, anio)

    if dia < 1 or dia > dias_del_mes:
        return None

    return [dia, mes, anio]


def convertir_fecha_a_dias(fecha):
    dia = fecha[0]
    mes = fecha[1]
    anio = fecha[2]

    total = 0

    for anio_actual in range(1900, anio):
        if es_bisiesto(anio_actual):
            total = total + 366
        else:
            total = total + 365

    for mes_actual in range(1, mes):
        total = total + obtener_dias_del_mes(mes_actual, anio)

    total = total + dia

    return total


def calcular_dias(fecha_inicio, fecha_fin):
    dias_inicio = convertir_fecha_a_dias(fecha_inicio)
    dias_fin = convertir_fecha_a_dias(fecha_fin)
    return dias_fin - dias_inicio + 1


def mostrar_fecha(fecha):
    dia = str(fecha[0]).zfill(2)
    mes = str(fecha[1]).zfill(2)
    anio = str(fecha[2])
    return dia + "/" + mes + "/" + anio


# Registro y visualizacion de solicitudes

def generar_id_solicitud():
    numero = len(solicitudes) + 1
    return "S" + str(numero).zfill(3)


def registrar_solicitud(legajo, fecha_inicio, fecha_fin, dias, estado, observacion):
    solicitud = {
        "id_solicitud": generar_id_solicitud(),
        "legajo": legajo,
        "fecha_inicio": mostrar_fecha(fecha_inicio),
        "fecha_fin": mostrar_fecha(fecha_fin),
        "dias_solicitados": dias,
        "estado_solicitud": estado,
        "observacion": observacion
    }

    solicitudes.append(solicitud)


def mostrar_solicitudes():
    print("\nSolicitudes registradas:")

    if len(solicitudes) == 0:
        print("No hay solicitudes registradas.")
    else:
        for solicitud in solicitudes:
            print(solicitud)


# Desarrollo principal del chatbot

def iniciar_chatbot():
    print("Bot: Bienvenido al sistema de solicitud de vacaciones.")
    print("Bot: Escriba 'cancelar' en cualquier momento para terminar la operacion.\n")

    legajo = input("Bot: Ingrese su numero de legajo: ")

    if legajo.lower() == "cancelar":
        print("Bot: Operacion cancelada.")
        return

    empleado = buscar_empleado(legajo)

    while empleado is None:
        print("Bot: El legajo ingresado no existe.")
        legajo = input("Bot: Ingrese nuevamente su numero de legajo: ")

        if legajo.lower() == "cancelar":
            print("Bot: Operacion cancelada.")
            return

        empleado = buscar_empleado(legajo)

    if empleado["estado"] != "Activo":
        print("Bot: El empleado no se encuentra activo. La solicitud debe ser revisada por RRHH.")
        return

    print("Bot: Legajo encontrado.")
    print("Bot: Empleado:", empleado["nombre"])
    print("Bot: Sector:", empleado["sector"])
    print("Bot: Saldo disponible:", empleado["saldo"], "dias.\n")

    fecha_inicio = None

    while fecha_inicio is None:
        texto_inicio = input("Bot: Ingrese fecha de inicio (DD/MM/AAAA): ")

        if texto_inicio.lower() == "cancelar":
            print("Bot: Operacion cancelada.")
            return

        fecha_inicio = convertir_fecha(texto_inicio)

        if fecha_inicio is None:
            print("Bot: Formato invalido. Use DD/MM/AAAA.")

    fecha_fin = None

    while fecha_fin is None:
        texto_fin = input("Bot: Ingrese fecha de fin (DD/MM/AAAA): ")

        if texto_fin.lower() == "cancelar":
            print("Bot: Operacion cancelada.")
            return

        fecha_fin = convertir_fecha(texto_fin)

        if fecha_fin is None:
            print("Bot: Formato invalido. Use DD/MM/AAAA.")

    dias_solicitados = calcular_dias(fecha_inicio, fecha_fin)

    if dias_solicitados <= 0:
        print("Bot: La fecha de fin no puede ser anterior a la fecha de inicio.")
        print("Bot: Solicitud cancelada. Inicie nuevamente el tramite.")
        return

    print("\nBot: Usted solicito", dias_solicitados, "dia/s de vacaciones.")

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

    mostrar_solicitudes()
    print("\nBot: Fin del proceso.")


# Ejecucion del programa

iniciar_chatbot()
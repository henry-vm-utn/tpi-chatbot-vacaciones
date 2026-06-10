# TPI - Chatbot de Solicitud de Vacaciones

## Descripción

Este proyecto corresponde al Trabajo Práctico Integrador de la materia Organización Empresarial.

Se desarrolló un simulador de chatbot para gestionar solicitudes de vacaciones del personal de una empresa ficticia llamada TecnoGestión S.R.L.

## Objetivo

El objetivo es mejorar un proceso administrativo manual mediante una solución automatizada simple. El bot permite ordenar la solicitud, validar datos, consultar saldo disponible y registrar el resultado.

## Funcionalidades del bot

El bot permite:

- Validar el legajo del empleado.
- Consultar saldo de vacaciones.
- Validar fechas ingresadas.
- Calcular días solicitados.
- Registrar solicitudes preaprobadas.
- Rechazar solicitudes por saldo insuficiente.
- Derivar solicitudes mayores a 15 días a RRHH.
- Cancelar la operación.

## Tecnologías utilizadas

- Python.
- CSV como base de datos simulada.
- BPMN para modelado del proceso.
- GitHub para control de versiones.

## Estructura del proyecto

- `src`: contiene el código del chatbot.
- `data`: contiene la base de datos simulada.
- `bpmn`: contiene los diagramas AS-IS y TO-BE.
- `pruebas`: contiene los casos de prueba.
- `capturas`: contiene evidencias del trabajo.
- `docs`: contiene el informe final.

## Ejecución

Para ejecutar el chatbot:

```bash

python src/bot_vacaciones.py

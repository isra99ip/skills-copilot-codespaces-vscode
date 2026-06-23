# Politica de datos

## Fuentes permitidas

- APIs oficiales.
- Datos con licencia.
- Datos propios.

## Restricciones

- No automatizar scraping sin revisar primero los terminos de uso.
- No versionar datasets grandes en Git.
- No guardar credenciales ni DSN reales en el repositorio.
- No mezclar datos de entrenamiento con datos futuros de evaluacion.

## Registro obligatorio de fuentes

Antes de conectar una fuente nueva, documentar:

| Campo | Descripcion |
| --- | --- |
| Proveedor | Nombre de la fuente o API. |
| URL legal/TOS | Enlace a terminos de uso o licencia. |
| Fecha de revision | Dia en que se revisaron los terminos. |
| Campos usados | Datos concretos que se consumen. |
| Uso permitido | Entrenamiento, backtesting, demo, produccion, etc. |
| Retencion | Cuanto tiempo se guarda el dato. |
| Riesgo | Bajo, medio o alto. |

## Objetivo

Mantener trazabilidad clara de origen, licencia, uso y retencion de cada fuente de datos.
# Bitácora de IA

## Sesión 1 — Preparación del repositorio

- Se creó la estructura base del proyecto.
- Se preservó el archivo heredado de MATLAB en `legacy/` sin editar.
- Se añadió un modelo inicial de trayectoria balística en Python.

## Sesión 2 — Estructura mínima de Python

- Se verificó y organizó el paquete `src/table_tennis_sim/`.
- Se separaron parámetros, física, ejecución de la simulación y visualización.
- Se mantuvo una implementación inicial, simple y tipada, pensada para fines didácticos.
- Aún no se ha traducido la física completa ni las colisiones del script MATLAB.

## Sesión 3 — Estructura alineada con el plan de migración

- Se añadieron los módulos `state.py`, `collisions.py` y `validation.py`.
- Se agruparon los parámetros de pelota, mesa, red y ejecución con `dataclasses` y unidades SI.
- La simulación devuelve un resultado estructurado con series temporales y eventos de rebote.
- Se mantiene un modelo físico básico de gravedad y rebote en mesa; arrastre, Magnus, giro y red quedan para fases posteriores.

## Próximos pasos

1. Revisar y documentar las ecuaciones del archivo MATLAB.
2. Validar parámetros y unidades.
3. Comparar resultados de MATLAB y Python.

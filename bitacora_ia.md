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

## Sesión 4 — Núcleo numérico en NumPy

- Se revisó `legacy/TableTennisTests.mlx` junto con el plan de migración del
  repositorio clonado antes de implementar cambios.
- Se tradujeron la integración de Euler, gravedad, arrastre lineal, efecto
  Magnus, arrastre rotacional, rebote con mesa y colisión simplificada con red.
- Se añadió `InitialConditions` separado de `SimulationParameters`.
- `simulate(parameters, initial_conditions)` devuelve tiempo, posición,
  velocidad, orientación y velocidad angular; `run_simulation` conserva el
  resultado completo con aceleraciones y eventos.
- Se verificaron formas, valores finitos, rebote de mesa y colisión de red.
- No se implementó animación. Los coeficientes de fuerza SI son provisionales
  debido a la ambigüedad de unidades documentada en el plan.

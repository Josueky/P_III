# Plan de migración de MATLAB a Python

## Objetivo

Migrar el contenido de `legacy/TableTennisTests.mlx` a un paquete Python mantenible, verificando que los resultados se conserven.

## Etapas

1. Inventariar variables, supuestos, unidades y gráficas del script original.
2. Extraer parámetros configurables a `parameters.py`.
3. Traducir ecuaciones y cálculos a `physics.py`.
4. Orquestar ejecuciones en `simulation.py`.
5. Replicar gráficas en `visualization.py`.
6. Crear casos de comparación y registrar diferencias en la bitácora.

## Criterio de aceptación

Para entradas equivalentes, Python debe producir trayectorias y métricas consistentes con MATLAB dentro de una tolerancia acordada.

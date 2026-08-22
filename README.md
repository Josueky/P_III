# Proyecto IA: simulación de tenis de mesa

Migración incremental del Live Script MATLAB `legacy/TableTennisTests.mlx` a
una implementación Python modular y verificable.

## Estado actual

El núcleo numérico ya está implementado con NumPy. Incluye integración de
Euler, gravedad, arrastre lineal, efecto Magnus, arrastre rotacional, rebote
con la mesa y colisión simplificada con la red. La función numérica no crea
figuras, pausas, animaciones ni archivos.

La ejecución de referencia de 301 muestras coincide con la exportación MATLAB
dentro de una tolerancia absoluta y relativa de `1e-10`. La animación y la
interfaz interactiva todavía no forman parte de esta fase.

## Estructura

- `legacy/`: Live Script original, conservado sin modificaciones.
- `src/table_tennis_sim/`: parámetros, estado, física, colisiones, simulación y validación.
- `notebooks/`: cuaderno reservado para la etapa interactiva.
- `docs/plan_migracion.md`: arquitectura, criterios de validación y riesgos.
- `docs/validacion_matlab.md`: reproducción completa de la comparación MATLAB–Python.
- `results/`: CSV y gráficas locales; no se versionan salvo archivos de control.
- `bitacora_ia.md`: trazabilidad cronológica del uso de IA y verificaciones.

## Instalación en Windows

Desde PowerShell, en la raíz del repositorio:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:PYTHONPATH = "$PWD\src"
```

## Ejecutar la simulación numérica

```powershell
.\.venv\Scripts\python.exe -c "from table_tennis_sim import InitialConditions, SimulationParameters, simulate; t, x, v, theta, omega = simulate(SimulationParameters(), InitialConditions()); print('Pasos:', len(t)); print('Posición final [m]:', x[-1]); print('Velocidad final [m/s]:', v[-1])"
```

La API principal recibe parámetros y condiciones iniciales por separado:

```python
from table_tennis_sim import InitialConditions, SimulationParameters, simulate

parameters = SimulationParameters()
initial_conditions = InitialConditions()

time, position, velocity, orientation, angular_velocity = simulate(
    parameters,
    initial_conditions,
)
```

`time` tiene forma `(N,)`; las demás salidas tienen forma `(N, 3)`. Las
unidades son segundos, metros, metros por segundo, radianes y radianes por
segundo.

## Reproducir la validación contra MATLAB

Con los cinco CSV en `results/matlab_reference/`:

```powershell
.\.venv\Scripts\python.exe -m table_tennis_sim.validation `
  ".\results\matlab_reference" `
  --plot ".\results\matlab_reference\comparison_python_matlab.png"
```

El comando imprime error máximo, error medio, RMSE, cumplimiento de tolerancia
y el primer paso divergente. También genera una gráfica con las series
superpuestas. Consulte [la guía de validación](docs/validacion_matlab.md) para
exportar los CSV y entender los resultados.

## Documentación

- [Plan de migración](docs/plan_migracion.md)
- [Validación MATLAB–Python](docs/validacion_matlab.md)
- [Bitácora de IA](bitacora_ia.md)

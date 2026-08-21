# Proyecto IA: simulación de tenis de mesa

Migración progresiva de un modelo heredado de MATLAB Live Script a Python, con una simulación interactiva y visualizaciones reproducibles.

## Estructura

- `legacy/`: fuente original, conservada sin modificaciones.
- `src/table_tennis_sim/`: paquete Python de simulación.
- `notebooks/`: exploración interactiva.
- `docs/`: documentación de la migración.
- `results/`: salidas generadas (no se versionan salvo archivos de control).

## Inicio rápido

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m src.table_tennis_sim.simulation
```

## Estado

La versión inicial implementa el esqueleto del simulador. Consulte la [bitácora](bitacora_ia.md) y el [plan de migración](docs/plan_migracion.md).

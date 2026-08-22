# Validación numérica MATLAB–Python

## Objetivo

Comprobar que la traducción NumPy reproduce las series generadas por
`legacy/TableTennisTests.mlx` para las mismas constantes, condiciones
iniciales, paso temporal y duración.

Esta validación demuestra equivalencia numérica para el escenario de
referencia. No demuestra que los coeficientes empíricos constituyan un modelo
físico calibrado para cualquier situación real.

## Escenario de referencia

| Variable | Valor |
| --- | --- |
| Paso temporal | `0.005 s` |
| Duración | `1.5 s` |
| Número de muestras | `301` |
| Posición inicial | `[0, 0.7625, 1.065] m` |
| Velocidad inicial | `[7, -3, -3] m/s` |
| Orientación inicial | `[0, 0, 0] rad` |
| Velocidad angular inicial | `[0, 0, 75·2π] rad/s` |

## 1. Exportar la referencia desde MATLAB

Trabaje sobre una copia del Live Script para preservar intacto el archivo de
`legacy/`. Desactive la animación en esa copia:

```matlab
animate = false;
```

Después de ejecutar la simulación, exporte las cinco series:

```matlab
writematrix(t(:), "matlab_time.csv");
writematrix(x.' / 1000, "matlab_position_m.csv");
writematrix(v.' / 1000, "matlab_velocity_m_s.csv");
writematrix(theta.', "matlab_orientation_rad.csv");
writematrix(omega.', "matlab_angular_velocity_rad_s.csv");
```

La transposición convierte las matrices MATLAB de `3 × N` a `N × 3`. La
división por `1000` convierte posición y velocidad de milímetros a metros.

Ubique los archivos en:

```text
results/matlab_reference/
├── matlab_time.csv
├── matlab_position_m.csv
├── matlab_velocity_m_s.csv
├── matlab_orientation_rad.csv
└── matlab_angular_velocity_rad_s.csv
```

## 2. Preparar Python

Desde PowerShell, en la raíz del repositorio:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:PYTHONPATH = "$PWD\src"
```

## 3. Ejecutar la comparación

```powershell
.\.venv\Scripts\python.exe -m table_tennis_sim.validation `
  ".\results\matlab_reference" `
  --plot ".\results\matlab_reference\comparison_python_matlab.png"
```

`validation.py` realiza estas operaciones:

1. Ejecuta Python con `SimulationParameters()` e `InitialConditions()`.
2. Carga los cinco CSV de MATLAB.
3. Comprueba que las formas de las matrices coincidan.
4. Calcula error absoluto máximo, error absoluto medio y RMSE.
5. Aplica tolerancias absoluta y relativa de `1e-10`.
6. Informa el primer paso fuera de tolerancia, si existe.
7. Guarda una gráfica con las curvas MATLAB y Python superpuestas.

## 4. Resultado obtenido

| Serie | Error absoluto máximo | Dentro de `1e-10` |
| --- | ---: | :---: |
| Tiempo | `2.22e-16 s` | Sí |
| Posición | `8.88e-15 m` | Sí |
| Velocidad | `7.11e-15 m/s` | Sí |
| Orientación | `5.12e-13 rad` | Sí |
| Velocidad angular | `5.12e-13 rad/s` | Sí |

No se encontró ningún paso fuera de tolerancia. Las diferencias observadas son
compatibles con redondeo de punto flotante y precisión de la exportación CSV.

## 5. Interpretación y límites

- La implementación Python reproduce el MATLAB exportado para este escenario.
- La comparación debe repetirse si cambian constantes, condiciones iniciales,
  duración, paso temporal o reglas de colisión.
- La coincidencia numérica no elimina la ambigüedad dimensional documentada en
  `plan_migracion.md` ni sustituye una calibración con datos experimentales.
- La visualización es consumidora de resultados y no interviene en el cálculo.

## Archivos relevantes

- `src/table_tennis_sim/parameters.py`: parámetros y unidades.
- `src/table_tennis_sim/state.py`: condiciones iniciales y resultado completo.
- `src/table_tennis_sim/physics.py`: fuerzas y derivadas.
- `src/table_tennis_sim/collisions.py`: mesa y red.
- `src/table_tennis_sim/simulation.py`: integración y API principal.
- `src/table_tennis_sim/validation.py`: comparación y gráfica.

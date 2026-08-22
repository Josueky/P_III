# Verificación de requisitos de entrega

Auditoría realizada el 22 de agosto de 2026 sobre la rama
`jose/experiments`. Los estados se basan en archivos, historial Git y
ejecuciones verificables; un requisito pendiente no se marca como cumplido.

## Resumen

| Requisito | Estado | Evidencia y observaciones |
| --- | --- | --- |
| Repositorio GitHub | Parcial | `origin` apunta a `github.com/Josueky/P_III` y la rama remota existe. El historial contiene commits separados para estructura, migración y validación. Hay cambios locales de visualización y documentación pendientes de commit. |
| `legacy/` | Cumple | `legacy/TableTennisTests.mlx` está versionado y no presenta diferencias frente a Git. SHA-256 auditado: `C5507EB60CE211511AABBB7ED066690209C8EFFB30C9AA9011351AC847108923`. |
| `src/table_tennis_sim/` | Cumple | Parámetros, estado, física, colisiones, simulación, validación y visualización están encapsulados en módulos independientes. |
| Notebook interactivo | Pendiente | `notebooks/01_simulacion_interactiva.ipynb` no contiene `ipywidgets` ni sliders. Además usa una API anterior: pasa la velocidad inicial a `SimulationParameters` y llama `run_simulation` sin `InitialConditions`. |
| `README.md` | Cumple | Incluye propósito, estructura, instalación, ejecución, API, validación, visualización y limitaciones. |
| `bitacora_ia.md` | Parcial | Registra objetivos, resultados y verificaciones por sesión. Los prompts y las decisiones aceptadas/rechazadas no se documentaron sistemáticamente en las primeras sesiones. No se reconstruyen datos históricos que no fueron registrados. |
| `docs/plan_migracion.md` | Cumple | Define arquitectura, variables de salida, riesgos, unidades, criterios de validación y resultado MATLAB–Python. |
| `requirements.txt` | Cumple | Declara `numpy`, `matplotlib`, `ipywidgets` y `jupyter` con versiones mínimas. |

## Criterios de calidad

| Criterio | Estado | Evidencia y observaciones |
| --- | --- | --- |
| Trazabilidad | Cumple con pendiente local | Existen commits significativos para estructura, documentación, migración NumPy y validación. La visualización debe confirmarse y subirse como un commit separado. |
| Modularidad | Cumple | El núcleo se ejecuta mediante imports desde `table_tennis_sim` y no depende del notebook. Visualización y validación consumen `SimulationResult`. |
| Migración técnica | Cumple para el escenario de referencia | Python y MATLAB coinciden en 301 muestras. El error máximo fue `8.88e-15 m` en posición, `7.11e-15 m/s` en velocidad y `5.12e-13` en las series angulares. |
| Interactividad | Pendiente | No hay sliders y el notebook debe migrarse a la API actual antes de poder regenerar salidas. |
| Documentación | Cumple para el núcleo actual | README, plan y guía de validación permiten instalar, ejecutar y comparar la simulación numérica. La futura interacción deberá documentarse cuando exista. |
| Uso legítimo de IA | Parcial | Hay trazabilidad de actividades y verificaciones, pero falta adoptar un formato obligatorio de prompt, resultado, aceptación/rechazo y comprobación para cada intervención futura. |

## Evidencia del historial

El historial auditado contiene, entre otros, estos cambios independientes:

```text
feat: alinear estructura Python con plan de migracion
docs: registrar estructura minima de Python
docs: detallar plan de migracion
feat: translate numerical simulation to numpy
test: automate and document MATLAB comparison
```

Los mensajes anteriores mezclan español e inglés. `CONTRIBUTING.md` define la
convención aplicable desde ahora: tipo de Conventional Commits en inglés y
descripción en español.

## Prioridades para completar la entrega

1. Actualizar `notebooks/01_simulacion_interactiva.ipynb` a la API actual.
2. Añadir sliders con `ipywidgets` para parámetros relevantes y regenerar las
   figuras cuando cambien.
3. Ejecutar el notebook desde un entorno limpio y guardar evidencia funcional.
4. Confirmar y subir los cambios locales de visualización y documentación.
5. Usar en la bitácora el formato mínimo definido a continuación.

## Formato mínimo para próximas entradas de IA

```markdown
## Sesión N — Título

- Prompt o solicitud:
- Resultado generado:
- Cambios aceptados:
- Cambios rechazados y motivo:
- Verificación realizada:
- Responsable de la revisión:
```

## Comandos de comprobación

```powershell
git status
git log --oneline --decorate -12
git diff -- legacy/TableTennisTests.mlx
$env:PYTHONPATH = "$PWD\src"
.\.venv\Scripts\python.exe -m table_tennis_sim.validation ".\results\matlab_reference"
```

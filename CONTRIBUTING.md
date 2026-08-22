# Convenciones de contribución

## Mensajes de commit

El proyecto usa Conventional Commits con el tipo en inglés y la descripción en
español:

```text
tipo(área opcional): acción breve en español
```

La descripción debe escribirse en minúscula, sin punto final y preferiblemente
con un verbo en infinitivo.

### Tipos permitidos

| Tipo | Uso |
| --- | --- |
| `feat` | Incorporar una capacidad nueva. |
| `fix` | Corregir un defecto. |
| `docs` | Cambiar únicamente documentación. |
| `test` | Añadir o modificar validaciones y pruebas. |
| `refactor` | Reorganizar código sin cambiar su comportamiento. |
| `chore` | Mantenimiento, configuración o estructura. |
| `perf` | Mejorar rendimiento sin cambiar resultados esperados. |

### Ejemplos

```text
feat(simulacion): traducir el nucleo numerico a numpy
feat(visualizacion): agregar trayectoria 3d y series temporales
test(validacion): comparar resultados de python y matlab
docs: documentar la reproduccion del experimento
fix(colisiones): corregir la deteccion de impacto con la red
```

No se reescribe el historial publicado solo para traducir mensajes antiguos.
La convención se aplica a los commits nuevos.

## Alcance de los commits

- Cada commit debe representar un cambio coherente y revisable.
- No se deben mezclar cambios numéricos con ajustes visuales sin necesidad.
- La bitácora y la documentación se actualizan cuando cambia el comportamiento
  o el procedimiento de reproducción.
- Antes de confirmar, se revisa `git diff --check` y se ejecuta la validación
  correspondiente.

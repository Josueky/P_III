# Plan de migración: simulación de tenis de mesa

## Alcance

Migrar de forma incremental el Live Script `legacy/TableTennisTests.mlx` a un paquete Python verificable. El plan define la arquitectura y los criterios de validación que guían la traducción del algoritmo MATLAB.

## Estado de implementación

La traducción inicial del núcleo numérico se realizó en `parameters.py`,
`state.py`, `physics.py`, `collisions.py` y `simulation.py`. No incluye
animación, figuras, pausas ni escritura de archivos. La equivalencia
cuantitativa con MATLAB queda pendiente por la ambigüedad de las unidades de
los coeficientes aerodinámicos del script heredado.

## Módulos propuestos

| Módulo | Responsabilidad |
| --- | --- |
| `parameters.py` | Definir configuraciones inmutables y tipadas para la pelota, la mesa, la red, el integrador y la visualización. Centraliza valores por defecto y sus unidades. |
| `state.py` | Representar el estado instantáneo de la pelota (posición, velocidad, orientación, velocidad angular y aceleraciones) y el resultado completo de una ejecución. |
| `physics.py` | Calcular gravedad, arrastre lineal, fuerza de Magnus, torque de arrastre y las derivadas del estado. No conoce figuras ni archivos. |
| `collisions.py` | Detectar impactos con mesa y red, corregir penetraciones y aplicar restitución/fricción según reglas explícitas y comprobables. |
| `simulation.py` | Construir el vector temporal, avanzar la integración, invocar física y colisiones, y devolver un resultado sin efectos visuales. |
| `visualization.py` | Generar gráficas de series temporales, escena 3D y animación a partir de un resultado ya calculado. |
| `validation.py` | Contener escenarios de referencia, validación de unidades, invariantes y comparaciones cuantitativas entre MATLAB y Python. |

## Parámetros de simulación

Los parámetros deberán agruparse en configuraciones separadas y documentar siempre sus unidades. El código heredado usa milímetros, gramos y segundos, aunque algunos comentarios mencionan mN; antes de implementar se debe fijar un sistema coherente, preferiblemente SI.

### Pelota y fuerzas

- Masa y radio de la pelota.
- Momento de inercia y modelo físico que lo justifica.
- Gravedad.
- Coeficiente de arrastre lineal.
- Coeficiente de Magnus.
- Coeficiente de arrastre rotacional.

### Escena y colisiones

- Longitud, anchura y altura de la mesa.
- Altura de la red y extensión lateral adicional.
- Coeficiente de restitución de la mesa.
- Coeficiente de restitución de la red.
- Parámetro o modelo de fricción mesa–pelota.

### Ejecución y condiciones iniciales

- Paso temporal, duración y método de integración.
- Posición, velocidad y velocidad angular iniciales.
- Activación y periodo de muestreo de la animación.
- Ángulos de cámara para la vista 3D.

## Variables de salida

Cada ejecución debe devolver un objeto `SimulationResult` con:

- `time`: vector temporal.
- `position`: matriz `N × 3` de posiciones.
- `velocity`: matriz `N × 3` de velocidades lineales.
- `acceleration`: matriz `N × 3` de aceleraciones lineales.
- `orientation`: matriz `N × 3` de ángulos acumulados.
- `angular_velocity`: matriz `N × 3` de velocidades angulares.
- `angular_acceleration`: matriz `N × 3` de aceleraciones angulares.
- `events`: registro opcional de impactos con tipo, instante y estado anterior/posterior.

La visualización debe ser consumidora de estas salidas y no parte del cálculo.

## Criterios mínimos de verificación

1. Las configuraciones rechazan valores físicamente inválidos: masa, radio, `dt` y duración deben ser positivos; los coeficientes de restitución deben estar entre 0 y 1.
2. Con fuerzas y colisiones desactivadas, el integrador reproduce movimiento uniforme dentro de una tolerancia numérica definida.
3. Con solo gravedad activada, la trayectoria coincide con la solución balística analítica para el mismo paso temporal.
4. Un impacto contra la mesa deja la pelota por encima de su superficie y cambia el signo de la velocidad normal conforme al coeficiente de restitución.
5. Un escenario de referencia equivalente al de MATLAB produce series de posición y velocidad comparables dentro de tolerancias acordadas y registradas.
6. Las funciones de simulación se ejecutan sin crear figuras, pausas ni archivos; las funciones de visualización no cambian el resultado numérico.
7. Las unidades de todas las ecuaciones y coeficientes quedan documentadas y pasan una revisión dimensional.

## Riesgos conocidos

- **Unidades ambiguas:** la combinación actual de gramos, milímetros, segundos y comentarios en mN puede alterar las magnitudes de las fuerzas. Debe resolverse antes de fijar resultados de referencia.
- **Modelo de inercia:** el factor `2/3` del script heredado no corresponde al habitual de una esfera maciza (`2/5`). Requiere validación del supuesto físico.
- **Colisiones discretas:** detectar impactos después de avanzar el estado permite penetración y hace que el resultado dependa de `dt`.
- **Red simplificada:** la respuesta actual solo invierte/amortigua una componente de velocidad y amortigua el giro; no representa la geometría ni fuerzas de contacto completas.
- **Acoplamiento con gráficos:** el script original mezcla cálculo, animación y pausas. La migración debe conservar resultados numéricos separando estas responsabilidades.
- **Detalle sintáctico de cámara:** `pitch = 23,5` en MATLAB se interpreta como expresiones separadas, no necesariamente como un decimal; debe decidirse el valor intencionado.
- **Parámetros no calibrados:** los coeficientes aerodinámicos y de fricción parecen empíricos y necesitan escenarios de validación antes de considerarlos predictivos.

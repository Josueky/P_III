"""Parámetros físicos y de ejecución de la simulación."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationParameters:
    """Valores base en unidades del SI."""

    gravity: float = 9.81
    time_step: float = 0.01
    duration: float = 1.5
    initial_x: float = 0.0
    initial_y: float = 0.30
    initial_vx: float = 4.0
    initial_vy: float = 1.5

"""Tipos de datos para el estado y los resultados de una simulación."""

from dataclasses import dataclass, field

import numpy as np


@dataclass(frozen=True)
class SimulationEvent:
    """Evento físico registrado durante una simulación."""

    time_s: float
    event_type: str


@dataclass(frozen=True)
class SimulationResult:
    """Series temporales producidas por una ejecución de la simulación."""

    time_s: np.ndarray
    position_m: np.ndarray
    velocity_m_s: np.ndarray
    acceleration_m_s2: np.ndarray
    orientation_rad: np.ndarray
    angular_velocity_rad_s: np.ndarray
    angular_acceleration_rad_s2: np.ndarray
    events: list[SimulationEvent] = field(default_factory=list)

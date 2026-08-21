"""Cálculos físicos independientes de la visualización."""

import numpy as np

from .parameters import SimulationParameters


def gravitational_acceleration(parameters: SimulationParameters) -> np.ndarray:
    """Devuelve la aceleración de gravedad en los ejes x, y, z."""
    return np.array([0.0, 0.0, -parameters.gravity_m_s2])


def advance_state(
    position_m: np.ndarray,
    velocity_m_s: np.ndarray,
    acceleration_m_s2: np.ndarray,
    time_step_s: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Avanza posición y velocidad un paso con Euler semiimplícito."""
    next_velocity = velocity_m_s + acceleration_m_s2 * time_step_s
    next_position = position_m + next_velocity * time_step_s
    return next_position, next_velocity

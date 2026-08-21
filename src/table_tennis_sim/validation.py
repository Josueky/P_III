"""Comprobaciones pequeñas para resultados de simulación."""

import numpy as np

from .state import SimulationResult


def has_valid_shapes(result: SimulationResult) -> bool:
    """Comprueba que las series de estado tengan una fila por instante."""
    steps = len(result.time_s)
    matrices = (
        result.position_m,
        result.velocity_m_s,
        result.acceleration_m_s2,
        result.orientation_rad,
        result.angular_velocity_rad_s,
        result.angular_acceleration_rad_s2,
    )
    return all(matrix.shape == (steps, 3) for matrix in matrices)


def has_finite_values(result: SimulationResult) -> bool:
    """Comprueba que el resultado no contiene valores no numéricos."""
    return bool(np.isfinite(result.position_m).all() and np.isfinite(result.velocity_m_s).all())

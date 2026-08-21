"""Detección y respuesta básica de colisiones con la mesa y la red."""

import numpy as np

from .parameters import BallParameters, TableParameters


def hits_table(
    position_m: np.ndarray, velocity_m_s: np.ndarray, ball: BallParameters, table: TableParameters
) -> bool:
    """Indica si una pelota descendente alcanza la superficie de la mesa."""
    within_length = 0.0 <= position_m[0] <= table.length_m
    within_width = 0.0 <= position_m[1] <= table.width_m
    surface_height = table.height_m + ball.radius_m
    return within_length and within_width and position_m[2] <= surface_height and velocity_m_s[2] < 0


def bounce_on_table(
    position_m: np.ndarray, velocity_m_s: np.ndarray, ball: BallParameters, table: TableParameters
) -> tuple[np.ndarray, np.ndarray]:
    """Corrige la penetración y aplica restitución a la velocidad vertical."""
    corrected_position = position_m.copy()
    corrected_velocity = velocity_m_s.copy()
    corrected_position[2] = table.height_m + ball.radius_m
    corrected_velocity[2] = -ball.table_restitution * corrected_velocity[2]
    return corrected_position, corrected_velocity

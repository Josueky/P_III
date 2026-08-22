"""Detección y respuesta de las colisiones de la simulación."""

import numpy as np

from .parameters import BallParameters, NetParameters, TableParameters


def hits_table(
    position_m: np.ndarray, velocity_m_s: np.ndarray, ball: BallParameters, table: TableParameters
) -> bool:
    """Indica si la pelota alcanza la superficie de juego de la mesa."""
    within_length = 0.0 < position_m[0] < table.length_m
    within_width = 0.0 < position_m[1] < table.width_m
    surface_height = table.height_m + ball.radius_m
    return within_length and within_width and position_m[2] < surface_height


def bounce_on_table(
    position_m: np.ndarray,
    velocity_m_s: np.ndarray,
    angular_velocity_rad_s: np.ndarray,
    ball: BallParameters,
    table: TableParameters,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Corrige la penetración y acopla velocidad lineal y giro.

    La regla reproduce la respuesta simplificada del script MATLAB: una parte
    de la velocidad tangencial relativa se intercambia con la rotación y se
    aplica restitución a la componente vertical.
    """
    corrected_position = position_m.copy()
    corrected_velocity = velocity_m_s.copy()
    corrected_angular_velocity = angular_velocity_rad_s.copy()
    corrected_position[2] = table.height_m + ball.radius_m
    radius_vector = np.array([0.0, 0.0, ball.radius_m])
    tangential_velocity = np.array([corrected_velocity[0], corrected_velocity[1], 0.0])
    linear_rotational_delta = np.cross(corrected_angular_velocity, radius_vector) - tangential_velocity
    corrected_velocity += ball.table_friction * linear_rotational_delta
    corrected_angular_velocity += (
        ball.table_friction
        * np.cross(linear_rotational_delta, np.array([0.0, 0.0, 1.0]))
        / ball.radius_m
    )
    corrected_velocity[2] = -ball.table_restitution * corrected_velocity[2]
    return corrected_position, corrected_velocity, corrected_angular_velocity


def hits_net(
    position_m: np.ndarray,
    ball: BallParameters,
    table: TableParameters,
    net: NetParameters,
) -> bool:
    """Detecta el volumen rectangular simplificado de la red del MATLAB."""
    reaches_net_plane = (
        table.length_m / 2 - ball.radius_m
        <= position_m[0]
        <= table.length_m / 2 + ball.radius_m
    )
    within_width = -net.extra_width_m < position_m[1] < table.width_m + net.extra_width_m
    within_height = (
        table.height_m + ball.radius_m
        < position_m[2]
        < table.height_m + net.height_m + ball.radius_m
    )
    return reaches_net_plane and within_width and within_height


def bounce_on_net(
    velocity_m_s: np.ndarray,
    angular_velocity_rad_s: np.ndarray,
    net: NetParameters,
) -> tuple[np.ndarray, np.ndarray]:
    """Refleja la velocidad longitudinal y amortigua el giro en la red."""
    corrected_velocity = velocity_m_s.copy()
    corrected_angular_velocity = net.restitution * angular_velocity_rad_s
    corrected_velocity[0] = -net.restitution * corrected_velocity[0]
    return corrected_velocity, corrected_angular_velocity

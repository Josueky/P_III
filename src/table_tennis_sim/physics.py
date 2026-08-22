"""Cálculos físicos independientes de la visualización."""

import numpy as np

from .parameters import SimulationParameters


def gravitational_acceleration(parameters: SimulationParameters) -> np.ndarray:
    """Devuelve la aceleración de gravedad en los ejes x, y, z."""
    return np.array([0.0, 0.0, -parameters.gravity_m_s2])


def linear_acceleration(
    velocity_m_s: np.ndarray,
    angular_velocity_rad_s: np.ndarray,
    parameters: SimulationParameters,
) -> np.ndarray:
    """Calcula gravedad, arrastre lineal y fuerza de Magnus.

    La ecuación conserva la estructura del Live Script MATLAB, pero opera en
    N, kg, m y s.
    """
    gravity_force_n = parameters.ball.mass_kg * gravitational_acceleration(parameters)
    drag_force_n = -parameters.forces.linear_drag_kg_s * velocity_m_s
    magnus_force_n = parameters.forces.magnus_kg * np.cross(
        angular_velocity_rad_s, velocity_m_s
    )
    return (gravity_force_n + drag_force_n + magnus_force_n) / parameters.ball.mass_kg


def angular_acceleration(
    angular_velocity_rad_s: np.ndarray,
    parameters: SimulationParameters,
) -> np.ndarray:
    """Calcula la desaceleración angular por arrastre rotacional."""
    torque_n_m = -parameters.forces.rotational_drag_n_m_s * angular_velocity_rad_s
    return torque_n_m / parameters.ball.rotational_inertia_kg_m2


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

"""Modelo físico simplificado de la pelota."""

import numpy as np

from .parameters import SimulationParameters


def trajectory(parameters: SimulationParameters) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calcula una trayectoria balística sin resistencia del aire."""
    time = np.arange(0.0, parameters.duration + parameters.time_step, parameters.time_step)
    x = parameters.initial_x + parameters.initial_vx * time
    y = parameters.initial_y + parameters.initial_vy * time - 0.5 * parameters.gravity * time**2
    return time, x, y

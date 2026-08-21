"""Ejecución de la simulación sin efectos visuales."""

import numpy as np

from .collisions import bounce_on_table, hits_table
from .parameters import SimulationParameters
from .physics import advance_state, gravitational_acceleration
from .state import SimulationEvent, SimulationResult


def run_simulation(parameters: SimulationParameters | None = None) -> SimulationResult:
    """Calcula una trayectoria simple y devuelve todas sus series temporales."""
    parameters = parameters or SimulationParameters()
    steps = int(parameters.duration_s / parameters.time_step_s) + 1
    time_s = np.linspace(0.0, parameters.duration_s, steps)

    position_m = np.zeros((steps, 3))
    velocity_m_s = np.zeros((steps, 3))
    acceleration_m_s2 = np.zeros((steps, 3))
    position_m[0] = parameters.initial_position_m
    velocity_m_s[0] = parameters.initial_velocity_m_s
    events: list[SimulationEvent] = []

    acceleration = gravitational_acceleration(parameters)
    for index in range(1, steps):
        acceleration_m_s2[index] = acceleration
        position, velocity = advance_state(
            position_m[index - 1], velocity_m_s[index - 1], acceleration, parameters.time_step_s
        )
        if hits_table(position, velocity, parameters.ball, parameters.table):
            position, velocity = bounce_on_table(position, velocity, parameters.ball, parameters.table)
            events.append(SimulationEvent(time_s[index], "table_bounce"))
        position_m[index] = position
        velocity_m_s[index] = velocity

    zeros = np.zeros((steps, 3))
    return SimulationResult(time_s, position_m, velocity_m_s, acceleration_m_s2, zeros, zeros, zeros, events)


if __name__ == "__main__":
    from .visualization import plot_trajectory

    plot_trajectory(run_simulation())

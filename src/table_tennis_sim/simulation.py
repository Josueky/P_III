"""Ejecución numérica de la simulación sin efectos visuales."""

import numpy as np

from .collisions import bounce_on_net, bounce_on_table, hits_net, hits_table
from .parameters import SimulationParameters
from .physics import advance_state, angular_acceleration, linear_acceleration
from .state import InitialConditions, SimulationEvent, SimulationResult


def run_simulation(
    parameters: SimulationParameters,
    initial_conditions: InitialConditions,
) -> SimulationResult:
    """Calcula la trayectoria completa con el esquema de Euler del MATLAB.

    No crea figuras, animaciones, pausas ni archivos. Las matrices de salida
    tienen forma ``(N, 3)``; cada fila representa el estado en un instante.
    """
    steps = int(np.floor(parameters.duration_s / parameters.time_step_s)) + 1
    time_s = np.arange(steps, dtype=float) * parameters.time_step_s

    position_m = np.zeros((steps, 3))
    velocity_m_s = np.zeros((steps, 3))
    acceleration_m_s2 = np.zeros((steps, 3))
    orientation_rad = np.zeros((steps, 3))
    angular_velocity_rad_s = np.zeros((steps, 3))
    angular_acceleration_rad_s2 = np.zeros((steps, 3))

    position_m[0] = initial_conditions.position_m
    velocity_m_s[0] = initial_conditions.velocity_m_s
    orientation_rad[0] = initial_conditions.orientation_rad
    angular_velocity_rad_s[0] = initial_conditions.angular_velocity_rad_s
    events: list[SimulationEvent] = []

    for index in range(1, steps):
        acceleration_m_s2[index] = linear_acceleration(
            velocity_m_s[index - 1], angular_velocity_rad_s[index - 1], parameters
        )
        position, velocity = advance_state(
            position_m[index - 1],
            velocity_m_s[index - 1],
            acceleration_m_s2[index],
            parameters.time_step_s,
        )
        angular_acceleration_rad_s2[index] = angular_acceleration(
            angular_velocity_rad_s[index - 1], parameters
        )
        angular_velocity = (
            angular_velocity_rad_s[index - 1]
            + angular_acceleration_rad_s2[index] * parameters.time_step_s
        )
        orientation = orientation_rad[index - 1] + angular_velocity * parameters.time_step_s

        if hits_table(position, velocity, parameters.ball, parameters.table):
            position, velocity, angular_velocity = bounce_on_table(
                position, velocity, angular_velocity, parameters.ball, parameters.table
            )
            events.append(SimulationEvent(time_s[index], "table_bounce"))
        if hits_net(position, parameters.ball, parameters.table, parameters.net):
            velocity, angular_velocity = bounce_on_net(velocity, angular_velocity, parameters.net)
            events.append(SimulationEvent(time_s[index], "net_collision"))

        position_m[index] = position
        velocity_m_s[index] = velocity
        orientation_rad[index] = orientation
        angular_velocity_rad_s[index] = angular_velocity

    return SimulationResult(
        time_s=time_s,
        position_m=position_m,
        velocity_m_s=velocity_m_s,
        acceleration_m_s2=acceleration_m_s2,
        orientation_rad=orientation_rad,
        angular_velocity_rad_s=angular_velocity_rad_s,
        angular_acceleration_rad_s2=angular_acceleration_rad_s2,
        events=events,
    )


def simulate(
    parameters: SimulationParameters,
    initial_conditions: InitialConditions,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Ejecuta la simulación y devuelve las cinco series principales.

    Returns
    -------
    time, position, velocity, orientation, angular_velocity
        Series sin efectos visuales. El tiempo está en segundos; posición y
        velocidad en m y m/s; orientación y velocidad angular en rad y rad/s.
    """
    result = run_simulation(parameters, initial_conditions)
    return (
        result.time_s,
        result.position_m,
        result.velocity_m_s,
        result.orientation_rad,
        result.angular_velocity_rad_s,
    )

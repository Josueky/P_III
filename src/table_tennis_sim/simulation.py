"""Punto de entrada para ejecutar la simulación."""

from .parameters import SimulationParameters
from .physics import trajectory
from .visualization import plot_trajectory


def run_simulation(parameters: SimulationParameters | None = None):
    """Ejecuta la simulación y devuelve tiempo y coordenadas."""
    parameters = parameters or SimulationParameters()
    time, x, y = trajectory(parameters)
    valid = y >= 0
    return time[valid], x[valid], y[valid]


if __name__ == "__main__":
    _, x_values, y_values = run_simulation()
    plot_trajectory(x_values, y_values)

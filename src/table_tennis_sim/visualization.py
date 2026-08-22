"""Visualizaciones estáticas que consumen resultados ya calculados.

Este módulo no recalcula ni modifica la simulación. Cada función crea una
figura independiente para mantener legibles las series y devuelve la figura
de Matplotlib para permitir guardarla o personalizarla.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .parameters import NetParameters, TableParameters
from .state import SimulationResult


COMPONENT_LABELS = ("x", "y", "z")
COMPONENT_COLORS = ("tab:blue", "tab:orange", "tab:green")


def _finish_figure(figure: Figure, show: bool) -> Figure:
    """Ajusta y muestra opcionalmente una figura antes de devolverla."""
    figure.tight_layout()
    if show:
        plt.show()
    return figure


def _plot_vector_series(
    result: SimulationResult,
    values: np.ndarray,
    *,
    title: str,
    ylabel: str,
    show: bool,
) -> Figure:
    """Dibuja las componentes x, y, z en un único eje temporal."""
    figure, axis = plt.subplots(figsize=(9, 5))
    for component, color in enumerate(COMPONENT_COLORS):
        axis.plot(
            result.time_s,
            values[:, component],
            color=color,
            linewidth=1.8,
            label=COMPONENT_LABELS[component],
        )
    axis.set_title(title)
    axis.set_xlabel("Tiempo [s]")
    axis.set_ylabel(ylabel)
    axis.grid(alpha=0.25)
    axis.legend(title="Componente")
    return _finish_figure(figure, show)


def plot_trajectory_3d(
    result: SimulationResult,
    table: TableParameters | None = None,
    net: NetParameters | None = None,
    *,
    show: bool = True,
) -> Figure:
    """Muestra la trayectoria tridimensional y, opcionalmente, mesa y red."""
    figure = plt.figure(figsize=(10, 7))
    axis = figure.add_subplot(111, projection="3d")
    position = result.position_m

    axis.plot(
        position[:, 0],
        position[:, 1],
        position[:, 2],
        color="tab:blue",
        linewidth=2.2,
        label="Trayectoria",
    )
    axis.scatter(*position[0], color="tab:green", s=55, label="Inicio")
    axis.scatter(*position[-1], color="tab:red", s=55, label="Final")

    if table is not None:
        table_x, table_y = np.meshgrid(
            [0.0, table.length_m],
            [0.0, table.width_m],
        )
        table_z = np.full_like(table_x, table.height_m)
        axis.plot_surface(
            table_x,
            table_y,
            table_z,
            color="tab:blue",
            alpha=0.18,
            edgecolor="navy",
            linewidth=0.5,
        )

        if net is not None:
            net_y, net_z = np.meshgrid(
                [-net.extra_width_m, table.width_m + net.extra_width_m],
                [table.height_m, table.height_m + net.height_m],
            )
            net_x = np.full_like(net_y, table.length_m / 2.0)
            axis.plot_surface(
                net_x,
                net_y,
                net_z,
                color="black",
                alpha=0.28,
                edgecolor="black",
                linewidth=0.5,
            )

    axis.set_title("Trayectoria 3D de la pelota")
    axis.set_xlabel("x [m]")
    axis.set_ylabel("y [m]")
    axis.set_zlabel("z [m]")
    axis.legend()
    return _finish_figure(figure, show)


def plot_position(result: SimulationResult, *, show: bool = True) -> Figure:
    """Muestra las componentes de posición en función del tiempo."""
    return _plot_vector_series(
        result,
        result.position_m,
        title="Posición de la pelota",
        ylabel="Posición [m]",
        show=show,
    )


def plot_velocity(result: SimulationResult, *, show: bool = True) -> Figure:
    """Muestra las componentes de velocidad lineal en función del tiempo."""
    return _plot_vector_series(
        result,
        result.velocity_m_s,
        title="Velocidad de la pelota",
        ylabel="Velocidad [m/s]",
        show=show,
    )


def plot_angular_velocity(result: SimulationResult, *, show: bool = True) -> Figure:
    """Muestra las componentes de velocidad angular en función del tiempo."""
    return _plot_vector_series(
        result,
        result.angular_velocity_rad_s,
        title="Velocidad angular de la pelota",
        ylabel="Velocidad angular [rad/s]",
        show=show,
    )


def plot_trajectory(result: SimulationResult, *, show: bool = True) -> Figure:
    """Alias compatible para la nueva trayectoria tridimensional."""
    return plot_trajectory_3d(result, show=show)


def _main() -> None:
    """Ejecuta el escenario por defecto y abre las cuatro figuras."""
    from .parameters import SimulationParameters
    from .simulation import run_simulation
    from .state import InitialConditions

    parameters = SimulationParameters()
    result = run_simulation(parameters, InitialConditions())
    plot_trajectory_3d(result, parameters.table, parameters.net, show=False)
    plot_position(result, show=False)
    plot_velocity(result, show=False)
    plot_angular_velocity(result, show=False)
    plt.show()


if __name__ == "__main__":
    _main()

"""Gráficas sencillas que consumen resultados ya calculados."""

import matplotlib.pyplot as plt

from .state import SimulationResult


def plot_trajectory(result: SimulationResult) -> None:
    """Muestra la trayectoria horizontal y vertical de la pelota."""
    plt.plot(result.position_m[:, 0], result.position_m[:, 2], label="Pelota")
    plt.axhline(0.0, color="black", linewidth=0.8)
    plt.xlabel("Distancia horizontal x (m)")
    plt.ylabel("Altura z (m)")
    plt.title("Trayectoria de la pelota de tenis de mesa")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.show()

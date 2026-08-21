"""Funciones para visualizar resultados de la simulación."""

import matplotlib.pyplot as plt
import numpy as np


def plot_trajectory(x: np.ndarray, y: np.ndarray) -> None:
    """Muestra la trayectoria en el plano vertical."""
    plt.plot(x, y, label="Pelota")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xlabel("Distancia horizontal (m)")
    plt.ylabel("Altura (m)")
    plt.title("Trayectoria de la pelota de tenis de mesa")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.show()

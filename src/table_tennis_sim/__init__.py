"""Herramientas didácticas para simular trayectorias de tenis de mesa."""

from .parameters import (
    BallParameters,
    NetParameters,
    SimulationParameters,
    TableParameters,
    VisualizationParameters,
)
from .simulation import run_simulation
from .state import SimulationResult

__all__ = [
    "BallParameters",
    "NetParameters",
    "SimulationParameters",
    "SimulationResult",
    "TableParameters",
    "VisualizationParameters",
    "run_simulation",
]

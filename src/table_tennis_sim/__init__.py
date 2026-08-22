"""Herramientas didácticas para simular trayectorias de tenis de mesa."""

from .parameters import (
    BallParameters,
    ForceParameters,
    NetParameters,
    SimulationParameters,
    TableParameters,
    VisualizationParameters,
)
from .simulation import run_simulation, simulate
from .state import InitialConditions, SimulationResult

__all__ = [
    "BallParameters",
    "ForceParameters",
    "InitialConditions",
    "NetParameters",
    "SimulationParameters",
    "SimulationResult",
    "TableParameters",
    "VisualizationParameters",
    "run_simulation",
    "simulate",
]

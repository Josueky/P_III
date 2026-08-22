"""Tipos de datos para las condiciones iniciales y los resultados."""

from dataclasses import dataclass, field

import numpy as np


def _as_vector3(value: np.ndarray | tuple[float, float, float], name: str) -> np.ndarray:
    """Convierte una entrada a un vector finito de tres componentes."""
    vector = np.asarray(value, dtype=float)
    if vector.shape != (3,):
        raise ValueError(f"{name} debe tener exactamente tres componentes.")
    if not np.isfinite(vector).all():
        raise ValueError(f"{name} debe contener únicamente valores finitos.")
    return vector.copy()


@dataclass(frozen=True)
class InitialConditions:
    """Estado de la pelota al iniciar una ejecución.

    Los valores por defecto corresponden al caso de estudio de MATLAB, ya
    convertidos de mm y mm/s a m y m/s.
    """

    position_m: np.ndarray = field(
        default_factory=lambda: np.array([0.0, 0.7625, 1.0650], dtype=float)
    )
    velocity_m_s: np.ndarray = field(
        default_factory=lambda: np.array([7.0, -3.0, -3.0], dtype=float)
    )
    orientation_rad: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=float))
    angular_velocity_rad_s: np.ndarray = field(
        default_factory=lambda: np.array([0.0, 0.0, 75.0 * 2.0 * np.pi], dtype=float)
    )

    def __post_init__(self) -> None:
        object.__setattr__(self, "position_m", _as_vector3(self.position_m, "position_m"))
        object.__setattr__(self, "velocity_m_s", _as_vector3(self.velocity_m_s, "velocity_m_s"))
        object.__setattr__(self, "orientation_rad", _as_vector3(self.orientation_rad, "orientation_rad"))
        object.__setattr__(
            self,
            "angular_velocity_rad_s",
            _as_vector3(self.angular_velocity_rad_s, "angular_velocity_rad_s"),
        )


@dataclass(frozen=True)
class SimulationEvent:
    """Evento físico registrado durante una simulación."""

    time_s: float
    event_type: str


@dataclass(frozen=True)
class SimulationResult:
    """Series temporales producidas por una ejecución de la simulación."""

    time_s: np.ndarray
    position_m: np.ndarray
    velocity_m_s: np.ndarray
    acceleration_m_s2: np.ndarray
    orientation_rad: np.ndarray
    angular_velocity_rad_s: np.ndarray
    angular_acceleration_rad_s2: np.ndarray
    events: list[SimulationEvent] = field(default_factory=list)

"""Configuraciones de la simulación en unidades del Sistema Internacional."""

from dataclasses import dataclass, field

Vector3 = tuple[float, float, float]


@dataclass(frozen=True)
class BallParameters:
    """Propiedades físicas de una pelota de tenis de mesa."""

    mass_kg: float = 0.0027
    radius_m: float = 0.02025
    table_restitution: float = 0.77

    def __post_init__(self) -> None:
        if self.mass_kg <= 0 or self.radius_m <= 0:
            raise ValueError("La masa y el radio deben ser positivos.")
        if not 0 <= self.table_restitution <= 1:
            raise ValueError("La restitución debe estar entre 0 y 1.")


@dataclass(frozen=True)
class TableParameters:
    """Dimensiones de la mesa de tenis de mesa."""

    length_m: float = 2.740
    width_m: float = 1.525
    height_m: float = 0.760


@dataclass(frozen=True)
class NetParameters:
    """Dimensiones básicas de la red."""

    height_m: float = 0.1525
    restitution: float = 0.50

    def __post_init__(self) -> None:
        if not 0 <= self.restitution <= 1:
            raise ValueError("La restitución debe estar entre 0 y 1.")


@dataclass(frozen=True)
class VisualizationParameters:
    """Opciones para las futuras gráficas y animaciones."""

    animate: bool = False
    sample_every_steps: int = 5
    yaw_degrees: float = -45.0
    pitch_degrees: float = 23.5

    def __post_init__(self) -> None:
        if self.sample_every_steps <= 0:
            raise ValueError("El periodo de muestreo debe ser positivo.")


@dataclass(frozen=True)
class SimulationParameters:
    """Configuración de ejecución y estado inicial de la simulación."""

    gravity_m_s2: float = 9.81
    time_step_s: float = 0.005
    duration_s: float = 1.5
    initial_position_m: Vector3 = (0.0, 0.7625, 1.065)
    initial_velocity_m_s: Vector3 = (4.0, 0.0, 1.5)
    ball: BallParameters = field(default_factory=BallParameters)
    table: TableParameters = field(default_factory=TableParameters)
    net: NetParameters = field(default_factory=NetParameters)
    visualization: VisualizationParameters = field(default_factory=VisualizationParameters)

    def __post_init__(self) -> None:
        if self.gravity_m_s2 <= 0 or self.time_step_s <= 0 or self.duration_s <= 0:
            raise ValueError("La gravedad, el paso temporal y la duración deben ser positivos.")
        if len(self.initial_position_m) != 3 or len(self.initial_velocity_m_s) != 3:
            raise ValueError("La posición y la velocidad inicial deben tener tres componentes.")

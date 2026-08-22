"""Configuraciones inmutables de la simulación en unidades SI.

Las dimensiones, restituciones y condiciones iniciales se convierten desde el
Live Script MATLAB. Los coeficientes aerodinámicos del legado son ambiguos; se
usan escalas provisionales y configurables que mantienen la integración finita.
"""

from dataclasses import dataclass, field

@dataclass(frozen=True)
class BallParameters:
    """Propiedades de la pelota y del contacto mesa-pelota."""

    mass_kg: float = 0.0027
    radius_m: float = 0.02025
    table_restitution: float = 0.77
    table_friction: float = 0.25
    rotational_inertia_factor: float = 2.0 / 3.0

    def __post_init__(self) -> None:
        if self.mass_kg <= 0 or self.radius_m <= 0:
            raise ValueError("La masa y el radio deben ser positivos.")
        for name in ("table_restitution", "table_friction"):
            if not 0 <= getattr(self, name) <= 1:
                raise ValueError(f"{name} debe estar entre 0 y 1.")
        if self.rotational_inertia_factor <= 0:
            raise ValueError("El factor de inercia debe ser positivo.")

    @property
    def rotational_inertia_kg_m2(self) -> float:
        """Momento de inercia usado en el script MATLAB convertido a SI."""
        return self.rotational_inertia_factor * self.mass_kg * self.radius_m**2


@dataclass(frozen=True)
class ForceParameters:
    """Coeficientes de fuerza provisionales para las ecuaciones en SI.

    El Live Script mezcla gramos, milímetros, segundos y comentarios en mN.
    Por ello estos valores deben calibrarse con una trayectoria de referencia
    antes de considerarse físicamente predictivos.
    """

    linear_drag_kg_s: float = 2.7e-3
    magnus_kg: float = 1.0e-5
    rotational_drag_n_m_s: float = 350e-9

    def __post_init__(self) -> None:
        if self.linear_drag_kg_s < 0 or self.magnus_kg < 0 or self.rotational_drag_n_m_s < 0:
            raise ValueError("Los coeficientes de fuerza no pueden ser negativos.")


@dataclass(frozen=True)
class TableParameters:
    """Dimensiones de la mesa de tenis de mesa."""

    length_m: float = 2.740
    width_m: float = 1.525
    height_m: float = 0.760

    def __post_init__(self) -> None:
        if self.length_m <= 0 or self.width_m <= 0 or self.height_m <= 0:
            raise ValueError("Las dimensiones de la mesa deben ser positivas.")


@dataclass(frozen=True)
class NetParameters:
    """Dimensiones básicas de la red."""

    height_m: float = 0.1525
    extra_width_m: float = 0.180
    restitution: float = 0.50

    def __post_init__(self) -> None:
        if self.height_m <= 0 or self.extra_width_m < 0:
            raise ValueError("Las dimensiones de la red no son válidas.")
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
    """Configuración física, geométrica y temporal de una ejecución."""

    gravity_m_s2: float = 9.8
    time_step_s: float = 0.005
    duration_s: float = 1.5
    ball: BallParameters = field(default_factory=BallParameters)
    forces: ForceParameters = field(default_factory=ForceParameters)
    table: TableParameters = field(default_factory=TableParameters)
    net: NetParameters = field(default_factory=NetParameters)
    visualization: VisualizationParameters = field(default_factory=VisualizationParameters)

    def __post_init__(self) -> None:
        if self.gravity_m_s2 <= 0 or self.time_step_s <= 0 or self.duration_s <= 0:
            raise ValueError("La gravedad, el paso temporal y la duración deben ser positivos.")

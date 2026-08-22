"""Validaciones estructurales y comparación con la referencia MATLAB."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from .state import SimulationResult

MATLAB_FILES = {
    "time": "matlab_time.csv",
    "position": "matlab_position_m.csv",
    "velocity": "matlab_velocity_m_s.csv",
    "orientation": "matlab_orientation_rad.csv",
    "angular_velocity": "matlab_angular_velocity_rad_s.csv",
}


def has_valid_shapes(result: SimulationResult) -> bool:
    """Comprueba que las series de estado tengan una fila por instante."""
    steps = len(result.time_s)
    matrices = (
        result.position_m,
        result.velocity_m_s,
        result.acceleration_m_s2,
        result.orientation_rad,
        result.angular_velocity_rad_s,
        result.angular_acceleration_rad_s2,
    )
    return all(matrix.shape == (steps, 3) for matrix in matrices)


def has_finite_values(result: SimulationResult) -> bool:
    """Comprueba que el resultado no contiene valores no numéricos."""
    return bool(np.isfinite(result.position_m).all() and np.isfinite(result.velocity_m_s).all())


def load_matlab_reference(directory: str | Path) -> dict[str, np.ndarray]:
    """Carga las cinco series exportadas desde MATLAB en formato CSV."""
    reference_directory = Path(directory)
    reference: dict[str, np.ndarray] = {}
    for name, filename in MATLAB_FILES.items():
        path = reference_directory / filename
        if not path.is_file():
            raise FileNotFoundError(f"No se encontró la referencia MATLAB: {path}")
        reference[name] = np.loadtxt(path, delimiter=",")
    return reference


def compare_with_matlab(
    result: SimulationResult,
    reference: dict[str, np.ndarray],
    *,
    absolute_tolerance: float = 1e-10,
    relative_tolerance: float = 1e-10,
) -> dict[str, dict[str, float | int | bool | None]]:
    """Calcula errores y localiza la primera muestra fuera de tolerancia."""
    python_series = {
        "time": result.time_s,
        "position": result.position_m,
        "velocity": result.velocity_m_s,
        "orientation": result.orientation_rad,
        "angular_velocity": result.angular_velocity_rad_s,
    }
    report: dict[str, dict[str, float | int | bool | None]] = {}

    for name, python_values in python_series.items():
        matlab_values = reference[name]
        if python_values.shape != matlab_values.shape:
            raise ValueError(
                f"Forma incompatible para {name}: Python {python_values.shape}, "
                f"MATLAB {matlab_values.shape}."
            )

        absolute_error = np.abs(python_values - matlab_values)
        close = np.isclose(
            python_values,
            matlab_values,
            atol=absolute_tolerance,
            rtol=relative_tolerance,
        )
        if close.ndim == 1:
            failing_rows = np.flatnonzero(~close)
        else:
            failing_rows = np.flatnonzero(np.any(~close, axis=1))

        report[name] = {
            "max_absolute_error": float(absolute_error.max(initial=0.0)),
            "mean_absolute_error": float(absolute_error.mean()),
            "rmse": float(np.sqrt(np.mean(absolute_error**2))),
            "within_tolerance": bool(close.all()),
            "first_failing_step": int(failing_rows[0]) if failing_rows.size else None,
        }

    return report


def plot_matlab_comparison(
    result: SimulationResult,
    reference: dict[str, np.ndarray],
    output_path: str | Path,
) -> Path:
    """Guarda una figura con las series Python y MATLAB superpuestas."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    series = (
        ("Posición [m]", result.position_m, reference["position"]),
        ("Velocidad [m/s]", result.velocity_m_s, reference["velocity"]),
        ("Orientación [rad]", result.orientation_rad, reference["orientation"]),
        (
            "Velocidad angular [rad/s]",
            result.angular_velocity_rad_s,
            reference["angular_velocity"],
        ),
    )
    figure, axes = plt.subplots(2, 2, figsize=(13, 8), sharex=True)
    colors = ("tab:blue", "tab:orange", "tab:green")

    for axis, (title, python_values, matlab_values) in zip(axes.flat, series):
        for component, color in enumerate(colors):
            axis.plot(
                result.time_s,
                python_values[:, component],
                color=color,
                label=f"Python {('x', 'y', 'z')[component]}",
            )
            axis.plot(
                reference["time"],
                matlab_values[:, component],
                color=color,
                linestyle="--",
                label=f"MATLAB {('x', 'y', 'z')[component]}",
            )
        axis.set_title(title)
        axis.set_xlabel("Tiempo [s]")
        axis.grid(alpha=0.25)

    axes[0, 0].legend(ncol=2, fontsize=8)
    figure.suptitle("Comparación de la simulación numérica: Python vs. MATLAB")
    figure.tight_layout()
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(destination, dpi=160)
    plt.close(figure)
    return destination


def _main() -> None:
    parser = argparse.ArgumentParser(description="Compara la simulación Python con CSV de MATLAB.")
    parser.add_argument("reference_directory", type=Path)
    parser.add_argument("--plot", type=Path, help="Ruta opcional para guardar la gráfica comparativa.")
    parser.add_argument("--atol", type=float, default=1e-10)
    parser.add_argument("--rtol", type=float, default=1e-10)
    args = parser.parse_args()

    from .parameters import SimulationParameters
    from .simulation import run_simulation
    from .state import InitialConditions

    result = run_simulation(SimulationParameters(), InitialConditions())
    reference = load_matlab_reference(args.reference_directory)
    report = compare_with_matlab(
        result,
        reference,
        absolute_tolerance=args.atol,
        relative_tolerance=args.rtol,
    )
    print("serie,max_abs,mean_abs,rmse,dentro_tolerancia,primer_paso_fuera")
    for name, metrics in report.items():
        print(
            f"{name},{metrics['max_absolute_error']:.17g},"
            f"{metrics['mean_absolute_error']:.17g},{metrics['rmse']:.17g},"
            f"{metrics['within_tolerance']},{metrics['first_failing_step']}"
        )
    if args.plot:
        print(f"Gráfica: {plot_matlab_comparison(result, reference, args.plot)}")


if __name__ == "__main__":
    _main()

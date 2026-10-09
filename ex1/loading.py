import importlib
import sys
from typing import Any


PACKAGES: dict[str, str] = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "matplotlib": "Visualization ready",
}


def check_packages() -> list[str]:
    missing: list[str] = []

    for name, description in PACKAGES.items():
        try:
            module = importlib.import_module(name)
        except ImportError:
            missing.append(name)
            print(f"Missing package {name} - {description}")
        else:
            version = getattr(module, "__version__", "unknown")
            print(f"[OK] {name} ({version}) - {description}")

    return missing


def show_install_help() -> None:
    print()
    print("Missing dependencies! Install them with one of:")
    print()
    print("With pip:")
    print("  pip install -r requirements.txt")
    print("  python3 loading.py")
    print()
    print("With Poetry:")
    print("  poetry install")
    print("  poetry run python loading.py")


def generate_data() -> Any:
    import numpy as np  # type: ignore

    rng = np.random.default_rng(42)
    data = rng.normal(0, 1, 1000)

    return data


def analyze_data(data: Any) -> Any:
    import pandas as pd  # type: ignore

    df = pd.DataFrame(data, columns=["signal"])
    print(df.describe())
    return df


def create_visualization(dataframe: Any) -> bool:
    import matplotlib  # type: ignore

    matplotlib.use("Agg")

    import matplotlib.pyplot as plt  # type: ignore

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(dataframe["signal"], bins=30)
    ax.set_title("Matrix signal distribution")
    ax.set_xlabel("Signal")
    ax.set_ylabel("Frequency")
    ax.grid(True)

    try:
        fig.savefig("matrix_analysis.png")
    except OSError as error:
        print(f"Error: {error}", file=sys.stderr)
        return False
    finally:
        plt.close(fig)

    return True


def compare_pip_poetry() -> None:
    from importlib.metadata import PackageNotFoundError, version

    for name in PACKAGES:
        try:
            installed_version = version(name)
        except PackageNotFoundError:
            print(f"{name} not installed")
        else:
            print(f"Package: {name}, version: {installed_version}")

    print()
    print(sys.executable)
    print(sys.prefix)
    print()
    print("Lock file: Poetry creates `poetry.lock` with exact versions"
          ", whereas pip with a simple `requirements.txt` does not.")
    print("Virtual environment: pip uses the one you create, while "
          "Poetry creates and manages one for you.")
    print("Dependency resolution: Poetry resolves versions holistically,"
          " whereas pip installs package by package.")


if __name__ == "__main__":
    print("LOADING STATUS: Loading programs...")
    print()
    print("Checking dependencies:")

    if check_packages():
        show_install_help()
        sys.exit(1)
    else:
        print()
        print("Analyzing Matrix data...")
        print("Processing 1000 data points...")
        print()
        data = generate_data()
        dataframe = analyze_data(data)

        print()
        print("Generating visualization...")

        if create_visualization(dataframe):
            print()
            compare_pip_poetry()
            print()
            print("Analysis complete!")
            print("Results saved to: matrix_analysis.png")
        else:
            sys.exit(1)

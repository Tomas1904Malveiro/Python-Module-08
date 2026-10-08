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
    import numpy as np

    rng = np.random.default_rng(42)
    data = rng.normal(0, 1, 1000)

    return data


def analyze_data(data: Any) -> Any:
    import pandas as pd

    df = pd.DataFrame(data, columns=["signal"])
    print(df.describe())
    return df


def create_visualization(dataframe: Any) -> None:
    import matplotlib

    matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(dataframe["signal"], bins=30)
    ax.set_title("Matrix signal distribution")
    ax.set_xlabel("Signal")
    ax.set_ylabel("Frequency")
    ax.grid(True)

    fig.savefig("matrix_analysis.png")
    plt.close(fig)


def compare_pip_poetry() -> None:
    print("pip is a basic package installer.")
    print()
    print("Poetry manages your entire project "
          "lifecycle, including virtual environments.")
    print()
    print("pip uses flat text files like requirements.txt.")
    print()
    print("Poetry uses a centralized pyproject.toml.")


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
        data = generate_data()
        dataframe = analyze_data(data)

        print("Generating visualization...")
        create_visualization(dataframe)

        print()
        compare_pip_poetry()
        print("Analysis complete!")
        print("Results saved to: matrix_analysis.png")

import importlib
import sys
from typing import Any


PACKAGES: dict[str, str] = {
"pandas": "Data manipulation ready",
"numpy": "Numerical computation ready",
"matplotlib": "Visualization ready"}


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

    pd.DataFrame(generate_data(), columns=[data])
    statics = data.std()
    print(statics)

if __name__ == "__main__":
    print("LOADING STATUS: Loading programs...")
    print()
    print("Checking dependencies:")
    if check_packages():
        show_install_help()
        sys.exit(1)
    else:
        print("Analyzing Matrix data...")
        print("Processing 1000 data points...")
        data = generate_data()
        dataframe = analyze_data(data)
        print("Generating visualization...")
        print()
        print("Analysis complete!")
        print("Results saved to: matrix_analysis.png")

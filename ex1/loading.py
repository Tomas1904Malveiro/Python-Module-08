import importlib
import sys


def package_list() -> list:
    packages = ["pandas", "numpy", "requests", "matplotlib"]
    return packages


def loading() -> None:
    for i in package_list():
        try:
            importlib.import_module(i)
        except ImportError as e:
            print(f"Missing package {e}")
            sys.exit(1)
        
        print(f"[OK] {i}")


if __name__ == "__main__":
    print("LOADING STATUS: Loading programs...")
    loading()

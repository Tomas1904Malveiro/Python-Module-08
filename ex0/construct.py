import os
import sys
import site


def virtual_venv() -> bool:
    if sys.prefix != sys.base_prefix:
        return True
    else:
        return False


def in_venv() -> None:
    print("MATRIX STATUS: Welcome to the construct")
    print()

    name = sys.executable
    print(f"Current Python: {name}")

    venv = os.path.basename(sys.prefix)
    print(f"Virtual Environment: {venv}")

    path = sys.prefix
    print(f"Environment Path: {path}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting the global system.")

    print()
    print("Package installation path:")
    packages = site.getsitepackages()
    package_path = packages[0]
    print(package_path)


def out_venv() -> None:
    print("MATRIX STATUS: You're still plugged in")
    print()

    name = sys.executable
    print(f"Current Python: {name}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print("matrix_env\\Scripts\\activate # On Windows")
    print()
    print("Then run this program again.")


if __name__ == "__main__":
    if virtual_venv():
        in_venv()
    else:
        out_venv()

import sys
import os


try:
    from dotenv import load_dotenv
except ImportError:
    print("Missing package: python-dotenv", file=sys.stderr)
    print("Install it with: pip install -r requirements.txt",
          file=sys.stderr)
    sys.exit(1)


REQUIRED_VARS: list[str] = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]

VALID_MODES: list[str] = ["development", "production"]


def load_config() -> dict[str, str | None]:
    import pandas as pd

    load_dotenv()
    config: dict[str, str | None] = {}
    for name in REQUIRED_VARS:
        config[name] = os.getenv(name)
    return config


def validate_config(config: dict[str, str | None]) -> list[str]:
    problems = list[str] = []

    for name in config:
        problems.append(name)
        


if __name__ == "__main__":
    print("ORACLE STATUS: Reading the Matrix...")
    print()
    config = load_config()
    problems = validate_config(config)
    print()
    print("The Oracle sees all configurations.")
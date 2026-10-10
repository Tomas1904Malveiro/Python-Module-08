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
DEFAULT_MODE: str = "development"
LOCAL_HOSTS: list[str] = ["localhost", "127.0.0.1"]


def find_overrides() -> list[str]:
    overrides: list[str] = []
    for name in REQUIRED_VARS:
        if name in os.environ:
            overrides.append(name)
    return overrides


def load_config() -> dict[str, str | None]:

    load_dotenv()
    config: dict[str, str | None] = {}
    for name in REQUIRED_VARS:
        config[name] = os.getenv(name)
    return config


def get_mode(config: dict[str, str | None]) -> str:
    return config["MATRIX_MODE"] or DEFAULT_MODE


def is_local(url: str) -> bool:
    return any(host in url for host in LOCAL_HOSTS)


def validate_config(config: dict[str, str | None]) -> list[str]:
    problems: list[str] = []

    for name, value in config.items():
        if not value:
            problems.append(f"{name} is missing")

    mode = get_mode(config)
    if mode not in VALID_MODES:
        problems.append(f"MATRIX_MODE '{mode}' is invalid "
                        f"(use {' or '.join(VALID_MODES)})")

    database = config["DATABASE_URL"]
    if mode == "production" and database and is_local(database):
        problems.append("DATABASE_URL points to a local database "
                        "in production")

    return problems


def show_config(config: dict[str, str | None]) -> None:
    print("Configuration loaded:")
    print(f"Mode: {get_mode(config)}")

    database = config["DATABASE_URL"]
    if not database:
        print("Database: Not configured")
    elif is_local(database):
        print("Database: Local instance configured")
    else:
        print("Database: Remote instance configured")

    if config["API_KEY"]:
        print("API Access: Key configured")
    else:
        print("API Access: Not configured")

    print(f"Log Level: {config['LOG_LEVEL'] or 'Not configured'}")

    if config["ZION_ENDPOINT"]:
        print("Zion Network: Endpoint configured")
    else:
        print("Zion Network: Not configured")


def gitignore_has_env() -> bool:
    try:
        with open(".gitignore") as file:
            lines = file.read().splitlines()
    except OSError:
        return False
    return ".env" in lines


def security_check(config: dict[str, str | None],
                   overrides: list[str]) -> None:
    print("Environment security check:")

    if os.path.isfile(".env"):
        print("[OK] .env file found")
    else:
        print("[Missing] .env file not found")

    if gitignore_has_env():
        print("[OK] .env is listed in .gitignore")
    else:
        print("[Missing] .env is not listed in .gitignore")

    if all(config.values()):
        print("[OK] All variables are defined")
    else:
        print("[Missing] Some variables are not defined")

    if overrides:
        names = ", ".join(overrides)
        print(f"[OK] Environment overrides in use: {names}")
    else:
        print("[OK] No overrides in use (environment beats .env)")


if __name__ == "__main__":
    print("ORACLE STATUS: Reading the Matrix...")
    print()

    overrides = find_overrides()
    config = load_config()
    problems = validate_config(config)
    strict = get_mode(config) != DEFAULT_MODE
    print()

    for problem in problems:
        if strict:
            print(f"[ERROR] {problem}", file=sys.stderr)
        else:
            print(f"[WARNING] {problem}")

    if problems and strict:
        sys.exit(1)
    if problems:
        print()

    show_config(config)
    print()
    security_check(config, overrides)
    print()
    print("The Oracle sees all configurations.")

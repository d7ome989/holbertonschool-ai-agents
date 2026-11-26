import os

REQUIRED_VARIABLES = [
    "OLLAMA_API_BASE",
    "EXPLAINER_MODEL",
    "PRACTICE_MODEL",
    "REVIEWER_MODEL",
    "SUMMARY_MODEL",
]


class ConfigError(Exception):
    """Raised when the project configuration is missing or invalid."""


def load_env_file(path: str = ".env") -> None:
    """Load KEY=VALUE lines from a .env file into os.environ."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def get_config() -> dict:
    """Return the configuration, or raise ConfigError if incomplete."""
    load_env_file()
    missing = [name for name in REQUIRED_VARIABLES if not os.getenv(name)]
    if missing:
        raise ConfigError(
            "Missing environment variables: "
            + ", ".join(missing)
            + ". Copy .env.example to .env and fill them in."
        )
    return {name: os.environ[name] for name in REQUIRED_VARIABLES}

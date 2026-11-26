import json
import urllib.error
import urllib.request


class CheckError(Exception):
    """Raised when a pre-run check fails."""


def check_topic(topic: str) -> str:
    """Return the cleaned topic or raise if it is empty."""
    if not topic or not topic.strip():
        raise CheckError("Topic cannot be empty.")
    return topic.strip()


def get_installed_models(api_base: str) -> list:
    """Return the model names installed in Ollama."""
    url = api_base.rstrip("/") + "/api/tags"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.load(response)
    except (urllib.error.URLError, OSError) as error:
        raise CheckError(
            f"Cannot reach Ollama at {api_base} ({error}). "
            "Start it with: sudo systemctl start ollama"
        ) from error
    return [model["name"] for model in data.get("models", [])]


def check_models(api_base: str, model_names: list) -> None:
    """Raise if any configured model is not installed in Ollama."""
    installed = get_installed_models(api_base)
    missing = []
    for full_name in set(model_names):
        name = full_name.split("/", 1)[-1]
        if name not in installed:
            missing.append(name)
    if missing:
        raise CheckError(
            "Model not available: "
            + ", ".join(sorted(missing))
            + ". Install with: ollama pull <model>"
        )

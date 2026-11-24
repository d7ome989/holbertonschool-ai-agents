from pathlib import Path


def save_markdown_file(file_path: str, content: str) -> str:
    """Save Markdown content to a file and return a status message."""
    if not file_path or not file_path.strip():
        return "Error: file path is empty."
    if not content or not content.strip():
        return "Error: content is empty."

    path = Path(file_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    except OSError as error:
        return f"Error: could not save file ({error})."

    return f"Saved: {path}"

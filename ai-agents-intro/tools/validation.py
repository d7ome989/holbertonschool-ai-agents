import re

REQUIRED_SECTIONS = [
    "Topic",
    "Simple Explanation",
    "Key Concepts",
    "Example",
    "Practice Exercise",
    "Common Mistakes",
    "Review Comments",
    "Final Summary",
]


def validate_required_sections(markdown: str) -> dict:
    """Check that every required section has a Markdown heading."""
    headings = set()
    for line in markdown.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            headings.add(match.group(1).strip().lower())

    missing = [
        section
        for section in REQUIRED_SECTIONS
        if section.lower() not in headings
    ]
    return {"valid": len(missing) == 0, "missing": missing}

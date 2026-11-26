from tools.validation import validate_required_sections

valid_md = """# Topic
Python decorators
## Simple Explanation
text
## Key Concepts
text
## Example
text
## Practice Exercise
text
## Common Mistakes
text
## Review Comments
text
## Final Summary
text
"""

incomplete_md = """# Topic
Python decorators
## Simple Explanation
text
## Example
text
"""

print("Valid:", validate_required_sections(valid_md))
print("Incomplete:", validate_required_sections(incomplete_md))

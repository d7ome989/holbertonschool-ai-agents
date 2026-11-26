# AI Agents Intro: Study Guide Generator

A small AI agent system built with Python, Google ADK, LiteLLM and Ollama.

## Model Provider

- **Provider:** Ollama (local), connected through LiteLLM
- **Explainer Agent:** `llama3.2:1b` (`ollama_chat/llama3.2:1b`)
- **Practice Designer Agent:** `gemma2:2b` (`ollama_chat/gemma2:2b`)
- **Reviewer Agent:** `gemma2:2b` (`ollama_chat/gemma2:2b`)

## Setup

1. Create and activate a virtual environment:

   ````bash
   python3 -m venv venv
   source venv/bin/activate
   ````

2. Install dependencies:

   ````bash
   pip install -r requirements.txt
   ````

3. Install Ollama (https://ollama.com) and pull the models:

   ````bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull llama3.2:1b
   ollama pull gemma2:2b
   ````

4. Test a model directly:

   ````bash
   ollama run llama3.2:1b "Say hello in one short sentence."
   ````

5. Create your local `.env` file from the example:

   ````bash
   cp .env.example .env
   ````

   The real `.env` is ignored by Git and must never be committed.

## Configuration

| Variable | Description |
|----------|-------------|
| `OLLAMA_API_BASE` | Address of the local Ollama server |
| `EXPLAINER_MODEL` | LiteLLM model name for the Explainer Agent |
| `PRACTICE_MODEL` | LiteLLM model name for the Practice Designer Agent |
| `REVIEWER_MODEL` | LiteLLM model name for the Reviewer Agent |

## Usage

````bash
python3 main.py "Python decorators"
````

The output is validated for required sections and saved to `output/study_guide.md`.

## Example Output

Topic: `Python decorators` (model: `llama3.2:1b`)

````markdown
## Simple Explanation

Python decorators are a powerful tool in Python that allow you to modify the behavior of a function without permanently changing its implementation. They are a way to wrap a function with additional functionality without permanently modifying the function itself. Decorators are useful for things like logging, timing, and authentication.

## Key Concepts

*   **Function**: a block of code that takes in arguments and returns a value.
*   **Decorator**: a function that takes in another function as an argument and returns a new function that "wraps" the original function.
*   **Wrapped function**: the original function that is passed to the decorator.

## Example

```python
import time

def timer_decorator(func):
    def wrapper():
        start_time = time.time()
        result = func()
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to run.")
        return result
    return wrapper

@timer_decorator
def example_function():
    time.sleep(2)  # Simulate some work
    print("Function executed.")

example_function()
```
````

> Note: the raw output was edited by hand. The model forgot `import time`, which was added. It also wrote an extra paragraph after the code (with an incorrect last sentence), which was removed because the instructions asked it to stop after the Example section.

## Known Limitations

- The 1B model sometimes leaks parts of its instructions into the reply (for example `Stop here.`).
- It may ignore the requested number of key concepts and repeat items.
- It can produce code with missing imports.
- With Arabic input it misunderstood the topic and explained Bayes' theorem instead of Python variables.
- The practice designer sometimes writes illogical exercises, vague expected output, or more hints than requested.
- With the 1B model, the practice designer often skipped the Hints section or wrote the solution, so `gemma2:2b` is used for this agent.
- The reviewer can miss real problems (for example an undefined name in the example) and sometimes gives generic comments. With the 1B model it approved an incomplete draft, so `gemma2:2b` is used for this agent.
- The pipeline's validator only checks that headings exist, so duplicated sections, unclosed code blocks, or an off-topic exercise still pass validation.
- The reviewer often misses these problems and gives generic comments.
- Generated facts can be wrong even when the structure is valid. For example, one run labeled HTTP codes 100-199 as "Success" instead of "Informational", and the reviewer did not catch it.
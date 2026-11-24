# AI Agents Intro: Study Guide Generator

A small AI agent system built with Python, Google ADK, LiteLLM and Ollama.

## Model Provider

- **Provider:** Ollama (local)
- **Model:** `llama3.2:1b`
- **Connector:** LiteLLM (`ollama_chat/llama3.2:1b`)

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

3. Install Ollama (https://ollama.com) and pull the model:

   ````bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull llama3.2:1b
   ````

4. Test the model directly:

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
| `MODEL_NAME` | LiteLLM model name (`ollama_chat/<model>`) |

## Usage

````bash
python3 main.py "Python decorators"
````

## Example Output

Topic: `Python decorators` (model: `llama3.2:1b`)

````markdown
## Explanation

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
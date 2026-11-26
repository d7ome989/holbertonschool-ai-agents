## Simple Explanation
Python decorators are a powerful feature that allows developers to add additional functionality to existing functions without modifying their source code. They provide a flexible way to wrap another function in order to extend the behavior of the wrapped function, without permanently modifying it.

## Key Concepts
*   **Decorators**: A decorator is a function that takes another function as an argument and returns a new function that "wraps" the original function.
*   **Functional Programming**: Decorators are a key concept in functional programming, allowing developers to write code that can be reused across multiple functions.
*   **Function Wrapping**: The decorator is essentially a function that wraps the original function, making it available as a new function with the added functionality.

## Example
```python
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
```
In this example, `my_decorator` is a decorator that takes `say_hello` as an argument and returns a new function `wrapper`. The `wrapper` function calls `say_hello` inside it, and also prints out a message before and after the call. When you run `say_hello()`, it will print the message and then call `say_hello`.
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

import os

from config import load_env_file

load_env_file()
MODEL_NAME = os.getenv("SUMMARY_MODEL", "ollama_chat/gemma2:2b")


INSTRUCTION = """You are a teaching assistant for beginner programmers.
The user message contains a topic and an explanation of that topic.
Do not explain the topic again. Never write code blocks.

Reply in Markdown with exactly these two parts, in this order:

## Common Mistakes
Two or three bullet points about mistakes beginners make with this topic.

## Final Summary
Two or three sentences that summarize the topic.

Every part above must appear in your reply.
"""

summary_agent = Agent(
    name="summary_agent",
    model=LiteLlm(model=MODEL_NAME),
    description="Writes common mistakes and a final summary.",
    instruction=INSTRUCTION,
)

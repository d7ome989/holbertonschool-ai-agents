import asyncio
import sys

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.explainer_agent import explainer_agent
from tools.file_writer import save_markdown_file
from tools.validation import validate_required_sections

APP_NAME = "study_guide_app"
USER_ID = "student"
SESSION_ID = "session_1"
OUTPUT_PATH = "output/study_guide.md"


async def run_agent(topic: str) -> str:
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    runner = Runner(
        agent=explainer_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    message = types.Content(role="user", parts=[types.Part(text=topic)])

    final_text = ""
    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_text = event.content.parts[0].text
    return final_text


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python3 main.py "<topic>"')
        sys.exit(1)
    topic = " ".join(sys.argv[1:])
    result = asyncio.run(run_agent(topic))
    print(result)

    validation = validate_required_sections(result)
    if validation["valid"]:
        print("Validation: all required sections are present.")
    else:
        print("Validation: missing sections ->", ", ".join(validation["missing"]))
    print(save_markdown_file(OUTPUT_PATH, result))

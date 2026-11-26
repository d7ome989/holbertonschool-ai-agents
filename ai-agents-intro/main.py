import asyncio
import sys

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.explainer_agent import explainer_agent
from agents.practice_designer_agent import practice_designer_agent
from agents.reviewer_agent import reviewer_agent
from agents.summary_agent import summary_agent
from tools.file_writer import save_markdown_file
from tools.validation import validate_required_sections

APP_NAME = "study_guide_app"
USER_ID = "student"
OUTPUT_PATH = "output/study_guide.md"
SUMMARY_HEADING = "## Final Summary"


async def run_agent(agent: Agent, message_text: str) -> str:
    """Run one agent in a fresh session and return its final text."""
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID
    )
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    message = types.Content(
        role="user", parts=[types.Part(text=message_text)]
    )

    final_text = ""
    async for event in runner.run_async(
        user_id=USER_ID, session_id=session.id, new_message=message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_text = event.content.parts[0].text
    return final_text.strip()


def topic_and_explanation(topic: str, explanation: str) -> str:
    """Build the input message for agents that need both."""
    return f"Topic: {topic}\n\nExplanation:\n{explanation}"


def split_summary(text: str) -> tuple[str, str]:
    """Split the summary agent reply into mistakes and final summary."""
    mistakes, marker, summary = text.partition(SUMMARY_HEADING)
    return mistakes.strip(), (marker + summary).strip()


def assemble_draft(
    topic: str, explanation: str, practice: str, mistakes: str
) -> str:
    """Build the draft study guide (everything except review and summary)."""
    return "\n\n".join(
        ["# Topic", topic, explanation, practice, mistakes]
    )


def assemble_final(draft: str, review: str, summary: str) -> str:
    """Build the final Markdown: draft, then review, then summary."""
    return "\n\n".join([draft, review, summary]) + "\n"


def report_validation(markdown: str) -> None:
    """Print the validation result and any missing sections."""
    result = validate_required_sections(markdown)
    if result["valid"]:
        print("Validation: all required sections are present.")
    else:
        print("Validation: missing sections ->", ", ".join(result["missing"]))


async def main(topic: str) -> None:
    print(f"[1/5] Explainer Agent: explaining '{topic}'...")
    explanation = await run_agent(explainer_agent, topic)

    print("[2/5] Practice Designer Agent: creating an exercise...")
    practice = await run_agent(
        practice_designer_agent, topic_and_explanation(topic, explanation)
    )

    print("[3/5] Summary Agent: common mistakes and summary...")
    summary_reply = await run_agent(
        summary_agent, topic_and_explanation(topic, explanation)
    )
    mistakes, summary = split_summary(summary_reply)

    draft = assemble_draft(topic, explanation, practice, mistakes)

    print("[4/5] Reviewer Agent: reviewing the draft...")
    review = await run_agent(reviewer_agent, draft)

    final_markdown = assemble_final(draft, review, summary)

    print("[5/5] Validating and saving...")
    report_validation(final_markdown)
    print(save_markdown_file(OUTPUT_PATH, final_markdown))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python3 main.py "<topic>"')
        sys.exit(1)
    asyncio.run(main(" ".join(sys.argv[1:])))

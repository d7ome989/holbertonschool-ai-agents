# AI Agents in Python

## Description

A small AI Study Guide Generator built with Python, Google ADK, LiteLLM and Ollama. Given a programming topic, a sequence of four agents generates a Markdown study guide. Two deterministic tools validate the required sections and save the file to `output/study_guide.md`.

The guide contains: Topic, Simple Explanation, Key Concepts, Example, Practice Exercise, Common Mistakes, Review Comments and Final Summary.

## Requirements

- Python 3.12 (tested with 3.12.3) on Linux (Pop!_OS)
- [Ollama](https://ollama.com) running locally
- Models: `llama3.2:1b` and `gemma2:2b`
- Python packages: `google-adk==2.15.0`, `litellm==1.110.3`
- Hardware used: 8 CPU cores and 6.7 GB RAM, no GPU assumed. Larger models were too heavy, so only small models are used.

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

3. Install Ollama and pull the models:

   ````bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull llama3.2:1b
   ollama pull gemma2:2b
   ````

4. Check that Ollama is running:

   ````bash
   curl http://localhost:11434
   ````

   Expected answer: `Ollama is running`.

## Configuration

Copy the example file. The real `.env` is ignored by Git and must never be committed. The default local setup needs no API keys.

````bash
cp .env.example .env
````

| Variable | Description |
|----------|-------------|
| `OLLAMA_API_BASE` | Address of the local Ollama server |
| `EXPLAINER_MODEL` | LiteLLM model for the Explainer Agent (`llama3.2:1b`) |
| `PRACTICE_MODEL` | LiteLLM model for the Practice Designer Agent (`gemma2:2b`) |
| `REVIEWER_MODEL` | LiteLLM model for the Reviewer Agent (`gemma2:2b`) |
| `SUMMARY_MODEL` | LiteLLM model for the Summary Agent (`gemma2:2b`) |

Model names use the format `ollama_chat/<model>`. To use another LiteLLM provider, change these values and put its API key in `.env`, never in the code.

## How to Run

````bash
python3 main.py "Python decorators"
````

The script prints its progress, validates the result, and saves it to `output/study_guide.md`. A run takes about a minute.

## Example Input

````bash
python3 main.py "HTTP status codes"
````

Other tested topics are listed in `data/topic_examples.json`.

## Example Output

Shortened from a real run (hand-corrected, see the note below).

````markdown
# Topic

HTTP status codes

## Simple Explanation
HTTP status codes are a way for a server to communicate the result of a request to a client.

## Key Concepts
*   100-199: Informational codes
*   200-299: Success codes
*   300-399: Redirection codes
*   400-499: Client error codes
*   500-599: Server error codes

## Practice Exercise
Create a program that prints the HTTP status codes for GET, POST and DELETE.

### Hints
1.  Look up the meaning of GET, POST, and DELETE requests.

## Review Comments
### Recommendation
Revise

## Final Summary
HTTP status codes are numerical codes used to communicate the result of a request.
````

> Note: the real output was shortened and corrected by hand. The model labeled 100-199 as "Success" and wrote "to a server" instead of "to a client", and the reviewer did not catch it.

## Project Structure

````text
ai-agents-intro/
├── agents/
│   ├── explainer_agent.py
│   ├── practice_designer_agent.py
│   ├── reviewer_agent.py
│   └── summary_agent.py
├── tools/
│   ├── file_writer.py
│   └── validation.py
├── output/
│   └── study_guide.md
├── data/
│   └── topic_examples.json
├── checks.py
├── config.py
├── main.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
````

## Agents

Each agent has one responsibility and runs in a fresh session. Agents communicate only through plain text passed by `main.py`.

| Agent | Model | Role |
|-------|-------|------|
| Explainer | `llama3.2:1b` | Writes Simple Explanation, Key Concepts and Example |
| Practice Designer | `gemma2:2b` | Creates an exercise from the topic and explanation |
| Summary | `gemma2:2b` | Writes Common Mistakes and Final Summary |
| Reviewer | `gemma2:2b` | Reviews the draft and writes Review Comments |

Order: Explainer, Practice Designer, Summary, then Reviewer reviews the assembled draft.

## Tools

| Tool | File | Role |
|------|------|------|
| `save_markdown_file()` | `tools/file_writer.py` | Creates the folder if needed, writes the file, returns a success or error message |
| `validate_required_sections()` | `tools/validation.py` | Checks that the 8 required headings exist and lists the missing ones |

Support modules: `config.py` reads `.env` and checks variables. `checks.py` checks the topic, Ollama and the installed models before any agent runs.

## Self-Validation Checklist

- [x] `README.md` includes all required sections
- [x] Dependencies, model configuration and run instructions are explained
- [x] One example input and one example output are included
- [x] Each agent and each tool is described
- [x] Reflection and known limitations are included
- [x] At least three agents and two deterministic tools
- [x] Output is saved as Markdown in `output/`
- [x] No secrets are committed (`.env` and `venv/` are ignored)

## Reflection

**1. Direct LLM call vs. AI agent.** A direct call sends text to a model and gets text back. An agent combines a model, a role and instructions (and can use tools), and runs inside a framework (Google ADK) that manages sessions and execution.

**2. Role of each agent.** The Explainer explains the topic. The Practice Designer creates an exercise from that explanation. The Summary agent writes common mistakes and a summary. The Reviewer comments on the draft without rewriting it.

**3. Role of each tool.** `save_markdown_file()` saves the guide predictably. `validate_required_sections()` checks the structure with plain code, since a model cannot be trusted to do that.

**4. Most difficult part.** Making the small 1B model follow the required format. The Practice Designer often skipped the Hints section or wrote the solution, and every prompt fix solved one problem and created another.

**5. Limitation observed.** `llama3.2:1b` leaks parts of its instructions, repeats items and invents facts. With Arabic input it explained Bayes' theorem instead of Python variables.

## Known Limitations

- The 1B model sometimes leaks instruction text into the reply, ignores requested counts and repeats items.
- It can produce code with missing imports, and the Explainer sometimes breaks its own format.
- Arabic input is not supported reliably.
- The practice designer can write illogical exercises or vague expected output. With the 1B model it often skipped Hints or wrote the solution, so `gemma2:2b` is used.
- The reviewer misses real problems (undefined names, wrong facts) and gives generic comments.
- The validator only checks that headings exist, so duplicated sections, unclosed code blocks or an off-topic exercise can still pass.
- Generated facts can be wrong even when the structure is valid (for example HTTP 100-199 labeled "Success").
- Model output varies between runs, and the machine has limited memory (6.7 GB), which rules out larger models.
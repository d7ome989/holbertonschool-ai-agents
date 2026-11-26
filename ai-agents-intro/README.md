# AI Agents Intro: Study Guide Generator

A small AI agent system built with Python, Google ADK, LiteLLM and Ollama. Given a programming topic, it generates a Markdown study guide with an explanation, key concepts, an example, a practice exercise, common mistakes, review comments and a final summary.

## Model Provider

- **Provider:** Ollama (local), connected through LiteLLM
- **Explainer Agent:** `llama3.2:1b` (`ollama_chat/llama3.2:1b`)
- **Practice Designer Agent:** `gemma2:2b` (`ollama_chat/gemma2:2b`)
- **Reviewer Agent:** `gemma2:2b` (`ollama_chat/gemma2:2b`)
- **Summary Agent:** `gemma2:2b` (`ollama_chat/gemma2:2b`)

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
├── checks.py
├── config.py
├── main.py
├── .env.example
├── requirements.txt
└── README.md
````

## Workflow

`main.py` runs the agents in sequence. Each agent runs in a fresh session and receives its input as plain text.

````text
Topic
  -> Explainer Agent          (Simple Explanation, Key Concepts, Example)
  -> Practice Designer Agent  (Practice Exercise, from topic + explanation)
  -> Summary Agent            (Common Mistakes, Final Summary)
  -> Draft Study Guide
  -> Reviewer Agent           (Review Comments, from the draft)
  -> Final Markdown assembly
  -> Validation tool          (checks the 8 required sections)
  -> Save Markdown tool       (output/study_guide.md)
````

The two deterministic tools are `save_markdown_file()` in `tools/file_writer.py` and `validate_required_sections()` in `tools/validation.py`. Before any agent runs, `checks.py` and `config.py` verify the topic, the configuration and the Ollama setup.

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

   The real `.env` is ignored by Git and must never be committed. It contains no secrets for the default local setup.

## Configuration

Configuration is read from `.env` (or from the shell environment, which takes priority).

| Variable | Description |
|----------|-------------|
| `OLLAMA_API_BASE` | Address of the local Ollama server |
| `EXPLAINER_MODEL` | LiteLLM model name for the Explainer Agent |
| `PRACTICE_MODEL` | LiteLLM model name for the Practice Designer Agent |
| `REVIEWER_MODEL` | LiteLLM model name for the Reviewer Agent |
| `SUMMARY_MODEL` | LiteLLM model name for the Summary Agent |

Model names use the LiteLLM format `ollama_chat/<model>`. To use another provider supported by LiteLLM, change these values and add the API key your provider needs to `.env`, never to the code.

## Usage

````bash
python3 main.py "Python decorators"
python3 main.py "HTTP status codes"
````

The script prints its progress, validates the final guide, and saves it to `output/study_guide.md`. A run takes about a minute because four agents call the model one after another.

## Example Output

Topic: `HTTP status codes` (models: `llama3.2:1b` and `gemma2:2b`)

````markdown
# Topic

HTTP status codes

## Simple Explanation
HTTP (Hypertext Transfer Protocol) status codes are a way for a server to communicate the result of a request to a client. Each status code has a specific meaning, such as success or failure. Understanding these codes is essential for working with web applications.

## Key Concepts
*   HTTP status codes are grouped into five classes:
    *   100-199: Informational codes
    *   200-299: Success codes
    *   300-399: Redirection codes
    *   400-499: Client error codes
    *   500-599: Server error codes
*   Each status code has a specific reason for the request to be unsuccessful.
*   Understanding HTTP status codes is crucial for building robust web applications.

## Example
Here's an example of using the HTTP status code 201 Created to create a new resource:

```python
import requests

def create_resource():
    url = "https://example.com/resources"
    response = requests.post(url, json={"name": "Resource Created", "description": "This is a new resource."})
    print(response.status_code)

create_resource()
```

## Practice Exercise
Create a program that prints the HTTP status codes for the following actions:

*   Fetching a resource (GET)
*   Submitting a form (POST)
*   Deleting a resource (DELETE)

### Expected Input
None

### Expected Output
200
201
204

### Hints
1.  Look up the meaning of GET, POST, and DELETE requests.
2.  Review the HTTP status codes in the explanation.

## Common Mistakes
*   Forgetting to check the status code to determine if the request was successful.
*   Not understanding the different categories of status codes and how they relate to the request outcome.

## Review Comments

### Missing Information
*   There is no mention of how to interpret the status code's meaning beyond just a number.
*   The practice exercise doesn't specify the URLs to use for testing.

### Unclear Parts
*   The explanation mentions "categories of status codes" but doesn't clearly differentiate between success, failure, or redirection codes in a concise way.

### Suggestions
*   Add a section explaining the different status codes, such as 200 (OK), 400 (Bad Request), or 500 (Internal Server Error).
*   Provide links to resources with more detailed explanations of HTTP status codes.

### Recommendation
Revise

## Final Summary
HTTP status codes are numerical codes used to communicate the result of a request to a server. Understanding these codes are crucial for debugging, analyzing, and building robust web applications.
````

> Note: this is a real run, edited by hand in two places. The model wrongly labeled 100-199 as "Success codes" and 200-299 as "Created, updated, or deleted codes", and wrote "four levels" for five classes. The Key Concepts list above is corrected. It also said the server sends the result "to a server", which was corrected to "to a client". The reviewer did not catch any of these errors.

## Troubleshooting

| Problem | Message | What to check |
|---------|---------|---------------|
| Empty topic | `Error: Topic cannot be empty.` | Pass a topic: `python3 main.py "Python decorators"` |
| Missing configuration | `Error: Missing environment variables: ...` | Run `cp .env.example .env` and check all variables are set |
| Ollama not running | `Error: Cannot reach Ollama at ...` | Run `sudo systemctl start ollama`, then `curl http://localhost:11434` |
| Model not installed | `Error: Model not available: ...` | Run `ollama pull <model>` and check with `ollama list` |
| Cannot write output | `Error: could not save file (...)` | Check that `output/` exists and is writable |
| Incomplete guide | `Validation: missing sections -> ...` | The guide is still saved. Run again, since model output varies |

Unexpected errors (for example a bug in agent code) are not hidden: the full traceback is printed so it can be debugged.

## Known Limitations

- The 1B model sometimes leaks parts of its instructions into the reply (for example `Stop here.`).
- It may ignore the requested number of key concepts and repeat items.
- It can produce code with missing imports.
- The Explainer sometimes breaks its own format (wrong heading level, repeated Example section, leaked instruction text).
- With Arabic input it misunderstood the topic and explained Bayes' theorem instead of Python variables.
- The practice designer sometimes writes illogical exercises, vague expected output, or more hints than requested.
- With the 1B model, the practice designer often skipped the Hints section or wrote the solution, so `gemma2:2b` is used for this agent.
- The reviewer can miss real problems (for example an undefined name in the example) and often gives generic comments. With the 1B model it approved an incomplete draft, so `gemma2:2b` is used for this agent.
- The validator only checks that headings exist, so duplicated sections, unclosed code blocks, or an off-topic exercise can still pass validation.
- Generated facts can be wrong even when the structure is valid. For example, one run labeled HTTP codes 100-199 as "Success" instead of "Informational", and the reviewer did not catch it.
# AI Agent

AI Agent is a Python-based local coding assistant that gives a large language model access to a small, safe set of tools for inspecting, modifying, and running code inside a defined working directory. The project demonstrates the tool-calling pattern used by modern AI agents: the model can reason about the task, call structured functions, and produce a final answer based on the results rather than guessing blindly.

This repository is useful for learning how AI agent workflows can be constrained with sandboxed file operations and explicit execution capabilities, while still working in a real project environment. It is intentionally lightweight and focused on safety, observability, and predictable function execution.

## Core Features

- File and directory inspection within a restricted project sandbox
- Safe file reads with output truncation for large files
- File writes that create parent directories when needed
- Python script execution with optional CLI arguments
- Tool orchestration through the Google GenAI function-calling API
- Local model inference via an Ollama-compatible endpoint
- Structured prompts and tool declarations that guide agent behavior

## Tech Stack

### Languages
- Python 3.10+
- Shell / CLI scripting

### AI & Runtime
- Google GenAI SDK
- OpenAI SDK
- Ollama-compatible local model server

### Databases
- None in the current implementation

### Tools & Infra
- `pip` and `venv`
- `pytest` (for smoke/integration-style validation)
- Git
- Local filesystem sandboxing

## Architecture & Directory Structure

This project follows a simple tool-calling agent architecture: the application exposes a set of explicit functions, the model decides when to call them, and each function performs a constrained operation safely within a designated working directory.

```text
aiagent/
├── main.py                     # CLI entrypoint; creates the AI client and orchestrates messages/tool calls
├── config.py                   # Shared configuration values (e.g. max file-read size)
├── prompts.py                  # System prompt that instructs the model how to use tools
├── pyproject.toml              # Python package metadata and direct dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
├── test_get_file_content.py    # Smoke test for reading a file
├── test_get_files_info.py      # Smoke test for listing directories
├── test_run_python_file.py     # Smoke test for executing Python files
├── test_write_file.py          # Smoke test for writing files
├── calculator/                 # Sandboxed project used as a working directory for tool calls
│   ├── README.md
│   ├── lorem.txt
│   ├── main.py
│   ├── tests.py
│   └── pkg/
│       ├── calculator.py
│       ├── morelorem.txt
│       └── render.py
├── functions/
│   ├── call_function.py        # Function registry and dispatch logic
│   ├── get_file_content.py     # Read file contents safely
│   ├── get_files_info.py       # List directory contents safely
│   ├── run_python_file.py      # Run Python files in a subprocess
│   └── write_file.py           # Write content to files within the allowed directory
├── help/                       # Local virtual environment included with the project
│   ├── pyvenv.cfg
│   ├── Scripts/
│   └── Lib/
└── .idea/                      # IDE metadata
```

### Architectural Pattern

- Tool-calling AI agent pattern
- Model layer: Google GenAI / Ollama-compatible inference
- Tool layer: read, list, write, run Python
- Safety layer: directory-bound validation before file access or execution
- Execution layer: Python subprocess calls for script execution

This keeps the agent predictable and reduces the risk of unrestricted file-system access.

## Prerequisites & System Requirements

### Required Software
- Python 3.10 or newer
- `pip` and `venv`
- Git
- A local Ollama server running on `http://localhost:11434/v1`
- An Ollama model available locally, such as `qwen3.5:27b`

### Optional Tools
- `curl` for simple health checks against local services
- `pytest` if you want to run the project’s validation scripts through the test runner
- An IDE such as VS Code with Python support

### Notes on Runtime Behavior

The project is hard-coded to use:

- `OLLAMA_URL = "http://localhost:11434/v1"`
- `OLLAMA_MODEl = "qwen3.5:27b"`

If your local model differs, update the constants in `main.py` before running the agent.

## Installation & Getting Started

### 1) Clone the Repository

```bash
git clone <your-repository-url>
cd aiagent
```

### 2) Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install Dependencies

This project uses `pyproject.toml` and direct Python dependencies. Install them with:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -e .
```

If you want to install the same packages explicitly, the project depends on:

```bash
python3 -m pip install "google-genai>=1.12.1" "openai>=2.30.0" "python-dotenv>=1.1.0"
```

### 4) Start the Local Model Service

This project expects Ollama to be running locally and the target model to be installed.

```bash
ollama serve
ollama pull qwen3.5:27b
```

### 5) Run the Agent

```bash
python3 main.py "Inspect the calculator project and explain what it does."
```

You can enable verbose output to see more of the tool invocation flow:

```bash
python3 main.py "List the files in calculator and summarize the project structure." --verbose
```

### Environment Variables

This repository does not currently include a `.env.example` or `.env` loader. Configuration is still embedded directly in code, primarily in `main.py` and `config.py`.

If you later decide to externalize configuration, the likely keys would be:

```env
OLLAMA_URL=http://localhost:11434/v1
OLLAMA_MODEL=qwen3.5:27b
MAX_CHARS=100000
```

These values are not currently consumed via `dotenv`, so the present implementation relies on in-file configuration.

## Usage & Examples

### Primary Workflows

The agent can perform the following tasks through tool calls:

| Tool | Purpose | Typical Use |
| --- | --- | --- |
| `get_files_info` | List files and metadata in a directory | Inspect a project structure |
| `get_file_content` | Read file contents safely | Review implementation details |
| `write_file` | Write or create a file inside the working directory | Save generated code or notes |
| `run_python_file` | Execute a Python script | Validate logic or run a demo |

### Example: Inspect a File

```bash
python3 main.py "Read calculator/main.py and explain the script’s purpose."
```

### Example: Browse a Directory

```bash
python3 main.py "List files in calculator/pkg and tell me which modules are present."
```

### Example: Execute and Validate Code

```bash
python3 main.py "Run calculator/tests.py and report the results."
```

### Example: Create or Update a File

```bash
python3 main.py "Write a short README for calculator/pkg with the purpose of each module."
```

## Testing & Quality Checks

This repository includes small smoke-style validation scripts at the project root, not a full production test suite. They are useful for confirming the tool functions behave as expected.

### Run the Test Scripts Directly

```bash
python3 test_get_file_content.py
python3 test_get_files_info.py
python3 test_run_python_file.py
python3 test_write_file.py
```

### Run with `pytest` (if installed)

```bash
python3 -m pytest -q
```

### Linting / Formatting

There is currently no configured linting or formatting pipeline in the repo (`ruff`, `black`, or `mypy` are not defined in `pyproject.toml`). If you want to add one, a common setup would be:

```bash
python3 -m pip install ruff black
ruff check .
black --check .
```

## Deployment & CI/CD

### Current State

This project is currently a local Python CLI agent and does not yet include:

- a Dockerfile
- Kubernetes manifests
- cloud deployment configuration
- GitHub Actions workflows

### Production Build Notes

For local production-like validation, run the following checks:

```bash
python3 -m compileall .
python3 -m pytest -q
```

### Recommended Deployment Strategy

1. Package the project as a proper Python application in a clean environment.
2. Run the service from a managed host or VM with an Ollama endpoint reachable at runtime.
3. Add environment-based configuration for the model URL and working directory.
4. Add CI steps to run tests and static analysis on every pull request.
5. If needed, containerize the agent with Docker for consistent deployment.

### Example CI Workflow Outline

```yaml
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: python -m pip install --upgrade pip
      - run: python -m pip install -e . pytest
      - run: python -m pytest -q
```

## Contributing

Contributions are welcome. To keep the project maintainable and safe:

- Open an issue before large changes
- Keep tool behavior constrained and explicit
- Add or update tests for new functionality
- Keep the model instruction prompt clear and deterministic
- Document changes that affect the tool contract or security boundaries

### Pull Request Checklist

- Follow the existing project structure
- Verify relevant test scripts still pass
- Explain the security impact of any new tool or file system operation
- Include a brief summary of the change and validation steps

## Licensing

This repository does not currently declare a license file. Before publishing or distributing the project publicly, add a license such as MIT or Apache 2.0 and include the appropriate notice in the repository root.

Suggested placeholder:

```text
License: MIT
```

## Notes

This project is best understood as a learning-oriented tool-calling agent rather than a production SaaS application. It is deliberately small, transparent, and easy to understand, which makes it a strong reference implementation for experimenting with agent tool design, safe file access, and local model integration.

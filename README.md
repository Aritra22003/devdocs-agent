@"
# DevDocs Agent

A local AI-powered developer documentation assistant built with Python,
Ollama, Qwen3, and the Model Context Protocol (MCP).

## Features

- Exposes documentation search as an MCP tool.
- Uses a local language model to decide when to call the tool.
- Searches local Markdown documentation.
- Returns answers with documentation source filenames.
- Handles queries for which no matching documentation is found.

## Tech Stack

- Python 3.11+
- Ollama with Qwen3
- MCP Python SDK
- Requests
- Python unittest

## Setup

1. Install Python and Ollama.
2. Download the model: `ollama pull qwen3:4b`
3. Install dependencies: `python -m pip install -r requirements.txt`
4. Run the agent: `python agent.py`

## Testing

Run: `python -m unittest test_server -v`

## Limitations

This is a local prototype with basic keyword-based document retrieval.
It has not been designed or audited for production use.
"@ | Set-Content -Encoding utf8 README.md
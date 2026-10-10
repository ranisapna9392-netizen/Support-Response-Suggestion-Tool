# Support Response Suggestion Tool

A Streamlit application that helps customer support teams identify customer issues and draft professional responses using a local language model.

## Features

- Customer message input through a Streamlit interface.
- TF-IDF and cosine similarity for support category matching.
- Response generation using Ollama and Qwen 2.5 3B.
- Suggested responses based on approved support guidance.
- Similarity scores, response downloads, and clear-form functionality.
- Automated tests for matching and pipeline behavior.

## Project Structure

```text
Support-Response-Suggestion-Tool/
├── data/
│   └── responses.json
├── src/
│   ├── app.py
│   ├── local_llm.py
│   ├── response_generator.py
│   ├── response_matcher.py
│   └── support_pipeline.py
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.12
- Ollama installed and running
- The Qwen 2.5 3B model

## Installation

Create and activate a virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

Download the language model if it is not already available:

```powershell
ollama pull qwen2.5:3b
```

## Run the Application

From the project root, run:

```powershell
python -m streamlit run src/app.py
```

## Run the Tests

```powershell
python -m pytest -v
```

The current automated test suite contains 11 tests, which passed in the local development environment.

## How It Works

1. The customer enters a support message.
2. The response matcher compares the message with example queries in `data/responses.json`.
3. TF-IDF vectors and cosine similarity are used to identify a likely support category.
4. Ollama sends the customer message and approved guidance to Qwen 2.5 3B.
5. The application displays a suggested response for human review.

## Limitations

The application uses a local Ollama server. A cloud deployment requires access to a separately hosted Ollama server or changes to use a hosted language-model API.

The application does not automatically access customer databases, order records, payment systems, or tracking services.

AI-generated responses should be reviewed before being sent to customers.

# LicenSage

A GenAI-powered platform for software license compliance checks. LicenSage accepts GitHub repository URLs or dependency files (requirements.txt, package.json, etc.) as input, scans for software packages, and outputs their licensing information, usage permissions, and restrictions.

## Features

1. **Input Parsing**: Accept GitHub repo links and dependency files (requirements.txt, package.json, .csproj, pyproject.toml)
2. **Metadata Extraction**: Automatically identify and retrieve package metadata
3. **GenAI Analysis**: Use LLM models to interpret license text, extracting key permissions, obligations, and usage limits
4. **Output Generation**: Provide a consolidated report listing each package, its license type, permissions, and limitations

## Tech Stack

1. **FastAPI**: Backend API
2. **Streamlit**: Frontend UI
3. **LangChain**: AI orchestration
4. **OpenAI/Google Gemini**: LLM models for license analysis

## Project Structure

```plaintext
licenSage/
├── backend/
│   ├── models/       # LLM integration and data models
│   ├── routes/       # API route handlers
│   ├── utils/        # Utility functions
│   ├── config.py     # Application configuration
│   └── main.py       # FastAPI application entry point
├── frontend/
│   └── app.py        # Streamlit application
├── .vscode/          # VS Code configuration
├── pyproject.toml    # Project dependencies
└── .env.example      # Environment variables template
```

## Setup

### Using uv (Recommended)

Follow these steps to set up the project:

```bash
# 1. Create a virtual environment
uv venv

# 2. Install all dependencies
uv sync

# 3. For development dependencies
uv sync --only-dev

# 4. Copy .env.example to .env and add your API keys
copy .env.example .env
```

## Running the Application

### Using VS Code

The project includes a `.vscode/launch.json` file with configurations for running both the frontend and backend:

1. Open the project in VS Code
2. Go to the Run and Debug view (Ctrl+Shift+D)
3. Select one of the following configurations:
   - **Backend: FastAPI**: Run only the backend API
   - **Frontend: Streamlit**: Run only the Streamlit frontend
   - **Run Full Stack**: Run both the backend and frontend simultaneously

### Using Command Line

To run the FastAPI backend:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

To run the Streamlit frontend:

```bash
streamlit run frontend/app.py
```

## Development Timeline

1. April 7th to April 11th: Setup of frontend, backend, and cloud environments, followed by initial input parsing implementation
2. April 14th to April 18th: Integration of Langchain and language models for AI-driven analysis
3. April 21st to April 23rd: Finalization of frontend development and project closure

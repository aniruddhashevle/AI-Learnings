# FAQs Agent

This project is an AI-powered FAQ and data analysis assistant built with Python, uv, LangChain, and Pandas.

The application loads one or more CSV files into Pandas DataFrames and uses a Large Language Model (LLM) to answer user questions based on the data. When a question is asked, the agent automatically identifies the most relevant DataFrame, analyzes the data, and generates a clear, human-readable response.

## Requirements

* Python 3.12+
* uv

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install Python version

```bash
uv python install
```

### 3. Create environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Update `.env` with your values.

### 4. Install dependencies

```bash
uv sync
```

### 5. Run the application

```bash
uv run python main.py
```

## Development

Add a dependency:

```bash
uv add <package-name>
```

Add a development dependency:

```bash
uv add --dev <package-name>
```

Update dependencies:

```bash
uv sync
```

## Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
OPENAI_API_KEY=
```

## License

MIT

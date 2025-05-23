# OpenAI Agent Example

This project demonstrates the implementation of an AI agent system using OpenAI's agents framework. The example showcases a sales email automation system that uses multiple specialized agents to generate, evaluate, and send cold sales emails.

## Features

- Multiple specialized AI agents working together:
  - Sales agents with different writing styles (professional, engaging, and concise)
  - Email subject writer
  - HTML email body converter
  - Email manager for formatting and sending
  - Sales manager for coordinating the process
- Integration with Resend for email delivery
- Asynchronous execution of agent tasks
- Trace logging for OpenAI platform monitoring

## Prerequisites

- Python 3.10 or higher
- OpenAI API key
- Resend API key
- uv (Python package installer and resolver)

## Setup

1. Clone the repository
2. Install dependencies using uv:
   ```bash
   uv sync
   ```
3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Then edit the `.env` file and fill in your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   RESEND_API_KEY=your_resend_api_key
   ```

## Running the Example

You can run the example using either of these commands:

```bash
uv run main.py
# or
make start
```

The script will:

1. Initialize multiple sales agents with different writing styles
2. Generate cold sales emails using these agents
3. Select the best email through the sales manager
4. Format the email with a subject and HTML body
5. Send the email using Resend

## Project Structure

- `main.py`: Main implementation file containing agent definitions and orchestration
- `pyproject.toml`: Project dependencies and metadata
- `.env`: Environment variables (not tracked in git)
- `.env.example`: Example environment variables file

## Dependencies

- openai-agents>=0.0.16
- python-dotenv>=1.1.0
- resend>=2.10.0
- black>=25.1.0 (for code formatting)

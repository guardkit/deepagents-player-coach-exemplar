# DeepAgents Exemplar

A generic exemplar demonstrating two-agent Player-Coach orchestration using the DeepAgents framework.

## Architecture

This project implements the Player-Coach pattern where:
- **Player** — executes domain tasks (search, write output, etc.)
- **Coach** — plans, delegates, and reviews the Player's work

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Copy environment template:
   ```bash
   cp .env.example .env
   ```

3. Configure your API keys in `.env`

## Usage

```bash
uv run python agent.py
```

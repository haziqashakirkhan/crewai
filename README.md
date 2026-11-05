# Smart Query Router using CrewAI & Groq

A multi-agent AI application that intelligently classifies user queries and routes them to specialized agents for mathematical problem-solving and concept explanation.

## Overview

The Smart Query Router uses **CrewAI** and **Groq-powered LLMs** to identify the intent behind a user's query and delegate it to the appropriate AI agent.

Instead of using a single general-purpose agent for every request, the system follows a routing-based architecture with specialized agents.

## Architecture

```text
             User Query
                  |
                  v
             Router Agent
                  |
           Intent Classification
                  |
           +------+------+
           |             |
           v             v
       MATH            EXPLAIN
           |             |
           v             v
       Math Agent    Teacher Agent
           |             |
           +------+------+
                  |
                  v
           Final Response
```

## Agents

| Agent | Responsibility |
|---|---|
| Query Router | Classifies queries into MATH or EXPLAIN |
| Math Expert | Solves mathematical problems with reasoning |
| Teacher | Explains academic and technical concepts |

## Tech Stack

- **Python** – Core application logic
- **CrewAI** – Multi-agent orchestration
- **Groq API** – LLM inference
- **python-dotenv** – Environment variable management

## Project Structure

```text
crewAI/
│
├── .crewai/
├── .venv/
├── .env
├── .env.example
├── .gitignore
├── app.py
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows – Git Bash**
```bash
source .venv/Scripts/activate
```

**Windows – PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install crewai python-dotenv
```

### 4. Configure environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

Never commit your actual API key.

### 5. Run the application

```bash
python app.py
```

## Example Queries

| User Query | Expected Agent |
|---|---|
| Calculate 25 × 12 | Math Expert |
| Solve x² - 5x + 6 = 0 | Math Expert |
| Explain neural networks | Teacher |
| What is Retrieval-Augmented Generation? | Teacher |

## How It Works

1. **Input:** The user submits a query through the command line.
2. **Classification:** The Router Agent analyzes the query and identifies its category.
3. **Routing:** Python conditional logic selects the corresponding specialist agent.
4. **Execution:** The selected agent processes the query through its assigned task.
5. **Output:** The application returns the specialist's response.

## Key Concepts Demonstrated

- Multi-agent systems
- Agent specialization
- Intent classification
- Conditional query routing
- LLM integration
- Task orchestration with CrewAI

## Current Scope

This is a foundational query-routing implementation with two supported categories: MATH and EXPLAIN.

Future improvements could include:
- Additional specialist agents
- More robust classification and fallback handling
- FastAPI-based interface
- Conversation memory
- Query logging and evaluation

## Author

**Haziqa Shakir Khan**

AI / ML Developer | Python | Machine Learning | Generative AI

[GitHub](https://github.com/haziqashakirkhan) · [LinkedIn](https://linkedin.com/in/haziqa-shakir-khan-8923513a6/)

---

*Built as a practical exploration of multi-agent orchestration and intelligent query routing using CrewAI.*

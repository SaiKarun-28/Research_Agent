# 🔍 AI Research Agent

An autonomous research assistant powered by **LangChain**, **Groq LLMs**, and dynamic tool calling. The agent gathers up-to-date web information via **DuckDuckGo**, extracts background knowledge from **Wikipedia**, validates schemas with **Pydantic**, and produces clean, formatted research reports saved directly to disk.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture & Workflow](#-architecture--workflow)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Available Tools](#-available-tools)
- [Output Example](#-output-example)
- [Extending & Customization](#-extending--customization)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## 📖 Overview

The **AI Research Agent** is designed to automate in-depth research across public web sources and Wikipedia. Using LangChain's agentic framework with ultra-fast inference via Groq, the agent dynamically decides which tools to query based on user input, synthesizes information from multiple sources, enforces structured Pydantic schema validation, and writes cleanly formatted text reports.

---

## ✨ Key Features

- **⚡ Ultra-Fast Inference with Groq**: Leverages high-throughput LLMs via `ChatGroq` for rapid, zero-temperature deterministic reasoning.
- **🌐 Dual-Engine Information Retrieval**:
  - Real-time web search powered by `ddgs` (DuckDuckGo Search).
  - Encyclopedic context extraction powered by `WikipediaQueryRun` with custom User-Agent configuration.
- **🛡️ Guardrailed Tool Execution**: System prompts enforce strict constraints against hallucinating unavailable tool names or attempting unsupported file/web operations.
- **📐 Structured Data Validation**: Utilizes Pydantic schemas (`ResearchResponse`) and strict JSON schema output formatting.
- **📝 Intelligent Text Formatter**: Custom line-wrapping utility that wraps long narrative paragraphs while strictly preserving Markdown headers, bullet points, numbered lists, and horizontal separators.
- **💾 Automated Report Persistence**: Automatically formats and saves comprehensive research outputs to `output.txt` and `research_output.txt`.

---

## 🏗️ Architecture & Workflow

```
┌─────────────────────────────────────────────────────────┐
│                      User Prompt                        │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                 LangChain Agent (ReAct)                 │
│                 Model: ChatGroq (LLM)                   │
└──────────────┬───────────────────────────┬──────────────┘
               │                           │
     ┌─────────┴─────────┐       ┌─────────┴─────────┐
     │  DuckDuckGo Tool  │       │  Wikipedia Tool   │
     │   (search_tool)   │       │    (wiki_tool)    │
     └─────────┬─────────┘       └─────────┬─────────┘
               │                           │
               └─────────────┬─────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│             Raw Synthesis & Tool Reasoning              │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│           Pydantic Structured Output Validation         │
│           (ResearchResponse: topic & summary)           │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│        Intelligent Markdown-Preserving Formatter        │
│          (Wraps prose, preserves markdown syntax)       │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│           Output Deliverable (output.txt)               │
└─────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```text
Research-Agent/
│
├── main.py              # Main execution script (agent initialization, formatting, and persistence)
├── tools.py             # Custom LangChain tools (DuckDuckGo search, Wikipedia query, and file save)
├── requirements.txt     # Project Python dependencies
├── .env                 # Environment variables (API keys - not committed)
├── output.txt           # Formatted output file containing the final research report
├── output.md            # Markdown copy of research results
└── README.md            # Project documentation
```

---

## ⚙️ Prerequisites

- **Python 3.10+** installed on your system.
- A **Groq API Key** (available free at [console.groq.com](https://console.groq.com/)).

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/Research-Agent.git
   cd Research-Agent
   ```

2. **Create and activate a virtual environment:**
   - **Linux / macOS:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - **Windows (Command Prompt / PowerShell):**
     ```cmd
     python -m venv .venv
     .venv\Scripts\activate
     ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔑 Configuration

Create a `.env` file in the root directory and add your Groq API key:

```env
GROQ_API_KEY=gsk_your_groq_api_key_here
```

---

## 💻 Usage

Run the agent from your terminal:

```bash
python main.py
```

### Interactive Prompt
When prompted:
```text
How can i help you? Research the latest developments in quantum computing and summarize key breakthroughs.
```

The agent will:
1. Formulate search queries for DuckDuckGo and Wikipedia.
2. Execute the tools and gather factual data.
3. Synthesize the findings into an organized report.
4. Apply structured validation and text wrapping.
5. Display the final response on the terminal and write it to `output.txt`.

---

## 🛠️ Available Tools

The agent is equipped with three tools defined in `tools.py`:

| Tool Name | Underlying Service | Description | Parameters |
| :--- | :--- | :--- | :--- |
| `search_tool` | `ddgs` (DuckDuckGo) | Performs real-time web search and returns top 5 text snippets. | `query: str` |
| `wiki_tool` | `WikipediaAPIWrapper` | Queries Wikipedia and retrieves the top article extract (up to 1,000 chars). | `query: str` |
| `save_tool` | Local File System | Appends timestamped research data into `research_output.txt`. | `data: str` |

---

## 📄 Output Example

Below is a snippet demonstrating how research reports are structured and preserved in `output.txt`:

```text
FINAL RESPONSE :

    **Quantum Computing Breakthroughs – Overview**

| Aspect | Details |
|--------|---------|
| **Primary Domain** | Quantum Information Science & Hardware Engineering |
| **Leading Architectures** | Superconducting Qubits, Trapped Ions, Neutral Atoms, Photonic Systems |
| **Recent Milestones** | Quantum Error Correction (QEC) threshold demonstrations, Logical Qubit scaling |

---

## 1. Key Architectural Developments

- **Logical Qubits & Error Mitigation**: Significant advancements in surface codes reducing fault rates.
- **Commercial Roadmaps**: Major industry roadmaps aiming for fault-tolerant quantum computing by 2030.

---

### TL;DR
Quantum computing is rapidly shifting from physical qubit benchmarks to fault-tolerant logical qubit operations, paving the way for practical applications in cryptography, materials discovery, and complex optimization.
```

---

## 🔧 Extending & Customization

### Changing the LLM Model
In `main.py`, you can change the model used by `ChatGroq`:
```python
llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # Or "openai/gpt-oss-120b", "mixtral-8x7b-32768"
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)
```

### Adding New Tools
Define new tools in `tools.py` using LangChain's `@tool` decorator:
```python
from langchain.tools import tool

@tool
def custom_tool(param: str) -> str:
    """Description of what the tool does."""
    # Custom tool logic here
    return "Result"
```
Then import and append it to the `tools` list in `main.py`:
```python
tools = [search_tool, wiki_tool, save_tool, custom_tool]
```

---

## ❓ Troubleshooting

- **`GROQ_API_KEY` missing**: Ensure `.env` is located in the working directory and `python-dotenv` is installed.
- **Wikipedia User-Agent warnings**: `tools.py` specifies a custom User-Agent in accordance with Wikipedia API policy. Modify the email string in `tools.py` to match your own contact info if needed.
- **Rate Limits**: Groq provides generous free-tier rate limits. If rate limits are encountered, consider adjusting request concurrency or switching model IDs.

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

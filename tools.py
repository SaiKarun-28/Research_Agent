from datetime import datetime

import wikipedia
from langchain.tools import tool
from langchain_community.tools import (
    WikipediaQueryRun,
)
from ddgs import DDGS
from langchain_community.utilities import WikipediaAPIWrapper

wikipedia.set_user_agent(
    "ResearchAgent/1.0 (isaikarun536@gmail.com)"
)



# -----------------------------
# Save Research Tool
# -----------------------------
@tool
def save_tool(data: str) -> str:
    """
    Saves structured research data to a text file.
    """

    filename = "research_output.txt"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    formatted_text = (
        f"\n---- Research Output -----\n"
        f"Timestamp: {timestamp}\n\n"
        f"{data}\n\n"
    )

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Data successfully saved to {filename}"


# -----------------------------
# DuckDuckGo Search Tool
# -----------------------------

@tool
def search_tool(query: str) -> str:
    """
    Search the web for information.
    """
    result = DDGS().text(query,max_results = 5)
    return result


# -----------------------------
# Wikipedia Tool
# -----------------------------
api_wrapper = WikipediaAPIWrapper(
    top_k_results=1,
    doc_content_chars_max=1000
)

wiki = WikipediaQueryRun(api_wrapper=api_wrapper)


@tool
def wiki_tool(query: str) -> str:
    """
    Search Wikipedia for information.
    """
    return wiki.run(query)
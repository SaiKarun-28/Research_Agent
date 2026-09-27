import os
import textwrap

from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from tools import search_tool, wiki_tool, save_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    # sources: list[str]
    # tools_used: list[str]

def format_output(text,width =100):
    lines = text.splitlines()
    formatted_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # Preserve empty lines
        if not stripped:
            formatted_lines.append("")
            continue
        
        #Preserve Markdown Strructures
        
        if(
            stripped.startswith("!") or
            stripped.startswith("#") or
            stripped.startswith("- ") or
            stripped.startswith("* ") or
            stripped.startswith("1. ") or
            stripped.startswith("2. ") or
            stripped.startswith("3. ") or
            stripped.startswith("4. ") or
            stripped.startswith("5. ") or
            stripped == "---"
        ):
          formatted_lines.append(line)
        
        else:
            
            wrapped = textwrap.fill(
                stripped,
                width = width,
                break_long_words = False,
                break_on_hyphens = False
            )
            formatted_lines.append(wrapped)
            
    return "\n".join(formatted_lines)


llm = ChatGroq(
    model = "openai/gpt-oss-120b",
    temperature = 0,
    groq_api_key = os.getenv("GROQ_API_KEY")
)

# parser = PydanticOutputParser(pydantic_object=ResearchResponse)

tools = [search_tool,wiki_tool,save_tool]


agent = create_agent(
    
    model = llm,
    tools = tools,
    system_prompt ="""
           
You are a research assistant that helps generate research reports.

You have access to these tools:

1. search_tool:
   Use this to search the web for current information.

2. wiki_tool:
   Use this to search Wikipedia for background information.

3. save_tool:
   Use this to save research data when appropriate.

IMPORTANT:
- Only use tools that are actually provided to you.
- Never invent or call a tool that is not available.
- Do not use tools named open_file, browse, fetch_url, or any other unavailable tool.
- If a search result contains a URL, treat the URL as information from the search result.
- Do not attempt to open the URL using an unavailable tool.

After completing the research, provide a clear and well-structured final answer.
"""

)

query = input("How can i help you? ")

raw_response = agent.invoke(
    {
        "messages" : [
            {
                "role" : "user",
                "content" : query
            }
        ]
    }
)


final_message = raw_response["messages"][-1].content

print("\nFINAL RESPONSE : ")
print(final_message)


# Second LLM call

structured_llm = llm.with_structured_output(ResearchResponse,
                                            method = "json_schema",
                                            strict = True
                                            )

try:
    structured_response = structured_llm.invoke(
        f"""
        Convert the following research report into the required structure.
        Research report:
        {final_message}       
        """   
    )
    
    # Format the final response before saving
    formatted_message = format_output(final_message)
    
    output_text = f"""FINAL RESPONSE :

    {formatted_message}
    """
    
    # Saves the entire response in output.txt file
     
    with open("output.txt","w",encoding = "utf-8")as f:
        f.write(output_text)
        
    print("\nResearch saved and can be viewed in output.txt file")

except Exception as k:
    print("Error parsing response",k)
    print("Raw Response",final_message)
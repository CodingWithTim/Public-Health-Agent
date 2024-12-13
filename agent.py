from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.googlesearch import GoogleSearch
from googlesearch import search
import os

def stream_agentic_response(query):
    web_agent = Agent(
        name="Web Agent",
        model=OpenAIChat(id="gpt-4o"),
        tools=[GoogleSearch()],
        # instructions=["Always include sources"],
        show_tool_calls=False,
        markdown=True,
        system_prompt='## Instructions\n- Always include sources\n- Use markdown to format your answers. Current date: Dec 12th, 2024.',
    )
    response = web_agent.run(query, stream=True)
    
    for chunck in response:
        yield chunck.content
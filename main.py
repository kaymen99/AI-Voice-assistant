import asyncio
from src.agents.agent import Agent
from src.tools.calendar.calendar_tool import CalendarTool
from src.tools.contacts import AddContactTool, FetchContactTool
from src.tools.emails.emailing_tool import EmailingTool
from src.tools.search import SearchWebTool, KnowledgeSearchTool
from src.speech_processing.conversation_manager import ConversationManager
from src.prompts.prompts import assistant_prompt
from dotenv import load_dotenv

load_dotenv()

# Choose any model with LiteLLM
model = "groq/llama3-70b-8192"
# model = "groq/llama-3.1-70b-versatile"
# model = "gemini/gemini-1.5-pro"

# agent tools
tools_list = [
    CalendarTool,
    AddContactTool,
    FetchContactTool,
    EmailingTool,
    SearchWebTool,
    # KnowledgeSearchTool
]

# Initiate the sale agent
agent = Agent("Assistant Agent", model, tools_list, system_prompt=assistant_prompt)

if __name__ == "__main__":
    manager = ConversationManager(agent)
    asyncio.run(manager.main())
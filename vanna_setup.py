from vanna import Agent, AgentConfig
from vanna.core.registry import ToolRegistry
from vanna.tools import RunSqlTool
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.google import GeminiLlmService
from vanna.integrations.local.agent_memory import DemoAgentMemory

from dotenv import load_dotenv
from pathlib import Path
import os

# ✅ Load .env correctly
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# ✅ Debug print
api_key = os.getenv("GOOGLE_API_KEY")
print("API KEY LOADED:", api_key)

# ❌ If missing
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found. Fix your .env file")

# ✅ LLM setup
llm = GeminiLlmService(
    api_key=api_key,
    model="gemini-2.5-flash"
)

registry = ToolRegistry()
registry.register(RunSqlTool(SqliteRunner("clinic.db")))

memory = DemoAgentMemory()

agent = Agent(
    AgentConfig(
        llm=llm,
        tool_registry=registry,
        memory=memory
    )
)

def get_agent():
    return agent
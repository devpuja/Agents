from typing import Any
from memory_service import get_memory
from agent_framework import (ContextProvider, SessionContext, AgentSession, SupportsAgentRun)

class SimpleMemoryProvider(ContextProvider):
    def __init__(self, source_id: str):
        super().__init__(source_id)
        
    async def before_run(self, *, agent: SupportsAgentRun, session: AgentSession, context: SessionContext, state: dict[str, Any]) -> None:
        favorite_database = get_memory("favorite_database")
        
        if favorite_database:
            context.extend_instructions(self.source_id, f"The user's favorite database is {favorite_database}.")
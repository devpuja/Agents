from typing import Any
from memory_service import search_memories
from agent_framework import (ContextProvider, SessionContext, AgentSession, SupportsAgentRun)

class SimpleMemoryProvider(ContextProvider):
    def __init__(self, source_id: str):
        super().__init__(source_id)
        
    async def before_run(self, *, agent: SupportsAgentRun, session: AgentSession, context: SessionContext, state: dict[str, Any]) -> None:
        memories = search_memories("personal")
        
        if not memories:
            return 
        
        memory_text = "\n".join(f"- {key} : {value}" for key, value in memories)
        
        context.extend_instructions(
            self.source_id,
            (
                "The following information has been stored as persistent memory about the user."
                "Use it when relevant to the user's question:\n" f"{memory_text}"
            )
        )
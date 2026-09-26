import re
from typing import Any
from memory_service import get_memory
from agent_framework import (ContextProvider, SessionContext, AgentSession, SupportsAgentRun)


class SimpleMemoryProvider(ContextProvider):
    def __init__(self, source_id: str):
        super().__init__(source_id)
        
    async def before_run(self, *, agent: SupportsAgentRun, session: AgentSession, context: SessionContext, state: dict[str, Any]) -> None:

        if not context.input_messages:
            return

        query = context.input_messages[-1].text or ""
        words = set(re.findall(r"[a-z]+", query.lower()))

        # Identify the memory topic.
        is_database = bool(words & {"database", "db"})

        is_personal_project = ("personal" in words and bool(words & {"project", "projects"}))

        if not (is_database and is_personal_project):
            return

        # Retrieve the canonical memory.
        key = "preferred_database_for_personal_projects"
        value = get_memory(key)

        if not value or value.strip().lower() in {"none", "null", "unknown", ""}:
            return

        # print(f"MEMORY RETRIEVED: {key} = {value}")

        context.extend_instructions(
            self.source_id,
            (
                "Stored user preference:\n"
                f"- Database for personal projects: {value}\n"
                "Use this preference when relevant. "
                "If the user states a newer preference, "
                "the newer statement takes precedence."
            )
        )
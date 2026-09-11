from dataclasses import dataclass
from typing import Any, Callable

@dataclass
class ToolDefinition:
    name: str
    description: str
    function: Callable[..., Any]
    
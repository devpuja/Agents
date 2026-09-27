import asyncio

from typing_extensions import Never
from agent_framework import (Executor, WorkflowBuilder, WorkflowContext, handler)


# ==============================Comments========================== #
# Executor → a unit of work
# Handler → defines how the executor processes input
# Edge → connects workflow steps
# send_message() → passes data to another workflow node
# yield_output() → exposes the final workflow output
# WorkflowBuilder → defines the workflow graph
# ==============================Comments========================== #

class UpperCaseExecutor(Executor):    
    @handler
    async def process(self, text: str, ctx: WorkflowContext[str]) -> None:
        result = text.upper()
        await ctx.send_message(result)
    
        
class AddExclamationExecutor(Executor):
    @handler
    async def process(self, text: str, ctx: WorkflowContext[Never, str]) -> None:
        result = text + " !!!"
        await ctx.yield_output(result)


async def main():
    upper_case = UpperCaseExecutor(id="upper_case")
    add_exclamation = AddExclamationExecutor(id="add_exclamation")
    
    workflow = (
        WorkflowBuilder(start_executor=upper_case)
        .add_edge(upper_case, add_exclamation)
        .build() 
    )
    
    events = await workflow.run("hello world")
    print(events.get_outputs())
    

if __name__ == "__main__":
    asyncio.run(main())

     
    
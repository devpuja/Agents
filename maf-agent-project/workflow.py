import asyncio
from typing import Any, cast

from agent_framework import Agent, Executor, WorkflowBuilder, WorkflowContext, handler
from agent_framework_ollama import OllamaChatClient

class DiagnosticExecutor(Executor):
    @handler
    async def inspect(self, message: Any, ctx: WorkflowContext) -> None:
        print("\n--------------- DIAGNOSTIC ---------------")
        print("Executor ID:", message.executor_id)
        print("Agent Response:", message.agent_response)
        print("------------------------------------\n")

        await ctx.send_message(cast(Any, str(message.agent_response)))
    
    
async def main():
    client = OllamaChatClient(model="llama3.1:latest")
    
    research_agent = Agent(
        client = client,
        name = "ResearchAgent",
        instructions=(
            "You are a research agent. "
            "Explain technical concepts accurately and concisely. "
            "For this exercise, research the user's question and provide the important facts."
        )
    )
    
    writer_agent = Agent(
        client=client,
        name = "WriterAgent",
        instructions=(
            "You are a writer agent. "
            "Take the research provided by another agent and turn it into a clear, easy-to-understand answer."
        )
    )
    
    # diagnostic = DiagnosticExecutor(id="diagnostic")
    
    # workflow = (
    #     WorkflowBuilder(start_executor=research_agent)
    #     .add_edge(research_agent, diagnostic)
    #     .add_edge(diagnostic, writer_agent)
    #     .build() 
    # )
    
    workflow = (
            WorkflowBuilder(start_executor=research_agent)
            .add_edge(research_agent, writer_agent)
            .build() 
        )
    
    events = await workflow.run("Explain CAP Theorem and why it is important.")
    outputs = events.get_outputs()
    
    print("\n------ FINAL OUTPUT ------")
    for output in outputs:
        print(output.text)
    

if __name__ == "__main__":
    asyncio.run(main())

     
    
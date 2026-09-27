import asyncio

from agent_framework import (Agent, AgentExecutorResponse, Executor, WorkflowBuilder, WorkflowContext, handler)
from agent_framework_ollama import OllamaChatClient

class ResearchAggregator(Executor):
    @handler
    async def aggregate(self, results: list[AgentExecutorResponse], ctx: WorkflowContext[str, str]) -> None:
        print("\n========== RESEARCH RESULTS ==========")

        research_text: list[str] = []
        for result in results:
            text = result.agent_response.text
            print(f"\n--- {result.executor_id} ---")
            print(text)
            research_text.append(f"{result.executor_id}:\n{text}")
        print("\n======================================")

        combined_research = "\n\n".join(research_text)
        await ctx.send_message(combined_research)
       


async def main():
    client = OllamaChatClient(model="llama3.1:latest")
    
    postgres_agent = Agent(
        client=client,
        name="PostgreSQLAgent",
        instructions=(
            "You are a PostgreSQL specialist. "
            "Analyze the question specifically from the PostgreSQL perspective. "
            "Provide concise technical facts, strengths, limitations, and relevant considerations."
        ),
    )
    
    mysql_agent = Agent(
        client=client,
        name="MySQLAgent",
        instructions=(
            "You are a MySQL specialist. "
            "Analyze the question specifically from the MySQL perspective. "
            "Provide concise technical facts, strengths, limitations, and relevant considerations."
        ),
    )
    
    architecture_agent = Agent(
        client=client,
        name="ArchitectureAgent",
        instructions=(
            "You are a software architecture specialist. "
            "Analyze the question from a system architecture perspective. "
            "Focus on scalability, reliability, operational concerns, and architectural trade-offs."
        ),
    )
    
    synthesis_agent = Agent(
        client=client,
        name="SynthesisAgent",
        instructions=(
            "You are a senior technical writer. "
            "You will receive research from multiple specialist agents. "
            "Synthesize their findings into one clear answer. "
            "Compare the relevant options and explain the trade-offs. "
            "Do not simply repeat the research."
        ),
    )
    
    aggregator = ResearchAggregator(id="research_aggregator")

    workflow = (
        WorkflowBuilder(start_executor=postgres_agent)
        .add_fan_out_edges(postgres_agent, [mysql_agent, architecture_agent])
        .add_fan_in_edges([postgres_agent, mysql_agent, architecture_agent], aggregator)
        .add_edge(aggregator, synthesis_agent)
        .build()
    )

    # events = await workflow.run("Compare Microsoft Agent Framework and Semantic Kernel for AI project.")
    events = await workflow.run("Compare PostgreSQL and MySQL for an enterprise application.")
    
    print("\n========== FINAL ANSWER ==========")
    for output in events.get_outputs():
        print(output)
        

if __name__ == "__main__":
    asyncio.run(main())
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama'
)


def ask_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model='llama3.1',
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].message.content or ""

print(ask_llm("What is the capital of Bihar?"))

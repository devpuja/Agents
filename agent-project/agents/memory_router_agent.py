from services.ollama_service import ask_llm

class MemoryRouterAgent:
    
    def should_recall(self, question: str) -> bool:
        prompt = f"""
                You are a memory routing assistant.

                Determine whether the question requires information
                from the user's previous conversations or previously stored preferences.

                Return ONLY:

                YES
                or
                NO

                Return YES when:
                - The question asks about something the user previously told us.
                - The question asks about the user's preferences.
                - The question asks about the user's personal information previously provided.
                - The question refers to something discussed earlier.
                - The question asks "what do I prefer", "what did I say", "what did we discuss", etc.

                Return NO when:
                - The question is asking for general knowledge.
                - The question is asking about a technical concept.
                - The question can be answered without knowing anything about the user's past conversations.
                - The question requires document research instead.

                Examples:

                Question: What is my name?
                Answer: YES

                Question: What database do I prefer?
                Answer: YES

                Question: What did we discuss about C#?
                Answer: YES

                Question: What is CAP Theorem?
                Answer: NO

                Question: Explain dependency injection.
                Answer: NO

                Question: What is polymorphism?
                Answer: NO

                Question:
                {question}

                Answer:
                """
            
        result = ask_llm(prompt)
        print("MEMORY ROUTER RAW RESPONSE:", repr(result))
        return "YES" in result.upper()
    
    
    def extract_memory_topic(self, question: str) -> str:
        prompt = f"""
            Extract ONLY the memory topic.

            Examples:

            Question: What is my name?
            Answer: name

            Question: What database do I prefer?
            Answer: database

            Question: Where do I work?
            Answer: work

            Question:
            {question}

            Answer:
            """
        
        result = ask_llm(prompt)
        print("MEMORY TOPIC RAW RESPONSE:", repr(result))
        return result.upper()
    

# print("\n===================================")
# print(MemoryRouterAgent().should_recall("What database do I prefer?"))
from services.ollama_service import ask_llm


class RouterAgent:

    def route(self, question: str) -> str:
        
        prompt = f"""
            You are a routing assistant.

            Return ONLY one word:

            CHAT
            RESEARCH
            TOOL

            Choose TOOL when:
            - The user asks for the current time.
            - The user asks for today's date or another date calculation.
            - The user asks to perform a calculation.
            - The user asks to perform a filesystem operation.

            Choose RESEARCH when:
            - The user asks about information that may exist in uploaded documents.
            - The user asks about a PDF, document, handbook, or knowledge base.
            - The user asks to explain a technical topic that may be covered by uploaded documents.
            - The user asks "according to the document", "according to the PDF", or similar.
            - The user asks to summarize or retrieve information from uploaded documents.

            Choose CHAT when:
            - The user is having a normal conversation.
            - The user says hello, hi, thanks, etc.
            - The user asks for casual conversation.
            - The user asks about their own preferences or previously provided information.
            - The user asks what they prefer, like, use, or have told us before.
            - The user asks about something from previous conversations.

            Important:
            Questions about the user's own preferences or previous conversations
            should be CHAT, even if they contain technical words.

            For example:
            "What database do I prefer?" → CHAT
            "What programming language do I prefer?" → CHAT
            "What did I tell you about my project?" → CHAT

            Document questions should be RESEARCH.

            For example:
            "What database does the document recommend?" → RESEARCH
            "Explain CAP Theorem from the PDF." → RESEARCH
            "What does the handbook say about databases?" → RESEARCH

            Question:
            {question}

            Answer:
            """

        decision = ask_llm(prompt).strip().upper()
        print("ROUTER RAW RESPONSE:", repr(decision))

        match decision:
            case "RESEARCH":
                return "RESEARCH"
            case "TOOL":
                return "TOOL"
            case _:
                return "CHAT"
    

# print("\n===================================")
# print(RouterAgent().route("What is CAP Theorem?"))
# print("\n++++++++++++++++++++++++++++++++++++++++++++++++++\n")
# print(RouterAgent().route("What database do I prefer?"))
# print("\n++++++++++++++++++++++++++++++++++++++++++++++++++\n")
# print(RouterAgent().route("What database does the document recommend?"))
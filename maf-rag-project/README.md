# MAF + RAG Multi-Agent Project

A hands-on **learning project with production considerations** exploring Retrieval-Augmented Generation (RAG), multi-agent workflows, reliability, observability, and evaluation using **Microsoft Agent Framework (MAF)**, Ollama, and ChromaDB.

The goal of this project is to understand how the individual components of an AI application work together rather than treating RAG or agents as isolated concepts.

---

## 🎯 Project Goal

This project was created as part of my learning journey with **Microsoft Agent Framework and RAG**.

The focus is on building an end-to-end RAG workflow and gradually adding capabilities that are important when moving from a basic AI prototype toward a more production-oriented application.

The project covers:

- RAG architecture
- Document ingestion
- Document chunking
- Embeddings
- Vector search
- ChromaDB
- Microsoft Agent Framework
- RAG Research Agent
- Multi-agent + RAG integration
- Structured output
- Error handling and retries
- Timeout handling
- Exponential backoff and jitter
- Observability and tracing
- Evaluation
- End-to-end workflow

> **Project status: Learning project with production considerations**

This is intentionally not positioned as a production-ready enterprise platform. The purpose is to understand the architecture and engineering considerations by implementing them hands-on.

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │    User Question    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   MAF RAG Workflow  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  RAG Research Agent │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Retrieval       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Embedding       │
                         │       Ollama        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      ChromaDB       │
                         │    Vector Store     │
                         └──────────┬──────────┘
                                    │
                                    │ Relevant Chunks
                                    ▼
                         ┌─────────────────────┐
                         │  Retrieved Context  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Ollama / LLM    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Structured RAG      │
                         │ Result              │
                         └─────────────────────┘
```

---

# 🔄 RAG Workflow

The RAG workflow can be understood in two main stages.

## 1. Document Ingestion

Source documents are loaded and prepared for retrieval.

```text
Documents
    ↓
Document Loader
    ↓
Chunking
    ↓
Embeddings
    ↓
ChromaDB
```

The project currently uses local documents as the knowledge source.

The document processing pipeline handles:

1. Loading documents
2. Splitting documents into chunks
3. Generating embeddings
4. Storing the embeddings and content in ChromaDB

---

## 2. Question and Retrieval

When a user asks a question, the retrieval pipeline searches the vector store for relevant information.

```text
User Question
      ↓
Embedding
      ↓
ChromaDB Search
      ↓
Relevant Chunks
      ↓
Retrieved Context
      ↓
RAG Research Agent
      ↓
Structured RAG Result
```

The retrieved context is then provided to the agent so that the response can be grounded in the retrieved information.

---

# 🤖 Microsoft Agent Framework

The project uses **Microsoft Agent Framework (MAF)** to implement the RAG Research Agent.

The agent receives:

- The user's question
- Retrieved context

The agent is instructed to use the retrieved information when generating the response.

Conceptually:

```text
                    User Question
                         │
                         ▼
                  ┌─────────────┐
                  │  Retriever  │
                  └──────┬──────┘
                         │
                         ▼
                  Relevant Context
                         │
                         ▼
              ┌────────────────────┐
              │ RAG Research Agent │
              │       (MAF)        │
              └─────────┬──────────┘
                        │
                        ▼
                 Structured Result
```

This helped me understand the relationship between **RAG and agents**:

- RAG provides relevant external knowledge.
- The agent uses that knowledge to produce the response.

---

# 📚 Core RAG Components

## Document Ingestion

Loads the source documents used by the RAG pipeline.

## Chunking

Splits documents into smaller pieces that can be embedded and retrieved independently.

## Embeddings

The project uses:

```text
nomic-embed-text
```

through Ollama to generate embeddings.

## Vector Store

ChromaDB is used to store:

- Embeddings
- Document chunks
- Associated metadata

## Retrieval

The retriever performs semantic search against ChromaDB and returns relevant chunks that can be passed to the RAG agent.

---

# 📦 Structured RAG Output

The project uses structured output rather than relying only on free-form text.

The RAG result contains:

```text
Answer
Sources
Retrieved Chunks
```

This provides additional visibility into the information used to generate the response.

It also makes the result easier for application code to consume.

---

# 🛡️ Reliability

After implementing the basic RAG workflow, reliability considerations were added.

The project includes:

### Error Handling

Handles failures that can occur during the RAG workflow.

### Retry Handling

Retry logic is included for retryable failures.

### Timeout Handling

Timeout handling prevents an operation from waiting indefinitely.

### Exponential Backoff

Retry delays increase between attempts.

```text
Attempt 1
   ↓
Failure
   ↓
Wait
   ↓
Attempt 2
   ↓
Failure
   ↓
Wait longer
   ↓
Attempt 3
```

### Jitter

A small amount of randomness is added to retry delays to avoid synchronized retry behaviour.

These patterns are included as learning exercises around reliability in AI applications.

---

# 🔍 Observability

The project includes basic observability and tracing.

The tracing captures information around RAG operations such as:

- Operation start
- Operation completion
- Execution duration
- Success/failure
- Exception information

Stage-level tracing provides visibility into different parts of the workflow.

This helps answer questions such as:

- Where did the request fail?
- Which stage took the most time?
- Did retrieval complete successfully?
- Did the agent execution fail?

---

# 🧪 Evaluation

The project includes evaluation tests covering several areas of the RAG workflow.

### Happy Path

Verifies that the basic workflow completes successfully.

### Retrieval

Verifies that relevant information can be retrieved.

### Structured Output

Verifies that the expected structured result is produced.

### Source Attribution

Verifies that the response includes the expected source information.

The evaluation is intentionally lightweight and focused on understanding the fundamentals of testing a RAG workflow.

---

# 🔄 End-to-End Production-Oriented Workflow

The project brings the different components together into an end-to-end workflow.

```text
User Question
      │
      ▼
RAG Retrieval
      │
      ▼
Relevant Context
      │
      ▼
MAF RAG Research Agent
      │
      ▼
Structured Output
      │
      ├───────────────┐
      ▼               ▼
Observability     Reliability
      │               │
      └───────┬───────┘
              ▼
          Evaluation
```

The intention is to understand how these concerns fit together rather than implementing them as completely separate examples.

---

# 📁 Project Structure

```text
maf-rag-project/
│
├── document_loader.py
│   └── Loads documents
│
├── chunker.py
│   └── Splits documents into chunks
│
├── embedding_service.py
│   └── Generates embeddings
│
├── vector_store.py
│   └── Stores embeddings in ChromaDB
│
├── retriever.py
│   └── Retrieves relevant chunks
│
├── rag_service.py
│   └── RAG retrieval/context service
│
├── rag_research_agent.py
│   └── MAF RAG Research Agent
│
├── rag_error_handling.py
│   └── Retry and timeout handling
│
├── rag_observability.py
│   └── Logging and tracing
│
├── evaluation_testing.py
│   └── RAG evaluation tests
│
├── production_workflow.py
│   └── End-to-end workflow
│
├── documents/
│   └── Sample knowledge documents
│
└── requirements.txt
```

---

# 🧰 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Microsoft Agent Framework | Agent implementation |
| Ollama | Local LLM and embedding execution |
| llama3.1 | Local LLM |
| nomic-embed-text | Embedding model |
| ChromaDB | Vector store |
| Pydantic | Structured output |

---

# 💻 Local Models

The project uses local models through Ollama:

```text
Ollama
├── llama3.1:latest
└── nomic-embed-text:latest
```

The models are installed locally and are not included in this repository.

---

# ⚙️ Prerequisites

Before running the project, make sure you have:

- Python installed
- Ollama installed and running
- Required Ollama models available locally

Pull the models:

```bash
ollama pull llama3.1
ollama pull nomic-embed-text
```

---

# 🚀 Getting Started

Clone the repository:

```bash
git clone https://github.com/devpuja/Agents.git
```

Navigate to the project:

```bash
cd Agents/maf-rag-project
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Make sure Ollama is running and the required models are available.

---

# ▶️ Running the Project

The project contains separate scripts for the different stages of the workflow.

### Vector Store

Use the vector store workflow to process the documents and populate ChromaDB.

```bash
python vector_store.py
```

### Application

Run the main application:

```bash
python app.py
```

### Evaluation

Run the evaluation tests:

```bash
python evaluation_testing.py
```

### End-to-End Workflow

Run the production-oriented workflow:

```bash
python production_workflow.py
```

---

# 📝 Example

### Question

```text
Which database supports ACID transactions?
```

### Answer

```text
PostgreSQL supports ACID transactions.
```

### Source

```text
postgresql.txt
```

The response also includes the retrieved context used by the RAG workflow.

---

# 📈 Learning Outcomes

This project helped me build practical understanding across several areas.

## RAG

- Document ingestion
- Chunking
- Embeddings
- Vector stores
- Semantic retrieval
- Retrieved context
- Source attribution

## Agent Development

- Microsoft Agent Framework
- MAF agents
- RAG + agent integration
- Multi-agent workflow concepts
- Structured agent output

## Reliability

- Error handling
- Retry strategies
- Timeout handling
- Exponential backoff
- Jitter

## Observability

- Basic tracing
- Stage-level tracing
- Execution timing
- Failure visibility

## Evaluation

- Happy-path testing
- Retrieval testing
- Structured-output testing
- Source attribution testing

---

# 🧠 Key Takeaways

The biggest learning from this project was that a RAG application is much more than:

```text
Documents → Vector Database → LLM
```

There are several layers involved:

```text
                ┌─────────────────┐
                │   Application   │
                └────────┬────────┘
                         │
                ┌────────▼────────┐
                │      Agent      │
                └────────┬────────┘
                         │
                ┌────────▼────────┐
                │      RAG        │
                └────────┬────────┘
                         │
                ┌────────▼────────┐
                │ Vector Retrieval│
                └────────┬────────┘
                         │
                ┌────────▼────────┐
                │   Knowledge     │
                └─────────────────┘
```

And around that core workflow, production-oriented applications also need:

```text
Reliability
Observability
Evaluation
```

This project helped me connect these concepts into one working system.

---

# 🔮 Possible Next Steps

Areas I plan to explore as I continue learning include:

- Improved chunking strategies
- Retrieval quality evaluation
- Metadata filtering
- Reranking
- More advanced agent workflows
- Improved observability
- Guardrails
- LLMOps
- Azure-based deployment
- Production AI architecture
- Advanced multi-agent systems

---

# 📌 Project Status

### Learning Project with Production Considerations

This project is intentionally evolving as I learn more about:

- Microsoft Agent Framework
- RAG
- Agent architecture
- AI application reliability
- Observability
- Evaluation
- Production AI architecture

The objective is to continuously improve the implementation while strengthening my understanding of how these components work together.

---

# 🔗 Repository

GitHub:

https://github.com/devpuja/Agents/tree/main/maf-rag-project

---

## 👨‍💻 Learning Journey

This project is part of my broader journey from software development toward **AI Engineering and AI Architecture**, with a focus on the Microsoft AI ecosystem.

The main objective is not just to learn individual technologies, but to understand how they can be combined to design and build complete AI systems.

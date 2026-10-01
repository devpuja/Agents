PHASE 3 — MAF + RAG

Core RAG
    Basic MAF + Ollama agent              ✅
    RAG architecture                      ✅
    Document ingestion                    ✅
    Chunking                              ✅
    Embeddings                            ✅
    Vector store                          ✅
    Retrieval                             ✅

Multi-Agent
    RAG Research Agent                    ✅
    Multi-agent + RAG                     ✅
    Structured RAG output                 ✅

Reliability
    Error handling / retries              ✅
    Timeout handling                      ✅
    Exponential backoff + jitter          ✅

Observability
    Basic tracing                         ✅
    Stage-level tracing                   ✅

Evaluation
    Happy path                            ✅
    Retrieval                             ✅
    Structured output                     ✅
    Source attribution                     ✅

Production Workflow
    End-to-end workflow                   ✅



# MAF + RAG Multi-Agent Project

A hands-on learning project demonstrating Retrieval-Augmented Generation
(RAG) and multi-agent workflows using Microsoft Agent Framework (MAF),
Ollama, ChromaDB, and local embedding models.

## Architecture

User Question
    ↓
MAF RAG Workflow
    ↓
RAG Research Agent
    ↓
Retrieval
    ↓
Embedding
    ↓
ChromaDB
    ↓
Retrieved Context
    ↓
Ollama / LLM
    ↓
Structured RAG Result

## Features

- Document ingestion
- Text chunking
- Embeddings using nomic-embed-text
- ChromaDB vector store
- Semantic retrieval
- RAG Research Agent
- Structured RAG output
- Retry handling
- Timeout handling
- Exponential backoff with jitter
- Observability and tracing
- Stage-level tracing
- Evaluation tests
- End-to-end RAG workflow

## Project Structure

- `document_loader.py` - Loads documents
- `chunker.py` - Splits documents into chunks
- `embedding_service.py` - Generates embeddings
- `vector_store.py` - Stores embeddings in ChromaDB
- `retriever.py` - Retrieves relevant chunks
- `rag_service.py` - RAG retrieval/context service
- `rag_research_agent.py` - MAF RAG research agent
- `rag_error_handling.py` - Retry and timeout handling
- `rag_observability.py` - Logging and tracing
- `evaluation_testing.py` - RAG evaluation tests
- `production_workflow.py` - End-to-end workflow

## Local Models

This project uses:

- Ollama
- `llama3.1:latest`
- `nomic-embed-text:latest`

The models are installed locally and are not included in this repository.

## Example

Question:

> Which database supports ACID transactions?

Answer:

> PostgreSQL supports ACID transactions.

Source:

> `postgresql.txt`

## Learning Outcomes

This project demonstrates practical understanding of:

- MAF agents
- RAG architecture
- Vector search
- Embeddings
- Multi-agent integration
- Structured outputs
- Error handling
- Retry strategies
- Timeout handling
- Observability
- Evaluation/testing
PHASE 2 — MAF CORE
════════════════════════════════════════════

Workflows
    Basic workflow                    ✅
    Sequential execution              ✅
    Parallel execution                ✅
    Fan-out                           ✅
    Fan-in                            ✅

Architecture
    Manual workflow graph             ✅
    Manual vs orchestration           ✅
    ConcurrentBuilder                 ✅

Multi-Agent
    Multiple agents                   ✅
    Parallel multi-agent workflow     ✅
    Agent-as-tool                     ✅
    Agent delegation                  ✅
    Structured outputs                ✅

Remaining
    Error handling / retries          🔲 ← NEXT
    Observability / tracing           🔲
    Guardrails / security             🔲
    Evaluation / testing              🔲


================Error handling / Retries===============

1. Simulate failure             ← NOW
        ↓
2. Observe exception propagation
        ↓
3. Add try/except
        ↓
4. Add retry
        ↓
5. Add maximum retry count
        ↓
6. Add timeout
        ↓
7. Handle partial specialist failure
        ↓
8. Add graceful fallback
        ↓
9. Test failure scenarios
        ↓
10. Mark Error Handling & Retries ✅
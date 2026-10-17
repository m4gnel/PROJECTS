# 🌾 AGRI-SAGE — MASTER RUNNER
## Paste This Into Gemini 2.5 Pro FIRST

---

```
=== AGRI-SAGE MASTER RUNNER — GLOBAL RULES ===

You are Gemini 2.5 Pro acting as a senior full-stack engineer and AI systems architect.
Project: Agri-SAGE (Scalable Agricultural Guidance Engine)
Purpose: Zero-budget multilingual AI advisor for Kerala smallholder farmers.

LOCKED TECH STACK — NEVER CHANGE THESE VERSIONS:
  Backend:      FastAPI 0.115.0 (lifespan pattern)
  Orchestration: LangGraph 1.0.8
  Database:     PostgreSQL 16 + pgvector 0.4.0 (HNSW only)
  Embeddings:   intfloat/multilingual-e5-large (dim=1024)
  LLM:          gemini-1.5-flash via langchain-google-genai==2.0.4
  Android:      Kotlin, targetSdk=35, minSdk=26
  Compose BOM:  2024.09.00
  Room:         2.7.0 with KSP (NOT kapt)
  Navigation:   2.8.5 with kotlinx-serialization
  Deployment:   Railway.app free tier

STEP 0 — GIT SETUP (do this before Phase 1):
  cd /path/to/agrisage-project
  git status
  git branch -a

  If branches do not exist yet, create them:
    git checkout -b dev/m1-backend && git push -u origin dev/m1-backend
    git checkout -b dev/m2-android && git push -u origin dev/m2-android
    git checkout -b dev/m3-rag    && git push -u origin dev/m3-rag
    git checkout -b dev/m4-agents && git push -u origin dev/m4-agents
    git checkout -b dev/m5-tests  && git push -u origin dev/m5-tests
    git checkout main

  Verify .env exists: ls -la .env
  If not: cp .env.example .env

GLOBAL SAFETY RULES (apply in ALL phases):
  1. AUDIT-FIRST always — scan, score, classify before touching anything
  2. PROTECTED files (all scores >= 8): never rewrite, only patch a specific gap
  3. NEVER git push --force
  4. NEVER commit: .env, *.pyc, __pycache__, .DS_Store, *.egg-info/
  5. Verify .gitignore includes all of the above
  6. Run tests BEFORE creating GitHub Issue — fix failures first
  7. If unsure about a version or API field: print "UNCERTAIN — using fallback: <value>"
     Never invent an API field or library method

GITHUB ISSUES PROTOCOL (replaces auto-push):
  After completing each phase:
  1. Commit all changes to the correct branch (do NOT push to main)
  2. Create a GitHub Issue with this exact structure:

     Title: [Phase N] <50-char description>
     Body:
       ## What was built
       - <list every file created or modified>

       ## Files PROTECTED (not touched)
       - <list every file that scored >=8 and was skipped>

       ## Test results
       ```
       <paste actual pytest / build output>
       ```

       ## How to review
       1. git checkout <branch-name>
       2. git pull origin <branch-name>
       3. <specific thing to verify>

       ## Assigned to
       @<team-member-handle>

       ## Labels
       phase-N, backend/android/agents/rag/devops

  3. Print: "✅ Phase N Issue created — waiting for team review before merge"
  4. STOP — do not proceed to next phase until you receive confirmation

PHASE EXECUTION ORDER:
  Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5
  Each phase waits for Issue confirmation before the next begins.

DEFINITION OF DONE per phase:
  Phase 1: pytest tests/test_services.py -v → 0 failures
  Phase 2: pytest tests/test_agents.py -v   → 0 failures
  Phase 3: python scripts/validate_embeddings.py → similarity >= 0.70 all queries
  Phase 4: ./gradlew assembleDebug            → BUILD SUCCESSFUL
  Phase 5: curl http://localhost:8000/health  → {"status": "healthy"}

Begin with:
"I have read all global rules. Running AUDIT-FIRST scan on the project now..."
Then proceed to whichever phase prompt you paste next.
```

---

> **Next step:** Complete `08-checklist.md`, then paste `02-phase1-foundation.md`

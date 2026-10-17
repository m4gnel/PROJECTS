# AGRI-SAGE BUILD FAILURE — ROOT CAUSE DIAGNOSIS & FIX PLAN

## Why the AI Agent Produced a "Framework/Junk" Output

### The Core Problem
You gave the AI agent PLANNING documents (PRD, Architecture, Data Model, API Contract).
Planning documents tell an AI agent WHAT to build — not HOW to build it line by line.

When an AI agent reads a planning doc and has to fill in ANY gap, it invents patterns.
It invented its own folder structure, its own function names, its own agent classes.
Result: a generic FastAPI + LangGraph scaffold that looks nothing like Agri-SAGE.

### What Was Missing: The Implementation Contracts Layer
The existing brain/ files covered LAYER 1 (planning).
You needed LAYER 2 (implementation contracts) — files so precise that the AI has
zero room to invent ANYTHING.

| What you had | What was missing |
|---|---|
| 01_PRD.md — WHAT features | 05_FOLDER_STRUCTURE.md — EVERY file path |
| 02_ARCHITECTURE.md — WHAT components | 06_PINNED_DEPENDENCIES.md — EXACT versions |
| 03_DATA_MODEL.md — WHAT data | 07_AGENT_CONTRACTS.md — EXACT function signatures |
| 04_API_CONTRACT.md — WHAT endpoints | 08_ANDROID_CONTRACTS.md — EXACT Compose signatures |
|  | 09_DATABASE_SCHEMA.md — EXACT SQL |
|  | 10_API_RESPONSE_SHAPES.md — EXACT JSON |

### Why There Were Duplicate/Confusing Files
The AI agent, lacking a file structure reference, invented its own layout.
It created multiple files for the same purpose with different names.
Rule for an AI agent: if it doesn't know the exact file name, it makes one up.

## What You Must Do Now

### Step 1 — Wipe the Junk
```bash
# Save any accidentally-good code first, then:
git checkout main
git branch -D dev/m1-backend  # or your working branch
git checkout -b dev/m1-backend
```

### Step 2 — Add the Missing Brain Files
Copy ALL 9 files from this package into your project's brain/ folder:
- 00_MASTER_RULES_V2.md  → replace brain/00_MASTER_RULES.md
- 05_FOLDER_STRUCTURE.md → brain/05_FOLDER_STRUCTURE.md  (NEW)
- 06_PINNED_DEPENDENCIES.md → brain/06_PINNED_DEPENDENCIES.md (NEW)
- 07_AGENT_CONTRACTS.md → brain/07_AGENT_CONTRACTS.md (NEW)
- 08_ANDROID_CONTRACTS.md → brain/08_ANDROID_CONTRACTS.md (NEW)
- 09_DATABASE_SCHEMA.md → brain/09_DATABASE_SCHEMA.md (NEW)
- 10_API_RESPONSE_SHAPES.md → brain/10_API_RESPONSE_SHAPES.md (NEW)

### Step 3 — Use PHASE_PROMPTS_V2.md
Throw away the old phase prompts. Use PHASE_PROMPTS_V2.md instead.
The new prompts start EVERY prompt with "Read brain/0*.md files first."
The new prompts include EXACT file lists the agent must produce.
The new prompts include VALIDATION CHECKLISTS — the agent cannot proceed without them passing.

### Step 4 — Give the Agent This Exact Instruction at Start of Every Session
```
Before writing any code:
1. Run: cat brain/00_MASTER_RULES.md
2. Run: cat brain/05_FOLDER_STRUCTURE.md
3. Run: git status
4. Only create files listed in brain/05_FOLDER_STRUCTURE.md
5. Only use versions from brain/06_PINNED_DEPENDENCIES.md
```

## Summary
Your planning documents were correct and complete.
The AI agent failure was not your fault — it was a missing implementation layer.
These 8 new files close every gap the agent was filling with hallucinations.

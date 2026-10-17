# 🔍 AUDIT-FIRST PROTOCOL
## Reference — This Logic Is Embedded in Every Phase Prompt

---

> This file explains what Gemini does to your existing files **before touching anything**.
> You don't paste this separately — it's already inside every phase prompt.

---

## What the Audit Does

```
=== AUDIT-FIRST PROTOCOL ===

STEP A — SCAN the entire project directory:
  find . -type f \
    | grep -v __pycache__ \
    | grep -v .git \
    | grep -v node_modules \
    | grep -v .gradle \
    | sort

STEP B — For every existing file, score it on 3 axes (each 0–10):

  COMPLETENESS (0–10):
    10 = every function fully implemented, no TODO, no pass, no ...
    5  = partial implementation, some stubs remain
    0  = empty or skeleton only

  CORRECTNESS (0–10):
    10 = uses locked versions exactly, logic is sound, no deprecated calls
    5  = mostly correct but uses wrong version or has a logic gap
    0  = wrong imports, wrong version, broken logic

  PRODUCTION_READY (0–10):
    10 = error handling on every external call, logging, type hints, no hardcoded secrets
    5  = partial error handling, missing some type hints
    0  = bare minimum, no error handling

STEP C — Classify every file:

  PROTECTED  → ALL THREE scores >= 8
               Action: DO NOT TOUCH this file unless patching one specific named gap.
               Never rewrite. Never restructure.

  NEEDS_WORK → ANY score < 8
               Action: Fix exactly what is missing. List what was missing in the Issue.

  MISSING    → File does not exist yet
               Action: Create it from scratch.

STEP D — Print the FILE AUDIT TABLE before doing anything:

  File                          | Complete | Correct | Prod-Ready | Status
  ------------------------------|----------|---------|------------|------------
  app/main.py                   |   9      |   9     |    8       | PROTECTED
  app/services/weather_service  |   6      |   9     |    5       | NEEDS_WORK
  app/agents/state.py           |   —      |   —     |    —       | MISSING
  ...

STEP E — Confirm:
  "Audit complete. X files PROTECTED, Y files NEEDS_WORK, Z files MISSING.
   Proceeding to build only NEEDS_WORK and MISSING files."
```

---

## Scoring Guide for Gemini

### COMPLETENESS
| Score | Meaning |
|---|---|
| 10 | Every function has a full body, no `pass`, no `TODO`, no `...` |
| 7–9 | Mostly complete, 1–2 minor stubs |
| 4–6 | Core logic present but 30–50% is stubs |
| 1–3 | Skeleton only |
| 0 | Empty file |

### CORRECTNESS
| Score | Meaning |
|---|---|
| 10 | Uses exact pinned versions, correct imports, sound logic |
| 7–9 | Correct but one minor version mismatch or import path off |
| 4–6 | Uses deprecated API or wrong LangGraph/Room import |
| 1–3 | Multiple wrong versions or broken logic |
| 0 | Completely wrong approach |

### PRODUCTION_READY
| Score | Meaning |
|---|---|
| 10 | `try/except` on every external call, structured logging, full type hints, secrets from env |
| 7–9 | Missing 1–2 error handlers or type hints |
| 4–6 | No logging, partial error handling |
| 1–3 | Bare code, no error handling |
| 0 | Hardcoded secrets or crashes on first error |

---

## What PROTECTED Means Exactly

If a file is PROTECTED:

- ✅ Gemini may **read** it to understand context
- ✅ Gemini may **append** a clearly missing piece (e.g., one missing route)
- ✅ Gemini may **fix one specific named bug**
- ❌ Gemini must NOT rewrite the whole file
- ❌ Gemini must NOT restructure or rename things
- ❌ Gemini must NOT change what already works

---

## Common Files That Are Often Already Done

These are files teams often partially or fully build manually. Gemini will check each:

| File | What to look for |
|---|---|
| `brain/00_MASTER_RULES.md` | All 7 locked versions present? |
| `app/main.py` | Lifespan pattern? CORS? Router registration? |
| `app/config.py` | Pydantic BaseSettings? All env vars? |
| `requirements.txt` | All pinned versions match locked stack? |
| `.gitignore` | `.env`, `__pycache__/`, `*.pyc` present? |
| `android/app/build.gradle.kts` | KSP plugin? Correct BOM? Room 2.7.0? |

---

> This protocol ensures your existing work is **never made worse**.

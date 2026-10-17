# 🐙 GitHub Issues — Contribution & Review Workflow
## How Issues Replace Auto-Push for Team Collaboration

---

## Why Issues Instead of Direct Push

Each phase prompt tells Gemini to **commit to a branch and create a GitHub Issue** — not push directly to main. This means:

- You see **exactly what changed** before it merges
- You can **assign work** to the right team member
- Every contribution is **tracked and attributed**
- The `main` branch stays **always working**

---

## The Flow — Phase by Phase

```
Gemini builds Phase N
        ↓
Commits to dev/mX-branch
        ↓
Creates GitHub Issue #N
        ↓
You review Issue → assign to team member
        ↓
Team member reviews code on their branch
        ↓
Opens Pull Request: dev/mX-branch → main
        ↓
You approve PR → merge
        ↓
GitHub Actions CI runs automatically
        ↓
Railway deploys (Phase 5 only, on main push)
        ↓
Paste next phase prompt into Gemini
```

---

## Issue Template (Gemini Creates This Automatically)

Every phase prompt instructs Gemini to create an issue with this exact structure:

```markdown
## What was built
- app/services/weather_service.py — created from scratch
- app/services/market_service.py — created from scratch
- brain/kerala_soil_data.json — created, all 14 districts
- tests/test_services.py — 6 tests, all passing

## Files PROTECTED (not touched)
- app/main.py — scored 9/9/8 — already complete
- brain/00_MASTER_RULES.md — scored 10/9/9 — already complete

## Test results
```
tests/test_services.py::test_weather_service_returns_context PASSED
tests/test_services.py::test_weather_service_uses_cache PASSED
tests/test_services.py::test_market_service_upserts_prices PASSED
tests/test_services.py::test_pest_service_parses_rss PASSED
tests/test_services.py::test_soil_service_ernakulam PASSED
tests/test_services.py::test_soil_service_unknown_district PASSED
6 passed in 1.23s
```

## How to review
1. git checkout dev/m1-backend
2. git pull origin dev/m1-backend
3. pytest tests/test_services.py -v
4. Check app/services/weather_service.py — verify cache logic

## Assigned to
@M1

## Labels
phase-1, backend
```

---

## Labels to Create in Your GitHub Repo

Go to **Issues → Labels → New label** and create these:

| Label | Color | Purpose |
|---|---|---|
| `phase-1` | `#14532d` | Foundation + data pipeline |
| `phase-2` | `#166534` | Agent orchestration |
| `phase-3` | `#15803d` | RAG pipeline |
| `phase-4` | `#16a34a` | Android app |
| `phase-5` | `#22c55e` | Deploy + CI/CD |
| `backend` | `#1e293b` | FastAPI / Python work |
| `agents` | `#7c3aed` | LangGraph / AI work |
| `rag` | `#2563eb` | Embeddings / pgvector |
| `android` | `#0e7490` | Kotlin / Compose |
| `devops` | `#d97706` | CI/CD / deployment |
| `protected` | `#64748b` | File was not touched |
| `needs-review` | `#dc2626` | Waiting for approval |

---

## Branch Protection Rules (Set These Once)

Go to **Settings → Branches → Add rule** for `main`:

```
Branch name pattern: main

☑ Require a pull request before merging
  ☑ Require approvals: 1
☑ Require status checks to pass before merging
  ☑ Status checks: test (from backend-ci.yml)
☑ Do not allow bypassing the above settings
```

This ensures nothing reaches `main` without passing CI and getting one approval.

---

## Team Assignment Map

| Phase | Issue Title | Assign To | Review Branch |
|---|---|---|---|
| Phase 1 | Foundation + Data Pipeline | M1 | `dev/m1-backend` |
| Phase 2 | 14-Agent Orchestration | M4 | `dev/m4-agents` |
| Phase 3 | KAU RAG Pipeline | M3 | `dev/m3-rag` |
| Phase 4 | Android App | M2 | `dev/m2-android` |
| Phase 5 | Deploy + CI/CD | M1 + M5 | `main` |

---

## PR Template (Save as `.github/pull_request_template.md`)

Create this file in your repo so every PR follows the same format:

```markdown
## Phase
<!-- Which phase does this PR belong to? e.g. Phase 1 -->

## Related Issue
Closes #<!-- issue number -->

## What changed
<!-- List files created or modified -->

## What was NOT touched (PROTECTED files)
<!-- List files Gemini skipped due to high audit score -->

## Test evidence
<!-- Paste test output here -->
pytest tests/ -v
```
output here
```

## Self-review checklist
- [ ] Tests pass locally
- [ ] No .env or secrets committed
- [ ] No hardcoded API keys or URLs
- [ ] requirements.txt versions match locked stack
- [ ] No kapt — only KSP (Android)
```

---

## Creating Issues Manually (If Gemini Doesn't)

If Gemini skips the issue creation step, create it manually:

**GitHub CLI (recommended):**
```bash
gh issue create \
  --title "[Phase 1] Foundation + Realtime Data Pipeline" \
  --label "phase-1,backend" \
  --assignee M1_github_username \
  --body "$(cat .github/issue-templates/phase1.md)"
```

**Web UI:**
1. Go to repo → Issues → New Issue
2. Fill Title, Labels, Assignee
3. Paste the body template above

---

## Notification Setup (Optional but Recommended)

To get notified when Gemini creates an issue:
1. Go to repo → **Watch → Custom**
2. Enable: **Issues**
3. You'll get email when each phase issue is created

---

> Issues keep your team in sync. You control what merges. Gemini builds. You decide.

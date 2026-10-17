# AGRI-SAGE — TEAM ROLES

## 5 Members — Parallel Work
M1 Lead/Backend dev/m1-backend: DB, auth, farm CRUD, API, deploy
M2 AI Agents dev/m2-agents: 14 agents, LangGraph, LLM, RAG
M3 Android dev/m3-android: all screens, camera, offline, sync
M4 Data dev/m4-data: JSON files, vision model, knowledge ingestion
M5 QA/DevOps dev/m5-tests: tests, CI/CD, security, deployment

## Daily Git Workflow
Morning: git checkout main && git pull && git checkout dev/YOUR-BRANCH && git merge main
After each task: git add -A && git commit -m "M[N]: description" && git push origin dev/YOUR-BRANCH
PR: GitHub → Compare & pull request → Tag M1 → WhatsApp "PR ready"
M1 merges: checkout branch, pytest tests/ -v, merge if green

## Dependency Order
M1 DB+Auth done → M2,M3,M4,M5 can proceed
M4 JSON files done (Day 3) → M2 can implement agents
M2 agents done → M1 can complete /diagnose
M1+M2 backend done → M3 connects Android to real API

## Cline Usage (Free Gemini API)
1. Click Cline robot icon in VSCode sidebar
2. Type @brain/00_MASTER_RULES.md @brain/[relevant].md
3. Paste prompt from 12_MICROTASKS.md EXACTLY
4. Review every line Cline writes
5. Run/test to verify, then commit

## Free Tool Limits Handling
Gemini limit hit → switch to Claude.ai free for that day
Claude limit hit → switch back to Gemini via Cline
Both limits → continue tomorrow (resets daily)

## October 1st — 22 Days
Days 1-3: Setup all environments, repo, JSON data files
Days 4-7: Backend /health live, Android project + design system, vision model training starts
Days 8-11: Auth, farm CRUD, camera screen, vision ONNX on Android
Days 12-15: All 6 MVP agents, full /diagnose, advisory screen
Days 16-18: Home screen, offline mode, Malayalam review, sync
Days 19-20: Android ↔ backend integration, end-to-end on real phone
Days 21-22: Demo practice, bug fixes, backup plan ready

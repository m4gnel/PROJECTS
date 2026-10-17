# AGRI-SAGE — 14 AGENTS

## Pipeline (LangGraph 1.0.8)
START→intake→[vision,weather,crop_stage,knowledge]PARALLEL→critic BARRIER
→scheme(always)+simulation(conditional)→decision→explanation→END

## LLM Usage
NO LLM: intake, vision, weather, crop_stage, knowledge, critic, soil, decision, simulation, market, economics
YES LLM: explanation(temp=0.2), scheme(temp=0.1,conditional), monitoring/briefing(temp=0.3)

## Agent 1: Intake
Merge observation+farm profile. Compute days_after_sowing=(today-planting_date).days
Normalize crop to: rice/banana/coconut/tomato/maize. Flag null fields in state.warnings.

## Agent 2: Vision
Singleton ONNX session. Load 22 classes from backend/data/disease_classes.json
Quality check: blur Laplacian<100 OR brightness mean<40or>220 OR crop<30% → INSUFFICIENT_DATA
Run inference→softmax→top-5. Return VisionResult.

## Agent 3: Weather
Call Open-Meteo (dev). Cache 30min by (round(lat,2),round(lon,2))
DFI = ((humidity>80)*0.4 + (20<=temp<=30)*0.3 + (wet_days/7)*0.3) clamped 0-1
Spray window: rain_prob<20% AND wind<15kmh for any 4hr block today

## Agent 4: Crop Stage
Load backend/data/gdd_thresholds.json
GDD daily = max(0, ((tmax+tmin)/2) - base_temp[crop])
base_temps: rice=10 maize=10 tomato=10 banana=15 coconut=20
Match cumulative GDD to stage threshold → return stage + vulnerability

## Agent 5: Knowledge (RAG)
Dense: pgvector cosine — ALWAYS prefix 'query: ', normalize_embeddings=True
Sparse: PostgreSQL to_tsvector FTS
Merge: RRF k=60. Rerank: cross-encoder/ms-marco-MiniLM-L-6-v2
Boost: Tier 1 sources × 1.3
Filter: valid_until>TODAY AND status='PUBLISHED'

## Agent 6: Critic (Safety Gate — NO LLM)
Confidence states:
vision>0.80 + weather supports + stage matches + Tier1 knowledge → CONFIRMED
vision 0.60-0.80 + most evidence → LIKELY
vision 0.40-0.60 OR minor conflict → POSSIBLE
vision<0.40 OR multiple conflicts → UNCERTAIN
OOD OR critical data missing → INSUFFICIENT_DATA
Vision says X + weather strongly contradicts X → CONFLICTING_EVIDENCE
Crop not supported → OUT_OF_SCOPE

Safety Blocks (BLOCK = hold advisory):
1. Product not in CIB&RC database
2. Product not registered for stated crop
3. Dosage outside label range
4. Scheme valid_until passed
5. LLM output product name not in knowledge chunks

run_simulation=True only if: confidence>0.65 AND conflicts=[] AND state in [CONFIRMED,LIKELY]

## Agent 7: Scheme (LLM temp=0.1)
System prompt: VERBATIM from 06_LLM_PROMPTS.md Prompt 2
Mandatory caveat always: "Final eligibility determined by the concerned authority."

## Agent 9: Decision (NO LLM)
score = yield_score + profit_score - risk_penalty(critical=-3,high=-2,medium=-1,low=0)
        - uncertainty_penalty((1-confidence)*2)
Flag BUDGET_EXCEEDED if over farmer_budget_inr

## Agent 10: Explanation (LLM temp=0.2 max_tokens=1500)
System prompt: VERBATIM from 06_LLM_PROMPTS.md Prompt 1
If UNCERTAIN/INSUFFICIENT_DATA/CONFLICTING_EVIDENCE → no treatment, request more info
Check for invented product names. Use SAFE_FALLBACK if LLM returns None.

## Agent 14: Monitoring (LLM temp=0.3)
Runs daily 05:30 UTC via APScheduler
System prompt: VERBATIM from 06_LLM_PROMPTS.md Prompt 4
Store in notifications table type=morning_briefing. Send FCM.

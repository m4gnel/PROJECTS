# AGRI-SAGE — ARCHITECTURE DECISIONS LOG

## These decisions are FINAL. Do not change without Team Lead approval.

| ID | Decision | Reason | Alternative Rejected |
|----|----------|--------|---------------------|
| D-001 | DSSAT (BSD-3-Clause) as primary simulation backend | Commercially free. APSIM requires paid license for revenue use. | APSIM Next Gen — commercial license required |
| D-002 | Open-Meteo for development weather | Free, non-commercial, 1500 req/day. Switch to IMD before monetization. | IMD commercial API — cost during dev |
| D-003 | pgvector HNSW index (not IVFFlat) | pgvector 0.4.0 — HNSW faster and more accurate for our dataset size | IVFFlat — requires lists tuning, slower |
| D-004 | Gemini API primary LLM (Ollama fallback) | Free API, 1M token context, no local GPU needed for team. | OpenAI — paid. Ollama needs good hardware. |
| D-005 | multilingual-e5-large for embeddings | MIT license, 1024-dim, best multilingual quality free model | OpenAI embeddings — paid. Others lower quality. |
| D-006 | KSP over kapt for Android Room | Room 2.7.0 requires KSP. 2x faster builds. kapt deprecated. | kapt — deprecated, slower |
| D-007 | Type-safe Navigation Compose 2.8.5 | Compile-time route safety, no string typos, Kotlin Serialization | String-based routes — runtime errors |
| D-008 | LangGraph 1.0.8 with MemorySaver | Latest stable, built-in checkpointing, proper START/END constants | LangGraph 0.2.x — old API, no MemorySaver |
| D-009 | Cloudflare R2 for image storage | Free 10GB, zero egress fees, integrated CDN | AWS S3 — egress costs. Firebase Storage — quota limits. |
| D-010 | Oracle Always-Free for hosting | 24GB RAM, 2 AMD instances, permanently free | Railway/Render — free tiers expire or suspend |
| D-011 | HNSW m=16, ef_construction=64 | Good quality/speed balance for our expected <100K chunk dataset | Higher values — better quality but slower build |
| D-012 | Farmer-level train/val/test split for vision model | Prevents data leakage from same-farmer near-duplicate images | Random split — inflates accuracy metrics |
| D-013 | Temperature scaling post-training calibration | Calibrated confidence (ECE<0.12) is safer for farmers than raw logits | No calibration — overconfident predictions |
| D-014 | 7 confidence states (not a percentage alone) | Farmer-actionable states vs abstract number. Critic assigns based on evidence. | Raw probability — not actionable for farmers |
| D-015 | Mandatory caveat on all scheme eligibility | Legal safety — Agri-SAGE cannot determine actual government eligibility | Definitive eligibility — legal risk |
| D-016 | FastAPI lifespan context manager | FastAPI 0.115.0 removed on_startup/on_shutdown. Lifespan is the standard. | on_startup — deprecated and removed |
| D-017 | Pydantic v2 model_config (not class Config) | pydantic-settings 2.7.0 uses model_config. class Config is v1 pattern. | class Config — Pydantic v1 pattern, deprecated |
| D-018 | ONNX Runtime for on-device inference | Cross-platform, NNAPI acceleration, INT8 quantization, MIT license | TFLite — TensorFlow dependency, larger APK |
| D-019 | EncryptedSharedPreferences for JWT on Android | Security requirement — never store JWT in plain SharedPreferences | Plain SharedPreferences — insecure |
| D-020 | Modelled estimate label on ALL simulation output | Farmer safety — simulation is not a guarantee. Field conditions vary. | No label — misleads farmers into treating as fact |

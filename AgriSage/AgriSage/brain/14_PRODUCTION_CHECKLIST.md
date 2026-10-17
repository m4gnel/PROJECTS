# AGRI-SAGE — PRODUCTION CHECKLIST

## Pre-Launch: ALL must pass before any public announcement

### Backend
- [ ] All 17 migrations run clean on fresh database
- [ ] `curl /health` returns `{db_connected: true}`
- [ ] RLS verified: User B gets 404 on User A's farm
- [ ] Rate limiting verified: 6th OTP request returns 429
- [ ] `pip-audit` shows zero CRITICAL CVEs
- [ ] `bandit -lll` shows zero HIGH severity issues
- [ ] No `.env` file in git history
- [ ] Advisory P95 < 8 seconds under 50 concurrent users (locust)
- [ ] All knowledge documents have valid `valid_until` dates
- [ ] Zero expired schemes in PUBLISHED status
- [ ] `scripts/smoke_tests.py` all 3 checks PASS

### AI & Model
- [ ] Vision model Macro-F1 ≥ 0.82 on **field** test set (not PlantVillage lab)
- [ ] Vision model ECE ≤ 0.12 after temperature scaling
- [ ] ONNX INT8 accuracy loss < 2% vs FP32
- [ ] 100 random advisories reviewed by 2 agronomists — zero unsafe recommendations
- [ ] All 5 Critic safety tests pass
- [ ] LLM outputs validated: zero invented product names in 50 test advisories
- [ ] RAG retrieval recall@5 > 0.80 on 20-query benchmark
- [ ] Explanation agent system prompt copied verbatim from `06_LLM_PROMPTS.md`

### Android
- [ ] All Malayalam strings reviewed by native Malayalam speaker
- [ ] No English text visible on Malayalam locale
- [ ] App works in airplane mode — offline advisory generated
- [ ] Camera quality indicator rejects blurry images with correct messages
- [ ] Voice input works in Malayalam (at least Android STT fallback)
- [ ] SyncWorker uploads offline observations on reconnect
- [ ] ProGuard/R8 obfuscation enabled in release build
- [ ] Privacy policy URL accessible at `https://yourdomain.in/privacy`
- [ ] App installs and runs on Tier 3 device (2GB RAM, Android 8)
- [ ] All touch targets ≥ 48dp

### Human Tasks (not automatable)
- [ ] Bhashini API approved (applied Day 1 — bhashini.gov.in)
- [ ] Firebase `google-services.json` added to Android project
- [ ] Cloudflare R2 credentials in `.env`
- [ ] Oracle Always-Free server provisioned and SSH accessible
- [ ] DSSAT registered and binary installed at `DSSAT_BIN_PATH`
- [ ] KAU contacted for field image collection partnership
- [ ] CIB&RC pesticide label data seeded into `chemical_labels` table
- [ ] PMFBY + PM-KISAN + 3 Kerala schemes seeded into `schemes` table
- [ ] Play Store developer account created ($25 one-time)
- [ ] Privacy policy page published

### October 1st Demo Specific
- [ ] Test phone charged, app installed
- [ ] Backend live on Oracle server
- [ ] At least 1 test farm created with crop data
- [ ] Vision model gives correct diagnosis for rice blast test image
- [ ] Offline mode demonstrated (airplane mode → advisory still works)
- [ ] Demo script practiced 3 times by all members
- [ ] Backup phone ready with app installed

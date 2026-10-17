# AGRI-SAGE — ERROR HANDLING & RECOVERY

## Backend Error Responses (Standardized)
```python
# NEVER expose internal details in API responses
# All errors follow this pattern:

400: {"detail": "Specific validation message"}      # Bad request
401: {"detail": "Invalid or expired token"}          # Auth failure
404: {"detail": "Not found"}                         # Not found OR not owned (RLS)
413: {"detail": "Image too large — maximum 5MB"}     # File too large
422: {"detail": "Request validation failed"}          # Pydantic validation
429: {"detail": "Rate limit exceeded — try again later"} # Rate limited
500: {"detail": "Internal server error"}              # Never expose more
503: {"detail": "Service temporarily unavailable"}    # Dependency down
```

## Advisory Generation Error Handling
```python
# When LLM returns invalid JSON twice:
# → Return SAFE_FALLBACK from brain/06_LLM_PROMPTS.md
# → Set confidence_state = INSUFFICIENT_DATA
# → Set safe_to_act = False
# → Log error with structlog — include observation_id and error details
# → NEVER propagate exception to farmer — always return a response

# When DSSAT simulation times out (>60 seconds):
# → Use LocalRulesEngine fallback
# → Mark scenarios with "simplified_estimate": True
# → Continue with advisory — do NOT fail entire pipeline

# When Weather API unavailable:
# → Use cached weather (last known)
# → Set indicators.is_cached = True, cache_age_minutes = X
# → Add warning to state.warnings: "Weather cached — may not be current"
# → Continue with advisory

# When knowledge chunks empty (RAG returns nothing):
# → Set confidence_state = INSUFFICIENT_DATA if no chunks at all
# → Log: "No knowledge chunks found for crop={crop} state={state}"
# → Return advisory with evidence showing knowledge gap
```

## Android Error States
```kotlin
// Every screen must handle these 4 states:
sealed class UiState<out T> {
    object Loading : UiState<Nothing>()
    data class Success<T>(val data: T) : UiState<T>()
    data class Error(val message: String) : UiState<Nothing>()
    object Offline : UiState<Nothing>()
}

// Error messages shown to farmer (Malayalam + English):
ERR_NO_INTERNET = "ഇന്റർനെറ്റ് ഇല്ല — ഓഫ്‌ലൈൻ ഡേറ്റ കാണിക്കുന്നു"
ERR_PHOTO_BLUR  = "ഫോട്ടോ മങ്ങിയിരിക്കുന്നു — ഉറച്ചു പിടിക്കുക"
ERR_PHOTO_DARK  = "ഇരുട്ടാണ് — തണൽ ഇടത്ത് നിൽക്കുക"
ERR_NOT_CROP    = "ഇത് ഒരു വിള ഫോട്ടോ അല്ല — വിളയുടെ ഇല കാണിക്കുക"
ERR_ANALYSIS    = "വിശകലനം പരാജയപ്പെട്ടു — വീണ്ടും ശ്രമിക്കുക"
ERR_UPLOAD      = "ഫോട്ടോ അപ്‌ലോഡ് ആയില്ല — ഇന്റർനെറ്റ് ലഭ്യമാകുമ്പോൾ ശ്രമിക്കും"
ERR_SYNC        = "ഡേറ്റ സൈങ്ക് ആയില്ല — ഇന്റർനെറ്റ് ലഭ്യമാകുമ്പോൾ ശ്രമിക്കും"
```

## Sync Queue Error Recovery
```kotlin
// SyncWorker retry logic:
// retryCount 0-4: exponential backoff (1min, 2min, 4min, 8min, 16min)
// retryCount >= 5: skip item, log warning — do NOT block other items
// On reconnect: always attempt sync — do not wait for next scheduled run
// Conflict resolution: server wins for farm state. Observations append-only (no conflict).
```

## Image Upload Recovery
```kotlin
// On upload failure:
// 1. Save image to local storage (app cache dir)
// 2. Add to sync_queue with priority=1 (highest)
// 3. Show snackbar: "Photo saved — will upload when connected"
// 4. Continue with offline advisory using local ONNX
// 5. On next connection: SyncWorker uploads image, then re-runs advisory if needed
```

## When AI Coding Agent Makes These Mistakes — Fix With These Prompts

### Mistake: AI uses on_startup instead of lifespan
```
Fix backend/main.py: FastAPI 0.115.0 requires lifespan context manager.
Replace @app.on_startup with @asynccontextmanager lifespan and pass to FastAPI(lifespan=lifespan).
Do not change anything else.
```

### Mistake: AI uses IVFFlat index in migration
```
Fix migration 011: Replace IVFFlat index with HNSW index for pgvector 0.4.0.
Use: CREATE INDEX idx_chunks_embedding ON knowledge_chunks USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);
Do not change any other part of the migration.
```

### Mistake: AI uses kapt instead of ksp for Room
```
Fix build.gradle.kts: Replace kapt("androidx.room:room-compiler:2.7.0") with ksp("androidx.room:room-compiler:2.7.0").
Also add ksp plugin and kotlin.serialization plugin to plugins block.
Do not change any other dependencies.
```

### Mistake: AI calls LLM from Critic agent
```
Fix backend/agents/critic.py: Critic agent must NOT call any LLM.
All logic is rule-based Python only.
Remove any LLM call. Use only: conflict detection rules, safety block checks, confidence state assignment formula.
```

### Mistake: AI omits modelled_estimate label on yield numbers
```
Fix: Every yield_kgha and net_return_inr value in AdvisoryResponse must have "modelled_estimate": true alongside it.
This is mandatory — not optional.
Add "modelled_estimate_label": "modelled estimate — actual results vary by field conditions" to every scenario object.
```

### Mistake: AI uses Image.LANCZOS instead of Image.Resampling.LANCZOS
```
Fix backend/services/image_security.py: Pillow 11.0.0 requires Image.Resampling.LANCZOS.
Replace all occurrences of Image.LANCZOS with Image.Resampling.LANCZOS.
```

### Mistake: AI embeds without 'query:' or 'passage:' prefix
```
Fix backend/services/embedding_service.py: multilingual-e5-large requires prefixes.
embed_query must use: model.encode(f'query: {text}', normalize_embeddings=True, convert_to_numpy=True)
embed_passage must use: model.encode(f'passage: {text}', normalize_embeddings=True, convert_to_numpy=True)
Omitting these prefixes degrades retrieval quality by 15-25%.
```
